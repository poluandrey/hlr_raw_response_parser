import requests

from parser.hlr_parser import InfobipHlrHlrParser

resp = requests.get('https://hlr.lancktele.com/hlr/mccmnc_request?login=alaris&password=dreaming&dnis=792165034312&debug=1&source_name=infobip_hlr')
raw_resp = resp.json()['context_log']
parser = InfobipHlrHlrParser(raw_resp)
print(parser.get_raw_fields())
print(parser.get_raw_fields([{'error': ['groupId', ]}]))
print(parser.get_raw_fields([{'error': ['groupId', 'groupName']}]))
print(parser.get_raw_fields([{'error': ['groupId', 'groupName'], 'status' : ['groupId', 'groupName']}]))
print(parser.get_raw_fields([{'error': [], 'status': ['groupId', 'groupName']}]))