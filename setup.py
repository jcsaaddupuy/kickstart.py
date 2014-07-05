import ez_setup
ez_setup.use_setuptools()

from setuptools import setup, find_packages

setup(name='kickstart',
        version='0.0.1',
        author='Zulko 2013',
        description='Module for easy python modules creation',
        long_description=open('README.rst').read(),
        license='LICENSE.txt',
        keywords="python module template engine setuptools",
        install_requires = ["jinja2 >= 2.7.2", "sh >= 1.09"],

        package_dir = {'':'src'},
        packages= find_packages('src', exclude='docs'),

        entry_points = {
            'console_scripts': [
                'kickstart = kickstart:main',
                ]
            },

        include_package_data = True,
        package_data = {
            '' : [ 'files/*.tpl', 'files/**/*.tpl' ]
            }

        )
