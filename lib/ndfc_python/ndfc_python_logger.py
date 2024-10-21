from ndfc_python.log_v2 import Log


class NdfcPythonLogger(Log):
    """
    # Summary
    Configure logging for ndfc-python.

    # Usage example
    ```python
    NdfcPythonLogger()
    ```
    """

    def __init__(self):
        super().__init__()
        try:
            self.commit()
        except ValueError as error:
            msg = "Error while instantiating Log(). "
            msg += f"Error detail: {error}"
            raise ValueError(msg) from error
