#!/usr/bin/python3
"""

This module contains a class Console that generates
a command-line interpreter

"""
import cmd
import sys
import json
import importlib
from models import storage


class HBNBCommand(cmd.Cmd):
    """Airbnb command processor."""
    prompt = "(hbbh) "

    def do_EOF(self, line):
        """Quit command to exit the program"""
        return True

    def do_quit(self, line):
        """Quit command to exit the program"""
        return True

    def emptyline(self):
        """Overrides emptyline to do nothing"""
        pass

    def do_create(self, line):
        """Creates an instance of class BaseModel:
            Usage: create <class name>"""
        args = line.split()
        if not args:
            print("** class name missing **")
            return

        class_name = args[0]
        module_path = f'models.base_model'

        try:
            module = importlib.import_module(module_path)
            class_obj = getattr(module, class_name)
            new_instance = class_obj()
            new_instance.save()
            print(new_instance.id)
        except (ModuleNotFoundError, AttributeError):
            print("** class doesn't exist **")

    def do_show(self, line):
        """Displays an instance based on class name & id:
            Usage: show <class name> <id>"""
        args = line.split()
        if not args:
            print("** class name missing **")

        class_name = args[0]
        module_path = f'models.base_model'

        try:
            module = importlib.import_module(module_path)
            class_obj = getattr(module, class_name)
        except (ModuleNotFoundError, AttributeError):
            print("** class doesn't exist **")

        if len(args) < 2:
            print("** instance id missing **")
            return

        instance_id = args[1]
        try:
            with open("file.json", "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            print("** File not found ***")

        instance_key = f'{class_name}.{instance_id}'

        if instance_key in data:
            instance_data = data[instance_key]
            instance = class_obj(**instance_data)
            print(instance)
            return
        else:
            print("** no instance found **")

    def do_destroy(self, line):
        """Deletes an instance of class:
            Usage: destroy <class name>"""
        args = line.split()

        if not args:
            print("** class name missing **")
            return

        if len(args) < 2:
            print("** instance id missing **")
            return

        class_name = args[0]
        class_id = args[1]

        try:
            module = importlib.import_module('models.base_model')
            class_obj = getattr(module, class_name)
        except (ModuleNotFoundError, AttributeError):
            print("** class doesn't exist **")
            return

        try:
            with open("file.json", "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            print("** File not found **")
            return

        instance_key = f'{class_name}.{class_id}'
        if instance_key in data:
            del data[instance_key]

            with open('file.json', 'w') as file:
                json.dump(data, file)
        else:
            print("** no instance found **")

    def do_all(self, line):
        """Displays all instances based or not on the class name:
        Usage: all
        Usage: all BaseModel"""
        args = line.split()

        try:
            with open('file.json', 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            print("** File not found **")

        if not args:
            all_instances = []
            for key, value in data.items():
                class_name = value.get('__class__')
                if class_name:
                    module = importlib.import_module(f'models.base_model')
                    class_obj = getattr(module, class_name)
                    instance = class_obj(**value)
                    print(str(instance))
            return

        class_name = args[0]

        try:
            module = importlib.import_module('models.base_model')
            class_obj = getattr(module, class_name)
        except (ModuleNotFoundError, AttributeError):
            print("** class doesn't exist **")

        for key, value in data.items():
            if '__class__' in value and value['__class__'] == class_name:
                instance = class_obj(**value)
                print(str(instance))

    def do_update(self, line):
        """Updates an instance based on the class name and id
        Usage: update <class name> <id> <attribute name> "<attribute value>"""
        args = line.split()
        if not args:
            print("** class name missing **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        if len(args) < 3:
            print("** attribute name missing **")
            return
        if len(args) < 4:
            print("** value missing **")
            return

        class_name = args[0]
        instance_id = args[1]
        instance_attr = args[2]
        new_value = args[3]

        try:
            with open('file.json', 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            print("** File not found **")

        for key, value in data.items():
            if '__class__' in value and value['__class__'] != class_name:
                print("** class doesn't exist")
                return

        instances = storage.all()
        instance_key = f'{class_name}.{instance_id}'
        if instance_key not in data:
            print("** no instance found **")
            return

        instance = instances[instance_key]
        if instance_attr != ('id', 'created_at', 'updated_at'):
            setattr(instance, instance_attr, new_value)
            instance.save()


if __name__ == '__main__':
    if not sys.stdin.isatty():
        HBNBCommand().cmdloop()
        print()
    else:
        HBNBCommand().cmdloop()
