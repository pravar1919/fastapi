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
