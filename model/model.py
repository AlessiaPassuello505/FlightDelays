import copy

import networkx as nx
from database.DAO import DAO

class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._airports = DAO.getAllAirports()
        self._idMapAirports = {}
        for a in self._airports:
            self._idMapAirports[a.ID] = a

    def creaGrafo(self, nMin):
        nodes = DAO.getAllNodes(nMin, self._idMapAirports)
        self._graph.add_nodes_from(nodes)
        # print(f"N nodi: {len(self._graph.nodes)}, n archi: {len(self._graph.edges)}" )
        # self.addEdges()
        # print(f"N nodi: {len(self._graph.nodes)}, n archi: {len(self._graph.edges)}" )
        # self._graph.clear_edges()
        self.addEdges()
        # print(f"N nodi: {len(self._graph.nodes)}, n archi: {len(self._graph.edges)}" )


    def addEdges(self):
        allTratte = DAO.getAllEdgesV1(self._idMapAirports)
        #Queste tratte hanno 2 problemi: i) ho archi diretti ed inversi,
        # e quindi dovrò fare la somma; ii) ho archi fra aeroporti che avevo filtrato

        for t in allTratte:
            if t.aeroportoP in self._graph and t.aeroportoA in self._graph:
                #allora posso aggiungerlo.
                if self._graph.has_edge(t.aeroportoP, t.aeroportoA):
                    self._graph[t.aeroportoP][t.aeroportoA]["weight"] += t.peso
                else:
                    self._graph.add_edge(t.aeroportoP, t.aeroportoA, weight = t.peso)

    def getDettagli(self):
        return len(self._graph.nodes), len(self._graph.edges)

    def getAllNodes(self):
        nodes =  list(self._graph.nodes)
        nodes.sort(key=lambda x: x.IATA_CODE)
        return nodes

    def getViciniOrdinati(self,source):
        vicini=self._graph.neighbors(source)
        viciniT=[]
        for v in vicini:
            viciniT.append((v,self._graph[source][v]["weight"]))
        viciniT.sort(key=lambda x:x[1], reverse=True)
        return viciniT

    def hasPath(self,v0,v1):
        #restituisce TRUE se ESISTE UN CAMMINO tra v0 e v1, sennò FALSE
        return v1 in nx.node_connected_component(self._graph,v0)
        #restituisce True se v1 è presente nella comp connessa di v0

    def getPath(self,v0,v1):
        dictPredecessori=dict(nx.bfs_predecessors(self._graph,v0))#ogni nodo è una chiave e mi dice il nodo precedente nell'albero di visita
        path=[v1]
        while path[0]!= v0: #finchè non sono arrivata a v0
            path.insert(0, dictPredecessori[path[0]])

        return path

    def getCamminoOttimo(self,v0,v1,t):
        self._bestCammino=[]
        self._bestScore=0

        parziale=[v0]
        self._ricorsione(parziale,v1,t)

        return self._bestCammino,self._bestScore

    def _getScore(self,parziale):
        sumPesi=0
        for i in range(0,len(parziale)-1):
            sumPesi+=self._graph[[parziale[i]][parziale[i+1]]["weight"]]
        return sumPesi

    def _ricorsione(self,parziale,v1,t):
        #verifica se parziale è una sol valida, sennò la salto
        if parziale[-1]==v1: #potenzialmente accettabile
            if self._getScore(parziale)> self._bestScore:
                self._bestCammino=copy.deepcopy(parziale)
                self._bestScore=self._getScore(parziale)

        #verifico se ha senso aggiungere ancora elem a parziale, sennò esco
        if len(parziale)==t+1:
            # parziale ha già raggiunto max num di tratte--->MI FERMO
            return
        #espando parziale e faccio ricorsione con backreturn
        for n in self._graph.neighbors(parziale[-1]):
            if n not in parziale:
                parziale.append(n)
                self._ricorsione(parziale,v1,t)
                parziale.pop()





