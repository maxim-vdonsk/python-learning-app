"""
12-week Python course structure.
12 weeks × 5 days × 4 lessons = 240 lessons total.
Defines the learning path from basics to Yandex CodeRun level.
"""

COURSE_STRUCTURE = [
    # ─────────────────────────────────────────────────────────────────
    # НЕДЕЛЯ 1: Знакомство с Python
    # ─────────────────────────────────────────────────────────────────
    {
        "number": 1,
        "title": "Знакомство с Python",
        "description": "Установка окружения, первые программы, переменные, операторы и ввод/вывод",
        "lessons": [
            # День 1: Введение
            {"title": "Что такое Python и зачем он нужен", "slug": "what-is-python", "topic": "python_intro", "order": 1,
             "description": "История Python, области применения, почему Python популярен среди новичков и профессионалов"},
            {"title": "Первая программа: вывод текста через print()", "slug": "install-python", "topic": "print_basics", "order": 2,
             "description": "Функция print(), вывод строк и чисел, несколько значений через запятую, строки в кавычках"},
            {"title": "Как Python выполняет код: интерпретатор и ошибки", "slug": "repl-scripts", "topic": "python_execution", "order": 3,
             "description": "Построчное выполнение, что такое интерпретатор, как читать сообщения об ошибках"},
            {"title": "Hello, World! и комментарии в коде", "slug": "hello-world", "topic": "hello_world", "order": 4,
             "description": "Первая программа, однострочные и многострочные комментарии, зачем они нужны"},
            # День 2: Переменные
            {"title": "Что такое переменная", "slug": "variables-intro", "topic": "variables", "order": 5,
             "description": "Понятие переменной, именование, оператор присваивания"},
            {"title": "Числовые типы: int и float", "slug": "int-float", "topic": "variables", "order": 6,
             "description": "Целые и вещественные числа, особенности float"},
            {"title": "Строки и булевы значения", "slug": "str-bool", "topic": "variables", "order": 7,
             "description": "Тип str, тип bool, True/False, None"},
            {"title": "type() и приведение типов", "slug": "type-casting", "topic": "variables", "order": 8,
             "description": "Функция type(), int(), float(), str() — явное приведение"},
            # День 3: Операторы
            {"title": "Арифметические операторы", "slug": "arithmetic-ops", "topic": "operators", "order": 9,
             "description": "Операторы +, -, *, /, //, %, ** с примерами"},
            {"title": "Операторы сравнения", "slug": "comparison-ops", "topic": "operators", "order": 10,
             "description": "==, !=, <, >, <=, >= — результат bool"},
            {"title": "Логические операторы", "slug": "logical-ops", "topic": "operators", "order": 11,
             "description": "and, or, not — логическая алгебра"},
            {"title": "Приоритет операторов", "slug": "operator-priority", "topic": "operators", "order": 12,
             "description": "Порядок вычислений, скобки, PEMDAS"},
            # День 4: Ввод и вывод
            {"title": "Функция print() и аргументы", "slug": "print-function", "topic": "io", "order": 13,
             "description": "print(), sep, end, вывод нескольких значений"},
            {"title": "Функция input() и ввод данных", "slug": "input-function", "topic": "io", "order": 14,
             "description": "Получение данных от пользователя, строка → число"},
            {"title": "f-строки и форматирование", "slug": "fstrings", "topic": "io", "order": 15,
             "description": "f-строки, format(), форматирование чисел"},
            {"title": "Комбинирование ввода и вывода", "slug": "io-combined", "topic": "io", "order": 16,
             "description": "Интерактивные программы, мини-калькулятор"},
            # День 5: Практика основ
            {"title": "Конвертация и проверка типов", "slug": "type-practice", "topic": "practice_basics", "order": 17,
             "description": "Практика приведения типов, isinstance()"},
            {"title": "Типичные ошибки новичков", "slug": "common-errors", "topic": "practice_basics", "order": 18,
             "description": "SyntaxError, NameError, TypeError — как читать ошибки"},
            {"title": "Решение первых задач", "slug": "first-tasks", "topic": "practice_basics", "order": 19,
             "description": "Задачи: площадь, периметр, перевод единиц"},
            {"title": "Мини-проект: Конвертер единиц", "slug": "unit-converter", "topic": "practice_basics", "order": 20,
             "description": "Программа перевода температур, длин и весов"},
        ]
    },
    # ─────────────────────────────────────────────────────────────────
    # НЕДЕЛЯ 2: Условия и ветвление
    # ─────────────────────────────────────────────────────────────────
    {
        "number": 2,
        "title": "Условия и ветвление",
        "description": "Булева логика, операторы if/elif/else, вложенные условия и практика",
        "lessons": [
            # День 1: Булева логика
            {"title": "True, False и булева логика", "slug": "bool-logic", "topic": "boolean", "order": 1,
             "description": "Тип bool, таблицы истинности and/or/not"},
            {"title": "Операторы сравнения в условиях", "slug": "comparison-in-cond", "topic": "boolean", "order": 2,
             "description": "Сравнение чисел, строк, is и =="},
            {"title": "Цепочки сравнений", "slug": "chained-comparison", "topic": "boolean", "order": 3,
             "description": "a < b < c, in, not in — удобный синтаксис Python"},
            {"title": "Truthy и Falsy значения", "slug": "truthy-falsy", "topic": "boolean", "order": 4,
             "description": "Когда 0, None, '' считаются False — неявное приведение"},
            # День 2: Оператор if
            {"title": "Синтаксис if и отступы", "slug": "if-syntax", "topic": "if_basic", "order": 5,
             "description": "Блок if, роль отступов в Python, IndentationError"},
            {"title": "Ветка else", "slug": "if-else", "topic": "if_basic", "order": 6,
             "description": "if-else конструкция, выбор из двух вариантов"},
            {"title": "Вложенные if", "slug": "nested-if", "topic": "if_basic", "order": 7,
             "description": "Условия внутри условий, глубина вложенности"},
            {"title": "Практика: if/else задачи", "slug": "if-practice", "topic": "if_basic", "order": 8,
             "description": "Определение знака числа, чётность, вилка цен"},
            # День 3: elif и сложные условия
            {"title": "Оператор elif", "slug": "elif-operator", "topic": "elif", "order": 9,
             "description": "Множественные ветки elif, порядок проверки"},
            {"title": "Множественные условия с elif", "slug": "multiple-elif", "topic": "elif", "order": 10,
             "description": "Классификация: оценки, категории, диапазоны"},
            {"title": "Тернарный оператор", "slug": "ternary", "topic": "elif", "order": 11,
             "description": "value if condition else other — однострочное условие"},
            {"title": "match-case (Python 3.10+)", "slug": "match-case", "topic": "elif", "order": 12,
             "description": "Структурное сопоставление с образцом"},
            # День 4: Практика условий
            {"title": "FizzBuzz для одного числа", "slug": "fizzbuzz", "topic": "conditions_practice", "order": 13,
             "description": "Дано одно число: вывести Fizz если делится на 3, Buzz на 5, FizzBuzz на оба — только if/elif/else без циклов"},
            {"title": "Задачи уровня А на условия", "slug": "cond-level-a", "topic": "conditions_practice", "order": 14,
             "description": "Задачи Яндекс контеста уровня A на if/elif"},
            {"title": "Оптимизация условий", "slug": "cond-optimization", "topic": "conditions_practice", "order": 15,
             "description": "Упрощение логики, de Morgan, читаемый код"},
            {"title": "Частые ошибки в условиях", "slug": "cond-errors", "topic": "conditions_practice", "order": 16,
             "description": "= вместо ==, логические ловушки, None-проверки"},
            # День 5: Проект
            {"title": "Валидация пользовательского ввода", "slug": "input-validation", "topic": "conditions_project", "order": 17,
             "description": "Проверка корректности ввода, диапазоны, типы"},
            {"title": "Калькулятор с выбором операции", "slug": "calc-operations", "topic": "conditions_project", "order": 18,
             "description": "Программа с меню операций: +, -, *, /"},
            {"title": "Классификатор данных", "slug": "data-classifier", "topic": "conditions_project", "order": 19,
             "description": "Определение категорий по значению"},
            {"title": "Итог недели: решаем задачи", "slug": "week2-final", "topic": "conditions_project", "order": 20,
             "description": "Комплексные задачи с ветвлением"},
        ]
    },
    # ─────────────────────────────────────────────────────────────────
    # НЕДЕЛЯ 3: Циклы
    # ─────────────────────────────────────────────────────────────────
    {
        "number": 3,
        "title": "Циклы",
        "description": "Цикл while, цикл for, break/continue, вложенные циклы и паттерны",
        "lessons": [
            # День 1: while
            {"title": "Цикл while: основы", "slug": "while-basics", "topic": "while_basics", "order": 1,
             "description": "Синтаксис while, условие выхода, бесконечный цикл"},
            {"title": "break и continue в while", "slug": "while-break-continue", "topic": "while_basics", "order": 2,
             "description": "Досрочный выход и пропуск итерации"},
            {"title": "Счётчики и накопители", "slug": "counters-accumulators", "topic": "while_basics", "order": 3,
             "description": "Паттерн счётчика, накопления суммы/произведения"},
            {"title": "while для валидации ввода", "slug": "while-validation", "topic": "while_basics", "order": 4,
             "description": "Повторный запрос ввода до корректного значения"},
            # День 2: for
            {"title": "Цикл for и range()", "slug": "for-range", "topic": "for_basics", "order": 5,
             "description": "Синтаксис for, range(start, stop, step)"},
            {"title": "Итерация по строкам", "slug": "for-strings", "topic": "for_basics", "order": 6,
             "description": "Перебор символов строки, подсчёт, поиск"},
            {"title": "enumerate() и zip()", "slug": "enumerate-zip", "topic": "for_basics", "order": 7,
             "description": "Индекс при итерации, параллельный перебор"},
            {"title": "break, continue и else в for", "slug": "for-control", "topic": "for_basics", "order": 8,
             "description": "Управление циклом, else после for"},
            # День 3: Продвинутые циклы
            {"title": "Вложенные циклы", "slug": "nested-loops", "topic": "loops_advanced", "order": 9,
             "description": "Циклы внутри циклов, таблицы, матрицы"},
            {"title": "Паттерны из символов", "slug": "symbol-patterns", "topic": "loops_advanced", "order": 10,
             "description": "Треугольники, ромбы, прямоугольники из символов"},
            {"title": "Перебор с условием", "slug": "filtered-loop", "topic": "loops_advanced", "order": 11,
             "description": "Фильтрация в цикле, поиск первого совпадения"},
            {"title": "Оптимизация циклов", "slug": "loop-optimization", "topic": "loops_advanced", "order": 12,
             "description": "Раннее завершение, сложность O(n) vs O(n²)"},
            # День 4: Практика циклов
            {"title": "Задачи на накопление", "slug": "accumulation-tasks", "topic": "loops_practice", "order": 13,
             "description": "Сумма цифр, факториал, степень числа"},
            {"title": "Числа Фибоначчи и последовательности", "slug": "fibonacci", "topic": "loops_practice", "order": 14,
             "description": "Генерация последовательностей с помощью циклов"},
            {"title": "Поиск в диапазоне", "slug": "range-search", "topic": "loops_practice", "order": 15,
             "description": "Простые числа, делители, кратные"},
            {"title": "Задачи уровня B на циклы", "slug": "loops-level-b", "topic": "loops_practice", "order": 16,
             "description": "Задачи Яндекс контеста уровня B с циклами"},
            # День 5: Проект
            {"title": "Таблица умножения", "slug": "multiplication-table", "topic": "loops_project", "order": 17,
             "description": "Генерация и вывод таблицы умножения"},
            {"title": "Угадай число", "slug": "guess-number", "topic": "loops_project", "order": 18,
             "description": "Игра с циклом: угадывание числа с подсказками"},
            {"title": "Анализ числовой последовательности", "slug": "sequence-analysis", "topic": "loops_project", "order": 19,
             "description": "Минимум, максимум, среднее из ввода пользователя"},
            {"title": "Итог недели: задачи на циклы", "slug": "week3-final", "topic": "loops_project", "order": 20,
             "description": "Комплексные задачи с for и while"},
        ]
    },
    # ─────────────────────────────────────────────────────────────────
    # НЕДЕЛЯ 4: Функции
    # ─────────────────────────────────────────────────────────────────
    {
        "number": 4,
        "title": "Функции",
        "description": "Создание функций, параметры, область видимости, лямбды и встроенные функции",
        "lessons": [
            # День 1: Основы функций
            {"title": "def и return: создаём функции", "slug": "def-return", "topic": "functions_basics", "order": 1,
             "description": "Синтаксис def, тело функции, оператор return"},
            {"title": "Функции без return", "slug": "void-functions", "topic": "functions_basics", "order": 2,
             "description": "Процедуры, None как возвращаемое значение"},
            {"title": "Вызов функции и передача данных", "slug": "function-call", "topic": "functions_basics", "order": 3,
             "description": "Аргументы при вызове, возвращаемое значение"},
            {"title": "Документирование функций", "slug": "docstrings", "topic": "functions_basics", "order": 4,
             "description": "Docstrings, аннотации типов, help()"},
            # День 2: Аргументы
            {"title": "Позиционные и именованные аргументы", "slug": "pos-kwargs", "topic": "function_args", "order": 5,
             "description": "Порядок аргументов, вызов по имени параметра"},
            {"title": "Значения по умолчанию", "slug": "default-args", "topic": "function_args", "order": 6,
             "description": "Параметры со значением по умолчанию, ловушки"},
            {"title": "*args — переменное число аргументов", "slug": "args-packing", "topic": "args_kwargs", "order": 7,
             "description": "Упаковка позиционных аргументов в кортеж"},
            {"title": "**kwargs — именованные аргументы", "slug": "kwargs-packing", "topic": "args_kwargs", "order": 8,
             "description": "Упаковка именованных аргументов в словарь"},
            # День 3: Область видимости
            {"title": "Локальные и глобальные переменные", "slug": "local-global", "topic": "scope", "order": 9,
             "description": "LEGB-правило, локальная область видимости"},
            {"title": "Ключевое слово global", "slug": "global-keyword", "topic": "scope", "order": 10,
             "description": "Изменение глобальных переменных из функции"},
            {"title": "Вложенные функции и nonlocal", "slug": "nonlocal", "topic": "scope", "order": 11,
             "description": "Замыкания, nonlocal, фабрики функций"},
            {"title": "Чистые функции и побочные эффекты", "slug": "pure-functions", "topic": "scope", "order": 12,
             "description": "Принципы написания предсказуемых функций"},
            # День 4: Lambda и встроенные
            {"title": "lambda-функции", "slug": "lambda-func", "topic": "lambda", "order": 13,
             "description": "Анонимные функции, синтаксис, ограничения"},
            {"title": "map() и filter()", "slug": "map-filter", "topic": "lambda", "order": 14,
             "description": "Применение функции к последовательности"},
            {"title": "sorted() с ключом", "slug": "sorted-key", "topic": "lambda", "order": 15,
             "description": "Сортировка по критерию, reversed()"},
            {"title": "Встроенные функции Python", "slug": "builtins", "topic": "lambda", "order": 16,
             "description": "sum, min, max, abs, round, all, any, zip, enumerate"},
            # День 5: Проект
            {"title": "Рефакторинг кода с функциями", "slug": "refactoring", "topic": "functions_project", "order": 17,
             "description": "Превращаем повторяющийся код в функции"},
            {"title": "Библиотека математических функций", "slug": "math-lib", "topic": "functions_project", "order": 18,
             "description": "Создаём свой модуль вычислений"},
            {"title": "Функции высшего порядка", "slug": "higher-order", "topic": "functions_project", "order": 19,
             "description": "Функции принимающие и возвращающие функции"},
            {"title": "Итог недели: функции на практике", "slug": "week4-final", "topic": "functions_project", "order": 20,
             "description": "Комплексные задачи с функциями"},
        ]
    },
    # ─────────────────────────────────────────────────────────────────
    # НЕДЕЛЯ 5: Строки
    # ─────────────────────────────────────────────────────────────────
    {
        "number": 5,
        "title": "Строки",
        "description": "Методы строк, форматирование, срезы, регулярные выражения и текстовые задачи",
        "lessons": [
            # День 1: Основы строк
            {"title": "Строка как последовательность символов", "slug": "string-as-seq", "topic": "strings_basics", "order": 1,
             "description": "Строка — это список символов, индексация, len()"},
            {"title": "Конкатенация и повторение", "slug": "string-concat", "topic": "strings_basics", "order": 2,
             "description": "Оператор + и *, строки неизменяемы"},
            {"title": "Экранирование и специальные символы", "slug": "escape-chars", "topic": "strings_basics", "order": 3,
             "description": r"\\n, \\t, \\\\, r-строки, многострочные строки"},
            {"title": "in, not in и поиск в строке", "slug": "string-search", "topic": "strings_basics", "order": 4,
             "description": "Проверка вхождения подстроки, find(), index()"},
            # День 2: Методы строк
            {"title": "Регистр: upper, lower, title, capitalize", "slug": "string-case", "topic": "string_methods", "order": 5,
             "description": "Преобразование регистра, isupper(), islower()"},
            {"title": "Обрезка и замена: strip, replace", "slug": "strip-replace", "topic": "string_methods", "order": 6,
             "description": "strip(), lstrip(), rstrip(), replace()"},
            {"title": "Разбивка и склейка: split, join", "slug": "split-join", "topic": "string_methods", "order": 7,
             "description": "split() по разделителю, join() для сборки"},
            {"title": "Проверка содержимого: isdigit, isalpha", "slug": "string-checks", "topic": "string_methods", "order": 8,
             "description": "isdigit(), isalpha(), isspace(), startswith(), endswith()"},
            # День 3: Форматирование
            {"title": "f-строки подробно", "slug": "fstrings-advanced", "topic": "string_format", "order": 9,
             "description": "Выражения в f-строках, форматные спецификаторы"},
            {"title": "Форматирование чисел", "slug": "number-format", "topic": "string_format", "order": 10,
             "description": "Ширина поля, знаки, точность float, разряды"},
            {"title": "Выравнивание текста", "slug": "text-align", "topic": "string_format", "order": 11,
             "description": "ljust(), rjust(), center(), zfill()"},
            {"title": "Шаблоны строк", "slug": "string-templates", "topic": "string_format", "order": 12,
             "description": "format(), Template, % оператор"},
            # День 4: Срезы
            {"title": "Срезы строк: синтаксис", "slug": "slicing-syntax", "topic": "slicing", "order": 13,
             "description": "s[start:stop:step], значения по умолчанию"},
            {"title": "Отрицательные индексы", "slug": "negative-index", "topic": "slicing", "order": 14,
             "description": "Доступ с конца строки, s[-1], s[-3:]"},
            {"title": "Реверс строки и шаг", "slug": "string-reverse", "topic": "slicing", "order": 15,
             "description": "s[::-1], чётные/нечётные символы через шаг"},
            {"title": "Срезы для обработки данных", "slug": "slicing-practice", "topic": "slicing", "order": 16,
             "description": "Извлечение дат, кодов, токенов из строки"},
            # День 5: Текстовые задачи
            {"title": "Палиндромы и анаграммы", "slug": "palindromes-anagrams", "topic": "strings_practice", "order": 17,
             "description": "Проверка палиндрома через срезы s[::-1], анаграммы через подсчёт символов — только строки и циклы"},
            {"title": "Компрессия строк", "slug": "string-compression", "topic": "strings_practice", "order": 18,
             "description": "RLE-кодирование, подсчёт повторений"},
            {"title": "Шифр Цезаря", "slug": "caesar-cipher", "topic": "strings_practice", "order": 19,
             "description": "Шифрование и дешифрование текста"},
            {"title": "Итог недели: текстовые задачи", "slug": "week5-final", "topic": "strings_practice", "order": 20,
             "description": "Задачи уровня B-C на обработку строк"},
        ]
    },
    # ─────────────────────────────────────────────────────────────────
    # НЕДЕЛЯ 6: Списки
    # ─────────────────────────────────────────────────────────────────
    {
        "number": 6,
        "title": "Списки",
        "description": "Создание, методы, list comprehension, сортировка и вложенные списки",
        "lessons": [
            # День 1: Основы списков
            {"title": "Создание и индексация списков", "slug": "list-basics", "topic": "lists_basics", "order": 1,
             "description": "list(), [], индексация, изменение элементов"},
            {"title": "Вложенные списки", "slug": "nested-lists-basics", "topic": "lists_basics", "order": 2,
             "description": "Список списков, доступ к элементам"},
            {"title": "Срезы списков", "slug": "list-slicing", "topic": "lists_basics", "order": 3,
             "description": "Срезы как у строк, копирование, замена"},
            {"title": "Распаковка списков", "slug": "list-unpacking", "topic": "lists_basics", "order": 4,
             "description": "a, b = list, *rest, обмен значениями"},
            # День 2: Методы списков
            {"title": "append, extend, insert", "slug": "list-add", "topic": "list_methods", "order": 5,
             "description": "Добавление элементов в конец, позицию, другой список"},
            {"title": "pop, remove, del", "slug": "list-remove", "topic": "list_methods", "order": 6,
             "description": "Удаление по индексу, значению, срезу"},
            {"title": "sort, sorted, reverse", "slug": "list-sort", "topic": "list_methods", "order": 7,
             "description": "Сортировка на месте и создание нового списка"},
            {"title": "index, count, copy, clear", "slug": "list-misc", "topic": "list_methods", "order": 8,
             "description": "Поиск, подсчёт, копирование списка"},
            # День 3: List comprehension
            {"title": "Синтаксис list comprehension", "slug": "listcomp-syntax", "topic": "list_comprehension", "order": 9,
             "description": "[expr for x in iterable] — замена цикла"},
            {"title": "Условие в comprehension", "slug": "listcomp-filter", "topic": "list_comprehension", "order": 10,
             "description": "[expr for x in iter if cond] — фильтрация"},
            {"title": "Вложенные comprehension", "slug": "listcomp-nested", "topic": "list_comprehension", "order": 11,
             "description": "Матрицы через comprehension, уплощение"},
            {"title": "Генераторные выражения", "slug": "generators", "topic": "list_comprehension", "order": 12,
             "description": "Отличие генератора от списка, экономия памяти"},
            # День 4: Алгоритмы на списках
            {"title": "Поиск минимума, максимума, суммы", "slug": "list-stats", "topic": "lists_algorithms", "order": 13,
             "description": "min(), max(), sum() — ручная реализация и встроенные"},
            {"title": "Фильтрация и преобразование", "slug": "list-transform", "topic": "lists_algorithms", "order": 14,
             "description": "Отбор по условию, применение функции к каждому"},
            {"title": "Дедупликация и уникальные элементы", "slug": "list-unique", "topic": "lists_algorithms", "order": 15,
             "description": "Удаление дублей, сохранение порядка"},
            {"title": "Задачи уровня B на списки", "slug": "lists-level-b", "topic": "lists_algorithms", "order": 16,
             "description": "Задачи на обработку последовательностей"},
            # День 5: Матрицы
            {"title": "Двумерные массивы (матрицы)", "slug": "matrices", "topic": "nested_lists", "order": 17,
             "description": "Создание матриц, доступ к строкам и столбцам"},
            {"title": "Транспонирование матрицы", "slug": "matrix-transpose", "topic": "nested_lists", "order": 18,
             "description": "Смена строк и столбцов, zip(*matrix)"},
            {"title": "Обход матрицы циклами", "slug": "matrix-traverse", "topic": "nested_lists", "order": 19,
             "description": "Поиск, суммирование по строкам/столбцам"},
            {"title": "Итог недели: задачи на списки", "slug": "week6-final", "topic": "nested_lists", "order": 20,
             "description": "Комплексные задачи с вложенными структурами"},
        ]
    },
    # ─────────────────────────────────────────────────────────────────
    # НЕДЕЛЯ 7: Словари и множества
    # ─────────────────────────────────────────────────────────────────
    {
        "number": 7,
        "title": "Словари и множества",
        "description": "dict и set: создание, методы, comprehension, практические задачи",
        "lessons": [
            # День 1: Основы словарей
            {"title": "Словарь: создание и доступ", "slug": "dict-create", "topic": "dict_basics", "order": 1,
             "description": "dict(), {}, ключи и значения, доступ по ключу"},
            {"title": "Изменение и удаление", "slug": "dict-modify", "topic": "dict_basics", "order": 2,
             "description": "Добавление, изменение, del, pop()"},
            {"title": "Проверка ключей: in, get()", "slug": "dict-check", "topic": "dict_basics", "order": 3,
             "description": "KeyError, безопасный доступ через get()"},
            {"title": "Перебор словаря: keys, values, items", "slug": "dict-iterate", "topic": "dict_basics", "order": 4,
             "description": "Итерация по ключам, значениям, парам"},
            # День 2: Методы словарей
            {"title": "update() и merge словарей", "slug": "dict-update", "topic": "dict_methods", "order": 5,
             "description": "Слияние словарей, update(), |= (Python 3.9+)"},
            {"title": "setdefault() и defaultdict", "slug": "dict-setdefault", "topic": "dict_methods", "order": 6,
             "description": "Создание ключа если нет, defaultdict из collections"},
            {"title": "Вложенные словари", "slug": "nested-dicts", "topic": "dict_methods", "order": 7,
             "description": "Словари в словарях, доступ и изменение"},
            {"title": "Counter для подсчёта", "slug": "counter", "topic": "dict_methods", "order": 8,
             "description": "collections.Counter — частотный анализ"},
            # День 3: Множества
            {"title": "Множество set: создание и операции", "slug": "set-create", "topic": "sets", "order": 9,
             "description": "set(), {}, уникальность, add(), remove()"},
            {"title": "Операции над множествами", "slug": "set-operations", "topic": "sets", "order": 10,
             "description": "Объединение |, пересечение &, разность -, симм. разность ^"},
            {"title": "Подмножества и проверки", "slug": "set-checks", "topic": "sets", "order": 11,
             "description": "issubset(), issuperset(), isdisjoint()"},
            {"title": "frozenset и применение", "slug": "frozenset", "topic": "sets", "order": 12,
             "description": "Неизменяемые множества, использование как ключей"},
            # День 4: Comprehensions
            {"title": "dict comprehension", "slug": "dict-comp", "topic": "comprehensions_adv", "order": 13,
             "description": "{k: v for k, v in ...} — создание словарей"},
            {"title": "set comprehension", "slug": "set-comp", "topic": "comprehensions_adv", "order": 14,
             "description": "{expr for x in ...} — создание множеств"},
            {"title": "Инверсия словаря", "slug": "dict-invert", "topic": "comprehensions_adv", "order": 15,
             "description": "Замена ключей и значений местами"},
            {"title": "Группировка данных", "slug": "data-grouping", "topic": "comprehensions_adv", "order": 16,
             "description": "Группировка списка по признаку в словарь"},
            # День 5: Практика структур данных
            {"title": "Частотный анализ текста", "slug": "freq-analysis", "topic": "data_structures_practice", "order": 17,
             "description": "Подсчёт букв/слов, топ-N элементов"},
            {"title": "Пересечение и разность данных", "slug": "data-intersection", "topic": "data_structures_practice", "order": 18,
             "description": "Общие и уникальные элементы двух коллекций"},
            {"title": "Кэширование результатов", "slug": "caching", "topic": "data_structures_practice", "order": 19,
             "description": "Словарь как кэш, мемоизация вычислений"},
            {"title": "Итог недели: словари и множества", "slug": "week7-final", "topic": "data_structures_practice", "order": 20,
             "description": "Задачи уровня B-C на dict и set"},
        ]
    },
    # ─────────────────────────────────────────────────────────────────
    # НЕДЕЛЯ 8: Файлы и модули
    # ─────────────────────────────────────────────────────────────────
    {
        "number": 8,
        "title": "Файлы и модули",
        "description": "Чтение и запись файлов, CSV, JSON, модуль os, создание своих модулей",
        "lessons": [
            # День 1: Чтение файлов
            {"title": "Открытие файлов: open() и режимы", "slug": "open-modes", "topic": "file_read", "order": 1,
             "description": "Режимы r, w, a, b, x — открытие и закрытие"},
            {"title": "Чтение: read, readline, readlines", "slug": "read-methods", "topic": "file_read", "order": 2,
             "description": "Разные способы чтения, итерация по строкам"},
            {"title": "with оператор", "slug": "with-statement", "topic": "file_read", "order": 3,
             "description": "Контекстный менеджер, автоматическое закрытие"},
            {"title": "Кодировки: UTF-8 и другие", "slug": "encodings", "topic": "file_read", "order": 4,
             "description": "encoding параметр, проблемы кодировок, errors"},
            # День 2: Запись файлов
            {"title": "Запись: write и writelines", "slug": "write-methods", "topic": "file_write", "order": 5,
             "description": "Запись строк и списков строк в файл"},
            {"title": "Добавление в файл (режим a)", "slug": "file-append", "topic": "file_write", "order": 6,
             "description": "Дозапись без перезаписи существующего"},
            {"title": "Работа с путями файлов", "slug": "file-paths", "topic": "file_write", "order": 7,
             "description": "Абсолютные и относительные пути, os.path"},
            {"title": "Буферизация и flush()", "slug": "file-buffer", "topic": "file_write", "order": 8,
             "description": "Буфер записи, принудительный сброс"},
            # День 3: CSV и JSON
            {"title": "Модуль csv: чтение", "slug": "csv-read", "topic": "csv_json", "order": 9,
             "description": "csv.reader, csv.DictReader, разделители"},
            {"title": "Модуль csv: запись", "slug": "csv-write", "topic": "csv_json", "order": 10,
             "description": "csv.writer, csv.DictWriter, заголовки"},
            {"title": "Модуль json: сериализация", "slug": "json-dumps", "topic": "csv_json", "order": 11,
             "description": "json.dumps(), json.dump() — Python → JSON"},
            {"title": "Модуль json: десериализация", "slug": "json-loads", "topic": "csv_json", "order": 12,
             "description": "json.loads(), json.load() — JSON → Python"},
            # День 4: os и pathlib
            {"title": "Модуль os: файловая система", "slug": "os-module", "topic": "os_pathlib", "order": 13,
             "description": "os.listdir, os.getcwd, os.makedirs, os.remove"},
            {"title": "pathlib.Path: современный подход", "slug": "pathlib", "topic": "os_pathlib", "order": 14,
             "description": "Path объекты, операции с путями, итерация"},
            {"title": "Поиск файлов: glob", "slug": "glob-search", "topic": "os_pathlib", "order": 15,
             "description": "glob.glob(), Path.glob() — поиск по шаблону"},
            {"title": "Работа с директориями", "slug": "directories", "topic": "os_pathlib", "order": 16,
             "description": "Создание, удаление, копирование директорий"},
            # День 5: Модули
            {"title": "Импорт модулей: import и from", "slug": "import-modules", "topic": "modules", "order": 17,
             "description": "import, from...import, as, __all__"},
            {"title": "Создание своего модуля", "slug": "create-module", "topic": "modules", "order": 18,
             "description": "Разбивка программы на файлы, пакеты"},
            {"title": "__name__ == '__main__'", "slug": "name-main", "topic": "modules", "order": 19,
             "description": "Точка входа в программу, условный запуск"},
            {"title": "Итог недели: файлы и модули", "slug": "week8-final", "topic": "modules", "order": 20,
             "description": "Проект: обработка CSV-файла с данными"},
        ]
    },
    # ─────────────────────────────────────────────────────────────────
    # НЕДЕЛЯ 9: Исключения и отладка
    # ─────────────────────────────────────────────────────────────────
    {
        "number": 9,
        "title": "Исключения и отладка",
        "description": "try/except, типы исключений, пользовательские ошибки, отладка кода",
        "lessons": [
            # День 1: Основы исключений
            {"title": "Что такое исключение", "slug": "exception-intro", "topic": "exceptions_basics", "order": 1,
             "description": "Ошибки времени выполнения, traceback"},
            {"title": "try/except: перехват ошибок", "slug": "try-except", "topic": "exceptions_basics", "order": 2,
             "description": "Базовый синтаксис try/except"},
            {"title": "Несколько except блоков", "slug": "multi-except", "topic": "exceptions_basics", "order": 3,
             "description": "Обработка разных типов исключений"},
            {"title": "Переменная исключения: as e", "slug": "except-as", "topic": "exceptions_basics", "order": 4,
             "description": "Получение информации об ошибке"},
            # День 2: Типы исключений
            {"title": "ValueError и TypeError", "slug": "value-type-error", "topic": "exception_types", "order": 5,
             "description": "Неверный тип или значение аргумента"},
            {"title": "IndexError и KeyError", "slug": "index-key-error", "topic": "exception_types", "order": 6,
             "description": "Ошибки доступа к коллекциям"},
            {"title": "FileNotFoundError и IOError", "slug": "file-error", "topic": "exception_types", "order": 7,
             "description": "Ошибки работы с файлами"},
            {"title": "ZeroDivisionError и OverflowError", "slug": "math-errors", "topic": "exception_types", "order": 8,
             "description": "Математические ошибки выполнения"},
            # День 3: Продвинутые исключения
            {"title": "else и finally", "slug": "else-finally", "topic": "exceptions_advanced", "order": 9,
             "description": "Код при успехе (else) и всегда (finally)"},
            {"title": "raise: генерация исключений", "slug": "raise-exc", "topic": "exceptions_advanced", "order": 10,
             "description": "Явное возбуждение исключений"},
            {"title": "Цепочки исключений", "slug": "exc-chaining", "topic": "exceptions_advanced", "order": 11,
             "description": "raise ... from ..., контекст исключений"},
            {"title": "Логирование ошибок", "slug": "error-logging", "topic": "exceptions_advanced", "order": 12,
             "description": "Модуль logging, уровни, запись в файл"},
            # День 4: Устойчивый код и практика
            {"title": "Повторные попытки и fallback", "slug": "custom-exc", "topic": "exceptions_practice", "order": 13,
             "description": "Цикл while для повторного запроса при ошибке, значения по умолчанию"},
            {"title": "Обработка ошибок ввода", "slug": "exc-messages", "topic": "exceptions_practice", "order": 14,
             "description": "try/except ValueError при вводе числа, проверка диапазона"},
            {"title": "Исключения в функциях", "slug": "exc-hierarchy", "topic": "exceptions_practice", "order": 15,
             "description": "Перехват ошибок внутри функций, возврат None или значения по умолчанию"},
            {"title": "Защитное программирование", "slug": "exc-best-practices", "topic": "exceptions_practice", "order": 16,
             "description": "Когда использовать try/except, а когда if-проверку — практические правила"},
            # День 5: Отладка
            {"title": "print-отладка и f-строки", "slug": "print-debug", "topic": "debugging", "order": 17,
             "description": "Вывод промежуточных значений, трассировка"},
            {"title": "assert для проверок", "slug": "assert-stmt", "topic": "debugging", "order": 18,
             "description": "Утверждения для отладки и документации"},
            {"title": "pdb: встроенный отладчик", "slug": "pdb-debugger", "topic": "debugging", "order": 19,
             "description": "breakpoint(), pdb команды, пошаговое выполнение"},
            {"title": "Итог недели: надёжный код", "slug": "week9-final", "topic": "debugging", "order": 20,
             "description": "Добавляем обработку ошибок в проекты"},
        ]
    },
    # ─────────────────────────────────────────────────────────────────
    # НЕДЕЛЯ 10: Объектно-ориентированное программирование
    # ─────────────────────────────────────────────────────────────────
    {
        "number": 10,
        "title": "ООП: Объектно-ориентированное программирование",
        "description": "Классы, объекты, наследование, инкапсуляция, магические методы",
        "lessons": [
            # День 1: Основы ООП
            {"title": "Что такое класс и объект", "slug": "class-object", "topic": "oop_basics", "order": 1,
             "description": "Класс как чертёж, объект как экземпляр"},
            {"title": "__init__ и атрибуты экземпляра", "slug": "init-attrs", "topic": "oop_basics", "order": 2,
             "description": "Конструктор, self, instance attributes"},
            {"title": "Методы класса", "slug": "instance-methods", "topic": "oop_basics", "order": 3,
             "description": "Методы с self, вызов методов через объект"},
            {"title": "Атрибуты класса vs экземпляра", "slug": "class-vs-instance", "topic": "oop_basics", "order": 4,
             "description": "Общие и индивидуальные данные"},
            # День 2: Методы класса
            {"title": "@classmethod", "slug": "classmethod", "topic": "oop_methods", "order": 5,
             "description": "Методы класса, cls, фабричные методы"},
            {"title": "@staticmethod", "slug": "staticmethod", "topic": "oop_methods", "order": 6,
             "description": "Статические методы, без self и cls"},
            {"title": "@property: геттеры и сеттеры", "slug": "property", "topic": "oop_methods", "order": 7,
             "description": "Вычисляемые атрибуты, контролируемый доступ"},
            {"title": "Практика: класс Rectangle", "slug": "oop-rect-practice", "topic": "oop_methods", "order": 8,
             "description": "Реализуем класс прямоугольника с методами"},
            # День 3: Наследование
            {"title": "Наследование: дочерние классы", "slug": "inheritance", "topic": "inheritance", "order": 9,
             "description": "class Child(Parent), наследование методов"},
            {"title": "super() и вызов родителя", "slug": "super-call", "topic": "inheritance", "order": 10,
             "description": "Расширение родительского конструктора"},
            {"title": "Переопределение методов", "slug": "method-override", "topic": "inheritance", "order": 11,
             "description": "Изменение поведения в дочернем классе"},
            {"title": "Множественное наследование и MRO", "slug": "multiple-inherit", "topic": "inheritance", "order": 12,
             "description": "Порядок разрешения методов, diamond problem"},
            # День 4: Инкапсуляция и полиморфизм
            {"title": "Инкапсуляция: _private и __mangling", "slug": "encapsulation", "topic": "encapsulation", "order": 13,
             "description": "Соглашения о приватности, name mangling"},
            {"title": "Полиморфизм в Python", "slug": "polymorphism", "topic": "encapsulation", "order": 14,
             "description": "Один интерфейс — разные реализации"},
            {"title": "isinstance() и issubclass()", "slug": "isinstance", "topic": "encapsulation", "order": 15,
             "description": "Проверка типов объектов"},
            {"title": "Абстрактные классы (ABC)", "slug": "abstract-classes", "topic": "encapsulation", "order": 16,
             "description": "abc.ABC, abstractmethod, интерфейсы"},
            # День 5: Магические методы
            {"title": "__str__ и __repr__", "slug": "str-repr", "topic": "dunder_methods", "order": 17,
             "description": "Строковое представление объектов"},
            {"title": "__len__, __contains__, __getitem__", "slug": "container-methods", "topic": "dunder_methods", "order": 18,
             "description": "Поведение как контейнер, индексация"},
            {"title": "__add__, __eq__, __lt__", "slug": "operator-methods", "topic": "dunder_methods", "order": 19,
             "description": "Перегрузка операторов +, ==, <"},
            {"title": "Итог недели: проектируем классы", "slug": "week10-final", "topic": "dunder_methods", "order": 20,
             "description": "Создаём иерархию классов для реальной задачи"},
        ]
    },
    # ─────────────────────────────────────────────────────────────────
    # НЕДЕЛЯ 11: Алгоритмы и структуры данных
    # ─────────────────────────────────────────────────────────────────
    {
        "number": 11,
        "title": "Алгоритмы и структуры данных",
        "description": "Сложность алгоритмов, сортировки, поиск, рекурсия, стек, очередь, DP",
        "lessons": [
            # День 1: Сложность алгоритмов
            {"title": "Big O нотация", "slug": "big-o", "topic": "complexity", "order": 1,
             "description": "O(1), O(n), O(n²), O(log n) — оценка сложности"},
            {"title": "Сравнение алгоритмов по скорости", "slug": "algo-compare", "topic": "complexity", "order": 2,
             "description": "Практическое сравнение, time module"},
            {"title": "Сложность операций коллекций", "slug": "collection-complexity", "topic": "complexity", "order": 3,
             "description": "list vs dict vs set — когда что быстрее"},
            {"title": "Оптимизация простого кода", "slug": "simple-optimization", "topic": "complexity", "order": 4,
             "description": "Улучшаем O(n²) → O(n) на реальных примерах"},
            # День 2: Алгоритмы сортировки
            {"title": "Пузырьковая сортировка", "slug": "bubble-sort", "topic": "sorting_algorithms", "order": 5,
             "description": "Алгоритм, реализация, O(n²)"},
            {"title": "Сортировка выбором и вставками", "slug": "select-insert-sort", "topic": "sorting_algorithms", "order": 6,
             "description": "Selection sort и Insertion sort"},
            {"title": "Быстрая сортировка (Quicksort)", "slug": "quicksort", "topic": "sorting_algorithms", "order": 7,
             "description": "Алгоритм divide & conquer, O(n log n)"},
            {"title": "Сортировка слиянием (Mergesort)", "slug": "mergesort", "topic": "sorting_algorithms", "order": 8,
             "description": "Стабильная сортировка, рекурсивное разделение"},
            # День 3: Поиск и рекурсия
            {"title": "Линейный и бинарный поиск", "slug": "linear-binary-search", "topic": "search_recursion", "order": 9,
             "description": "O(n) vs O(log n), требования к бинарному поиску"},
            {"title": "Рекурсия: базовый случай и шаг", "slug": "recursion-basics", "topic": "search_recursion", "order": 10,
             "description": "Рекурсивные функции, стек вызовов"},
            {"title": "Рекурсивные алгоритмы", "slug": "recursive-algos", "topic": "search_recursion", "order": 11,
             "description": "Факториал, числа Фибоначчи, ханойские башни"},
            {"title": "Хвостовая рекурсия и itertools", "slug": "tail-recursion", "topic": "search_recursion", "order": 12,
             "description": "Оптимизация, замена рекурсии итерацией"},
            # День 4: Стек, очередь, дек
            {"title": "Стек (Stack) на основе list", "slug": "stack-impl", "topic": "stack_queue_deque", "order": 13,
             "description": "LIFO, push/pop, применение стека"},
            {"title": "Очередь (Queue) с deque", "slug": "queue-impl", "topic": "stack_queue_deque", "order": 14,
             "description": "FIFO, collections.deque, appendleft/popleft"},
            {"title": "Двусторонняя очередь (Deque)", "slug": "deque-ops", "topic": "stack_queue_deque", "order": 15,
             "description": "Операции с обоих концов, rotate"},
            {"title": "Задачи на стек и очередь", "slug": "stack-queue-tasks", "topic": "stack_queue_deque", "order": 16,
             "description": "Скобочные выражения, BFS обходы"},
            # День 5: Динамическое программирование
            {"title": "Мемоизация: кэш рекурсии", "slug": "memoization", "topic": "dp_intro", "order": 17,
             "description": "functools.lru_cache, ручной кэш через dict"},
            {"title": "Числа Фибоначчи через DP", "slug": "fib-dp", "topic": "dp_intro", "order": 18,
             "description": "Сверху вниз vs снизу вверх, таблица"},
            {"title": "Задача о монетах (Coin Change)", "slug": "coin-change", "topic": "dp_intro", "order": 19,
             "description": "Классическая задача DP, оптимальная разбивка"},
            {"title": "Итог недели: алгоритмические задачи", "slug": "week11-final", "topic": "dp_intro", "order": 20,
             "description": "Задачи уровня C на алгоритмы и структуры данных"},
        ]
    },
    # ─────────────────────────────────────────────────────────────────
    # НЕДЕЛЯ 12: Подготовка к Yandex CodeRun
    # ─────────────────────────────────────────────────────────────────
    {
        "number": 12,
        "title": "Подготовка к Yandex CodeRun",
        "description": "Типовые паттерны задач, строки, массивы, числа, графы и финальный экзамен",
        "lessons": [
            # День 1: Задачи на строки
            {"title": "Паттерн: два указателя на строках", "slug": "two-pointers-str", "topic": "string_problems", "order": 1,
             "description": "Палиндром, реверс слов, сравнение с двух концов"},
            {"title": "Паттерн: скользящее окно", "slug": "sliding-window", "topic": "string_problems", "order": 2,
             "description": "Подстрока фиксированной длины, максимум в окне"},
            {"title": "Анаграммы и перестановки", "slug": "anagram-tasks", "topic": "string_problems", "order": 3,
             "description": "Сортировка символов, Counter, хэш-подход"},
            {"title": "Разбор и форматирование строк", "slug": "string-parsing", "topic": "string_problems", "order": 4,
             "description": "Парсинг выражений, сборка результата"},
            # День 2: Задачи на массивы
            {"title": "Два указателя на массивах", "slug": "two-pointers-arr", "topic": "array_problems", "order": 5,
             "description": "Сумма двух чисел, уникальные пары, reverse"},
            {"title": "Скользящее окно на массивах", "slug": "sliding-window-arr", "topic": "array_problems", "order": 6,
             "description": "Максимальная сумма подмассива (Kadane)"},
            {"title": "Префиксные суммы", "slug": "prefix-sums", "topic": "array_problems", "order": 7,
             "description": "Быстрые запросы суммы на отрезке"},
            {"title": "Задачи на сортировку массива", "slug": "sorted-array-tasks", "topic": "array_problems", "order": 8,
             "description": "Поиск дублей, медиана, k-й элемент"},
            # День 3: Задачи на числа
            {"title": "НОД и НОК (алгоритм Евклида)", "slug": "gcd-lcm", "topic": "number_problems", "order": 9,
             "description": "Рекурсивный и итеративный НОД, НОК через НОД"},
            {"title": "Простые числа: решето Эратосфена", "slug": "sieve", "topic": "number_problems", "order": 10,
             "description": "Генерация простых до N, эффективно O(n log log n)"},
            {"title": "Разряды числа и цифры", "slug": "digits-ops", "topic": "number_problems", "order": 11,
             "description": "Сумма цифр, разворот числа, работа с разрядами"},
            {"title": "Модульная арифметика", "slug": "modular-arith", "topic": "number_problems", "order": 12,
             "description": "% оператор, задачи с остатком, цикличность"},
            # День 4: Графы
            {"title": "Представление графов", "slug": "graph-repr", "topic": "graph_problems", "order": 13,
             "description": "Список смежности, матрица смежности"},
            {"title": "Обход в ширину (BFS)", "slug": "bfs", "topic": "graph_problems", "order": 14,
             "description": "BFS с очередью, кратчайший путь без весов"},
            {"title": "Обход в глубину (DFS)", "slug": "dfs", "topic": "graph_problems", "order": 15,
             "description": "DFS рекурсивный и итеративный"},
            {"title": "Задачи на графы уровня C", "slug": "graph-tasks", "topic": "graph_problems", "order": 16,
             "description": "Связность, количество компонент, топ. сортировка"},
            # День 5: Финальный экзамен
            {"title": "Разбор задач Yandex CodeRun уровня A-B", "slug": "coderun-ab", "topic": "final_practice", "order": 17,
             "description": "Разбор типовых задач первых уровней"},
            {"title": "Разбор задач Yandex CodeRun уровня C", "slug": "coderun-c", "topic": "final_practice", "order": 18,
             "description": "Задачи на алгоритмы и структуры данных"},
            {"title": "Советы по участию в контесте", "slug": "contest-tips", "topic": "final_practice", "order": 19,
             "description": "Стратегия, работа со временем, оформление решений"},
            {"title": "Финальный экзамен курса", "slug": "final-exam", "topic": "final_practice", "order": 20,
             "description": "Финальный набор задач уровня Yandex CodeRun"},
        ]
    },
]
