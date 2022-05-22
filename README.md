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
make migrate_acc
make migrate_tst
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
