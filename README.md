<!-- TODO: Polish the README docs-->
## requirements

 1. docker compose v1.29.1 or newer
 2. aws cli


## Running locally

1. Set up env vars `echo -e "AIRFLOW_UID=$(id -u)\nAIRFLOW_GID=0" > .env`
2. Run `docker-compose up airflow-init` which essentially runs `airflow db init`
   3.1. Access the airflow web server by navigating to "localhost:8080" with the default user and password:
      - User: `airflow`
      - Password: `airflow`
3. Simulate user events being available by running 
<!-- TODO: add S3 cp command -->

5. Clean up by running: `docker-compose down --volumes --rmi all`


## Setup
1) First create a container with the webservice and create the `airflow` user, [as described in the official docs](https://airflow.apache.org/docs/apache-airflow/stable/start/docker.html):

```bash
$ docker-compose up airflow-init
```

1) Build the Spark job.

```bash
$ docker build -f spark/app/Dockerfile -t event-transformation-task spark/app
```

1) Start the Airflow web service and other components via `docker-compose up`

3) Emulate incoming data:
   `aws s3 cp ./data/example.csv  s3://user-events/year=2023/month=03/day=23/example.csv --endpoint-url=http://localhost:4566`

4) Finally when you're done with your experiment, stop all containers running the following command:
```bash
$  `docker-compose down --volumes --rmi all`
```

## References
- [Airflow docker compose](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html)