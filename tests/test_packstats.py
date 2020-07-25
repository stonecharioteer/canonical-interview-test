import unittest


class TestPackTest(unittest.TestCase):
    """This test case tests the entirety of packstats"""

    def test_lists_architectures(self):
        """the application can list the architectures in the provided debian mirror"""
        
    def test_downloads_content_file(self):
        """the application can download the right contents file given an architecture
        string"""

    def test_gets_package_data_from_contents(self):
        """the application can get the package data from a contents file"""

    def test_prints_top_ten_packages_given_arch(self):
        """The application can output the top ten packages given the architecture"""
        