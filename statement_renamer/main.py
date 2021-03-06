import argparse
import logging
import os
import sys
from tasks.task import Task

LOG_FILE_NAME = 'Logs/output.log'
logger = logging.getLogger('StatementRenamer')


def main():

    handler = logging.FileHandler(LOG_FILE_NAME)
    logger.addHandler(handler)
    logger.setLevel("DEBUG")  # WARNING")
    logger.warning('Starting rename with params: [{}]'.format(' '.join(sys.argv[1:])))

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

    try:
        # TODO: next step: decouple the CLI arguments from the Task class. Possibly with a TaskBuilder?
        task = Task(parser, logger)
        task.execute()
    except Exception as e:
        logger.exception(e)
        raise e


def walkdir(folder):
    """Walk through each files in a directory"""
    results = []
    for dirpath, dirs, files in os.walk(folder):
        for filename in files:
            # yield os.path.abspath(os.path.join(dirpath, filename))
            results.append(os.path.abspath(os.path.join(dirpath, filename)))
    return results
