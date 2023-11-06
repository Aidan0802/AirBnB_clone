#!/usr/bin/python3
"""

This module contains a class Console that generates
a command-line interpreter

"""
import cmd
import sys


class Console(cmd.Cmd):
    """Simple command processor example."""
    prompt = "(hbbh) "

    def do_EOF(self, line):
        """Closes the interpreter"""
        return True

    def do_quit(self, line):
        """Closes the interpreter"""
        return True

    def emptyline(self):
        """Overrides emptyline to do nothing"""
        pass

if __name__ == '__main__':
    if not sys.stdin.isatty():
        Console().cmdloop()
        print()
    else:
        Console().cmdloop()
