import sys
import unittest
import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
# Assume you have test classes in different modules
from test_case.test_usecase.test_user.test_get_all_resource import TestGetAllResourceUsecase


# Create a TestSuite and add the test classes
test_suite = unittest.TestSuite()
test_suite.addTest(unittest.makeSuite(TestGetAllResourceUsecase))
# Create a test runner
runner = unittest.TextTestRunner()

# Run the tests
runner.run(test_suite)


