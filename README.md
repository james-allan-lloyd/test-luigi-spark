# test-luigi-spark

Simple setup to test luigi and spark integration.

## Setting up basic spark cluster

```shell
export INSTALL_DIR=$HOME
# goto https://spark.apache.org/downloads.html to select a different version/mirror
curl -OL https://ftp.nluug.nl/internet/apache/spark/spark-3.1.2/spark-3.1.2-bin-hadoop3.2.tgz
tar xvf spark-3.1.2-bin-hadoop3.2.tgz
cd spark-3.1.2-bin-hadoop3.2
echo SPARK_MASTER_HOST=localhost > conf/spark-env.sh
./sbin/start-master
./sbin/start-worker spark://localhost:7077
# logs should be in $PWD/logs
# dashboard should be at http://localhost:8080
```

Stopping the spark cluster:
```shell
./sbin/stop-worker
./sbin/stop-master
```

Ensure that spark-3.1.2-bin-hadoop3.2/bin is in your path:
```shell
export OLD_PATH=$PATH
export PATH=$OLD_PATH:$INSTALL_DIR/spark-3.1.2-bin-hadoop3.2/bin
```

## Submitting a script based spark job with luigi
SparkScriptTask is pretty thin wrapper around spark-submit, adding luigi
monitoring and output control.

```shell
PYTHONPATH=$PWD luigi --module spark_tasks SparkScriptTask --local-scheduler --partitions 10
```

## Submitting a spark job with luigi using a direct module import
The SparkModuleTask runs code directly (as opposed to a stand alone script).
Probably means you need to do more to ensure that identical versions of python
are running on both the luigi node and the spark workers.

```shell
PYTHONPATH=$PWD luigi --module spark_tasks SparkModuleTask --local-scheduler --partitions 10
```
