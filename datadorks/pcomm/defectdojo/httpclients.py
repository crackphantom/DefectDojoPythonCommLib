'''
Created on Feb 19, 2020

@author: crackphantom
'''
import logging
import json
from datetime import datetime

from datadorks.pcomm.http.clients import factory
from datadorks.pcomm.http.consts import POST_METHOD
from datadorks.pcomm.http import wrappers

LOGGER = logging.getLogger()


class ApiV1(object):
    '''
    classdocs
    '''


    def __init__(self, baseurl, apiuser, apiuserkey):
        '''
        Constructor
        '''
        self.proxyclient = factory.getNewSyncHttpClient()
        # TODO: Pull out logic to strip off '/' into re-usable util function
        if baseurl.endswith('/'):
            self.baseurl = baseurl[:-1]
        else:
            self.baseurl = baseurl

        self.apiuserkey = apiuserkey
        self.apiuser = apiuser

    def connect(self):
        pass

    def disconnect(self):
        pass
    
    def _getBaseRequest(self, path):
        url = '{}{}'.format(self.baseurl, path)
        request = wrappers.HttpRequest(url)
        request.addHeader('Authorization', 'ApiKey {}:{}'.format(self.apiuser, self.apiuserkey))
        return request

    def getEngagements(self):
        engagements = []
        nextPage = True
        request = self._getBaseRequest('/api/v1/engagements')
        
        while nextPage:
            nextPage = False
            response = self.proxyclient.doRequest(request)
            if response.exists:
                try:
                    parsedResp = json.loads(response.body)
                    # add to any previous results we had
                    engagements.extend(parsedResp.get('objects', []))
                    # any more?
                    nextUrl = parsedResp.get('meta', {}).get('next', None)
                    if nextUrl is not None:
                        nextPage = True
                        url = '{}{}'.format(self.baseurl, nextUrl)
                        request.url = url
                except(KeyError, ValueError):
                    LOGGER.error("Response body is not valid JSON, value in response body was\n{}".format(response.body))
            else:
                LOGGER.error("No response exists, the caught exception, if any, was\n{}".format(response.caughtException))
        return engagements

    def postImportScanString(self, importScan, engagement, lead, scanType,
                             scan_date=None, minimumSeverity='Info', verified='false'):
        request = self._getBaseRequest('/api/v1/importscan/')
        request.method = POST_METHOD

        request.addParameter('engagement', engagement)
        request.addParameter('lead', lead)
        request.addParameter('scan_type', scanType)
        request.addParameter('minimum_severity', minimumSeverity)
        request.addParameter('verified', verified)
        if scan_date is None:
            # default to zero padded todays date
            scan_date = datetime.today().strftime('%Y-%m-%d')
        request.addParameter('scan_date', scan_date)
        
        request.addFile('file', 'file', importScan, 'text/plain')

        request.multipart = True

        response = self.proxyclient.doRequest(request)
        if response.exists:
            return response.body
        else:
            LOGGER.error("No response exists, the caught exception, if any, was\n{}".format(response.caughtException))
        return response
