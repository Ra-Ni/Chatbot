"""
Entry point of the application.

It calls on to parse courses, descriptions, and topics in a sequential manner.

"""
from environment import course, description, topic
from utils import rdf_converter

if __name__ == '__main__':
    target = '../assets/Courses'
    course.fetch(f'{target}_Raw.json')
    course.parse(f'{target}_Raw.json', f'{target}.ttl')

    target = '../assets/Descriptions'
    description.fetch(f'{target}_Raw.json')
    description.parse(f'{target}_Raw.json', f'{target}.ttl')

    output = '../assets/Topics.ttl'
    rdf_converter.fetch(f'{target}.ttl', f'{target}.json')
    topic.parse(f'{target}.json', output)
