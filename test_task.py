import luigi
import pickle
import pprint

# $ rm *.output; PYTHONPATH=$PWD luigi --module test_task TaskA --local-scheduler --config '{"keyA": "value", "keyB":"value", "keyC":"value"}'

class ParsedDict:

    keys = ["keyA", "keyB", "keyC"]

    def __init__(self, config):
        missing_keys = set(self.keys) - set(config)
        extra_keys = set(config) - set(self.keys)
        if len(missing_keys) or len(extra_keys):
            raise ValueError("Invalid dict (TODO: print the keys here)")

        for key in config.keys():
            setattr(self, key, config[key])

    def to_dict(self):
        return {key: getattr(self, key) for key in self.keys}

class TaskA(luigi.Task):
    config = luigi.DictParameter()

    def output(self):
        return luigi.LocalTarget("task1.output")

    def requires(self):
        parsed_dict = ParsedDict(self.config)
        yield SubTaskB(pyobj_param=parsed_dict.to_dict(), pickled_param=pickle.dumps(parsed_dict)) 

    def run(self):
        with self.output().open('w') as out_file:
            print("Task output", file=out_file) 

class SubTaskB(luigi.Task):

    pyobj_param = luigi.DictParameter()
    pickled_param = luigi.Parameter()

    def output(self):
        return luigi.LocalTarget("subtaskB.output")

    def run(self):
        with self.output().open('w') as out_file:
            print("Task output", repr(self.pyobj_param), file=out_file) 
            parsed_dict = pickle.loads(self.pickled_param)
            print("Task output", repr(parsed_dict), pprint.pformat(parsed_dict.to_dict()), file=out_file) 
