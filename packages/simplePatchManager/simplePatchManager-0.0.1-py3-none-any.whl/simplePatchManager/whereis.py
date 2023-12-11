from .command import AbstractCommand
from .status import Status
import os

class WhereIsCommand(AbstractCommand):

    def __init__(self, args):
        super().__init__(args)

    @staticmethod
    def make_parser(subparsers):
        parser = subparsers.add_parser('whereis', aliases=['where', 'w'], help='Print the folder where patchs are, or one or more patch locations')
        parser.set_defaults(handler_class=WhereIsCommand)
        parser.add_argument('-f', '--filenames', default=list(), action='extend', nargs='+')

    def _check_args(self):
        return self._check_filename_existence(self._args.filenames)

    def _do_run(self):
        if len(self._args.filenames) == 0:
            print(self._getPatchsFolder())
        else:
            for fullPathFileName in self._args.fullpathfilenames:
                print(fullPathFileName)

        return Status.ok()
