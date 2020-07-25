import unittest


class TestPackTest(unittest.TestCase):
    """This test case tests the entirety of packstats"""

    def test_lists_architectures(self):
        """the application can list the architectures in the provided debian mirror"""
        from packstats.packstats import get_content_files_list

        result = get_content_files_list()
        
        self.assertTrue(result is not None, "The function returned a None value where a non-empty list was expected.")
        
        self.assertTrue(isinstance(result, list), "The function failed to return a list")
        
        self.assertTrue(len(result) > 0, "An empty list was returned. Either the code is broken, or the url has no Content Indices!")
        result_contains_dicts = all(isinstance(item, dict) for item in result)
        self.assertTrue(result_contains_dicts, "each item in the result should be a dictionary")
        result_contains_keys = all("filename" in item.keys() and "url" in item.keys() for item in result)
        self.assertTrue(result_contains_keys, "each item in the result should contain a filename and a url value")
        
    def test_downloads_content_file(self):
        """the application can download the right contents file given an architecture
        string"""

    def test_gets_package_data_from_contents(self):
        """the application can get the package data from a contents file"""

    def test_prints_top_ten_packages_given_arch(self):
        """The application can output the top ten packages given the architecture"""
