# -*- coding: utf-8 -*-
from plone.app.testing import setRoles
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.app.testing import TEST_USER_ID
from plone.dexterity.utils import createContentInContainer
from plone.restapi.testing import PLONE_RESTAPI_DX_FUNCTIONAL_TESTING
from plone.restapi.testing import RelativeSession

import transaction
import unittest


class TestServicesSitemap(unittest.TestCase):

    layer = PLONE_RESTAPI_DX_FUNCTIONAL_TESTING

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.portal_url = self.portal.absolute_url()
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

        self.api_session = RelativeSession(self.portal_url)
        self.api_session.headers.update({'Accept': 'application/json'})
        self.api_session.auth = (SITE_OWNER_NAME, SITE_OWNER_PASSWORD)

        self.folder = createContentInContainer(
            self.portal, u'Folder',
            id=u'folder',
            title=u'Some Folder')
        createContentInContainer(
            self.folder, u'Document',
            id=u'doc1',
            title=u'A document')
        transaction.commit()

    def test_sitemap(self):
        response = self.api_session.get('/@sitemap')

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('@id', data)
        self.assertIn('items', data)
        self.assertEqual(data['@id'], 'http://localhost:55001/plone/@sitemap')
        items = data['items']
        self.assertEqual(len(items), 3)
        self.assertEqual(items[0]['loc'], u'http://localhost:55001/plone')
        self.assertEqual(items[1]['loc'], u'http://localhost:55001/plone/folder')
        self.assertEqual(items[2]['loc'], u'http://localhost:55001/plone/folder/doc1')
