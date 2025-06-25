For database connection

1. Create an .env file in the base of the project.
2. Create a config file in the base of the project add Settings class, that can be used to access the .env variables, using the pydantic-settings module. Create an object of that class to access those throughout the project.
3. Create a DB pakage, using async db engine and connection using Sqlmodel and SqlAlchemy.

- To Connect to the database the right time is when the project starts i.e in the main file or in "**init**.py" file of src package.
- FastAPI provide us doing that in the form of lifespan events.
- This can be achieved by using a contextlib library by asynccontextmanager decorator
- There is a keyword 'yeild',
  - everyting above yield executed when the server is started.
  - everyting below yield executed when the server is stopped.

For Migration:

- Alembic is used for migrating the tables in FastAPI.
- For that have to create a migration environment, which track the changes in the database using a file, which tracks all the changes in the structure of the database.

```
uv run alembic init -t async migrations
```

- This commands create a migration folder and ini file in the root of the folder which tracks the version and migrations for the project.

Command to do migration

```
uv run alembic revision --autogenerate -m "initial migration"
```

Command to migrate

```
uv run alembic upgrade head
```
