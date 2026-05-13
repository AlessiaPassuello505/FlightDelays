from model.model import Model

myModel=Model()
myModel.creaGrafo(5)
nNodi,nArchi=myModel.getDettagli()
print(f"Num nodi: {nNodi}, num archi {nArchi}")