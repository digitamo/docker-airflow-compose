# Take home assignment

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
4. Start the Airflow web service and other components via `docker-compose up`
5. Simulate writing user events into S3
   ```bash
    $ aws s3 cp ./data/example.csv  s3://user-events/year=${year}/month=${month}/day=${day}/example.csv --endpoint-url=http://localhost:4566
    ```
    Where `${year}`, `${month}` and `${day}` represent today's date
6. Once you're done, clean up by running: `docker-compose down --volumes --rmi all`

# Design Questions
## Design diagram
![design-diagram](./dist/system-design.jpg)

## Design considerations

### AWS kinesis Firehose
Kinesis Firehose is used as the main ingestion point for flexibility and scalability. 
A Firehose stream offers multiple integration points, moreover, dynamic partitioning is possible at ingestion time [ref](https://docs.aws.amazon.com/firehose/latest/dev/dynamic-partitioning.html#dynamic-partitioning-partitioning-keys).

Alternatively, Kinesis and Firehose can be discarded if the budget is limited in favor of
writing the raw data into S3 directly. However, this delegates the partitioning 
responsibility to the data producers (Mobile devices)

### AWS EKS
Kubernetes is used for scalability and the number of integrations available. Both Apache 
Spark and Airflow can be setup with the help of Helm charts. EKS is chosen for ease of use compared to a self-managed approach

### Airflow and Spark
Given the data volume in conjunction with the fact that most of the workloads are processed in batches rather than even-driven,
Apache Airflow and Apache Spark are used. Offering a versatile data processing platform capable of handling large data volumes

### S3
S3 is the main data storage solution offering a durable and low cost storage solution
for both structured and unstructured data with a wide range of storage classes. 
Combined with AWS IAM data can be shared in a secure way, offering fine-grained access control to stockholders with the possibility
to extend and customize data access control

### Athena
With AWS Athena we can analyze semi-structured and structured data without the need to 
run a dedicated database system. Using AWS Athena helps bring the costs down since it's
a serverless interactive query service

### Power BI
Power BI is used as the main business intelligence service for reporting. Using [Amazon Athena Power BI connector](https://docs.aws.amazon.com/athena/latest/ug/connect-with-odbc-and-power-bi.html) Power BI can be connected to AWS Athena, in order to
keep the data up to date for recurring report we can use [Power BI gateway](https://powerbi.microsoft.com/en-us/gateway/)