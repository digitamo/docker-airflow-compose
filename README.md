# Docker Airflow Spark
An example repo demonstrating usage of Airflow and Docker withing a containerized environment. The Airflow job runs a simple Spark job estimating the value of π (Pi))

**NOTE** This example is based on the official [Running Airflow in Docker](https://airflow.apache.org/docs/apache-airflow/2.5.3/docker-compose.yaml) guide with minor tweaks.
## requirements

 1. docker compose v1.29.1 or newer


## Running locally

1. Set up env vars `echo -e "AIRFLOW_UID=$(id -u)\nAIRFLOW_GID=0" > .env`
2. Build the Spark job
   ```bash
   $ docker build -f spark/app/Dockerfile -t pi-estimate-task spark/app
   ```
3. Run `docker-compose up airflow-init` which essentially runs `airflow db init`
4. Start the Airflow web service and other components via `docker-compose up`
   4.1. (Optional) you can access the airflow web server by navigating to "localhost:8080" with the default user and password:
      - User: `airflow`
      - Password: `airflow`
6. Once you're done, clean up by running: `docker-compose down --volumes --rmi all`
