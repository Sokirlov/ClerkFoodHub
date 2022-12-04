# Hello, it's my pet project Foods HUB
### The project is designed to help order food to the office and offset between employees


For start project you need have the Docker.
1. run the command `"git clone https://github.com/Sokirlov/ImperialFoodPars.git"`
2. create the file dev.env in directory ImperialFoodPars
3. Add the following content to the `dev.env`
```dev.env
PYTHONDONTWRITEBYTECODE=1
PYTHONUNBUFFERED=1
DJANGO_SETTINGS_MODULE=ClerkFoodhub.settings

POSTGRES_DB= write here your database name
POSTGRES_USER= write here user for database
POSTGRES_PASSWORD= write here password for database
ADM_USER= write here SuperAdministrator name
ADM_PASS= write here SuperAdministrator password
```
4. run the command "docker-compose up --build"
5. Project automatic add Super User and update data from caterings base
