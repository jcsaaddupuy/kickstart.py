""" {{ options.package_name }}/__init__.py """
# -*- coding: utf-8 -*

from . import test_{{ options.package_name }}

def suite():
    import unittest
    suite = unittest.TestSuite()
    suite.addTests(test_{{ options.package_name }}.suite())

    return suite

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
