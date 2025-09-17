import sys
import os

# Add the package to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', 'package-larapy'))

from larapy.console.command import Command


class CustomCommand(Command):
    """
    Demo custom command specific to this application
    """

    signature = "app:demo {name? : The name to greet} {--excited : Add excitement}"
    description = "Demo command showing custom application commands"

    def handle(self) -> int:
        """Execute the custom command"""
        name = self.argument('name') or 'World'
        excited = self.option('excited', False)

        greeting = f"Hello, {name}!"
        if excited:
            greeting += " 🎉"

        self.success(greeting)
        self.info("This is a demo command from the myapp application")

        return 0
    
    def get_name(self) -> str:
        """Get the command name"""
        return "app:demo"