import unittest
import tempfile
import pathlib


class TestPackStats(unittest.TestCase):
    """This test case tests the entirety of packstats"""

    def setUp(self) -> None:
        self.architecture = "armel"

    def test_lists_architectures(self):
        """the application can list the architectures in the provided debian mirror"""
        from packstats.packstats import get_content_files_list

        result = get_content_files_list()

        self.assertTrue(
            result is not None, "The function returned a None value where a non-empty list was expected.")

        self.assertTrue(isinstance(result, list),
                        "The function failed to return a list")

        self.assertTrue(len(
            result) > 0, "An empty list was returned. Either the code is broken, or the url has no Content Indices!")
        result_contains_dicts = all(isinstance(item, dict) for item in result)
        self.assertTrue(result_contains_dicts,
                        "each item in the result should be a dictionary")
        result_contains_keys = all("filename" in item.keys(
        ) and "url" in item.keys() for item in result)
        self.assertTrue(result_contains_keys,
                        "each item in the result should contain a filename and a url value")

    def test_get_content_index_file_url(self):
        """the application can get the content index file url given the architecture and whether or not udeb files are needed"""
        from packstats.packstats import get_contents_file_urls

        urls = get_contents_file_urls(arch=self.architecture)
        self.assertIsInstance(
            urls, list, "output of the function was expected to be a list of urls")
        self.assertEqual(
            len(urls), 1, "only one url is expected when udeb isn't requested")
        self.assertTrue(urls[0].endswith(
            f"{self.architecture}.gz"), "output url should end with the `architecture`.gz")
        self.assertFalse(
            "udeb" in urls[0], "url should not contain the udeb link when it is not requested")

    def test_get_content_index_file_url_with_udeb(self):
        """the application can get the content index file url for both the base arch
        contents file as well as the udeb file"""
        from packstats.packstats import get_contents_file_urls
        urls = get_contents_file_urls(
            arch=self.architecture, include_udeb=True)
        self.assertIsInstance(
            urls, list, "when the udeb is requested, the output is a list")
        found_udeb = False
        for url in urls:
            self.assertTrue(url.endswith(
                f"{self.architecture}.gz"), "url should end with `architecture`.gz")
            if not found_udeb:
                found_udeb = url.endswith(f"udeb-{self.architecture}.gz")
        self.assertTrue(found_udeb, "the udeb file url was not returned.")

    def test_downloads_content_file(self):
        """the application can download the right contents file given an architecture
        string"""
        from packstats.packstats import download_contents_file, get_contents_file_urls
        urls = get_contents_file_urls(self.architecture)

        with tempfile.TemporaryDirectory() as temp_directory:
            url = urls[0]
            download_contents_file(content_file_url=url,
                                   output_dir=temp_directory)
            expected_file = pathlib.Path(
                temp_directory) / f"Contents-{self.architecture}"
            self.assertTrue(expected_file.exists(
            ), "The requested contents index was not downloaded and unpacked")
            self.assertTrue(expected_file.is_file(
            ), "The requested contents index was not downloaded and unpacked to a file, it is a directory")

    def test_gets_package_data_from_contents(self):
        """the application can get the package data from a contents file

        Also checks that that when the udeb files are added, the package gets
        extended."""
        from packstats.packstats import get_contents_file_urls, download_contents_file, parse_contents_index
        urls = get_contents_file_urls(self.architecture, include_udeb=True)
        with tempfile.TemporaryDirectory() as temp_directory:
            # merge udeb and deb info, if required.
            complete_package_data = {}
            total_keys = 0
            for url in urls:
                contents_file = download_contents_file(url)
                package_dict = parse_contents_index(contents_file)
                self.assertIsInstance(
                    package_dict, dict, "Package metadata should be a dictionary")
                self.assertTrue(len(package_dict.keys()) > 0,
                                "Package list is not empty")
                complete_package_data.update(**package_dict)
                total_keys += len(package_dict)
            self.assertEqual(total_keys, len(complete_package_data),
                             "the two package files were not added together")
