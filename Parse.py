import rdflib
import json

CourseData = json.load(open("courses.json"))
out =  open("out.txt","w")
out.write(
    "@prefix courseNum: <TBA>.\n"+
    "@prefix Course: <TBA>.\n"+
    "@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>.\n"+
    "@prefix careerRoot: <TBA>."
)
preRecs = "";
for I in CourseData :
        for X in I["prerequisites"].split():
            if(len(X)==7):
                print(X)
        n = ""
        n = (
            "\nCourse:" + I["subject"] + I["catalog"] + "" +
            "\n\tCourse:ID "+I["ID"]+";"+
            "\n\ta <https://schema.org/Course>" + ";" +
            #"\n\tCourse:courseCode '" + I["subject"]+I["catalog"] + "';" +
            "\n\tCourse:numberOfCredits " + I["classUnit"]+";" +
            '\n\tCourse:name "' + I["title"]+'"'+";"+
            "\n\tCourse:carrer careerRoot:" + I['career']+""
            )
        if(I["prerequisites"] != ""):
            n += ";\n\tCourse:coursePrerequisites '" + I["prerequisites"].replace("\n" , " ")+"'"
        n += "."
        out.write(n)
out.close()
