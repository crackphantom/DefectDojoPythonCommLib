'''
Created on Feb 19, 2020

@author: crackphantom
'''
# first thing so other loggers are properly set when loading modules etc...
# set to DEBUG for troubleshooting
import logging
logging.basicConfig(level=logging.ERROR)

import unittest
from tests.integration import settings
from datadorks.pcomm.defectdojo.httpclients import ApiV1


class Test(unittest.TestCase):


    def testGetEngagements(self):
        client = ApiV1(settings.BASEURL, settings.APIUSER, settings.APIUSERKEY)
        engagements = client.getEngagements()
        self.assertIsNotNone(engagements)
        self.assertEquals(32, len(engagements))

    def testPostImportScanString(self):
        client = ApiV1(settings.BASEURL, settings.APIUSER, settings.APIUSERKEY)
        fileStr = '''
{
    "data": {
        "repository": {
            "name":"zing-web",
            "vulnerabilityAlerts": {
                "edges": [{
                        "cursor": "Y3Vyc29yOnYyOpHOBj-XYw=="
                    }
                ],
                "nodes": [{
                        "id": "MDI4OlJlcG9zaXRvcnlWdWxuZXJhYmlsaXR5QWxlcnQxMDQ4MzA4MTk=",
                        "vulnerableManifestFilename": "yarn.lock",
                        "vulnerableManifestPath": "yarn.lock",
                        "vulnerableRequirements": "= 3.4.0",
                        "securityVulnerability": {
                            "advisory": {
                                "databaseId": 1521,
                                "description": "A vulnerability was found in diff before v3.5.0, the affected versions of this package are vulnerable to Regular Expression Denial of Service (ReDoS) attacks.",
                                "origin": "WHITESOURCE",
                                "publishedAt": "2019-06-13T18:58:54Z",
                                "summary": "High severity vulnerability that affects diff"
                            },
                            "package": {
                                "name": "diff",
                                "ecosystem": "NPM"
                            },
                            "severity": "HIGH",
                            "vulnerableVersionRange": "< 3.5.0"
                        }
                    }
                ]
            }
        }
    }
}'''.strip()

        response = client.postImportScanString(fileStr, '/api/v1/engagements/10/', '/api/v1/users/2/', 'GitHub Vulnerability Alerts')
        self.assertIsNotNone(response)

if __name__ == "__main__":
    # Assuming you set PYTHONPATH to contain dependency e.g. 
    # export PYTHONPATH=/some/path/to/project/GenericPythonCommLib
    # /usr/bin/python2.7 -m unittest -v tests.integration.testApiv1Client.Test
    # /usr/bin/python3 -m unittest -v tests.integration.testApiv1Client.Test
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
