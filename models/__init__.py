"""

models package: A package for managing and storing model data.

"""
from models.engine.file_storage import FileStorage


storage = FileStorage()
storage.reload()
