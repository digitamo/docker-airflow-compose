<!-- TODO: Polish the README docs-->
## requirements

~~1. Python 3.8~~
~~2. `pip install -r requirements.txt~~
~~2. Airflow installation~~
~~`export AIRFLOW_HOME=~/.airflow`~~

 1. docker compose v1.29.1 or newer

## Running locally
1. `pip install -r requirements.txt`
2. `airflow standalone`

## Running locally

1. Set up env vars `echo -e "AIRFLOW_UID=$(id -u)\nAIRFLOW_GID=0" > .env`
2. Initialize airflow database: `docker-compose up airflow-init` more info on the docker compose setup can be found [here](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html)
3. Run `docker-compose up airflow-init` which essentially runs `airflow db init`
   3.1. Access the airflow web server by navigating to "localhost:8080" with the default user and password:
      - User: `airflow`
      - Password: `airflow`
4. Clean up by running: `docker-compose down --volumes --rmi all`


## Setup
1) First create a container with the webservice and create the `airflow` user, [as described in the official docs](https://airflow.apache.org/docs/apache-airflow/stable/start/docker.html):

```bash
$ docker-compose up airflow-init
```

1) Build the Spark job.

```bash
$ docker build -f dags/docker_job/Dockerfile -t event-transformation-task .
```

1) Start the Airflow web service and other components via `docker-compose up`

2) Finally when you're done with your experiment, stop all containers running the following command:
```bash
$  `docker-compose down --volumes --rmi all`
```