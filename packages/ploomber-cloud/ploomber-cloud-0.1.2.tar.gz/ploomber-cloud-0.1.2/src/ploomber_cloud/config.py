import json
from pathlib import Path


class PloomberCloudConfig:
    """Manages the ploomber-cloud.json file"""

    def __init__(self) -> None:
        self._path = Path("ploomber-cloud.json")
        self._data = None

    @property
    def data(self):
        """Return the data stored in the config file"""
        if self._data is None:
            raise RuntimeError("Data has not been loaded")

        return self._data

    def exists(self):
        """Return True if the config file exists, False otherwise"""
        return self._path.exists()

    def load(self):
        """
        Load the config file. Accessing data will raise an error if this
        method hasn't been executed
        """
        if not self.exists():
            raise FileNotFoundError(
                "Project not initialized. "
                "Run 'ploomber-cloud init' to initialize your project."
            )

        self._data = json.loads(self._path.read_text())

    def dump(self, data_new):
        """Dump data to the config file"""
        self._data = data_new
        self._path.write_text(json.dumps(data_new, indent=4))
