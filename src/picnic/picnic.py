#!/usr/bin/env python

import shutil
import os

from quik import FileLoader

module_path = os.path.dirname(os.path.realpath(__file__))
#TODO : manage local template installation, e.g in ~/.picnic
files_path = os.path.join(module_path, 'files')

class Picnic(object):
    def __init__(self, name):
        self.name = name
        self.module_path = name
        
        # BASIC LAYOUT
        self.basic_layout_folders = [self.name,
                os.path.join(self.name, "src"),
                os.path.join(self.name, "src", self.name),
                # for unitests, should use an option. templates ?
                #os.path.join(self.name, "src", "tests"),
                # for cli entry points, should use an option. templates ?
                #os.path.join(self.name, "src", "bin") 
                ]
        # root files
        self.basic_layout_templates= [ "README.rst",
                "MANIFEST.in" ,
                "LICENCE.txt",
                "setup.py",
                "ez_setup.py"]

    def write_file(self, filename, content=''):
        """ Creates a new file and initializes it with the given content."""
        with open(filename, 'w') as f:
            f.write(content)
    
    def create_folders(self, folders):
        """ Create module folders """
        for folder in folders:
            try:
                os.makedirs(folder)
            except:
                pass

    def write_template(self, copy_to, templates, values = {}):
        loader = FileLoader(files_path)
        for tpl in templates:
            if type(templates) == dict:
                outfile = templates[tpl]
            else:
                outfile = tpl

            template = loader.load_template(tpl+".tpl").render(values, loader = loader).encode('utf-8')
            self.write_file(os.path.join(copy_to, outfile), template)

    def create_basic_layout(self):
        self.create_folders(self.basic_layout_folders)
        self.write_template(self.module_path, self.basic_layout_templates, {"PACKAGE_NAME" : self.name})
        self.write_template( os.path.join(self.name, "src", self.name), ["__init__.py"], {"PACKAGE_NAME" : self.name})
        # copy the template module.py.tpl to PACKAGE_NAME.py
        self.write_template(os.path.join(self.name, "src", self.name), {"module.py" : self.name+".py"}, {"PACKAGE_NAME" : self.name})
        

    def main(self):
        """ Class entry point """
        self.create_basic_layout()

def main():
    """ command line entry point """

    # TODO : use optparse
    import sys

    name = sys.argv[1]

    p = Picnic(name)
    p.main()

    # OPTIONS

    if '-doc' in sys.argv:
        # TODO : move the code in Picnic class
        os.mkdir('docs')

    if '-git' in sys.argv:
        # TODO : move the code in Picnic class
        copy_file('.gitignore')
        os.system('git init ; git add . ;')
        os.system('git commit -m "Initial commit"')

    if '-dev' in sys.argv:
        # TODO : do not call sudo here, but run script as sudo.
        # chek user id
        os.system("sudo python setup.py develop")


if __name__ == "__main__":
    main()
