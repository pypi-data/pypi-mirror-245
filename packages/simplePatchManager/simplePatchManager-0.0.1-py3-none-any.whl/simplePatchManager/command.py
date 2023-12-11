import logger
import subprocess
import os
from . status import Status


class AbstractCommand(object):

    def __init__(self, args):
        self._args = args
        self.logger_name = self.__class__.__qualname__

    @staticmethod
    def _append_filenames_parameter(parser):
        parser.add_argument('filenames', action='extend', nargs="+")

    def _log(self):
        return logger.get(self)

    def _wrapErrorMessage(self, status):
        if status.errorMessage:
            initial = status.errorMessage
            status.errorMessage = f'\nfolder: {self._args.patchs_folder}'
            status.errorMessage += f'\ncontext: {self._args.context}'
            status.errorMessage += '\n'
            status.errorMessage += f'\n{initial}'

    def run(self):
        self._log().info('Running command %s', self._args.command)
        self._log().debug('With args %s', str(self._args))

        status = self._check_args()
        if status.errorMessage:
            self._wrapErrorMessage(status)

            return status
        self._log().debug('Arguments OK')

        status = self._do_run()
        self._log().debug('Command ran, quitting')

        if status.errorMessage:
            self._wrapErrorMessage(status)

        return status

    def _system(self, *args, **kwargs):
        self._log().info(f'Calling subprocess.run with "{args}" and {kwargs}')
        process = subprocess.run(*args, **kwargs)

        if process.returncode != 0:
            # Im not sure if it will run
            self._log().warning('Non zero status code returned by "%s"', ' '.join(*args))
        return process

    def _getPatchsFolder(self):
        return os.path.join(self._args.patchs_folder, self._args.context)

    def _getPatchFileName(self, patchFileName):
        return os.path.join(self._getPatchsFolder(), patchFileName + '.patch')

    def _check_filename_existence(self, filenames):
        setattr(self._args, 'fullpathfilenames', list())
        fullpathfilenames = self._args.fullpathfilenames

        for patchBaseFileName in self._args.filenames:
            patchFileName = self._getPatchFileName(patchBaseFileName)

            if not os.path.isfile(patchFileName) and not os.path.islink(patchFileName):
                return Status.error(f'Patch file "{patchBaseFileName}" doesn\'t exists...')

            fullpathfilenames.append(patchFileName)

        return Status.ok()

    def _list_patches(self):
        patches = dict()

        for node in os.scandir(self._getPatchsFolder()):
            if node.is_file() or node.is_symlink():
                patch_name = node.name[:node.name.find('.')]
                without_extension = node.name[:node.name.rfind('.')]
                extension = node.name[node.name.find('.')+1:]
                if extension == 'patch':
                    if patch_name not in patches:
                        patches[patch_name] = ''
                elif extension == 'description':
                    patches[patch_name] = self._first_line_of(node.path)

        return patches


    def _first_line_of(self, file_path):
        with open(file_path) as file:
            line = file.readline()
            return line.strip()


    # Implement in subclasses, optional
    def _check_args(self):
        return Status.ok()

    # Implement in subclasses, required
    def _do_run(self):
        pass
