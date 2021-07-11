#!/usr/bin/python3
import argparse
import requests
from html.parser import HTMLParser
from urllib.parse import urlparse
from prowler.gather_resources_to_namespaces import GatherResourcesToNamespaces
from prowler.gather_finished import GatherFinished
from prowler.gather_cluster_resources import GatherClusterResources
from prowler.gather_namespaces import GatherNamespaces
from prowler.gather_pods import GatherPods
from prowler.gather_must_gather import GatherMustGather
from prowler.job_handler import waitForJobsToComplete

IGNORE_PATHS = ['artifacts/junit']

HANDLERS = [
    
]


def handle(url):
    for handler in HANDLERS:
        if handler.enabled() and handler.handles(url):
            handler.handle(url)


class TagParser(HTMLParser):
    startUrl = ""

    def __init__(self, start_url, base_domain):
        self.start_url = start_url
        self.base_domain = base_domain
        HTMLParser.__init__(self)
    
    def handle_starttag(self, tag, attrs):
        if tag == "a":
            attrs = dict(attrs)
            if "href" in attrs.keys():
                url = "https://"+self.base_domain+attrs['href']
                if len(url) <= len(self.start_url):
                    return
                if url.endswith("/"):
                    getLinksAtLocation(url, self.base_domain)
                else:
                    handle(url)


def getLinksAtLocation(url, base_domain):
    for IGNORE_PATH in IGNORE_PATHS:
        if IGNORE_PATH in url:
            return

    response = requests.get(url)
    parser = TagParser(url, base_domain)
    parser.feed(response.text)


def buildHandlers(mgOnly):
    HANDLERS.append(GatherFinished())
    
    if mgOnly.lower() == 'true':
        HANDLERS.append(GatherMustGather())
    else:
        HANDLERS.append(GatherClusterResources())
        HANDLERS.append(GatherPods())
        HANDLERS.append(GatherResourcesToNamespaces())
        HANDLERS.append(GatherNamespaces())
        

def main():
    parser = argparse.ArgumentParser(description="Translates logs from prow in to something that omg and Insights can analyze")
    parser.add_argument('--url', dest='base_url', type=str, help='URL to prow job', required=True)
    parser.add_argument('--must-gather', dest='mg_enable', type=str, help='Retrieves a must-gather from the build if it exists.  If false, a must-gather archive is constructed from available data.', default='true')
    args = parser.parse_args()

    base_url = args.base_url
    MG_ENABLE = args.mg_enable
    url = urlparse(base_url)

    base_domain = url.hostname
    buildHandlers(MG_ENABLE)
    getLinksAtLocation(base_url, base_domain)

    waitForJobsToComplete()

    for handler in HANDLERS:
        handler.complete()
