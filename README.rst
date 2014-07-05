Pyckstart
=========

Pyckstart is a simple template engine for writing python modules, based on Jinja2.

It can generate bases layout for simple python modules, with or without CLI, unitests, and git local repo initialization.

It is a fork of Picnic_ by Zulko_.

You open a console and in any folder you type ::
    
    pyckstart -n ModuleName

and it will produce the following folder, with (almost ?) all the files you need. All there is left to do is write the actual code : ::

    ~: find ModuleName 
     ModuleName
     ModuleName/README.rst
     ModuleName/setup.py
     ModuleName/src
     ModuleName/src/modulename
     ModuleName/src/modulename/modulename.py
     ModuleName/src/modulename/__init__.py
     ModuleName/LICENCE.txt
     ModuleName/MANIFEST.in


You can then cd to you module folder and type : ::

    python setup.py develop


Options
--------
    Usage: pyckstart -n module_name [options]

    Options:
      -h, --help            show this help message and exit
      -d, --debug           Enable debug output
      -q, --quiet           Disable output
      -v VERSION, --version=VERSION
                            Module version
      -t, --tests           Create tests layout
      -g, --git             Enable git repo creation
      -c, --cli             Create CLI layout
      -p PY_VERSION, --pyversion=PY_VERSION
                            Python version for #!/usr/bin/env python#. Default
                            value : current python major version (2)
      -n PACKAGE_NAME, --name=PACKAGE_NAME
                            Package name
      -i, --install         Install templates in home folder
      -f, --force           Will override existing files. Use with care.



Examples
--------
To create a new module, with CLI, unitests and git, juste type : ::

     pyckstart -t -c -g -n MyModulename

I will generate the folowing layout : ::

    find MyModulename | grep -v git
     MyModulename
     MyModulename/README.rst
     MyModulename/setup.py
     MyModulename/src
     MyModulename/src/tests
     MyModulename/src/tests/test_mymodulename.py
     MyModulename/src/tests/__init__.py
     MyModulename/src/mymodulename
     MyModulename/src/mymodulename/mymodulename.py
     MyModulename/src/mymodulename/__init__.py
     MyModulename/src/bin
     MyModulename/src/bin/mymodulename.py
     MyModulename/src/bin/__init__.py
     MyModulename/LICENCE.txt
     MyModulename/MANIFEST.in
 
You can then cd to you module folder and type : ::

    # install it in dev mode
    python setup.py develop    
    # run unitests
    python setup.py test

By installing in dev mode, your module as automagically created the CLI entrypoint. You can then, in a terminal, type : ::

    mymodulename

Wich will run the file MyModulename/src/bin/mymodulename.py.

Installation and customization
--------------------------------

From the source
''''''''''''''''

    git clone https://github.com/jcsaaddupuy/pyckstart.py.git

    cd pyckstart 

    sudo python setup.py install




Customization
''''''''''''''

If you want to pimp the templates, you can install them locall in your home foler : ::

    pyckstart -i

All templates will be copied to ~/.pyckstart/files/, wich you can edit freely to override defaults.

Contribute
-----------

Pyckstart is an open source software originally written by Zulko_ and released under the MIT licence. Please help make Pyckstart or Picnic betters, for instance by expanding the capabilities, providing advice for sounder standards if you are an experienced module-maker, reporting bugs, etc. We love forks and pull resquests !
Pyckstart is being developped on Github_, that's where you should go for troubleshooting and bug reports.

.. _Zulko : https://github.com/Zulko
.. _Github :  https://github.com/jcsaaddupuy/pyckstart.py.git
.. _Picnic :  https://github.com/Zulko/picnic.py
