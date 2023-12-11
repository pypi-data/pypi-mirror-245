from .command import AbstractCommand
import os
from . status import Status

class RemoveCommand(AbstractCommand):

    def __init__(self, args):
        super().__init__(args)

    @staticmethod
    def make_parser(subparsers):
        parser = subparsers.add_parser('remove', aliases=['rm', 'r'], help='Removes one or more patchs')
        parser.set_defaults(handler_class=RemoveCommand)
        AbstractCommand._append_filenames_parameter(parser)

    def _check_args(self):
        return self._check_filename_existence(self._args.filenames)

    def _do_run(self):
        for patchFileName in self._args.fullpathfilenames:
            os.unlink(patchFileName)
            print(f'Removed "{patchFileName}"')

        return Status.ok()