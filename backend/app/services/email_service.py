"""
Email service - sends transactional emails via SMTP.
"""
import smtplib
import asyncio
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app.core.config import settings

logger = logging.getLogger(__name__)


def _send_smtp(to_email: str, subject: str, html: str) -> None:
    """Blocking SMTP send — runs in a thread pool."""
    if not settings.SMTP_HOST or not settings.SMTP_USER:
        logger.warning("SMTP not configured, skipping email to %s", to_email)
        return

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = f"{settings.SMTP_FROM_NAME} <{settings.SMTP_USER}>"
    msg["To"] = to_email
    msg.attach(MIMEText(html, "html", "utf-8"))

    try:
        if settings.SMTP_TLS:
            server = smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT, timeout=10)
        else:
            server = smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT, timeout=10)
            server.starttls()
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        server.sendmail(settings.SMTP_USER, to_email, msg.as_string())
        server.quit()
        logger.info("Email sent to %s: %s", to_email, subject)
    except Exception as e:
        logger.error("Failed to send email to %s: %s", to_email, e)


async def send_email(to_email: str, subject: str, html: str) -> None:
    """Async wrapper — offloads blocking SMTP to thread pool."""
    await asyncio.to_thread(_send_smtp, to_email, subject, html)


async def send_welcome_email(to_email: str, username: str, password: str) -> None:
    """Send welcome email after registration."""
    html = f"""
<!DOCTYPE html>
<html>
<head><meta charset="utf-8"></head>
<body style="background:#0a0a0f;color:#e0e0e0;font-family:monospace;padding:40px;">
  <div style="max-width:520px;margin:0 auto;background:#111118;border:1px solid #2a2a3e;border-radius:12px;padding:40px;">
    <div style="text-align:center;margin-bottom:32px;">
      <h1 style="color:#a855f7;font-size:32px;margin:0;letter-spacing:2px;">⚡ PyNeon</h1>
      <p style="color:#6b7280;font-size:13px;margin-top:8px;">// Обучение Python нового уровня</p>
    </div>
    <h2 style="color:#e0e0e0;font-size:20px;">Добро пожаловать, {username}!</h2>
    <p style="color:#9ca3af;line-height:1.6;">
      Твой аккаунт успешно создан. Сохрани данные для входа:
    </p>
    <div style="background:#0a0a0f;border:1px solid #2a2a3e;border-radius:8px;padding:20px;margin:24px 0;">
      <p style="margin:6px 0;color:#6b7280;font-size:12px;">// ДАННЫЕ ДЛЯ ВХОДА</p>
      <p style="margin:8px 0;"><span style="color:#6b7280;">Email:&nbsp;&nbsp;&nbsp;</span><span style="color:#38bdf8;">{to_email}</span></p>
      <p style="margin:8px 0;"><span style="color:#6b7280;">Логин:&nbsp;&nbsp;</span><span style="color:#38bdf8;">{username}</span></p>
      <p style="margin:8px 0;"><span style="color:#6b7280;">Пароль:&nbsp;</span><span style="color:#a855f7;">{password}</span></p>
    </div>
    <p style="color:#9ca3af;line-height:1.6;">
      Курс рассчитан на 12 недель — 240 уроков от нуля до Yandex CodeRun.<br>
      Удачи в обучении! 🚀
    </p>
    <div style="margin-top:32px;padding-top:24px;border-top:1px solid #2a2a3e;text-align:center;">
      <p style="color:#4b5563;font-size:12px;margin:0;">PyNeon Platform • Это письмо отправлено автоматически</p>
    </div>
  </div>
</body>
</html>
"""
    await send_email(to_email, "Добро пожаловать в PyNeon! Данные для входа", html)


async def send_reset_password_email(to_email: str, username: str, new_password: str) -> None:
    """Send new password after forgot-password request."""
    html = f"""
<!DOCTYPE html>
<html>
<head><meta charset="utf-8"></head>
<body style="background:#0a0a0f;color:#e0e0e0;font-family:monospace;padding:40px;">
  <div style="max-width:520px;margin:0 auto;background:#111118;border:1px solid #2a2a3e;border-radius:12px;padding:40px;">
    <div style="text-align:center;margin-bottom:32px;">
      <h1 style="color:#a855f7;font-size:32px;margin:0;letter-spacing:2px;">⚡ PyNeon</h1>
      <p style="color:#6b7280;font-size:13px;margin-top:8px;">// Восстановление доступа</p>
    </div>
    <h2 style="color:#e0e0e0;font-size:20px;">Привет, {username}!</h2>
    <p style="color:#9ca3af;line-height:1.6;">
      Мы получили запрос на восстановление пароля. Твой новый пароль для входа:
    </p>
    <div style="background:#0a0a0f;border:1px solid #2a2a3e;border-radius:8px;padding:20px;margin:24px 0;">
      <p style="margin:6px 0;color:#6b7280;font-size:12px;">// НОВЫЕ ДАННЫЕ ДЛЯ ВХОДА</p>
      <p style="margin:8px 0;"><span style="color:#6b7280;">Email:&nbsp;&nbsp;&nbsp;</span><span style="color:#38bdf8;">{to_email}</span></p>
      <p style="margin:8px 0;"><span style="color:#6b7280;">Пароль:&nbsp;</span><span style="color:#a855f7;font-size:18px;font-weight:bold;">{new_password}</span></p>
    </div>
    <p style="color:#9ca3af;line-height:1.6;">
      После входа рекомендуем сменить пароль в настройках профиля.<br>
      Если ты не запрашивал восстановление — просто проигнорируй это письмо.
    </p>
    <div style="margin-top:32px;padding-top:24px;border-top:1px solid #2a2a3e;text-align:center;">
      <p style="color:#4b5563;font-size:12px;margin:0;">PyNeon Platform • Это письмо отправлено автоматически</p>
    </div>
  </div>
</body>
</html>
"""
    await send_email(to_email, "PyNeon — Восстановление пароля", html)
