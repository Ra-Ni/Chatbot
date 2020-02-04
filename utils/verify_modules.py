"""
A module dependency checker when setting up/ working on the project.

It's important to keep this updated so we can avoid any errors when pulling

"""
import pkg_resources

required = {'rdflib': 'https://github.com/RDFLib/rdflib'}
installed = {pkg.key for pkg in pkg_resources.working_set}
missing = set(required.keys()) - installed

if missing:
    print('\033[41m The following modules are missing: \033[0m')
    for i in missing:
        print('%-15s %s' % (i, required[i]))
else:
    print('\033[42m No modules are missing \033[0m')
