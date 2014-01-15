import ez_setup
ez_setup.use_setuptools()

from setuptools import setup, find_packages

setup(name='{{options.package_name}}',
        version='0.0.0.0',
        author='',
        description='{{ options.package_name }} description',
        long_description=open('README.rst').read(),
        license='LICENSE.txt',
        keywords="",

        package_dir = {'':'src'},
        packages= find_packages('src', exclude='docs'),
{% if options.with_cli %}
        entry_points = { 
            'console_scripts': [
                '{{options.package_name}} = bin.{{options.package_name}}:main',
                ]
            },
{% endif %}
        include_package_data = True,
        package_data = {
            '' : [ 'files/*' ]
            }

        )	
