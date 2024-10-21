import copy
import inspect
import yaml

class YamlReader:
    def __init__(self):
        self.class_name = self.__class__.__name__
        self._filename = None
        self._contents = None

    def validate(self):
        method_name = inspect.stack()[1][0]
        if self.filename is None:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"{self.class_name}.filename must be set before "
            msg += f"calling {self.class_name}.commit()."
            raise ValueError(msg)
    def commit(self):
        method_name = inspect.stack()[1][0]
        self.validate()
        try:
            with open(self.filename, 'r') as file:
                self.contents = yaml.safe_load(file)
        except IOError as error:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"Unable to read filename {self.filename}. "
            msg += f"Error detail: {error}"
            raise ValueError(msg) from error
    
    @property
    def filename(self):
        return self._filename
    @filename.setter
    def filename(self, value):
        self._filename = value
        
    @property
    def contents(self):
        return copy.deepcopy(self._contents)
    @contents.setter
    def contents(self, value):
        self._contents = value
