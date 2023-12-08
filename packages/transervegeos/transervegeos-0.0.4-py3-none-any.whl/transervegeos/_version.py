import json

version_json = '''
{
 "date": "2023-12-07T16:09:28+0100",
 "dirty": false,
 "error": null,
 "full-revisionid": "0eb2a5ecdc3b7b595e406c9f7bf1e6435ad39829",
 "version": "0.0.4"
}
'''  # END VERSION_JSON

def get_versions():
    return json.loads(version_json)