import copy
import inspect

import yaml


class YamlReader:
    """
    # Summary
    Read a YAML file and return its contents as a python dict.

    # Usage

    ## Assume /tmp/config.yaml contains the following YAML:

    ```yaml
    config:
        discover_password: MySwitchPassword
        discover_username: admin
        fabric_name: MyFabric
        seed_ip: 10.1.1.2
    ```

    ## Code

    ```python
    reader = YamlReader()
    reader.filename = "/tmp/config.yaml"
    print(f"reader.contents: {reader.contents}")

    discover_password = reader.contents.get("config", {}).get("discover_password")
    # etc
    ```

    """

    def __init__(self):
        self.class_name = self.__class__.__name__
        self._filename = None
        self._contents = None

    def validate(self):
        """
        # Summary
        Validate user input

        # Raises
        - ValueError if user input is invalid
        """
        method_name = inspect.stack()[1][0]
        if self.filename is None:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"{self.class_name}.filename must be set before "
            msg += f"calling {self.class_name}.commit()."
            raise ValueError(msg)

    def commit(self):
        """
        # Summary
        Read the contents of ``filename`` and populate accessor
        property ``contents`` with its contents.

        # Raises
        - ValueError if ``filename`` cannot be read.
        """
        method_name = inspect.stack()[1][0]
        self.validate()
        try:
            with open(self.filename, "r", encoding="UTF-8") as file:
                self.contents = yaml.safe_load(file)
        except IOError as error:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"Unable to read filename {self.filename}. "
            msg += f"Error detail: {error}"
            raise ValueError(msg) from error

    @property
    def filename(self):
        """
        # Summary
        YAML file to read.
        """
        return self._filename

    @filename.setter
    def filename(self, value):
        self._filename = value

    @property
    def contents(self):
        """
        # Summary
        Return the contents of ``filename`` as a python dictionary.
        """
        return copy.deepcopy(self._contents)

    @contents.setter
    def contents(self, value):
        self._contents = value
