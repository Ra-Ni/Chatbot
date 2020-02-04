import rdflib
from rdflib import Graph

g = Graph()
ss = rdflib.util.guess_format('../assets/demo.xml')
g.parse('../assets/demo.xml', 'xml')

for stmt in g:
    print(stmt)
