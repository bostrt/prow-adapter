#!/usr/bin/python3
import argparse
import requests
from html.parser import HTMLParser
from urllib.parse import urlparse
from gather_pod_logs import GatherPodLogs
from gather_resources_to_namespaces import GatherResourcesToNamespaces
from gather_finished import GatherFinished
from gather_cluster_resources import GatherClusterResources
from job_handler import waitForJobsToComplete

IGNORE_PATHS = ['artifacts/junit']

BASE_DOMAIN=""
BASE_URL=""

HANDLERS = [
    GatherClusterResources(),
    GatherPodLogs(),
    GatherResourcesToNamespaces(),
    GatherFinished()
]

def handle(url):
    for handler in HANDLERS:
        if handler.handles(url):
            handler.handle(url)

class TagParser(HTMLParser):
    startUrl = ""
    def __init__(self, startUrl):
        self.startUrl = startUrl
        HTMLParser.__init__(self)
    
    def handle_starttag(self, tag, attrs):
        if tag == "a":            
            attrs = dict(attrs)            
            if "href" in attrs.keys():
                url = "https://"+BASE_DOMAIN+attrs['href']
                if len(url) <= len(self.startUrl):
                    return                
                
                if url.endswith("/"):
                    getLinksAtLocation(url)
                else:
                    handle(url)

def getLinksAtLocation(url):
    for IGNORE_PATH in IGNORE_PATHS:
        if IGNORE_PATH in url:
            return

    response = requests.get(url)
    parser = TagParser(url)
    parser.feed(response.text)

parser = argparse.ArgumentParser(description="Translates logs from prow in to something that omg and Insights can analyze")

parser.add_argument('--url', dest='base_url', type=str, help='URL to prow job', required=True)

args = parser.parse_args()



BASE_URL = args.base_url
url = urlparse(BASE_URL)

BASE_DOMAIN = url.hostname

getLinksAtLocation(BASE_URL)

waitForJobsToComplete()

for handler in HANDLERS:
    handler.complete()


