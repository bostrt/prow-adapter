
from prowler.handler import Handler
import os
import requests
import yaml
from prowler.job_handler import submitJob


class GatherResourcesToNamespaces(Handler):
    collections = []

    def __init__(self):
        Handler.__init__(self,'')
        self.collections = [{
            'path': '/gather-extra/artifacts/events.json',
            'outputDir': 'core',
            'outputName': 'events.yaml',
            'namespaces': {}
        }, 
        {
            'path': '/gather-extra/artifacts/configmaps.json',
            'outputDir': 'core',
            'outputName': 'configmaps.yaml',
            'namespaces': {}
        },
        {
            'path': '/gather-extra/artifacts/secrets.json',
            'outputDir': 'core',
            'outputName': 'secrets.yaml',
            'namespaces': {}
        },        
        {
            'path': '/gather-extra/artifacts/endpoints.json',
            'outputDir': 'core',
            'outputName': 'endpoints.yaml',
            'namespaces': {}
        },        
        {
            'path': '/gather-extra/artifacts/persistentvolumeclaims.json',
            'outputDir': 'core',
            'outputName': 'persistentvolumeclaims.yaml',
            'namespaces': {}
        },        
        {
            'path': '/gather-extra/artifacts/pods.json',
            'outputDir': 'core',
            'outputName': 'pods.yaml',
            'namespaces': {}
        },        
        {
            'path': '/gather-extra/artifacts/services.json',
            'outputDir': 'core',
            'outputName': 'services.yaml',
            'namespaces': {}
        },        
        {
            'path': '/gather-extra/artifacts/daemonsets.json',
            'outputDir': 'app',
            'outputName': 'daemonsets.yaml',
            'namespaces': {}
        },        
        {
            'path': '/gather-extra/artifacts/deployments.json',
            'outputDir': 'app',
            'outputName': 'deployments.yaml',
            'namespaces': {}
        },        
        {
            'path': '/gather-extra/artifacts/replicasets.json',
            'outputDir': 'app',
            'outputName': 'replicasets.yaml',
            'namespaces': {}
        },        
        {
            'path': '/gather-extra/artifacts/statefulsets.json',
            'outputDir': 'app',
            'outputName': 'statefulsets.yaml',
            'namespaces': {}
        },        
        {
            'path': '/gather-extra/artifacts/machines.json',
            'outputDir': 'machine.openshift.io/machines',            
            'namespaces': {}
        },        
        {
            'path': '/gather-extra/artifacts/machinesets.json',
            'outputDir': 'machine.openshift.io/machinesets',            
            'namespaces': {}
        }]


    def storeYamlForNs(self, event, metadata, collection):
        nsArray = {
                'apiVersion': 'v1',
                'items':[]
        }
        namespace = metadata['namespace']
        if namespace not in collection['namespaces']:
            collection['namespaces'][namespace] = nsArray
        else:
            nsArray = collection['namespaces'][namespace]
        nsArray['items'].append(event)

    def writeYamls(self, collection):
        for namespace in collection['namespaces']:
            path = 'out/namespaces/'+namespace+'/'+collection['outputDir']+'/'
            self.ensurePathExists(path)
            
            if 'outputName' in collection:
                outPath = os.path.join(path,collection['outputName'])
                print("Writing "+ collection['outputName'] + " to ["+ collection['outputDir'] +"] in ["+namespace+"]")
                with open(outPath, 'wb') as f:
                    f.write(bytes(yaml.dump(collection['namespaces'][namespace]),"utf-8"))    

            elif 'items' in collection['namespaces'][namespace]:
                for item in collection['namespaces'][namespace]['items']:
                    metadata = item['metadata']
                    if ('name' not in metadata) or \
                        ('namespace' not in metadata):
                        continue
                    outPath = os.path.join(path,metadata['name']+".yaml")
                    with open(outPath, 'wb') as f:
                        f.write(bytes(yaml.dump(item),"utf-8"))    


    def processResource(self, url, collection):
        r = requests.get(url)
        events = r.json()
        
        if 'items' not in events:
            return
        
        for event in events['items']:
            if 'metadata' not in event:
                continue
            metadata = event['metadata']
            if ('name' not in metadata) or \
                ('namespace' not in metadata):
                continue
            self.storeYamlForNs(event,metadata,collection)
        self.writeYamls(collection)

    def processUrl(self, url):
        for collection in self.collections:
            if collection['path'] in url:
                submitJob(self.processResource,url, collection)

                
    def handle(self,url):        
        self.processUrl(url)        
        
    def handles(self, url):
        for collection in self.collections:            
            if collection['path'] in url:                
                return True

        


