# -*- coding: utf-8 -*-
"""
Created on Wed Jul 03 09:23:31 2013

@author: aitor
"""

import networkx as nx
from collections import OrderedDict

class network_analyzer():
    
    def load_edgelist(self, edgelist): 
        G = nx.parse_edgelist(edgelist)
        return G
        
    def calculate_degree_centrality(G):
        cent_degree = nx.degree_centrality(G)
        sorted_cent_degree = OrderedDict(sorted(cent_degree.items(), key=lambda t: t[1], reverse=True))
        return sorted_cent_degree
        
    def calculate_betweenness_centrality(G):    
        cent_betweenness = nx.betweenness_centrality(G)
        sorted_cent_betweenness = OrderedDict(sorted(cent_betweenness.items(), key=lambda t: t[1], reverse=True))
        return sorted_cent_betweenness
        
    def calculate_closeness_centrality(G):   
        cent_closeness = nx.closeness_centrality(G)
        sorted_cent_closeness = OrderedDict(sorted(cent_closeness.items(), key=lambda t: t[1], reverse=True))
        return sorted_cent_closeness

    def calculate_eigenvector_centrality(G):   
        cent_eigenvector = nx.eigenvector_centrality(G)
        sorted_cent_eigenvector = OrderedDict(sorted(cent_eigenvector.items(), key=lambda t: t[1], reverse=True))
        return sorted_cent_eigenvector
            
    def calculate_pagerank(G):
        page_rank = nx.pagerank(G)
        sorted_page_rank = OrderedDict(sorted(page_rank.items(), key=lambda t: t[1], reverse=True))
        return sorted_page_rank