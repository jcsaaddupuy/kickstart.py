import ez_setup
ez_setup.use_setuptools()

from setuptools import setup, find_packages

setup(name='{{options.package_name}}',
        version='{{options.version}}',
        author='',
        description='{{ options.package_name }} description',
        long_description=open('README.rst').read(),
        license='LICENSE.txt',
        keywords="",
        
        # package source directory
        package_dir = {'':'src'},
        packages= find_packages('src', exclude='docs')
{% if options.with_cli %}
{% set module_name = options.package_name.lower() %}
        # configure the default command line entry point.
        ,entry_points = { 
            'console_scripts': [
                '{{module_name}} = bin.{{module_name}}:main',
                ]
            }
{% endif %}
{% if options.with_tests %}
        # configure the default test suite
       , test_suite = 'tests.suite'
{% endif %}
        )    
