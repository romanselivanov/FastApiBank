http:/localhost:8000/docs - документация  

http:/localhost:8000/ - POST отправить dna 3 буквы для поиска  
Для авторизации используется JWT токен, нужно зарегистрировать пользователя  
и в http:/localhost:8000/docs нажать Authorise, либо отправить токен в POST'е)  

http:/localhost:8000/ - GET просто проверка работоспособности сервера  

/sign-up - регистрация  
/login - аутентификация  
/me - просмотр о себе для авторизации используется JWT токен  

How to install:  

1) pip install poetry  
2) poetry install  
3) alembic upgrade 1111111111@head
4) python main.py  

1.	Пользователь должен иметь возможность зарегистрироваться в системе (для регистрации использовать почту и пароль и номер телефона. Пароль состоит не менее, чем из 8 знаков обязательно содержит минимум одну заглавную букву и одну цифру). После регистрации пользователь должен подтвердить свою почту через 6-ти значный цифровой код, который должен быть отправлен ему после завершения регистрации на почту. Данные пользователя: Имя Фамилия Отчество, электронная почта, номер телефона  
2.	Пользователь должен иметь возможность входа в систему. Для входа используются почта или номер телефона и пароль  

для асинхронной работы с бд используются:  
SQLAlchemy  
aiosqlite  
databases  

для миграций:  
alembic  

генерация JWT токена:  
python-jose[cryptography]  
passlib[bcrypt]  

тесты:  
pytest  
SQLAlchemy-Utils  

для отправки email:  
emails  
Jinja2  