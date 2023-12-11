from .command import AbstractCommand
from .status import Status
import os
import subprocess


class CreateCommand(AbstractCommand):

    def __init__(self, args):
        super().__init__(args)

    @staticmethod
    def make_parser(subparsers):
        create_parser = subparsers.add_parser('create', aliases=['c'], help='Create a new patch file')
        create_parser.set_defaults(handler_class=CreateCommand)
        create_parser.add_argument('-a', '--append', action='store_true', help='Append to file, without this flag overwrite existing file')
        create_parser.add_argument('filename')
        create_parser.add_argument('-da', '--git-diff-args', nargs='+', default=['--no-prefix', '--no-color'], help='Arguments to git diff')
        create_parser.add_argument('-ga', '--git-args', nargs='+', default=['-c', 'core.pager='], help='Arguments to git')

    def _do_run(self):
        params = list()
        params.append('git')
        params.extend(self._args.git_args)
        params.append('diff')
        params.extend(self._args.git_diff_args)

        fullPathFileName = self._getPatchFileName(self._args.filename)

        mode = 'a' if self._args.append else 'w'
        with open(fullPathFileName, mode) as patchFile:
            process = self._system(params, stdout=patchFile, stderr=subprocess.PIPE)

        if process.returncode == 0:
            print(f'New patch created at {fullPathFileName} usings command line "{" ".join(params)}"')

        return Status.ok() if process.returncode == 0 else Status.error('Error generating patch...')
