import re
from utils import session

def getPairs():
    #function provides a a list of patern/querry pairs
    #format of list is [<patern>,<query>]

    paterns = [
        ["what is "," about?","SELECT  ?Description WHERE { ?u schema:courseCode '%s' .?u schema:description ?Description .}"],

        ["which courses did "," take?","SELECT ?Course, ?Grade WHERE {?s rdfs:subClassOf foaf:Person .?s foaf:firstName %s .?s foaf:lastName %s .?s cpo:took ?assessment .?assessment  rdfs:label ?courseId .?assessment  cpo:grade ?Grade .?courseId schema:courseCode ?Course .} "],

        ["which courses cover ", "?", "SELECT DISTINCT ?Course WHERE {?courseId schema:courseCode ?Course . ?courseId owl:sameAs ?link . ?link rdfs:label ?Topic . FILTER regex(?Topic, '%s', 'i') .} "],

        ["who is familiar with ", "?", """SELECT  DISTINCT  ?First ,?Last WHERE {?s rdfs:subClassOf foaf:Person .?s foaf:firstName ?First .?s foaf:lastName ?Last .?s cpo:took ?assessment .?assessment  rdfs:label ?courseId .?assessment  cpo:grade ?Grade .?courseId schema:courseCode ?Course .?courseId owl:sameAs ?link .?link rdfs:label ?Topic . FILTER(?Grade != "F"). FILTER regex(?Topic, "%s", "i") .} """]
    ]
    return paterns

def grounding(phrase):
    phrase.lower()

    for i in getPairs():
        X = phrase.find(i[0])
        if(X != -1):
            Y = phrase.strip(i[1])
            Y = (Y[len(i[0]):])
            if(i[1] == " take?"):
                Y = Y.split(" ")
            else:
                Y = [Y]
            print("grounding reurning:\n"+(i[2] % tuple(Y)))
            return(i[2] % tuple(Y))

def Chatbot():
    phrase = input("Question: ")
    query = grounding(phrase)
    json_t = session.submit(query)
    print(json_t)

Chatbot()