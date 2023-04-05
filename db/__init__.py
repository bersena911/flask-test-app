import importlib
import os

from db.base_class import Base  # noqa

for module in os.listdir("models"):
    if module == "__init__.py" or module[-3:] != ".py":
        continue
    importlib.import_module(f".{module[:-3]}", package="models")
