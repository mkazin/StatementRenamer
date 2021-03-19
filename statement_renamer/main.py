""" Command Line Interface for StatementRenamer """
import argparse
import logging
import sys

import config
from statement_renamer.tasks.task import Task
from statement_renamer.tasks.disk_file_handler import DiskFileHandler

LOG_FILE_NAME = 'Logs/output.log'
logger = logging.getLogger('StatementRenamer')


def main():

    """ Provides the command Line Interface """
    handler = logging.FileHandler(LOG_FILE_NAME)
    logger.addHandler(handler)
    logger.setLevel("DEBUG")  # WARNING")
    logger.warning('Starting rename with params: [%s]', ' '.join(sys.argv[1:]))

    parser = argparse.ArgumentParser()

    parser.add_argument('-E', '--extract-only',
                        dest='extract_only',
                        action='store_true',
                        help=('Extract-only mode. Returns content of PDF'),
                        required=False)
    parser.add_argument('-H', '--hash-only',
                        dest='hash_only',
                        action='store_true',
                        help=('Hash-only mode. Returns MD5 hash of input files'),
                        required=False)
    parser.add_argument('-S', '--simulate',
                        dest='simulate',
                        action='store_true',
                        help=('Simulation mode. Outputs actions that would be taken'),
                        required=False)
    parser.add_argument('-v', '--verbose',
                        dest='verbose',
                        action='store_true',
                        help=('Verbose mode. Outputs detailed information'),
                        required=False)
    parser.add_argument('-q', '--quiet',
                        dest='quiet',
                        action='store_true',
                        help=('Quiet mode. Produces no console output'),
                        required=False)

    parser.add_argument('location',
                        # dest='target',
                        action='store',
                        help='File or folder to process',
                        # required=True,
                        type=str)

    parser.add_argument('--destination',
                        # dest='target',
                        action='store',
                        help='Output folder',
                        required=False,
                        default=None,
                        type=str)
    try:
        args = parser.parse_args()
        config.LOCATION = args.location
        config.DESTINATION = args.destination
        config.QUIET = args.quiet
        config.VERBOSE = args.verbose
        config.SIMULATE = args.simulate
        config.HASH_ONLY = args.hash_only
        config.EXTRACT_ONLY = args.extract_only

        task = Task(parser, DiskFileHandler)
        task.execute()
    except Exception as ex:
        logger.exception(ex)
        raise ex


# def walkdir(folder):
#     """Walk through each files in a directory"""
#     results = []
#     for dirpath, dirs, files in os.walk(folder):
#         for filename in files:
#             # yield os.path.abspath(os.path.join(dirpath, filename))
#             results.append(os.path.abspath(os.path.join(dirpath, filename)))
#     return results
