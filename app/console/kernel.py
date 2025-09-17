import sys
import os

# Add the package and application to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'package-larapy'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from larapy.console.kernel import ConsoleKernel as BaseKernel


class ConsoleKernel(BaseKernel):
    """
    Application Console Kernel

    Defines the artisan commands included with your application.
    Similar to Laravel's App\\Console\\Kernel.
    """

    # Application-specific commands
    command_classes = [
        # Register custom application commands here
        'app.console.commands.custom_command.CustomCommand',
    ]

    def schedule(self, schedule):
        """
        Define the application's command schedule.

        Similar to Laravel's schedule method for task scheduling.
        """
        # Example:
        # schedule.command('inspire').hourly()
        pass

    def commands(self):
        """
        Register the application's commands.

        This method is called automatically during bootstrap.
        """
        super().commands()

        # Load commands from the commands directory
        self.load_commands_from_directory(
            self.app.base_path('app/console/commands') if hasattr(self.app, 'base_path') 
            else os.path.join(os.path.dirname(__file__), 'commands')
        )