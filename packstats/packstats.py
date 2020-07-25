#!/usr/bin/env python3
"""Debian Package Statistics CLI Tool"""

import argparse
import gzip
import os
import urllib.request
import pathlib


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
    # TODO: change and get the href instead using xmltree
    for line in html.split("\r\n"):
        if line.startswith("<a href=\"Contents-"):
            filename = line[line.find("Contents-"):line.find(".gz")+3]
            url = f"{mirror_url}{filename}" if mirror_url.endswith("/") else f"{mirror_url}/{filename}"
            arch = filename[filename.find("-"):filename.rfind(".gz")-1]
            content_types.append(dict(filename=filename, url=url))
    return content_types


def get_contents_file_urls(arch, mirror_url=None, include_udeb=False) -> list:
    """Gets the URL(s) of the debian content index file for the given architecture"""
    if mirror_url is not None:
        contents_file_list = get_content_files_list(mirror_url)
    else:
        contents_file_list = get_content_files_list()
    # filter for the content file that was requested.
    urls = []
    for file in contents_file_list:
        url = file["url"]
        filename = file["filename"]
        file_arch = filename[filename.rfind("-")+1:filename.rfind(".gz")]
        is_udeb = filename.endswith(f"udeb-{file_arch}.gz")
        if arch == file_arch:
            if is_udeb:
                if include_udeb:
                    urls.append(url)
            else:
                urls.append(url)
    return urls


def download_contents_file(content_file_url, output_dir=None, overwrite=True) -> str:
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
        if not overwrite:
            # TODO: implement a form of check where the filesize becomes a parameter of
            # interest.
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



def main(mirror_url, arch, count, include_udeb, sort_increasing):

    # get one of these.
    required = "amd64"
    get_udeb = False

    required_content_files = []
    for content_file in content_types:
        content_file_arch_matches = content_file.endswith(f"{required}.gz")
        is_udeb = content_file.endswith(f"udeb-{required}.gz")
        if is_udeb and get_udeb:
            required_content_files.append(content_file)
        elif content_file_arch_matches and not is_udeb:
            required_content_files.append(content_file)

    for file in required_content_files:
        if not os.path.isfile(file):
            with urllib.request.urlopen(f"{mirror_url}{file}") as response:
                data = response.read()
                with open(file, "wb") as f:
                    f.write(data)
                print(file)

    file_data_dict = {}
    for file in required_content_files:
        # unzip them
        with gzip.open(file, "rb") as f:
            data = f.read()
            data = data.decode()
            file_data_dict[file] = {}
            for ix, row in enumerate(data.split("\n")):
                if row.strip() == "":
                    continue
                file_name, packages = row[:row.rfind(
                    " ")].strip(), row[row.rfind(" "):].strip()
                packages = packages.split(",")
                for package in packages:
                    if file_data_dict[file].get(package) is None:
                        file_data_dict[file][package] = [file_name]
                    else:
                        file_data_dict[file][package].append(file_name)


def cli_main():
    """Command line interface function"""
    parser = argparse.ArgumentParser(
        description=(
            "A tool to get the package statistics by parsing "
            "a Contents index (defined here - https://wiki.debian.org/RepositoryFormat#A.22Contents.22_indices)"
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
    parser.add_argument("-c", "--count", type=int, default=10,
                        help="number of packages to list. DEFAULT 10")
    parser.add_argument(
        "-d", "--sort-increasing", action="store_true",
        help="Sort package stats list by increasing number of files. DEFAULT False")
    args = parser.parse_args()
    main(
        mirror=args.mirror_url,
        arch=args.arch,
        include_udeb=args.include_udeb,
        sort_increasing=args.sort_increasing,
        count=args.count,
    )


if __name__ == "__main__":
    cli_main()
