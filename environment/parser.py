"""
Entry point of the application.

It calls on to parse courses, descriptions, and topics in a sequential manner.

"""
from re import sub

from environment import course, description, topic
from utils import rdf_converter
from utils.progress_bar import ProgressBar

"""
 target = '../assets/Courses'
    course.fetch(f'{target}_Raw.json')
    course.parse(f'{target}_Raw.json', f'{target}.ttl')

    target = '../assets/Descriptions'
    description.fetch(f'{target}_Raw.json')
    description.parse(f'{target}_Raw.json', f'{target}.ttl')

    output = '../assets/Topics.ttl'
    rdf_converter.fetch(f'{target}.ttl', f'{target}.json')
    topic.parse(f'{target}.json', output)

    
"""
if __name__ == '__main__':

    prefixes = set()
    courses = {}

    folder = '../assets'
    files = [f'{folder}/Courses.ttl', f'{folder}/Descriptions.ttl', f'{folder}/Topics.ttl']

    for file in files:
        print(f'reading {file}')
        with open(file, 'r') as reader:
            line = reader.readline()
            course_id = None
            while line:

                if '@prefix' in line:
                    new_prefix = sub('\n', '', line)
                    prefixes.add(new_prefix)
                if '<cpc:' in line:
                    course_id = line
                    if course_id not in courses:
                        courses[course_id] = []
                if '\t' in line:
                    new_line = sub('[;.]\n', '', line)
                    courses[course_id].append(new_line)
                line = reader.readline()

    with open(f'{folder}/Output.ttl', 'w') as writer:
        writer.write('\n'.join(prefixes))

        for key, value in courses.items():


            body = ' ;\n'.join(value)

            writer.write(f'\n\n{key}{body} .')
