#!/usr/bin/python2
# -*- coding: utf-8 -*-

import shutil
import os
import sys

from jinja2 import Environment, PackageLoader, FileSystemLoader
import sh
import shutil
import optparse

import logging

module_path = os.path.dirname(os.path.realpath(__file__))
files_path = os.path.join(module_path, 'files')

loader = FileSystemLoader(files_path)
env = Environment(loader=loader)


class Picnic(object):
    def __init__(self, options):
        self.options = options
        self.init_logger()

        # BASIC LAYOUT
        self.basic_layout_folders = [self.options.package_name,
                os.path.join(self.options.package_name, "src"),
                os.path.join(self.options.package_name, "src", self.options.package_name),
                ]
        if self.options.with_tests :
            self.basic_layout_folders.append(os.path.join(self.options.package_name, "src", "tests"))

        # root files
        self.basic_layout_templates= [ "README.rst", "MANIFEST.in", "LICENCE.txt", "setup.py", "ez_setup.py"]

    def init_logger(self):
        if self.options.debug :
            logging.basicConfig(level = logging.DEBUG)
        elif not self.options.quiet:
            logging.basicConfig(level = logging.INFO)
        self.logger = logging.getLogger(__name__)

    def write_file(self, filename, content=''):
        """ Creates a new file and initializes it with the given content."""
        if self.options.force or not os.path.exists(filename):
            with open(filename, 'w') as f:
                f.write(content)

    def create_folders(self, folders):
        """ Create module folders """
        for folder in folders:
            self.create_folder(folder)

    def create_folder(self, folder):
        try:
            self.logger.debug("Creating folder %s", folder)
            os.makedirs(folder)
        except:
            pass

    def write_template(self, copy_to, templates, values = {}):
        for tpl in templates:
            tpl_fullname = tpl+".tpl"
            if type(templates) == dict:
                outfile = templates[tpl]
            else:
                outfile = tpl
            self.logger.debug("Copying %s to %s", tpl_fullname, outfile)
            template = env.get_template(tpl_fullname).render(values, loader = loader).encode('utf-8')
            self.write_file(os.path.join(copy_to, outfile), template)

    def create_basic_layout(self):
        """Create base module layout """
        self.logger.info("Creating basic layout")
        pkg_path = os.path.join(self.options.package_name)
        self.create_folders(self.basic_layout_folders)
        self.write_template(pkg_path, self.basic_layout_templates, {"options" : self.options})

        src_path = os.path.join(self.options.package_name, "src", self.options.package_name)
        self.write_template( src_path, ["__init__.py"], {"options" : self.options})
        self.write_template( src_path, { "module.py" : self.options.package_name+".py"}, {"options" : self.options})

    def create_cli_layout(self):
        self.logger.info("Creating CLI layout")
        """ Create module layout for command line entrypoint """
        cli_folder = os.path.join(self.options.package_name, "src", "bin")
        self.create_folder(cli_folder)
        self.write_template( cli_folder, { "bin/main.py" : self.options.package_name+".py"}, {"options" : self.options})
        self.write_template( cli_folder, { "bin/__init__.py" : "__init__.py"}, {"options" : self.options})

    def create_tests_layout(self):
        """ Create module layout for unitests """
        self.logger.info("Creating tests layout")
        cli_folder = os.path.join(self.options.package_name, "src", "tests")
        self.create_folder(cli_folder)
        self.write_template( cli_folder, { "tests/__init__.py" : "__init__.py"}, {"options" : self.options})
        self.write_template( cli_folder, { "tests/test_module.py" : "test_"+self.options.package_name+".py"}, {"options" : self.options})

    def create_git_layout(self):
        """ Create module layout for GIT and initialize the repo """
        self.logger.info("Creating git repository")
        module_folder = self.options.package_name

        git_folder = os.path.join(module_folder, ".git")
        if self.options.force and os.path.exists(git_folder):
            self.logger.debug("Removing old git files")
            shutil.rmtree(git_folder)

        self.write_template( module_folder, { "git/gitignore" : ".gitignore"}, {"options" : self.options})
        git = sh.git
        
        self.logger.info("Git init")
        git.init(_cwd=module_folder)

        # get an repo object 
        repo = git.bake(_cwd=module_folder)
        # add the module folder to git
        self.logger.info("Adding files")
        repo.add(".")
        # commit
        self.logger.info("Initial commit")
        try:
            repo.commit(m='Initial commit')
        except Exception, e:
            self.logger.error(e.message)


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
    parser = optparse.OptionParser("usage: %prog -n module_name [options]")

    parser.add_option("-d", "--debug", dest="debug", action="store_true", default=False, help="Enable debug output")
    parser.add_option("-q", "--quiet", dest="quiet", action="store_true", default=False, help="Disable output")

    parser.add_option("-v", "--version", dest="version", action="store", type= "string", default="0.0.0.0", help="Module version")
    parser.add_option("-t", "--tests", dest="with_tests", action="store_true", default=False, help="Create tests layout")
    parser.add_option("-g", "--git", dest="with_git", action="store_true", default=False, help="Enable git repo creation")
    parser.add_option("-c", "--cli", dest="with_cli", action="store_true", default=False, help="Create CLI layout")

    parser.add_option("-p", "--pyversion", dest="py_version", action="store", default=sys.version_info.major, help="Default python version for #!")
    parser.add_option("-n", "--name", dest="package_name", action="store", default=None, help="Package name")

    parser.add_option("-f", "--force", dest="force", action="store_true", default=False, help="Will override existing files. Use with care.")

    (options, args) = parser.parse_args()
    if options.package_name is None :
        parser.error("You must provide a package name. See --help")

    p = Picnic(options)
    p.create_module()


if __name__ == "__main__":
    main()
