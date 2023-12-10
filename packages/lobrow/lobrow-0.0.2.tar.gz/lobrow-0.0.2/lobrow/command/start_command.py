from argparse import ArgumentParser

from lobrow.command import LoBrowCommand


class StartCommand(LoBrowCommand):
    """Start a server"""

    name = 'start'

    @LoBrowCommand.wrap
    def execute(self):
        """Start a server"""
        default = self.config.get('lobrow-default')
        dirpath = self.config.get(f"lobrow-sites-{default}-dirpath")
        port = self.config.get(f"lobrow-sites-{default}-port")
        self.status = f"Started {dirpath} on port {port}"
        return f""
