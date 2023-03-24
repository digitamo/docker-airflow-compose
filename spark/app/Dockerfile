FROM python:3.9.1

ARG SPARK_VERSION="3.3.2"
ARG HADOOP_VERSION="3"
# ARG AWS_ACCESS_KEY_ID="XXX"
# ARG AWS_SECRET_ACCESS_KEY="XXX"

ENV S3_ENDPOINT="http://localstack:4566"


###############################
## Begin JAVA installation
###############################
# Java is required in order to spark-submit work
# Install OpenJDK-8
RUN apt-get update && \
    apt-get install -y software-properties-common && \
    apt-get install -y gnupg2 && \
    apt-key adv --keyserver keyserver.ubuntu.com --recv-keys EB9B1D8886F44E2A && \
    add-apt-repository "deb http://security.debian.org/debian-security stretch/updates main" && \ 
    apt-get update && \
    apt-get install -y openjdk-11-jdk && \
    pip freeze && \
    java -version $$ \
    javac -version

# Setup JAVA_HOME 
ENV JAVA_HOME /usr/lib/jvm/java-11-openjdk-amd64
RUN export JAVA_HOME
###############################
## Finish JAVA installation
###############################

###############################
## SPARK files and variables
###############################

# DOWNLOAD SPARK AND INSTALL
RUN DOWNLOAD_URL_SPARK="https://dlcdn.apache.org/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz" \
    && wget --no-verbose -O apache-spark.tgz  "${DOWNLOAD_URL_SPARK}"\
    && mkdir -p /home/spark \
    && tar -xf apache-spark.tgz -C /home/spark --strip-components=1 \
    && rm apache-spark.tgz

# SET SPARK ENV VARIABLES
ENV SPARK_HOME="/home/spark"
ENV PATH="${SPARK_HOME}/bin/:${PATH}"

# SET PYSPARK VARIABLES
ENV PYTHONPATH="${SPARK_HOME}/python/:$PYTHONPATH"
ENV PYTHONPATH="${SPARK_HOME}/python/lib/py4j-0.10.9.5-src.zip:$PYTHONPATH"


# Add jars
WORKDIR ${SPARK_HOME}/jars
RUN wget https://repo1.maven.org/maven2/com/google/guava/guava/23.1-jre/guava-23.1-jre.jar
RUN wget https://repo1.maven.org/maven2/org/apache/spark/spark-hadoop-cloud_2.12/3.3.0/spark-hadoop-cloud_2.12-3.3.0.jar
RUN wget https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/1.11.1026/aws-java-sdk-bundle-1.11.1026.jar
RUN wget https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/3.3.2/hadoop-aws-3.3.2.jar
WORKDIR ${SPARK_HOME}
###############################
## Finish SPARK files and variables
###############################

# Install PySpark
RUN pip install pyspark==${SPARK_VERSION}

# Switch users
RUN adduser --disabled-password --gecos '' spark
USER spark

COPY . .


CMD ["spark-shell"]