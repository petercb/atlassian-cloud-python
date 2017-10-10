# -*- coding: utf-8 -*-

'''Python module to work with the Confluence Cloud API'''

import logging
import os.path
import magic
from requests.exceptions import HTTPError
from atlassiancloud import AtlassianCloudRestAPI

class Confluence(AtlassianCloudRestAPI):
    '''
    Connection object to Confluence Cloud API
    '''

    def space_exists(self, spacekey):
        '''Check that a space key name exists'''
        try:
            self.get('/wiki/rest/api/space/{0}'.format(spacekey))
            return True
        except (HTTPError, KeyError, IndexError):
            return False


    def lookup_page_id(self, spacekey, title):
        '''Lookup a page by title, and return it's id'''
        params = {
            'spaceKey': spacekey,
            'title': title,
        }
        try:
            return self.get('/wiki/rest/api/content', params=params)['results'][0].get('id')
        except (KeyError, IndexError):
            return None


    def lookup_attachment_id(self, pageid, name):
        '''Lookup the attachment and return it's id'''
        params = {
            'filename': name,
        }
        path = '/wiki/rest/api/content/{0}/child/attachment'.format(pageid)
        try:
            return self.get(path, params=params)['results'][0].get('id')
        except (KeyError, IndexError):
            return None


    def upload_file(self, path, filepath, name=None, content_type=None):
        '''Do the work of uploading the attachment'''
        if name is None:
            name = os.path.basename(filepath)
        if content_type is None:
            content_type = magic.from_file(filepath, mime=True)
        headers = {
            'X-Atlassian-Token': 'nocheck',
        }
        files = {
            'file': (name, open(filepath, 'rb'), content_type),
        }
        req = self.request('POST', path=path, headers=headers, files=files)
        logging.debug('Attachment upload returned %u : %s', req.status_code, req.text)
        return req.status_code == 200


    def _create_attachment(self, pageid, filepath):
        '''Create a new attachment on a page'''
        path = '/wiki/rest/api/content/{0}/child/attachment'.format(pageid)
        return self.upload_file(path, filepath)


    def _update_attachment(self, pageid, attachmentid, filepath):
        '''Update an existing attachment on a page'''
        path = '/wiki/rest/api/content/{pageid}/child/attachment/{attachmentid}/data'.format(
            pageid=pageid, attachmentid=attachmentid)
        return self.upload_file(path, filepath)


    def upload_attachment(self, spacekey, title, filepath):
        '''Create or update attachment a page'''
        if self.space_exists(spacekey):
            pageid = self.lookup_page_id(spacekey, title)
            if pageid is not None:
                name = os.path.basename(filepath)
                attachmentid = self.lookup_attachment_id(pageid, name)
                if attachmentid is None:
                    return self._create_attachment(pageid, filepath)
                else:
                    return self._update_attachment(pageid, attachmentid, filepath)
        return False
