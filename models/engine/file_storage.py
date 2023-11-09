#!/usr/bin/python
"""

This module contain a class FileStorage

"""
import json
import importlib


class FileStorage:
    """This class serializes to JSON file and
    desrializes JSON file to instances
    """
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Returns the dictionary __objects"""
        return FileStorage.__objects

    def new(self, obj):
        """Sets obj in __objects with key <obj class name>.id"""
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        FileStorage.__objects[key] = obj

    def save(self):
        """Serializes __objects to the JSON file (path: __file_path)"""
        serialize_data = {}
        for key, obj in FileStorage.__objects.items():
            serialize_data[key] = obj.to_dict()

        with open(FileStorage.__file_path, 'w', encoding='utf-8') as file:
            json.dump(serialize_data, file)

    def reload(self):
        """Deserializes the JSON file to __object if it exist"""
        try:
            with open(FileStorage.__file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                for key, value in data.items():
                    class_name, obj_id = key.split('.')
                    module_name = 'models.base_model'
                    module = importlib.import_module(module_name)
                    cls = getattr(module, class_name)
                    obj = cls(**value)
                    FileStorage.__objects[key] = obj
        except FileNotFoundError:
            pass
