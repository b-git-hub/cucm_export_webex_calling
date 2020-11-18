#!/usr/bin/python3



from zeep import Client
from zeep.cache import SqliteCache
from zeep.transports import Transport
from zeep.exceptions import Fault
from zeep.plugins import HistoryPlugin
from requests import Session
from requests.auth import HTTPBasicAuth
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning
from lxml import etree
 
 
disable_warnings(InsecureRequestWarning)
 
username = 'cucmadmin'
password = 'CUCM_ADMIN'
# If you're not disabling SSL verification, host should be the FQDN of the server rather than IP
host = '192.168.68.204'
 
wsdl = '/home/brian/Documents/GIT/cucm_export_webex_calling/axlsqltoolkit/schema/current/AXLAPI.wsdl'
location = 'https://{host}:8443/axl/'.format(host=host)
binding = "{http://www.cisco.com/AXLAPIService/}AXLAPIBinding"
 
# Create a custom session to disable Certificate verification.
# In production you shouldn't do this, 
# but for testing it saves having to have the certificate in the trusted store.
session = Session()
session.verify = False
session.auth = HTTPBasicAuth(username, password)
 
transport = Transport(cache=SqliteCache(), session=session, timeout=20)
history = HistoryPlugin()
client = Client(wsdl=wsdl, transport=transport, plugins=[history])
service = client.create_service(binding, location)
 
def show_history():
    for item in [history.last_sent, history.last_received]:
        print(etree.tostring(item["envelope"], encoding="unicode", pretty_print=True))
'''
try:
    resp = service.listPhone(searchCriteria={'name': 'd%'}, 
                             returnedTags={'name': '', 'description': ''})
    print(resp)
except Fault:
    show_history()

try:
    resp = service.listLine(searchCriteria={'pattern': '%'},
                             returnedTags={'pattern': ''})
    print(resp)
except Fault:
    show_history()
'''
try:
    resp1 = service.listUser(searchCriteria={'userid': '%'}, 
                             returnedTags={'userid': '', 'firstName': '', 'lastName': '', 'mailid': '', 'primaryExtension': ''})
    print(resp1)
except Fault:
    show_history()

try:
    resp2 = service.listUser(searchCriteria={'userid': '%'}, 
                             returnedTags={'userid': '', 'firstName': '', 'lastName': '', 'telephoneNumber': ''})
    print(resp2)
except Fault:
    show_history()

