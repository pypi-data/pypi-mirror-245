import os
from importlib import metadata
from pathlib import Path

HERE = Path(__file__).parent.resolve()
PROJECT_NAME = os.path.basename(HERE)
PACKAGE_NAME = PROJECT_NAME.replace("-", "_")

__version__ = metadata.version(PACKAGE_NAME)

if __name__ == "__main__":
    print(__version__)
