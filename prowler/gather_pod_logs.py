
from urllib.parse import urlparse
from prowler.handler import Handler
import os
import requests
from prowler.job_handler import submitJob

class GatherPodLogs(Handler):
    def __init__(self):
        Handler.__init__(self,"/gather-extra/artifacts/pods")

    def getFileParts(self,url):
        partsDef = {
            'namespace': None,
            'podName': None,
            'container': None,
            'previous': False
        }
        
        logFileName = url.rsplit('/', 1)[-1]
        
        parts = logFileName.split('_')
        
        if len(parts) < 3:
            return partsDef
        partsDef['namespace'] = parts[0]
        partsDef['podName'] = parts[1]
        partsDef['container'] = parts[2]
        if len(parts)>=4:
            partsDef['previous'] = parts[3] == 'previous'
        return partsDef    

    def downloadFile(self,parts, url):
        path = 'out/namespaces/'+   \
                parts['namespace']+ \
                '/pods/'+           \
                parts['podName']+'/' +\
                parts['container']+'/' +\
                parts['container']+'/logs/'

        if os.path.exists(path) == False:
            os.makedirs(path)

        outPath = ""
        if parts['previous']: 
            outPath = os.path.join(path,"previous.log")
        else:
            outPath = os.path.join(path,"current.log")
        
        r = requests.get(url)

        print("Saving pod log ["+outPath+"]")
        with open(outPath, 'wb') as f:
            f.write(r.content)    
        
    def handle(self,url):        
        if url.endswith(".log") == False:
            return        
        
        parts = self.getFileParts (os.path.splitext(url)[0])
        if parts['namespace'] == None or \
           parts['podName'] == None or \
            parts['container'] == None:
            return
                
        submitJob(self.downloadFile, parts, url)

