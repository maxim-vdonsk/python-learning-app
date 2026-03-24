"""
Sandbox service - executes user code in a Docker container.
Enforces CPU, memory, and time limits.
"""
import asyncio
import time
import json
from typing import Optional
import docker
from docker.errors import DockerException

from app.core.config import settings


class SandboxService:
    """
    Executes Python code in isolated Docker containers.
    Enforces resource limits for security.
    """

    def __init__(self):
        try:
            self.docker_client = docker.from_env()
        except DockerException:
            self.docker_client = None

    async def execute_code(
        self,
        code: str,
        stdin_data: str = "",
        timeout: int = None
    ) -> dict:
        """
        Execute Python code in a sandboxed Docker container.

        Returns:
            dict with: output, error, execution_time_ms, memory_used_mb, success
        """
        if not self.docker_client:
            return await self._execute_fallback(code, stdin_data)

        timeout = timeout or settings.SANDBOX_TIMEOUT
        start_time = time.time()

        try:
            # Prepare code to execute with stdin handling
            runner_code = f"""
import sys
import io

# Redirect stdin if needed
if {repr(stdin_data)}:
    sys.stdin = io.StringIO({repr(stdin_data)})

# User code
{code}
"""
            result = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self.docker_client.containers.run(
                    image=settings.SANDBOX_IMAGE,
                    command=["python3", "-c", runner_code],
                    mem_limit=settings.SANDBOX_MEM_LIMIT,
                    cpu_quota=settings.SANDBOX_CPU_QUOTA,
                    network_disabled=True,
                    read_only=True,
                    remove=True,
                    stdout=True,
                    stderr=True,
                    timeout=timeout,
                )
            )

            execution_time = (time.time() - start_time) * 1000
            output = result.decode("utf-8", errors="replace") if isinstance(result, bytes) else str(result)

            return {
                "output": output.strip(),
                "error": None,
                "execution_time_ms": round(execution_time, 2),
                "memory_used_mb": None,  # Docker stats require additional call
                "success": True,
            }

        except docker.errors.ContainerError as e:
            execution_time = (time.time() - start_time) * 1000
            error_output = e.stderr.decode("utf-8", errors="replace") if e.stderr else str(e)
            return {
                "output": "",
                "error": error_output.strip(),
                "execution_time_ms": round(execution_time, 2),
                "memory_used_mb": None,
                "success": False,
            }
        except Exception as e:
            return {
                "output": "",
                "error": f"Ошибка выполнения: {str(e)}",
                "execution_time_ms": round((time.time() - start_time) * 1000, 2),
                "memory_used_mb": None,
                "success": False,
            }

    async def _execute_fallback(self, code: str, stdin_data: str = "") -> dict:
        """
        Fallback execution without Docker using subprocess with timeout.
        Used when Docker is not available.
        """
        import subprocess
        import tempfile
        import os

        start_time = time.time()

        # Write code to temp file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(code)
            temp_file = f.name

        try:
            proc = await asyncio.create_subprocess_exec(
                "python3", temp_file,
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )

            stdin_bytes = stdin_data.encode() if stdin_data else b""
            stdout, stderr = await asyncio.wait_for(
                proc.communicate(input=stdin_bytes),
                timeout=settings.SANDBOX_TIMEOUT
            )

            execution_time = (time.time() - start_time) * 1000

            return {
                "output": stdout.decode("utf-8", errors="replace").strip(),
                "error": stderr.decode("utf-8", errors="replace").strip() if stderr else None,
                "execution_time_ms": round(execution_time, 2),
                "memory_used_mb": None,
                "success": proc.returncode == 0,
            }
        except asyncio.TimeoutError:
            return {
                "output": "",
                "error": f"Превышен лимит времени выполнения ({settings.SANDBOX_TIMEOUT}с)",
                "execution_time_ms": settings.SANDBOX_TIMEOUT * 1000,
                "memory_used_mb": None,
                "success": False,
            }
        finally:
            os.unlink(temp_file)

    async def run_tests(self, code: str, test_cases: list) -> dict:
        """
        Run code against multiple test cases.

        Returns:
            dict with: passed, total, results, execution_time_ms
        """
        results = []
        total_time = 0
        passed = 0

        for i, test_case in enumerate(test_cases):
            stdin_input = str(test_case.get("input", ""))
            expected_output = str(test_case.get("expected_output", "")).strip()

            result = await self.execute_code(code, stdin_input)
            actual_output = result["output"].strip()
            total_time += result.get("execution_time_ms", 0)

            is_passed = actual_output == expected_output or (
                result["success"] and not result["error"] and
                self._output_matches(actual_output, expected_output)
            )

            if is_passed:
                passed += 1

            results.append({
                "test_num": i + 1,
                "input": stdin_input,
                "expected": expected_output,
                "actual": actual_output,
                "passed": is_passed,
                "error": result.get("error"),
            })

        return {
            "passed": passed,
            "total": len(test_cases),
            "results": results,
            "execution_time_ms": round(total_time, 2),
            "all_passed": passed == len(test_cases),
        }

    def _output_matches(self, actual: str, expected: str) -> bool:
        """Flexible output comparison."""
        # Normalize whitespace
        actual_norm = " ".join(actual.split())
        expected_norm = " ".join(expected.split())
        return actual_norm == expected_norm


sandbox_service = SandboxService()
