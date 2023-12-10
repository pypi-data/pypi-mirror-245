from argparse import ArgumentParser

from wizlib.command import WizCommand
from wizlib.input_handler import InputHandler
from wizlib.config_handler import ConfigHandler


class LoBrowCommand(WizCommand):

    default = 'default'
    handlers = [InputHandler, ConfigHandler]
