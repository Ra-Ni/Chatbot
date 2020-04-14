import re
import json
from utils import session

def getPairs():
    #function provides a a list of patern/querry pairs
    #format of list is [<patern>,<query>]

    paterns = [
        ["what is "," about?","SELECT  ?Description WHERE { ?u schema:courseCode '%s' .?u schema:description ?Description .}"],

        ["which courses did ","take?","SELECT ?Course, ?Grade WHERE {?s rdfs:subClassOf foaf:Person .?s foaf:firstName '%s' .?s foaf:lastName '%s' .?s cpo:took ?assessment .?assessment  rdfs:label ?courseId .?assessment  cpo:grade ?Grade .?courseId schema:courseCode ?Course .} "],

        ["which courses cover ", "?", "SELECT DISTINCT ?Course WHERE {?courseId schema:courseCode ?Course . ?courseId owl:sameAs ?link . ?link rdfs:label ?Topic . FILTER regex(?Topic, '%s', 'i') .} "],

        ["who is familiar with ", "?", """SELECT  DISTINCT  ?First ,?Last WHERE {?s rdfs:subClassOf foaf:Person .?s foaf:firstName ?First .?s foaf:lastName ?Last .?s cpo:took ?assessment .?assessment  rdfs:label ?courseId .?assessment  cpo:grade ?Grade .?courseId schema:courseCode ?Course .?courseId owl:sameAs ?link .?link rdfs:label ?Topic . FILTER(?Grade != "F"). FILTER regex(?Topic, "%s", "i") .} """],
    ]

    return paterns

def grounding(phrase):
    for queryInstanceList in getPairs():
        if(phrase.lower().find(queryInstanceList[0]) != -1):
            Y = phrase.strip(queryInstanceList[1])
            Y = (Y[len(queryInstanceList[0]):])
            if(queryInstanceList[1] == "take?"):
                Y = Y.strip()
                Y = Y.split(" ")
            else:
                Y = [Y]
            #print("grounding reurning:\n"+(queryInstanceList[2] % tuple(Y)))
            return(queryInstanceList[2] % tuple(Y))
    return -1

def Chatbot():
    phrase = input("Question: ")
    query = grounding(phrase)
    Se = session.Session()
    print("\nAnswer:\n")
    if(query != -1):
        response = Se.submit(query)
        if(response):
            for key in response[0]:
                print(key, end='\t')
            print("\n")
            for element in response:
                for key in element:
                    print(element[key], end='\t')
                print()

if __name__ == '__main__':
    Chatbot()