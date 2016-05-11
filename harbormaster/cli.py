# -*- coding: utf-8 -*-
from __future__ import absolute_import

import logging

logger = logging.getLogger(__name__)

import os
import sys
import argparse

from . import engine

from logging import config
logging.config.dictConfig(
    {
        'version': 1,
        'disable_existing_loggers': True,
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
            },
        },
        'loggers': {
            'harbormaster': {
                'handlers': ['console'],
                'level': 'INFO',
            },
            'compose': {
                'handlers': [],
                'level': 'INFO'
            },
            'docker': {
                'handlers': [],
                'level': 'INFO'
            }
        },
    }
)

AVAILABLE_COMMANDS = {'help': 'Display this help message',
                      'init': 'Initialize a new harbormaster project',
                      'build': 'Build new images based on harbormaster.yml',
                      'run': 'Run and orchestrate built images based on harbormaster.yml'}

def subcmd_init_parser(subparser):
    return

def subcmd_build_parser(subparser):
    subparser.add_argument('--recreate', action='store_true',
                           help=u'Recreate the build container image',
                           dest='recreate', default=False)

def subcmd_run_parser(subparser):
    return

def subcmd_help_parser(subparser):
    return

def commandline():
    parser = argparse.ArgumentParser(description=u'Build, orchestrate, run, and '
                                                 u'ship Docker containers with '
                                                 u'Ansible playbooks')
    subparsers = parser.add_subparsers(title='subcommand', dest='subcommand')
    for subcommand in AVAILABLE_COMMANDS:
        subparser = subparsers.add_parser(subcommand,
                                          help=AVAILABLE_COMMANDS[subcommand])
        globals()['subcmd_%s_parser' % subcommand](subparser)
    args = parser.parse_args()
    if args.subcommand == 'help':
        parser.print_help()
        sys.exit(0)
    getattr(engine, u'cmdrun_{}'.format(args.subcommand))(os.getcwd())
