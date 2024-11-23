# manage-books app

CLI приложение для управления списком книг.

## First time setup

Приложение написано без использования сторонних библиотек, в связи с чем не нуждается в установке зависимостей. 


## Run app

Чтобы создать файл хранилища, используйте команду добавленяи книги либо создайте вручную `src/data/storage.jsonl`

1. Добавление книги. Команда создаст файл-хранилище, если его еще нет. При указании опционального аргумента `-p` будут распечатаны данные добавленной книги. 

```PowerShell
# три позиционных аргумента: название, год публикации, имя автора
# название и имя автора необходимо указывать в кавычках, год без кавычек
python -m books add "book title" 2000 "book author"
```

2. Удаление книги через указание id. При указании опционального аргумента `-p` будут распечатаны данные удалённой книги.
```PowerShell
python -m books del bookid
```

3. Поиск книг по названию, году публикации или автору. Необходимо указать один из трёх взаимоисключающих аргументов: `-t --title`, `-y --year` или `-a --author`. Команда распечатает все совпадающие результаты.
```PowerShell
# название и имя автора необходимо указывать в кавычках, год без кавычек
python -m books search -t "book title"

python -m books search -y 2000

python -m books search -a "book author"
```

4. Показать весь список книг. Команда распечатает все книги из хранилища в виде таблицы.
```PowerShell
python -m books list
```

5. Изменить статус книги через id. При указании опционального аргумента `-p` будут распечатаны данные изменённой книги.
```PowerShell
# доступны два статуса: 'in stock' и 'out of stock'. этот аргумент необхожимо указывать в кавычках
python -m books status bookid "out of stock"

python -m books status bookid "in stock"
```


## Run tests

Тесты также написаны без использования сторонних библиотек и не нуждаются в установке зависимостей.

```PowerShell
# команда запустит test discovery, благодаря чему все тесты должны запуститься "из коробки"
python -m unittest
```

Запуск тестовых модулей по отдельности

```PowerShell
python -m unittest .\tests\test_module_name.py
```