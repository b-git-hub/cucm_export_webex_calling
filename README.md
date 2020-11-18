# CUCM export to migrate to Webex Calling
A little program to export the user details from CUCM append those details to a CSV that can be used to import your user details to deploy Webex Calling. Possibly in the future will look to use a bit of REST to post the details rather than a manual import but for the moment this is a proof of concept. By default all services are set to false in the CSV but those can be ammended as needed per client

# Running the code
    git clone https://github.com/b-git-hub/cucm_export_webex_calling/script.py
    pip install requirements.txt 
    python3 script.py

# Information required to run
    The program assumes that you already have the below information 
    CUCM IP, username and password
    Webex subscriptions numbers and Webex domain name
    
# Operation
    This script will ask you some basic information to fill out the CSV file. This script was wrote using CUCM 12.O SOAP API.
    The pull request will contain the 12.X SOAP API toolkit. You'll have to download the latest version for the version of CUCM you are using.
    Once downloaded the SOAP API you'll have to update the location for the variable wsdl on your own PC.
    The SOAP API is available to download for your version of CUCM through Application > Plugins
    Each version is different for each CUCM but this code was wrote with get requests available since version 8.X so there shouldn't be an issue for you.
    
    The script will loop through all the users in the end users page pulling out first/last names, email, primary extension and telephone numbers and appened them to a CSV called webex_calling_user.csv. This can be then imported into the webex admin hub to import the users you require.
    
# Successful output
A successful output will look like the below. Opened in Excel.Libre will produce better results.
First Name,Last Name,Display Name,UserID/Email (Required),User Status,Last Service Accessed Time,Days since Last Service Accessed,Extension,Phone Number,Caller ID Number,Caller ID First Name,Caller ID Last Name,Location,Hybrid Calendar Service Resource Group,Hybrid Call Service Resource Group,Jabber with Webex Teams,Jabber Calling,UC Manager Profile,Contact Migration Required,Upgrade Profile,Calling Behavior,Calling Behavior UC Manager Profile,Call Service Aware,Call Service Connect,Enterprise Content Management,Hybrid Calendar Service (Exchange),Hybrid Calendar Service (Google),Hybrid Message Service,Webex Meeting Assistant,Care Digital Channel [Sub121331],Webex Team Meeting [Sub121331],youtube.com - WebEx Enterprise Edition [Sub121331],Webex Calling SP Enterprise [Sub121331],Webex Teams [Sub121331]
Brian,McBride,Brian McBride,bmcbride@natilik.com,,,,1111,442035978111,442035978111,Brian,McBride,UK,FALSE,,FALSE,FALSE,FALSE,FALSE,FALSE,FALSE,FALSE,FALSE,,FALSE,FALSE,FALSE,FALSE,FALSE,FALSE,FALSE,FALSE,FALSE,FALSE
Gerry,Adams,Gerry Adams,gadams@natilik.com,,,,2222,442035978222,442035978222,Gerry,Adams,UK,FALSE,,FALSE,FALSE,FALSE,FALSE,FALSE,FALSE,FALSE,FALSE,,FALSE,FALSE,FALSE,FALSE,FALSE,FALSE,FALSE,FALSE,FALSE,FALSE
