import re
import json
from utils import session

def getPairs():
    #function provides a a list of patern/querry pairs
    #format of list is [<patern>,<query>]

    paterns = [
        ["what is "," about?","SELECT  ?Description WHERE { ?u schema:courseCode '%s' .?u schema:description ?Description .}", "%s is described as being about %s"],

        ["which courses did ","take?","SELECT ?Course, ?Grade WHERE {?s rdfs:subClassOf foaf:Person .?s foaf:firstName '%s' .?s foaf:lastName '%s' .?s cpo:took ?assessment .?assessment  rdfs:label ?courseId .?assessment  cpo:grade ?Grade .?courseId schema:courseCode ?Course .} ","%s has taken %s where they were awarded a grade of %s"],

        ["which courses cover ", "?", "SELECT DISTINCT ?Course WHERE {?courseId schema:courseCode ?Course . ?courseId owl:sameAs ?link . ?link rdfs:label ?Topic . FILTER regex(?Topic, '%s', 'i') .} ","%sis a topic covered by %s"],

        ["who is familiar with ", "?", """SELECT  DISTINCT  ?First ,?Last WHERE {?s rdfs:subClassOf foaf:Person .?s foaf:firstName ?First .?s foaf:lastName ?Last .?s cpo:took ?assessment .?assessment  rdfs:label ?courseId .?assessment  cpo:grade ?Grade .?courseId schema:courseCode ?Course .?courseId owl:sameAs ?link .?link rdfs:label ?Topic . FILTER(?Grade != "F"). FILTER regex(?Topic, "%s", "i") .} ""","The topic of %sis understood by %s %s"],
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
            querryTarget = ""
            for i in Y:
                querryTarget += i + " "
            return([queryInstanceList[2] % tuple(Y), queryInstanceList[3], querryTarget])
    return -1

def Chatbot():
    phrase = input("What would you like to know about Concordia?\n")
    ground = grounding(phrase)
    if(ground == -1):
        return
    query = ground[0]
    responseFormat = ground[1]
    Se = session.Session()
    if(query != -1):
        response = Se.submit(query)
        if(response):
            #for key in response[0]:
            #   print(key, end='\t')
            #print("\n")

            for element in response:
                Answer = []
                (Answer.append(ground[2]))
                for key in element:
                    Answer.append(element[key])
                # print(responseFormat)
                # print(Answer)
                print(responseFormat % tuple(Answer))

        else:
            print("Sorry, I couldn't find anything to help you with that")


if __name__ == '__main__':
    while(True):
        Chatbot()