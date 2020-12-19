# AKUMCauto
Arkansas Korean United Methodist Church Bulletin Uploading Automation tool

SUMMARY : Retrieving data through GMAIL API, Post data using WORDPRESS API

1. Get credentials.json file from "https://developers.google.com/gmail/api/quickstart/python" and add to directory
2. Create credentials.py (contains Wordpress credentials) and it should contain USER, PASSWORD, WORDPRESSURL.
        USER and PASSWORD can be found at AKUM Wordpress admin page.
        WORDPRESSURL = "http://arkmumc.org/wp-json/wp/v2"
3. install requirements.txt       
4. verification window for Gmail will prompt. Verify app by clicking 'Advanced' and 'Go to {appName}' 

* When Token Expired error occurs, replace credentials.json by conducting step 1.
