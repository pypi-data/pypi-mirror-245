#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import logger
import os
from .apply import ApplyCommand, UnapplyCommand
from .list import ListCommand
from .view import ViewCommand
from .edit import EditCommand
from .create import CreateCommand
from .remove import RemoveCommand
from .isapplied import IsAppliedCommand
from .whereis import WhereIsCommand
import sys


def _default_patchs_context():
    if 'PATCHS_CONTEXT' in os.environ:
        return os.environ['PATCHS_CONTEXT']
    else:
        return os.path.basename(os.getcwd())


def default_patchs_folder():
    if 'PATCHS_FOLDER' in os.environ:
        return os.environ['PATCHS_FOLDER']
    elif 'XDG_CONFIG_FOLDER' in os.environ:
        return os.path.join(os.environ['XDG_CONFIG_FOLDER'], 'patchs')
    else:
        return os.path.join(os.environ['HOME'], '.config', 'patchs')


def _patchs_folder(parameter, parser):
    patchs_folder = _get_patchs_folder(parameter)

    os.mkdir(patchs_folder)

    return patchs_folder


def parse_command_line(given_args):
    '''
    Reference: https://docs.python.org/3/library/argparse.html
    '''
    parser = argparse.ArgumentParser()

    parser.add_argument('-c', '--context', default=_default_patchs_context(), help='Context subfolder to use (default: current folder name if PATCHS_CONTEXT not defined)')
    # TODO Let it clearer
    parser.add_argument('-p', '--patchs-folder', default=default_patchs_folder(), help='Patch files location')

    subparsers = parser.add_subparsers(
        dest='command', required=True, help='Command to run')

    ApplyCommand.make_parser(subparsers)

    UnapplyCommand.make_parser(subparsers)

    ListCommand.make_parser(subparsers)

    ViewCommand.make_parser(subparsers)

    EditCommand.make_parser(subparsers)

    CreateCommand.make_parser(subparsers)

    RemoveCommand.make_parser(subparsers)

    IsAppliedCommand.make_parser(subparsers)

    WhereIsCommand.make_parser(subparsers)

    logger.make_verbosity_argument(parser)

    return parser, parser.parse_args(given_args or sys.argv[1:])


def main(given_args = None):
    global args

    parser, args = parse_command_line(given_args)

    logger.configure(args)

    '''
    Logger reference: https://docs.python.org/3/library/logging.html
    '''
    logger.get(__name__).info('Calling handler %s', str(args.handler_class))
    logger.get(__name__).debug('With args %s', str(args))

    handler = args.handler_class(args)

    status = handler.run()

    if status.errorMessage:
        parser.error(status.errorMessage)

if __name__ == '__main__':
    main()
