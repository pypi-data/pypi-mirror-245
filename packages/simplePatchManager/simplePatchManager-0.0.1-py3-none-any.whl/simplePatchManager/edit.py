from .command import AbstractCommand
from .status import Status
import os


class EditCommand(AbstractCommand):

    def __init__(self, args):
        super().__init__(args)

    @staticmethod
    def make_parser(subparsers):
        parser = subparsers.add_parser('edit', aliases=['e'], help='Opens the patch(s) in $EDITOR')
        parser.set_defaults(handler_class=EditCommand)
        parser.add_argument('-e', '--editor', default=os.environ.get('EDITOR', 'vim'), help='The editor to use (must be in $PATH, defaults to $EDITOR, or vim)')
        AbstractCommand._append_filenames_parameter(parser)

    def _check_args(self):
        return self._check_filename_existence(self._args.filenames)

    def _do_run(self):
        params = list()
        params.append(self._args.editor)
        params.extend(self._args.fullpathfilenames)

        process = self._system(params)

        return Status.ok() if process.returncode == 0 else Status.error('Error calling editor...')
