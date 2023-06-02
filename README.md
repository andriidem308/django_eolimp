# django_eolimp

## Запуск

Клонуємо проект:
```
git clone https://github.com/projectowner/projectname.git
```

Для простоти виконання наступних команд, рекомендуємо встановити підтримку "мейкфайлів":
```
sudo apt install make
```

Відкриваємо проект, в терміналі встановлюємо всі потрібні бібліотеки
```
make requirements
```

Робимо міграції бази даних
```
make migrate_tst
make migrate_acc
make migrate
```

Запускаємо проект
```
make run
```

Переходимо за посиланням у командному вікні, а саме
```
http://127.0.0.1:8000/
```


Переходимо послідовно за посиланнями щоб заповнити базу даних:
```
1. http://127.0.0.1:8000/create_teachers
2. http://127.0.0.1:8000/create_groups
3. http://127.0.0.1:8000/create_students
4. http://127.0.0.1:8000/create_problems
5. http://127.0.0.1:8000/create_lectures
```
