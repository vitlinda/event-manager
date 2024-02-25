## Run the application

Build the docker image:
```bash
docker-compose build
``` 

Run the container:
```bash
docker-compose up
```

The application can be accessed at http://127.0.0.1:8000/

Tests can be run using the following command from the root directory of the project:
```bash
pytest
```

The API can be tried out using the following link via swagger interface:

http://127.0.0.1:8000/api/schema/swagger/
