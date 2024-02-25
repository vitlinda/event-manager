## Run the application

Build the docker image:
```bash
> docker build -t event_manager .
``` 

Run the docker container:
```bash
> docker run -p 8080:8080 event_manager
```

Then the application can be accessed at http://127.0.0.1:8000/

The tests can be run using the following command from the root directory of the project:

```bash
> pytest
```

The API can be tried out using the following link via the swagger interface:

http://127.0.0.1:8000/swagger/
