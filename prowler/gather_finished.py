
from prowler.handler import Handler
import requests

class GatherFinished(Handler):
    def __init__(self):        
        Handler.__init__(self,"/finished.json")
        self.setEnable(True)

    results = {}

    def processUrl(self, url):
        r = requests.get(url)
        result = r.json()
        parts = url.split("/")
        part = parts[-2:-1][0]
        self.results[part] = result["passed"]
        
    def handle(self,url):        
        self.processUrl(url)

    def complete(self):
        print("Step results >>>")
        for step in self.results:
            print("\t" + step + ": " + str(self.results[step]))
