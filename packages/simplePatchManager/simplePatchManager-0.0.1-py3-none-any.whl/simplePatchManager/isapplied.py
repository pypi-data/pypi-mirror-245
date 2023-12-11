from .command import AbstractCommand
import subprocess
import os
from . status import Status


class IsAppliedCommand(AbstractCommand):

    def __init__(self, args):
        super().__init__(args)

    @staticmethod
    def make_parser(subparsers):
        parser = subparsers.add_parser('applied', aliases=['ap'], help='Says which patchs are applied')
        parser.set_defaults(handler_class=IsAppliedCommand)
        parser.add_argument('-f', '--filenames', default=list(), action='extend', nargs='+')
        # AbstractCommand._append_filenames_parameter(parser)

    def _check_args(self):
        return self._check_filename_existence(self._args.filenames)

    def _do_run(self):
        if len(self._args.filenames) == 0:
            for patch in self._list_patches().keys():
                self._args.filenames.append(patch)
                fullpathfilename = os.path.join(self._getPatchsFolder(), patch + '.patch')
                self._args.fullpathfilenames.append(fullpathfilename)

        self._patch_params = ['patch', '--dry-run', '--force', '--strip=0']
        self._reverse_params = ['patch', '--dry-run', '--reverse', '--force', '--strip=0']

        for filename, fullPathFileName in zip(self._args.filenames, self._args.fullpathfilenames):
            apply_ok = self._try_apply(fullPathFileName)
            reverse_ok = self._try_apply(fullPathFileName, reverse=True)

            if apply_ok:
                print(f'[ ] {filename}')
            elif reverse_ok:
                print(f'[X] {filename}')
            else:
                print(f'[E] {filename}')

        return Status.ok()

    def _try_apply(self, filename, reverse=False):
        with open(filename, 'r') as input_file:
            params = self._reverse_params if reverse else self._patch_params
            process = self._system(params, stdin=input_file, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            return process.returncode == 0


