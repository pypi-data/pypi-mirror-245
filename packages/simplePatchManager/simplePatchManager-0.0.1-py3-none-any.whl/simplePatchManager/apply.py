from .command import AbstractCommand
import os
from .status import Status
import subprocess


class ApplyCommand(AbstractCommand):

    def __init__(self, args):
        super().__init__(args)

    @staticmethod
    def _append_common_parameters(parser):
        parser.add_argument('-d', '--dry-run', action='store_true', help='Simulate, but does nothing')
        AbstractCommand._append_filenames_parameter(parser)

    @staticmethod
    def make_parser(subparsers):
        apply_parser = subparsers.add_parser('apply', aliases=['a'], help='Applies a patch')
        apply_parser.set_defaults(handler_class=ApplyCommand)
        ApplyCommand._append_common_parameters(apply_parser)

    def _check_args(self):
        return self._check_filename_existence(self._args.filenames)

    def _base_params(self, base_params):
        base_params.append('--no-backup-if-mismatch')
        base_params.append('--force')
        base_params.append('--strip=0')
        base_params.append('--input')

        return base_params

    def _do_run(self):
        self._log().debug(f'Applying patch with args {self._args}')

        someError = False

        for patchFileName in self._args.fullpathfilenames:
            params = list(self._base_params(list()))
            params.append(patchFileName)

            all_params = ['patch'] + params

            if self._args.dry_run:
                print(' '.join(all_params))
            else:
                process = self._system(all_params, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

                if process.returncode != 0:
                    someError = True

        if someError:
            return Status.error('Error applying some patchs...')
        else:
            return Status.ok()


class UnapplyCommand(ApplyCommand):

    @staticmethod
    def make_parser(subparsers):
        unapply_parser = subparsers.add_parser('unapply', aliases=['u'], help='Unapplies a patch')
        unapply_parser.set_defaults(handler_class=UnapplyCommand)
        ApplyCommand._append_common_parameters(unapply_parser)

    def _base_params(self, base_params):
        base_params.append('--reverse')
        return super()._base_params(base_params)
