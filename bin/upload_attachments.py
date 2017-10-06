#!/usr/bin/env python

'''
Script to update attachments in Confluence using the cloud REST API
'''

import argparse
import logging
import sys
from atlassiancloud.confluence import Confluence


def read_cli_args():
    '''Read the command line args passed to the script.'''
    parser = argparse.ArgumentParser(
        description='Script to update attachments in Confluence',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        '--username', action='store', required=True,
        help='specify the user to connect as'
    )
    parser.add_argument(
        '--password', action='store', required=True,
        help='specify the password for the connect user'
    )
    parser.add_argument(
        '--space', action='store', required=True,
        help='The space key the attachment is under'
    )
    parser.add_argument(
        '--title', action='store', required=True,
        help='The title of the page to upload the attachment under'
    )
    parser.add_argument(
        '--file', action='store', required=True,
        help='Path to the file to upload'
    )
    parser.add_argument(
        '--uri', action='store',
        help='specify the base URI'
    )
    parser.add_argument(
        '--loglevel', action='store', default='INFO',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
        help="Set the logging level"
    )
    return parser.parse_args()


def main():
    '''Entry point for CLI'''
    args = read_cli_args()
    logging.basicConfig(level=logging.getLevelName(args.loglevel))
    ccapi = Confluence(args.uri)
    if ccapi.auth(args.username, args.password):
        if ccapi.upload_attachment(args.space, args.title, args.file):
            return 0
        else:
            logging.error('Failed to upload attachment')
    else:
        logging.error('Failed to authenticate')
    return 1


if __name__ == '__main__':
    sys.exit(main())
