import unittest

from context import *
import networkx

class AuthTestCase(unittest.TestCase): 
    
    def testReadGraph(self):
        """Tests the configuration of a NetAPIClient via a config-file.
        
        Not included in AllTests.py as it depends on a local config
        """
        client = NetAPIClient.fromConfig("dev")
         
        """Verifies the (authenticated) reading of the MiniGraph.dgs"""
        req = GraphQueryRequest()\
            .setSource(Source(type="InputStreamReplayToSource", name="MiniGraph.dgs"))

        res = client.query(req);

        #print("res:" + str(res))
        
        graphModel = res.getGraphModel()
        
        graph = graphModel.asMultiDiGraph()
        print(graph)
        
    def testDefaultSource(self):
        """Tests the default-Sourcing-Argument
        
        Not included in AllTests.py as it depends on a local config
        """
        client = NetAPIClient.fromConfig("qknow-live")
         
        """Verifies the (authenticated) reading of the MiniGraph.dgs"""
        req = GraphQueryRequest()\
            .setSource(Source(name="QKnowLegacyGraphEventSource")\
                .setArgs(limit = 100))

        res = client.query(req);

        #print("res:" + str(res))
        
        graphModel = res.getGraphModel()
        
        graph = graphModel.asMultiDiGraph()
        print(graph)