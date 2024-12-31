## Переводчик

Бот-переводчик, позволяющий перевести любой текст на практически любом языке мира.

## Руководство по эксплуатации

- В корне проекта создаем файл .env
- В него добавляем переменную ```BOT_TOKEN```
- Сохраняем и далее скачиваем все пакеты, которые перечислены в requirements.txt
- Переходим в каталог нашего проекта через терминал и запускаем файл **main.py**
- Довольствуемся результатом

## Тесты

- Для тестов вводим pytest в терминал, находясь в корневом каталоге проекта

## Документация

### config.py

Получение переменной окружения ```BOT_TOKEN```.

### languages.py

Класс с вложенным словарем из всех языков и их кодов.

### main.py

Основной файл. В нём реализуется следующее:

- Обработка базовых команд */start*, */help* и */cancel*
- Сам перевод текста с помощью FSM

### translate.py

Одна лишь функция для перевода текста с помощью API Mymemory.

### test_main.py

Файл с тестами основных команд и перевода.

## Предупреждение

Если слова будут переводиться некорректно, то проблема связана с Mymemory.
Лучше чем Mymemory я не нашел (другие либо недоступны в РФ, либо платные).
Просьба отнестись с пониманием!

## CI/CD

В пайплайне я добавил всего лишь две джобы: build и test.
Да, джобы по типу deploy нет, т.к у [render](https://render.com/) CI/CD уже настроено, но на всякий случай закомментил джобу deploy.

## Никнейм

Никнейм в телеграме вот: @translatorinksne_bot

Можете распространять код, делать с ним что угодно, если будут вопросы, то вот почта:
```inksne@gmail.com```
