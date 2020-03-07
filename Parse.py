import rdflib
import json
def CourseParsing(IN , OUT):
    CourseData = json.load(open(IN))#"courses.json"
    out =  open(OUT,"w")#"Courses.ttl"
    out.write(
        #"@prefix courseNum: <https://conupedia.sytes.net/CourseNum/>.\n"+
        "@prefix Cr: <https://conupedia.sytes.net/Course/>.\n"+
        "@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>.\n"+
        "@prefix Career: <https://conupedia.sytes.net/Career/>.\n\n"+

        "Career:UGRD\n" +    #Carrer Touples
            "\tCareer:URL " +
                "<https://www.concordia.ca/academics/undergraduate.html>;\n" +
            "\tCareer:Name " +
                '"Undergraduate Studies".' +
        "\nCareer:GRAD\n" +
            "\tCareer:URL "+
                "<https://www.concordia.ca/academics/graduate.html>;\n" +
            "\tCareer:Name " +
                '"Graduate Studies".' +
        "\nCareer:CCCE\n" +
            "\tCareer:URL " +
                "\t<https://www.concordia.ca/cce.html>;\n" +
            "\tCareer:Name " +
                '"Concordia Center for Continued Education".' +
        "\nCareer:PDEV\n" +
            "\tCareer:URL " +
                "\t<https://www.concordia.ca/students/gradproskills.html>;\n" +
            "\tCareer:Name " +
                '"GradProSkills".' +

        "\t"
        "\n"

    )
    preRecs = ""
    for I in CourseData :
            n = ""
            n = (
                #"\nCourse:" + I["subject"] + I["catalog"] + "" +
                "\nCr:"+I["ID"]+""+
                "\n\ta <https://schema.org/Course>" + ";" +
                "\n\tCr:courseCode '" + I["subject"]+I["catalog"] + "';" +
                "\n\tCr:numberOfCredits " + I["classUnit"]+";" +
                '\n\tCr:name "' + I["title"].replace('"',"'")+'"'+";"+
                '\n\tCr:career Career:' + I['career']+' '
                )
            if(I["prerequisites"] != ""):
                n += ";\n\tCr:coursePrerequisites '" + I["prerequisites"].replace("\n" , " ")+"'"
            n += (
                    "." +
                    "\n<http://dbpedia.org/resource/Concordia_University> Cr:offers Cr:" + I["ID"] + "."
                )
            out.write(n)
    out.close()

CourseParsing("courses.json","Courses.ttl")
