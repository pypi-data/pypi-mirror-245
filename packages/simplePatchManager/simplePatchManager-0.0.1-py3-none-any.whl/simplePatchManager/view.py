from .command import AbstractCommand
from .status import Status


class ViewCommand(AbstractCommand):

    def __init__(self, args):
        super().__init__(args)

    @staticmethod
    def make_parser(subparsers):
        parser = subparsers.add_parser('view', aliases=['v'], help='View the contents of a patch')
        parser.set_defaults(handler_class=ViewCommand)
        # parser.add_argument('-np', '--no-pager', action='store_true')
        AbstractCommand._append_filenames_parameter(parser)

    def _check_args(self):
        return self._check_filename_existence(self._args.filenames)

    def _do_run(self):
        # if self._args.no_pager:
        #     return self._noPagerView()
        # else:
        #     return self._pagerView()
        return self._noPagerView()

    def _noPagerView(self):
        for patchFileName in self._args.fullpathfilenames:
            print(f'>>>>> {patchFileName}')

            with open(patchFileName) as patch:
                while line := patch.readline()[:-1]:
                    print(line)

                print(f'<<<<< {patchFileName}')

                print()

        return Status.ok()

    # def _pagerView(self):
    #     return Status.error('TODO')
