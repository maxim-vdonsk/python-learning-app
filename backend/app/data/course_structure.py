"""
12-week Python course structure.
Defines the learning path from basics to Yandex CodeRun level.
"""

COURSE_STRUCTURE = [
    {
        "number": 1,
        "title": "Основы Python",
        "description": "Введение в Python: синтаксис, переменные, типы данных",
        "lessons": [
            {"title": "Введение в Python", "slug": "intro-python", "topic": "introduction", "order": 1,
             "description": "Что такое Python, история, установка, первая программа"},
            {"title": "Переменные и типы данных", "slug": "variables-types", "topic": "variables", "order": 2,
             "description": "int, float, str, bool — основные типы данных"},
            {"title": "Ввод и вывод данных", "slug": "input-output", "topic": "io", "order": 3,
             "description": "print(), input(), форматирование строк"},
            {"title": "Арифметические операции", "slug": "arithmetic", "topic": "arithmetic", "order": 4,
             "description": "Операторы: +, -, *, /, //, %, **"},
        ]
    },
    {
        "number": 2,
        "title": "Условия и циклы",
        "description": "Управление потоком выполнения программы",
        "lessons": [
            {"title": "Условные операторы if/elif/else", "slug": "conditionals", "topic": "conditionals", "order": 1,
             "description": "Ветвление программы, булева логика"},
            {"title": "Цикл while", "slug": "while-loop", "topic": "while_loop", "order": 2,
             "description": "Цикл с условием, break, continue"},
            {"title": "Цикл for и range()", "slug": "for-loop", "topic": "for_loop", "order": 3,
             "description": "Итерация по последовательностям"},
            {"title": "Вложенные циклы", "slug": "nested-loops", "topic": "nested_loops", "order": 4,
             "description": "Циклы внутри циклов, паттерны"},
        ]
    },
    {
        "number": 3,
        "title": "Функции",
        "description": "Создание повторно используемого кода",
        "lessons": [
            {"title": "Определение функций", "slug": "functions-basics", "topic": "functions", "order": 1,
             "description": "def, параметры, return"},
            {"title": "Аргументы функций", "slug": "function-args", "topic": "function_args", "order": 2,
             "description": "Позиционные, именованные, *args, **kwargs"},
            {"title": "Область видимости", "slug": "scope", "topic": "scope", "order": 3,
             "description": "local, global, nonlocal"},
            {"title": "Лямбда-функции и встроенные", "slug": "lambda-builtins", "topic": "lambda", "order": 4,
             "description": "lambda, map, filter, sorted"},
        ]
    },
    {
        "number": 4,
        "title": "Строки и списки",
        "description": "Работа с последовательностями данных",
        "lessons": [
            {"title": "Методы строк", "slug": "string-methods", "topic": "strings", "order": 1,
             "description": "split, join, strip, replace, format, f-strings"},
            {"title": "Срезы и индексация", "slug": "slicing", "topic": "slicing", "order": 2,
             "description": "Индексация, срезы, отрицательные индексы"},
            {"title": "Списки", "slug": "lists", "topic": "lists", "order": 3,
             "description": "Создание, методы, list comprehension"},
            {"title": "Сортировка и поиск", "slug": "sorting-search", "topic": "sorting", "order": 4,
             "description": "sort(), sorted(), min(), max(), in"},
        ]
    },
    {
        "number": 5,
        "title": "Словари и множества",
        "description": "Хранение и поиск данных",
        "lessons": [
            {"title": "Словари (dict)", "slug": "dictionaries", "topic": "dictionaries", "order": 1,
             "description": "Создание, доступ, методы словаря"},
            {"title": "Методы словарей", "slug": "dict-methods", "topic": "dict_methods", "order": 2,
             "description": "keys(), values(), items(), get(), update()"},
            {"title": "Множества (set)", "slug": "sets", "topic": "sets", "order": 3,
             "description": "Операции над множествами: объединение, пересечение"},
            {"title": "Comprehensions", "slug": "comprehensions", "topic": "comprehensions", "order": 4,
             "description": "dict/set/list comprehension, генераторы"},
        ]
    },
    {
        "number": 6,
        "title": "Работа с файлами",
        "description": "Чтение и запись файлов",
        "lessons": [
            {"title": "Чтение файлов", "slug": "file-reading", "topic": "file_io", "order": 1,
             "description": "open(), read(), readline(), readlines()"},
            {"title": "Запись в файлы", "slug": "file-writing", "topic": "file_write", "order": 2,
             "description": "write(), writelines(), контекстный менеджер"},
            {"title": "Работа с CSV и JSON", "slug": "csv-json", "topic": "csv_json", "order": 3,
             "description": "Модули csv и json"},
            {"title": "Модуль os и pathlib", "slug": "os-pathlib", "topic": "os_module", "order": 4,
             "description": "Работа с файловой системой"},
        ]
    },
    {
        "number": 7,
        "title": "Исключения",
        "description": "Обработка ошибок и исключений",
        "lessons": [
            {"title": "try/except/finally", "slug": "try-except", "topic": "exceptions", "order": 1,
             "description": "Базовая обработка исключений"},
            {"title": "Типы исключений", "slug": "exception-types", "topic": "exception_types", "order": 2,
             "description": "ValueError, TypeError, IndexError и другие"},
            {"title": "Создание исключений", "slug": "custom-exceptions", "topic": "custom_exceptions", "order": 3,
             "description": "raise, создание собственных исключений"},
            {"title": "Контекстные менеджеры", "slug": "context-managers", "topic": "context_managers", "order": 4,
             "description": "with, __enter__, __exit__"},
        ]
    },
    {
        "number": 8,
        "title": "ООП",
        "description": "Объектно-ориентированное программирование",
        "lessons": [
            {"title": "Классы и объекты", "slug": "classes-objects", "topic": "oop_basics", "order": 1,
             "description": "class, __init__, self, атрибуты и методы"},
            {"title": "Наследование", "slug": "inheritance", "topic": "inheritance", "order": 2,
             "description": "Наследование классов, super()"},
            {"title": "Инкапсуляция и полиморфизм", "slug": "encapsulation", "topic": "encapsulation", "order": 3,
             "description": "Приватные атрибуты, полиморфизм"},
            {"title": "Магические методы", "slug": "magic-methods", "topic": "dunder_methods", "order": 4,
             "description": "__str__, __repr__, __len__, __eq__ и другие"},
        ]
    },
    {
        "number": 9,
        "title": "Алгоритмы и структуры данных",
        "description": "Основы алгоритмического мышления",
        "lessons": [
            {"title": "Сортировка", "slug": "sorting-algorithms", "topic": "sorting_algorithms", "order": 1,
             "description": "Пузырьковая, сортировка выбором, быстрая"},
            {"title": "Поиск", "slug": "search-algorithms", "topic": "search", "order": 2,
             "description": "Линейный и бинарный поиск"},
            {"title": "Рекурсия", "slug": "recursion", "topic": "recursion", "order": 3,
             "description": "Рекурсивные функции, факториал, числа Фибоначчи"},
            {"title": "Стек и очередь", "slug": "stack-queue", "topic": "stack_queue", "order": 4,
             "description": "Реализация стека и очереди"},
        ]
    },
    {
        "number": 10,
        "title": "Продвинутые алгоритмы",
        "description": "Алгоритмы для олимпиадных задач",
        "lessons": [
            {"title": "Динамическое программирование", "slug": "dynamic-programming", "topic": "dp", "order": 1,
             "description": "Мемоизация, табуляция, задача о рюкзаке"},
            {"title": "Жадные алгоритмы", "slug": "greedy", "topic": "greedy", "order": 2,
             "description": "Жадный выбор, задачи оптимизации"},
            {"title": "Графы", "slug": "graphs", "topic": "graphs", "order": 3,
             "description": "BFS, DFS, представление графов"},
            {"title": "Деревья", "slug": "trees", "topic": "trees", "order": 4,
             "description": "Бинарные деревья, обходы"},
        ]
    },
    {
        "number": 11,
        "title": "Подготовка к Yandex CodeRun",
        "description": "Типовые задачи и паттерны решений",
        "lessons": [
            {"title": "Задачи на строки", "slug": "string-problems", "topic": "string_problems", "order": 1,
             "description": "Анаграммы, палиндромы, компрессия строк"},
            {"title": "Задачи на массивы", "slug": "array-problems", "topic": "array_problems", "order": 2,
             "description": "Два указателя, скользящее окно"},
            {"title": "Задачи на числа", "slug": "number-problems", "topic": "number_problems", "order": 3,
             "description": "НОД, НОК, простые числа, разряды"},
            {"title": "Комбинированные задачи", "slug": "combined-problems", "topic": "combined", "order": 4,
             "description": "Сложные задачи требующие нескольких техник"},
        ]
    },
    {
        "number": 12,
        "title": "Финальный проект",
        "description": "Применение всех знаний в реальных задачах",
        "lessons": [
            {"title": "Проект: Калькулятор выражений", "slug": "project-calculator", "topic": "project_calculator", "order": 1,
             "description": "Разбор и вычисление математических выражений"},
            {"title": "Проект: Анализ данных", "slug": "project-data", "topic": "project_data", "order": 2,
             "description": "Обработка и анализ текстовых данных"},
            {"title": "Проект: Мини-игра", "slug": "project-game", "topic": "project_game", "order": 3,
             "description": "Текстовая игра с применением ООП"},
            {"title": "Финальный экзамен", "slug": "final-exam", "topic": "final_exam", "order": 4,
             "description": "Финальный набор задач уровня Yandex CodeRun"},
        ]
    },
]
