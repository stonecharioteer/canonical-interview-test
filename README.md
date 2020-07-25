# Canonical Interview Question: Debian Package Statistics

## Instructions

Debian uses *deb packages to deploy and upgrade software. The packages
are stored in repositories and each repository contains the so called "Contents
index". The format of that file is well described here
https://wiki.debian.org/RepositoryFormat#A.22Contents.22_indices

Your task is to develop a python command line tool that takes the
architecture (amd64, arm64, mips etc.) as an argument and downloads the
compressed Contents file associated with it from a Debian mirror. The
program should parse the file and output the statistics of the top 10
packages that have the most files associated with them.
An example output could be:

./package_statistics.py amd64

1. <package name 1>         <number of files>
2. <package name 2>         <number of files>
......
10. <package name 10>         <number of files>

You can use the following Debian mirror
http://ftp.uk.debian.org/debian/dists/stable/main/. Please do try to
follow Python's best practices in your solution. Hint: there are tools
that can help you verify your code is compliant. In-line comments are
appreciated.

It will be good if the code is accompanied by a 1-page report of the
work that you have done including the time you actually spent working on it.

Once started, please return your work in approximately 24 hours.

Note: the focus is not to write the perfect Python code, but to see how
you'll approach the problem and how you organize your work.

## Application Installation

`packstats` can be both run as a standalone command using the `packstats.py` file,
or, after installing this package using `python setup.py install`, it can be used
with the `packstats` command.

Of course, if you'd like to use the standalone file, ensure you allow execution permissions.

## Assumptions

Ubuntu currently ships Python3, so I will use it. Python 2 suppport is possible, but out of the scope of this solution.

I am not using any 3rd party applications for the core application. The performance could be improved using other packages, or other versions of Python.


## `packstats` CLI

The command line interface has a help command that teaches you what you can do with the tool.

```
packstats --help
usage: packstats.py [-h] [-m MIRROR_URL] [-u] [-c COUNT] [-d] arch

A tool to get the package statistics by parsing a Contents index (defined here
- https://wiki.debian.org/RepositoryFormat#A.22Contents.22_indices)from a
debian mirror, given a system architecture.

positional arguments:
  arch                  the architecture of the Contents index you would like
                        to parse.

optional arguments:
  -h, --help            show this help message and exit
  -m MIRROR_URL, --mirror_url MIRROR_URL
                        Mirror URL from which to fetch the contents file.
                        DEFAULT
                        http://ftp.uk.debian.org/debian/dists/stable/main/
  -u, --include-udeb    include udeb file for the given architecture. DEFAULT
                        False
  -c COUNT, --count COUNT
                        number of packages to list.
  -d, --sort-increasing
                        Sort package stats list by increasing number of files.
                        DEFAULT False
```
