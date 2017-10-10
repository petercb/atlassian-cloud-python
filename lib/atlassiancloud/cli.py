# -*- coding: utf-8 -*-
'''
Entry points for CLI's
'''

import logging
from atlassiancloud.confluence import Confluence
import click


@click.command()
@click.option('--username', help='specify the user to connect as')
@click.option('--password', help='specify the password for the connect user')
@click.option('--space', help='The space key the attachment is under')
@click.option('--title', help='The title of the page to upload the attachment under')
@click.option('--file', multiple=True, help='Path to the file to upload')
@click.option('--uri', help='specify the base URI')
@click.option(
    '--loglevel', type=click.Choice(['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']),
    default='INFO', help="Set the logging level"
)
def upload_attachments_cli(username, password, space, title, file, uri, loglevel):
    '''Script to upload attachments to Confluence using the cloud REST API'''
    logging.basicConfig(level=logging.getLevelName(loglevel))
    ccapi = Confluence(uri)
    rc = 0
    if ccapi.auth(username, password):
        logging.info('Uploading files: %s', ', '.join(file))
        for att in file:
            if ccapi.upload_attachment(space, title, att):
                logging.info('Uploaded "%s" to "%s" in "%s"', att, title, space)
            else:
                logging.error('Failed to upload attachment', att)
                rc += 1
    else:
        logging.error('Failed to authenticate')
    return rc
