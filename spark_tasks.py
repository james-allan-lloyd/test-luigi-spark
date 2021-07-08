from luigi.contrib.spark import SparkSubmitTask, PySparkTask
import luigi


class SparkScriptTask(SparkSubmitTask):
    partitions = luigi.IntParameter()
    app = "spark_app.py"

    @property
    def name(self):
        return self.__class__.__name__

    @property
    def master(self):
        return 'spark://localhost:7077'

    def app_options(self):
        return [self.partitions]

class SparkModuleTask(PySparkTask):

    partitions = luigi.IntParameter()

    @property
    def name(self):
        return self.__class__.__name__

    @property
    def master(self):
        return 'spark://localhost:7077'

    def main(self, sc, *args):
        import spark_app
        spark_app.run(sc, self.partitions)
        
