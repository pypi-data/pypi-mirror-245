from wizlib.app import WizApp

from lobrow.command import LoBrowCommand


class LoBrowApp(WizApp):

    base_command = LoBrowCommand
    name = 'lobrow'
