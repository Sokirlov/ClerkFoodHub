# Привіт, це Clerk Foodhub він ще На стадії розробки 
### Він допоможе замовляти їжу в офіс для себе та колег. Розділти рахунки та слідкувати за боргами.


Щоб спробувати проект вам потрібно мати Docker.
1. Завантажте проект, для цього виконате команду`git clone https://github.com/Sokirlov/ImperialFoodPars.git`
2. Відкрите сомандну строку у завантаженій папці 
3. Виконате команду `docker-compose --env-file dev.env up --build`
4. Проект автоматично запуститься та завантажить демонстраціні данні. 
5. Головний користувач `root` та пароль `root`



#### Для налаштувань редагуйте dev.env файл 

1. У фалі `dev.env` такі налаштування
```dev.env
PYTHONDONTWRITEBYTECODE=1
PYTHONUNBUFFERED=1
DJANGO_SETTINGS_MODULE=ClerkFoodhub.settings

POSTGRES_DB= database name
POSTGRES_USER= database user
POSTGRES_PASSWORD= database password
ADM_USER= SuperAdministrator name in Django
ADM_PASS= SuperAdministrator password in Django
LOAD_DEMO_DATA=  True for add demo data
```

