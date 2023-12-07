import json

version_json = '''
{
 "date": "2023-12-07T01:31:28+0200",
 "dirty": false,
 "error": null,
 "full-revisionid": "0eb2a5ecdc3b7b595e406c9f7bf1e6435ad39828",
 "version": "0.0.1"
}
'''  # END VERSION_JSON

def get_versions():
    return json.loads(version_json)