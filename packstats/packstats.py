#!/usr/bin/env python3
"""Debian Package Statistics CLI Tool"""

import argparse
import gzip
import os
import urllib.request
import pathlib
from collections import defaultdict

from packstats.exceptions import ContentIndexForArchitectureNotFound


def get_content_files_list(mirror_url: str = "http://ftp.uk.debian.org/debian/dists/stable/main/") -> list:
    """Returns a list of content files as defined
    by Debian docs here
    Args:
        mirror_url

    Returns:
        list: A list of dictionaries with the following structure
            [{
                "filename": "Contents-amd64.gz",
                "url": ""http://ftp.uk.debian.org/debian/dists/stable/main/Contents-amd64.gz"
            }]
    """
    with urllib.request.urlopen(mirror_url) as response:
        raw_html = response.read()
    html = raw_html.decode()

    content_types = []
    for line in html.split("\r\n"):
        if line.startswith("<a href=\"Contents-"):
            filename = line[line.find("Contents-"):line.find(".gz")+3]
            url = f"{mirror_url}{filename}" if mirror_url.endswith(
                "/") else f"{mirror_url}/{filename}"
            arch = filename[filename.rfind("-")+1:filename.rfind(".gz")]
            content_types.append(dict(filename=filename, url=url, arch=arch))
    return content_types


def get_contents_file_urls(arch, mirror_url=None, include_udeb=False) -> list:
    """Gets the URL(s) of the debian content index file for the given architecture
    If the architecture is None it returns all the content indices.
    """
    if mirror_url is not None:
        contents_file_list = get_content_files_list(mirror_url)
    else:
        contents_file_list = get_content_files_list()
    # filter for the content file that was requested.
    urls = []
    for file in contents_file_list:
        url = file["url"]
        filename = file["filename"]
        file_arch = file["arch"]
        is_udeb = filename.endswith(f"udeb-{file_arch}.gz")
        if (arch == file_arch):
            if is_udeb:
                if include_udeb:
                    urls.append(url)
            else:
                urls.append(url)
    return urls


def download_contents_file(content_file_url, output_dir=None, reuse_if_exists=False) -> str:
    """This function takes a Debian contents index and extracts the file to a given folder"""
    if output_dir is None:
        output_dir = os.getcwd()
    basename = os.path.basename(content_file_url)
    file_name = os.path.splitext(basename)[0]

    # gz file path
    output_gz_file = pathlib.Path(output_dir) / basename
    # extracted contents index file path
    output_file = pathlib.Path(output_dir) / file_name
    if output_file.exists():
        if reuse_if_exists:
            return output_file

    # download the file given the url
    with urllib.request.urlopen(content_file_url) as response:
        data = response.read()
    with open(output_gz_file, "wb") as buffer:
        buffer.write(data)

    # FIXME: use urllib.request.urlopen to do this.
    with gzip.open(output_gz_file, "rb") as buffer:
        data = buffer.read()
    with open(output_file, "wb") as buffer:
        buffer.write(data)

    return output_file


def parse_contents_index(contents_index_file):
    """Parses a given contents index file and returns a dictionary with the package names and their associated files"""
    with open(contents_index_file) as buffer:
        data = buffer.read()

    lines = data.split("\n")
    package_dict = defaultdict(list)
    for line in lines:
        if line.strip() == "":
            # skip empty lines
            continue
        else:
            file_name, packages = line[:line.rfind(
                " ")].strip(), line[line.rfind(" "):].strip()
            packages = packages.split(",")
            for package in packages:
                if file_name != "EMPTY_PACKAGE":
                    package_dict[package].append(file_name)
    return package_dict


def main(
        mirror_url, arch, count, include_udeb, sort_increasing,
        output_dir, reuse_if_exists):
    """This is the function that orchestrates the entirety of this application.

    1. It gets a list of all content indices from a mirror url
    2. It checks whether the provided arch is valid
    3. It filters the content indices for the requested architecture
    4. It downloads the content indices file(s)
    5. It parses the content indices files(s)
    6. It prints out the statistics"""
    arch = arch.lower()  # use lowercase for the architecture.
    # get a list of content index urls
    content_indices_urls = get_contents_file_urls(
        arch, mirror_url, include_udeb)

    if len(content_indices_urls) == 0:
        # if the architecture didn't retrieve anything, output an error,
        # with a list of architectures
        content_indices = get_content_files_list(mirror_url)
        found_architectures = [item["arch"] for item in content_indices]
        found_architectures = sorted(set(found_architectures))
        found_architectures = ", ".join(found_architectures)
        # raise a custom exception
        raise ContentIndexForArchitectureNotFound(
            f"{arch} was not found in the given mirror. Available architectures are: {found_architectures}")

    # prepare to summarize the data
    complete_package_data = {}
    for url in content_indices_urls:
        content_index_file = download_contents_file(
            url, output_dir=output_dir, reuse_if_exists=reuse_if_exists)
        print(content_index_file)
        package_data = parse_contents_index(content_index_file)
        complete_package_data.update(**package_data)

    package_list = complete_package_data.keys()
    # sort them in the ascending order of the number of packages
    package_list = sorted(
        package_list, key=lambda x: len(complete_package_data[x]))
    # reverse the sorting direction unless the user wants the ascending order
    if not sort_increasing:
        package_list = reversed(package_list)

    # print the output, only print how many ever the user asks through the count argument

    for ix, package in enumerate(package_list):
        if ix == 0:
            print(f"{'No.':<10}\t{'Package Name':<50}\tFile Count")
        print(f"{ix+1:<10}\t{package:<50}\t{len(complete_package_data[package])}")
        if ix+1 == count:
            break  # use this instead of slicing the reversed list because this way, the overhead of converting a giant iterator to a list is avoided. Some milliseconds may be saved.


def cli_main():
    """Command line interface function"""
    parser = argparse.ArgumentParser(
        description=(
            "A tool to get the package statistics by parsing "
            "a Contents Index (defined here - https://wiki.debian.org/RepositoryFormat#A.22Contents.22_indices)"
            "from a debian mirror, given a system architecture."
        )
    )
    parser.add_argument(
        "arch", type=str,
        help="the architecture of the Contents index you would like to parse.")
    parser.add_argument(
        "-m", "--mirror_url", type=str,
        default="http://ftp.uk.debian.org/debian/dists/stable/main/",
        help=(
            "Mirror URL from which to fetch the contents file. "
            "DEFAULT http://ftp.uk.debian.org/debian/dists/stable/main/")
    )
    parser.add_argument(
        "-u", "--include-udeb",
        help="include udeb file for the given architecture. DEFAULT False",
        action="store_true")
    parser.add_argument(
        "-c", "--count", type=int, default=10,
        help="number of packages to list. Use -1 to list all. DEFAULT 10")
    parser.add_argument(
        "-i", "--sort-increasing", action="store_true",
        help="Sort package stats list by increasing number of files. DEFAULT False")
    parser.add_argument(
        "-o", "--output-dir", type=str, default=os.getcwd(),
        help="a directory in which to store the downloaded contents indices. DEFAULT <current-directory>")
    parser.add_argument(
        "-r", "--reuse-if-exists", help="Reuses a content file if it has been downloaded previously and exists in the output directory.",
        action="store_true",
    )
    args = parser.parse_args()
    main(
        mirror_url=args.mirror_url,
        arch=args.arch,
        include_udeb=args.include_udeb,
        sort_increasing=args.sort_increasing,
        count=args.count,
        output_dir=args.output_dir,
        reuse_if_exists=args.reuse_if_exists,
    )
