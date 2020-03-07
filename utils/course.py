from json import load, loads, dump
from re import sub
from string import capwords
from typing import Union

from utils import prefixes, opendata
from utils.progress_bar import ProgressBar


def fetch(output: Union[str, bytes, int]) -> None:
    with open(output, 'w') as writer:
        json_form = opendata.fetch('/course/catalog/filter/*/*/*')
        dump(json_form, writer, indent=4)


def parse(target: Union[str, bytes, int], output: Union[str, bytes, int]) -> None:
    course_prefix, course_acronym = prefixes.COURSE
    rdfs_prefix, rdfs_acronym = prefixes.RDFS
    career_prefix, career_acronym = prefixes.CAREER
    course_number_prefix, course_number_acronym = prefixes.COURSE_NUMBER
    schema_prefix, schema_acronym = prefixes.SCHEMA
    dbpedia_resource_prefix, dbpedia_resource_acronym = prefixes.DBPEDIA_RESOURCE
    xsd_prefix, xsd_acronym = prefixes.XMLSCHEMA

    careers = {
        'UGRD': '<https://www.concordia.ca/academics/undergraduate.html>',
        'GRAD': '<https://www.concordia.ca/academics/graduate.html>',
        'CCCE': '<https://www.concordia.ca/cce.html>',
        'PDEV': '<https://www.concordia.ca/students/gradproskills.html>'
    }

    courses_seen = set()

    with open(output, 'w') as writer:

        writer.write(f'{course_prefix}\n{rdfs_prefix}\n{career_prefix}\n{course_number_prefix}\n{schema_prefix}\n{dbpedia_resource_prefix}\n{xsd_prefix}')

        with open(target, 'r') as reader:
            json_form = load(reader)
            progress_bar = ProgressBar(len(json_form))

            for item in json_form:
                progress_bar.console_update()
                if item['ID'] in courses_seen:
                    continue

                courses_seen.add(item['ID'])
                subject = f'<{course_acronym}:{item["ID"]}>'
                turtle_form = list()
                turtle_form.append(f'\n\t{rdfs_acronym}:type {schema_acronym}:Course')
                turtle_form.append(f'\n\t{schema_acronym}:courseCode \"{item["subject"]}{item["catalog"]}\"')
                turtle_form.append(f'\n\t{schema_acronym}:numberOfCredits \"{item["classUnit"]}\"^^{xsd_acronym}:float')

                title = sub('["\']', '\'', item['title'])
                title = title.lower()
                title = capwords(title)

                turtle_form.append(f'\n\t{schema_acronym}:name \"{title}\"')
                turtle_form.append(f'\n\t{schema_acronym}:isPartOf {careers[item["career"]]}')

                if item['prerequisites']:
                    prerequisites = sub('( ){2,}', ' ', item['prerequisites'])
                    prerequisites = sub('[\r\n]+', '', prerequisites)
                    turtle_form.append(f'\n\t{course_acronym}:coursePrerequisites \"{prerequisites}\"')

                turtle_form.append(f'\n\t{schema_acronym}:provider {dbpedia_resource_acronym}:Concordia_University')

                properties = ' ;'.join(turtle_form)

                writer.write(f'\n\n{subject}{properties} .')


if __name__ == '__main__':
    fetch('../assets/Courses.json')
    parse("../assets/Courses.json", "../assets/Courses.ttl")
