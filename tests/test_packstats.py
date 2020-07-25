import unittest
import tempfile
import pathlib

class TestPackTest(unittest.TestCase):
    """This test case tests the entirety of packstats"""
    def setUp(self) -> None:
        self.architecture = "amd64"

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


    def test_get_content_index_file_url(self):
        """the application can get the content index file url given the architecture and whether or not udeb files are needed"""
        from packstats.packstats import get_contents_file_urls

        urls = get_contents_file_urls(arch=self.architecture)
        self.assertIsInstance(urls, list, "output of the function was expected to be a list of urls")
        self.assertEqual(len(urls), 1, "only one url is expected when udeb isn't requested")
        self.assertTrue(urls[0].endswith(f"{self.architecture}.gz"), "output url should end with the `architecture`.gz")
        self.assertFalse("udeb" in urls[0], "url should not contain the udeb link when it is not requested")
        urls = get_contents_file_urls(arch=self.architecture, include_udeb=True)
        self.assertIsInstance(urls, list, "when the udeb is requested, the output is a list")
        found_udeb = False
        for url in urls:
            self.assertTrue(url.endswith(f"{self.architecture}.gz"), "url should end with `architecture`.gz")
            if not found_udeb:
                found_udeb = url.endswith(f"udeb-{self.architecture}.gz")
        self.assertTrue(found_udeb, "the udeb file url was not returned.")

    def test_downloads_content_file(self):
        """the application can download the right contents file given an architecture
        string"""
        from packstats.packstats import download_contents_file

        with tempfile.TemporaryDirectory() as temp_directory:
            download_contents_file(arch=self.architecture, output_dir=temp_directory)
            expected_file = pathlib.Path(temp_directory) / f"Contents-{self.architecture}"
            self.assertTrue(expected_file.exists())
            self.assertTrue(expected_file.is_file())


    def test_gets_package_data_from_contents(self):
        """the application can get the package data from a contents file"""

    def test_prints_top_ten_packages_given_arch(self):
        """The application can output the top ten packages given the architecture"""
