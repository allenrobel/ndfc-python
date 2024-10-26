import copy
import inspect
import logging

from ndfc_python.yaml_reader import YamlReader


class ReadConfig:
    """
    # Summary
    Returns the contents of a YAML file as a dictionary, given a path to the file.

    # Usage example

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
    try:
        ndfc_config = ReadConfig()
        ndfc_config.filename = "/tmp/config.yaml"
        ndfc_config.commit()
    except ValueError as error:
        msg = f"Exiting: Error detail: {error}"
        log.error(msg)
        sys.exit()
    config = ndfc_config.contents.get("config")
    if config is None:
        exit()
    print(f"config.fabric_name: {config.get("fabric_name)}"
    ```

    ## Output

    config.fabric_name: MyFabric

    """

    def __init__(self):
        self.class_name = self.__class__.__name__
        self.log = logging.getLogger(f"ndfc_python.{self.class_name}")
        self.reader = YamlReader()
        self._filename = None

    def commit(self):
        """
        # Summary

        Set self.contents to the contents of the YAML file pointed to by filename.

        # Raises
        - ValueError if:
            - filename is not set
            - YamlRead().commit() raises ValueError
        """
        method_name = inspect.stack()[0][3]
        if self.filename is None:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"{self.class_name}.filename must be set before calling "
            msg += f"{self.class_name}.commit"
            raise ValueError(msg)

        self.reader.filename = self.filename
        try:
            self.reader.commit()
        except ValueError as error:
            msg = f"Cannot read configuration file {self.filename}. "
            msg += f"Error detail: {error}"
            raise ValueError(msg) from error

        self.contents = self.reader.contents
        if self.contents is None:
            msg = f"Configuration file {self.filename} is empty."
            raise ValueError(msg)

    @property
    def filename(self):
        """
        # Summary
        Absolute path to a YAML file.
        """
        return self._filename

    @filename.setter
    def filename(self, value):
        self._filename = value

    @property
    def contents(self):
        """
        # Summary
        The contents of filename, as a python dict.
        """
        return copy.deepcopy(self._contents)

    @contents.setter
    def contents(self, value):
        self._contents = value
