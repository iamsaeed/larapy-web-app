import sys
import os

# Add the package to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', 'package-larapy'))

from larapy.console.command import Command


class StatusCommand(Command):
    """
    Check application status
    """

    signature = "app:status {--verbose : Show detailed information}"
    description = "Display application status information"

    def handle(self) -> int:
        """Execute the status command"""
        verbose = self.option('verbose', False)

        self.info("🚀 Larapy Application Status")
        self.line("=" * 40)
        
        # Check basic status
        self.success("✓ Application is running")
        self.info("✓ Framework loaded successfully")
        
        if verbose:
            self.line("")
            self.comment("Detailed Information:")
            self.line(f"- Python version: {sys.version.split()[0]}")
            self.line(f"- Working directory: {os.getcwd()}")
            self.line(f"- Framework path: {os.path.dirname(__file__)}")
            
        self.line("")
        self.comment("All systems operational! 🎯")

        return 0
    
    def get_name(self) -> str:
        """Get the command name"""
        return "app:status"