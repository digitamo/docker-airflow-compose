<!-- TODO: Polish the README docs-->
## requirements

 1. docker compose v1.29.1 or newer
 2. aws cli


## Running locally

1. Set up env vars `echo -e "AIRFLOW_UID=$(id -u)\nAIRFLOW_GID=0" > .env`
2. Build the Spark job
   ```bash
   $ docker build -f spark/app/Dockerfile -t event-transformation-task spark/app
   ```
3. Run `docker-compose up airflow-init` which essentially runs `airflow db init`
   3.1. (Optionally) access the airflow web server by navigating to "localhost:8080" with the default user and password:
      - User: `airflow`
      - Password: `airflow`
4. Simulate writing user events into S3
   ```bash
    $ aws s3 cp ./data/example.csv  s3://user-events/year=2023/month=03/day=23/example.csv --endpoint-url=http://localhost:4566
    ```
5. Start the Airflow web service and other components via `docker-compose up`
6. Clean up by running: `docker-compose down --volumes --rmi all`
