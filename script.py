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
import csv
 
 
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


user_subscription=int(input("Enter the user subscribtion number: "))
user_subscription = f'Sub{user_subscription}'
webex_enterprise = input('Enter webex domain URL: ')
location_user = input('Enter the user location (manually modify if multiple locations): ')

print(user_subscription)

try:
    resp1 = service.listUser(searchCriteria={'userid': '%'}, 
                             returnedTags={'userid': '', 'firstName': '', 'lastName': '', 'mailid': '', 'primaryExtension': ''})
    resp1 = resp1['return']['user']
except Fault:
    show_history()

try:
    resp2 = service.listUser(searchCriteria={'userid': '%'}, 
                             returnedTags={'userid': '', 'firstName': '', 'lastName': '', 'telephoneNumber': ''})
    resp2 = resp2['return']['user']
except Fault:
    show_history()


with open('webex_calling_user.csv', 'w', newline='' ) as f:
    fieldnames = [
        'First Name', 'Last Name', 'Display Name', 'UserID/Email (Required)','User Status',
        'Last Service Accessed Time', 'Days since Last Service Accessed', 'Extension',
        'Phone Number', 'Caller ID Number', 'Caller ID First Name', 'Caller ID Last Name','Location', 'Hybrid Calendar Service Resource Group',
        'Hybrid Call Service Resource Group', 'Jabber with Webex Teams', 'Jabber Calling', 'UC Manager Profile',
        'Contact Migration Required', 'Upgrade Profile', 'Calling Behavior', 'Calling Behavior UC Manager Profile',
        'Call Service Aware', 'Call Service Connect','Enterprise Content Management', 'Hybrid Calendar Service (Exchange)',
        'Hybrid Calendar Service (Google)', 'Hybrid Message Service', 'Webex Meeting Assistant', f'Care Digital Channel [{user_subscription}]',
        f'Webex Team Meeting [{user_subscription}]', f'{webex_enterprise} - WebEx Enterprise Edition [{user_subscription}]', 
        f'Webex Calling SP Enterprise [{user_subscription}]', f'Webex Teams [{user_subscription}]'
        ]
    thewriter = csv.DictWriter(f, fieldnames=fieldnames)
    thewriter.writeheader()
    for i,b in zip(resp1, resp2):
        thewriter.writerow({
            'First Name' : i['firstName'], 'Last Name' : i['lastName'],
            'Display Name' : i['firstName'] + ' ' + i['lastName'],
            'UserID/Email (Required)' : i['mailid'], 'Extension' : i['primaryExtension']['pattern'],
            'Caller ID First Name' : i['firstName'], 'Caller ID Last Name' : i["lastName"],
            'Location' : f'{location_user}', 'Hybrid Calendar Service Resource Group' : 'FALSE',
            'Jabber with Webex Teams' : 'FALSE', 'Jabber Calling' : 'FALSE', 'UC Manager Profile' : 'FALSE',
            'Contact Migration Required' : 'FALSE', 'Upgrade Profile' : 'FALSE', 'Calling Behavior' :'FALSE',
            'Calling Behavior UC Manager Profile' : 'FALSE', 'Call Service Aware' : 'FALSE', 'Enterprise Content Management' : 'FALSE',
            'Hybrid Calendar Service (Exchange)' : 'FALSE', 'Hybrid Calendar Service (Google)' : 'FALSE', 'Hybrid Message Service' : 'FALSE',
            'Webex Meeting Assistant' : 'FALSE', f'Care Digital Channel [{user_subscription}]' : 'FALSE', f'Webex Team Meeting [{user_subscription}]' : 'FALSE',
            f'{webex_enterprise} - WebEx Enterprise Edition [{user_subscription}]' : 'FALSE', f'Webex Calling SP Enterprise [{user_subscription}]' : 'FALSE',
            f'Webex Teams [{user_subscription}]': 'FALSE', 'Phone Number' : b['telephoneNumber'], 'Caller ID Number' : b['telephoneNumber']
            })