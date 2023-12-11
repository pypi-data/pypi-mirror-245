from .command import AbstractCommand
import os
from . status import Status


class ListCommand(AbstractCommand):

    def __init__(self, args):
        super().__init__(args)

    @staticmethod
    def make_parser(subparsers):
        list_parser = subparsers.add_parser('list', aliases=['l', 'ls'], help='List the existing patchs')
        list_parser.set_defaults(handler_class=ListCommand)
        list_parser.add_argument('-r', '--raw', action='store_true', help='Raw listing, no formatted output')

    def _do_run(self):
        if not os.path.isdir(self._getPatchsFolder()):
            return Status.error(f'Patchs folder doesn\'t exist ({self._getPatchsFolder()})...')

        if not self._args.raw:
            print(f'Folder: {self._getPatchsFolder()}')

        patches = self._list_patches()

        widest_patch = -1
        for patch_name in patches.keys():
            if len(patch_name) > widest_patch:
                widest_patch = len(patch_name)

        separator = '    '

        for patch, description in patches.items():
            filler = ' ' * (widest_patch - len(patch))
            print(f'{patch}{filler}{separator}{description}')

        return Status.ok()

