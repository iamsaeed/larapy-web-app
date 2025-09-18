import sys
import os

# Add the package to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', 'package-larapy'))

from larapy.console.command import Command


class HelloWorldCommand(Command):
    """
    Simple hello world command
    """

    signature = "hello {name? : Name to greet}"
    description = "A simple hello world command"

    def handle(self) -> int:
        """Execute the hello command"""
        name = self.argument('name') or 'World'
        self.success(f"Hello, {name}!")
        return 0