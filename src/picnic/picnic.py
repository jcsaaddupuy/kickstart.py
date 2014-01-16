#!/usr/bin/python2

import shutil
import os
import sys

from jinja2 import Environment, PackageLoader, FileSystemLoader
import sh

module_path = os.path.dirname(os.path.realpath(__file__))
files_path = os.path.join(module_path, 'files')

loader = FileSystemLoader(files_path)
env = Environment(loader=loader)

class PicnicOptions(object):
    def __init__(self):
        self.module_path = ""
        self.package_name = ""
        self.with_cli = False
        self.with_tests = False
        self.with_git = False
        self.version = '0.0.0.0'
        self.py_version = sys.version_info.major

class Picnic(object):
    def __init__(self, options):
        self.options = options

        # BASIC LAYOUT
        self.basic_layout_folders = [self.options.package_name,
                os.path.join(self.options.package_name, "src"),
                os.path.join(self.options.package_name, "src", self.options.package_name),
                ]
        if self.options.with_tests :
            self.basic_layout_folders.append(os.path.join(self.options.package_name, "src", "tests"))

        # root files
        self.basic_layout_templates= [ "README.rst", "MANIFEST.in", "LICENCE.txt", "setup.py", "ez_setup.py"]

    def write_file(self, filename, content=''):
        """ Creates a new file and initializes it with the given content."""
        with open(filename, 'w') as f:
            f.write(content)

    def create_folders(self, folders):
        """ Create module folders """
        for folder in folders:
            self.create_folder(folder)

    def create_folder(self, folder):
        try:
            os.makedirs(folder)
        except:
            pass

    def write_template(self, copy_to, templates, values = {}):
        for tpl in templates:
            if type(templates) == dict:
                outfile = templates[tpl]
            else:
                outfile = tpl
            template = env.get_template(tpl+".tpl").render(values, loader = loader).encode('utf-8')
            self.write_file(os.path.join(copy_to, outfile), template)

    def create_basic_layout(self):
        """Create base module layout """
        self.create_folders(self.basic_layout_folders)
        self.write_template(self.options.module_path, self.basic_layout_templates, {"options" : self.options})

        pkg_path = os.path.join(self.options.package_name, "src", self.options.package_name)
        self.write_template( pkg_path, ["__init__.py"], {"options" : self.options})
        self.write_template( pkg_path, { "module.py" : self.options.package_name+".py"}, {"options" : self.options})

    def create_cli_layout(self):
        """ Create module layout for command line entrypoint """
        cli_folder = os.path.join(self.options.package_name, "src", "bin")
        self.create_folder(cli_folder)
        self.write_template( cli_folder, { "bin/main.py" : self.options.package_name+".py"}, {"options" : self.options})
        self.write_template( cli_folder, { "bin/__init__.py" : "__init__.py"}, {"options" : self.options})

    def create_tests_layout(self):
        """ Create module layout for unitests """
        cli_folder = os.path.join(self.options.package_name, "src", "tests")
        self.create_folder(cli_folder)
        self.write_template( cli_folder, { "tests/__init__.py" : "__init__.py"}, {"options" : self.options})
        self.write_template( cli_folder, { "tests/test_module.py" : "test_"+self.options.package_name+".py"}, {"options" : self.options})
    
    def create_git_layout(self):
        """ Create module layout for GIT and initialize the repo """
        module_folder = self.options.package_name
        self.write_template( module_folder, { "git/gitignore" : ".gitignore"}, {"options" : self.options})
        git = sh.git
        # initialize git repo
        git.init(_cwd=module_folder)
        # get an repo object 
        repo = git.bake(_cwd=module_folder)
        # add the module folder to git
        repo.add(".")
        # commit
        repo.commit(m='Initial commit')


    def create_module(self):
        """ Class entry point """
        self.create_basic_layout()
        if self.options.with_cli:
            self.create_cli_layout()
        if self.options.with_tests:
            self.create_tests_layout()
        if self.options.with_git:
            self.create_git_layout()


def main():
    """ command line entry point """
    # TODO : use optparse
    import sys

    name = sys.argv[1]

    options = PicnicOptions() 
    options.module_path = name
    options.package_name = name
    options.with_cli = True
    options.with_tests = True
    options.with_git = True
#    options.version = '0.0.1-test'

    p = Picnic(options)
    p.create_module()


if __name__ == "__main__":
    main()
