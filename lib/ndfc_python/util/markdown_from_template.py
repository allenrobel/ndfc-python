import inspect
import logging
import sys

import yaml


class MarkdownFromTemplate:
    """
    # Name

    lib/ndfc_python/util/markdown_from_template.py

    # Description

    Read a YAML file given by `template_path` and output `markdown_file`
    containing markdown representing the parameters in `template_path`.

    ## Usage

    ``` python
    from ndfc_python.util.markdown_from_template import MarkdownFromTemplate
    instance = MarkdownFromTemplate()
    instance.template_file = "/tmp/template_file.yaml"
    instance.markdown_file = "/tmp/markdown_file.md"
    instance.commit()
    ```

    ## Sample markdown

    ```
    #### parameter_1

    Description.

    - default: <default>
    - example: <example>
    - type: str | bool | int | etc

    #### parameter_2

    Description.

    - default: <default>
    - example: <example>
    - type: str | bool | int | etc
    ```
    """

    def __init__(self):
        self.class_name = self.__class__.__name__
        self.log = logging.getLogger(f"ndfc_python.{self.class_name}")

        self._contents = None
        self._markdown_file = None
        self._property_map = {}
        self._template_file = None

    def load_property_map(self):
        """
        Open the YAML self.property_map, and load its contents
        into self.property_map
        """
        method_name = inspect.stack()[0][3]
        if self.property_map_file is None:
            self.property_map = {}
            return
        try:
            with open(self.property_map_file, "r", encoding="utf-8") as handle:
                self.property_map = yaml.safe_load(handle)
        except FileNotFoundError as exception:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"Exiting. template_file not found {self.property_map_file}"
            msg += f"Exception detail: {exception}"
            self.log.error(msg)
            sys.exit(1)
        except EOFError as exception:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"Exiting. property_map_file file {self.property_map_file} "
            msg += "has no contents? "
            msg += f"Exception detail: {exception}"
            self.log.error(msg)
            sys.exit(1)

        if self.property_map == {}:
            msg = f"{self.class_name}.{method_name}: "
            msg += "No key/values found in property_map_file: "
            msg += f"{self.property_map_file}"
            self.log.warning(msg)

    def load_template(self):
        """
        Open the YAML self.template_path, and load its contents
        into self.contents
        """
        method_name = inspect.stack()[0][3]
        try:
            with open(self.template_file, "r", encoding="utf-8") as handle:
                self.contents = yaml.safe_load(handle)
        except FileNotFoundError as exception:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"Exiting. template_file not found {self.template_file}"
            msg += f"Exception detail: {exception}"
            self.log.error(msg)
            sys.exit(1)
        except EOFError as exception:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"Exiting. template_file file {self.template_file} "
            msg += "has no contents? "
            msg += f"Exception detail: {exception}"
            self.log.error(msg)
            sys.exit(1)
        if self.contents is None:
            msg = f"{self.class_name}.{method_name}: "
            msg += "Exiting. No key/values found in template_file: "
            msg += f"{self.template_file}"
            self.log.error(msg)
            sys.exit(1)

    def make_markdown(self):
        """
        Generate the markdown.
        """
        method_name = inspect.stack()[0][3]
        options = self.contents.get("options", {})
        config = options.get("config", {})
        if config.get("elements") != "dict":
            msg = f"{self.class_name}.{method_name}: "
            msg += "Exiting.  Cannot parse options.config.suboptions "
            msg += "when options.config.elements is not dict."
            raise ValueError(msg)
        suboptions = config.get("suboptions", {})
        markdown = ""
        for key, value in sorted(suboptions.items()):
            if key in self.property_map:
                mapped_key = self.property_map[key]
            else:
                mapped_key = key
            markdown += f"#### {mapped_key}"
            markdown += "\n\n"
            markdown += f"{value.get("description", "No description provided.")[0]}\n\n"
            markdown += f"- default: {value.get("default", "None")}\n"
            markdown += "- example: NA\n"
            markdown += f"- type: {value.get("type", "None")}\n"
            markdown += "\n"

        try:
            with open(self.markdown_file, "w", encoding="utf-8") as handle:
                handle.write(markdown)
        except IOError as exception:
            msg = f"{self.class_name}.{method_name}: "
            msg += "Exiting. Could not write markdown_file: "
            msg += f"{self._markdown_file}"
            raise ValueError(msg) from exception

    def validate(self):
        """
        Validate that all mandatory parameters are set.

        Called from commit()
        """
        method_name = inspect.stack()[0][3]
        if self.markdown_file is None:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"Exiting.  Set {self.class_name}.markdown_file "
            msg += f"before calling {self.class_name}.commit"
            raise ValueError(msg)
        if self.template_file is None:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"Exiting.  Set {self.class_name}.template_file "
            msg += f"before calling {self.class_name}.commit"
            raise ValueError(msg)

    def commit(self):
        """
        Load the template, property_map.
        Generate the markdown.
        Print the markdown.
        """
        self.validate()
        self.load_template()
        self.load_property_map()
        self.make_markdown()
        print(f"Template: {self.template_file}")
        if self.property_map_file is not None:
            print(f"Property map: {self.property_map_file}")
        print(f"Markdown: {self.markdown_file}")

    @property
    def contents(self):
        """
        The contents of template_file as a python dict.
        """
        return self._contents

    @contents.setter
    def contents(self, value):
        self._contents = value

    @property
    def markdown_file(self):
        """
        The markdown file to save
        """
        return self._markdown_file

    @markdown_file.setter
    def markdown_file(self, value):
        self._markdown_file = value

    @property
    def property_map(self):
        """
        Populated from property_map_file in load_property_map().

        A dictionary containing template parameter to property-name mapping.
        """
        return self._property_map

    @property_map.setter
    def property_map(self, value):
        self._property_map = value

    @property
    def property_map_file(self):
        """
        The property_map file to load (YAML format)

        Optional.  If not set, no property mapping is performed.
        See also: property_map.
        """
        return self._property_map_file

    @property_map_file.setter
    def property_map_file(self, value):
        self._property_map_file = value

    @property
    def template_file(self):
        """
        The template file to load
        """
        return self._template_file

    @template_file.setter
    def template_file(self, value):
        self._template_file = value
