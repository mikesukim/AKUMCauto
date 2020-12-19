# AKUMCauto
Arkansas Korean United Methodist Church Bulletin Uploading Automation tool

SUMMARY : Retrieving data through GMAIL API, Post data using WORDPRESS API

Requirement : Mac OS & python3 

1. Get credentials.json file from "https://developers.google.com/gmail/api/quickstart/python" and add to directory      
        1) Click Enable the Gmail API (Login to Gmail if necessary)
        2) Create new project
        3) Select Desktop App
        4) Click download configuration
2. Create credentials.py (contains Wordpress credentials) and it should contain USER, PASSWORD, WORDPRESSURL.
        USER and PASSWORD can be found at AKUM Wordpress admin page.
        WORDPRESSURL = "http://arkmumc.org/wp-json/wp/v2"
3. Go to directory at terminal and run "pip3 install -r requirement.txt" 
4. Edit second line of bulletinAuto.sh to current directory url
5. Run "bash bulletinAuto.sh" if your terminal is using ZSH. or use command "sh bulletinAuto.sh"
6. verification window for Gmail will prompt. Verify app by clicking 'Advanced' and 'Go to {appName}' 

        

* When Token Expired error occurs, replace credentials.json by conducting step 1.
