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


## Assumptions

Ubuntu currently ships Python3, so I will use it. Python 2 suppport is possible, but out of the scope of this solution.

I am not using any 3rd party applications for the core application. The performance could be improved using other packages, or other versions of Python (perhaps PyPy).


### Regarding `udeb` content indices

I am treating the `udeb` files as additional sources, which can be included in the
report for an architecture by means of an `--include-udeb` flag.
Check the help output for more information.

## Application Installation

If you would like to install this application into your python3 environment, run the following:

```bash
python3 setup.py install
```

*Note that the installation is not necessary to run this application*.

## Usage

### With Installation

Once `packstats` is installed, you can run it in one of two ways.

```packstats --help```

Or:

```python -m packstats --help```

The second version is preferred in places where you would want to *ensure* the right version of python is being used, perhaps with a virtal environment.

### Without Installation

If you want to run `packstats` without installation, use the helper file instead.

Either modify permissions to make it executable and use a version of python3 to run it:

```bash
chmod +x package_statistics.py
./package_statistics.py --help
```

Or, you can run it with the python command directly.

```bash
python3 package_statistics.py
```

## `packstats` CLI

The command line interface has a help command that teaches you what you can do with the tool.

```
$ python package_statistics.py --help
usage: package_statistics.py [-h] [-m MIRROR_URL] [-u] [-c COUNT] [-i]
                             [-o OUTPUT_DIR] [-r]
                             arch

A tool to get the package statistics by parsing a Contents Index (defined here
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
                        number of packages to list. Use -1 to list all.
                        DEFAULT 10
  -i, --sort-increasing
                        Sort package stats list by increasing number of files.
                        DEFAULT False
  -o OUTPUT_DIR, --output-dir OUTPUT_DIR
                        a directory in which to store the downloaded contents
                        indices. DEFAULT <current-directory>
  -r, --reuse-if-exists
                        Reuses a content file if it has been downloaded
                        previously and exists in the output directory.
```


## Examples

### Getting `armel` Statistics

```
$ packstats armel

No.	Package Name                                      	File Count
1.	fonts/fonts-cns11643-pixmaps                      	110999
2.	x11/papirus-icon-theme                            	69475
3.	fonts/texlive-fonts-extra                         	65577
4.	games/flightgear-data-base                        	62463
5.	devel/piglit                                      	49913
6.	doc/trilinos-doc                                  	49591
7.	x11/obsidian-icon-theme                           	48829
8.	games/widelands-data                              	34984
9.	doc/libreoffice-dev-doc                           	33667
10.	misc/moka-icon-theme                              	33326
```

### Getting the top 25 packages

```bash
$ packstats -c 25 armel
No.	Package Name                                      	File Count
1.	fonts/fonts-cns11643-pixmaps                      	110999
2.	x11/papirus-icon-theme                            	69475
3.	fonts/texlive-fonts-extra                         	65577
4.	games/flightgear-data-base                        	62463
5.	devel/piglit                                      	49913
6.	doc/trilinos-doc                                  	49591
7.	x11/obsidian-icon-theme                           	48829
8.	games/widelands-data                              	34984
9.	doc/libreoffice-dev-doc                           	33667
10.	misc/moka-icon-theme                              	33326
11.	x11/numix-icon-theme                              	31098
12.	gnome/faenza-icon-theme                           	29400
13.	doc/vtk6-doc                                      	29370
14.	doc/vtk7-doc                                      	28640
15.	science/esys-particle                             	27143
16.	x11/mate-icon-theme-faenza                        	26494
17.	science/gromacs-data                              	24491
18.	gnome/ukui-themes                                 	22123
19.	python/python3-azure                              	20785
20.	net/oca-core                                      	20780
21.	doc/lazarus-doc-2.0                               	20484
22.	fonts/jsmath-fonts                                	20129
23.	devel/rust-src                                    	19464
24.	doc/pike8.0-doc                                   	18487
25.	lisp/racket-common                                	18197
```

### Getting `amd64` packages, with `udeb` files included
```
$ packstats --include-udeb amd64

No.	Package Name                                      	File Count
1.	fonts/fonts-cns11643-pixmaps                      	110999
2.	x11/papirus-icon-theme                            	69475
3.	fonts/texlive-fonts-extra                         	65577
4.	games/flightgear-data-base                        	62463
5.	devel/piglit                                      	49913
6.	doc/trilinos-doc                                  	49591
7.	x11/obsidian-icon-theme                           	48829
8.	games/widelands-data                              	34984
9.	doc/libreoffice-dev-doc                           	33667
10.	misc/moka-icon-theme                              	33326
```

### Redirecting Downloaded Files to `/tmp`

```
$ packstats -o /tmp armel
No.	Package Name                                      	File Count
1.	fonts/fonts-cns11643-pixmaps                      	110999
2.	x11/papirus-icon-theme                            	69475
3.	fonts/texlive-fonts-extra                         	65577
4.	games/flightgear-data-base                        	62463
5.	devel/piglit                                      	49913
6.	doc/trilinos-doc                                  	49591
7.	x11/obsidian-icon-theme                           	48829
8.	games/widelands-data                              	34984
9.	doc/libreoffice-dev-doc                           	33667
10.	misc/moka-icon-theme                              	33326
```
This downloads all files in the given directory. In this case: `/tmp`.

### Reusing Downloaded Files

If you want to preserve your bandwidth while testing this tool, like I did while developing it, try the `-r` flag, which reuses the Contents Index files for the architecture, if it has already been downloaded into the directory.

```
$ packstats -r amd64
```

### Attempting to Get Stats for an Incorrect Arch
If a user attempts to get the statistics for an architecture that does not exist,
they will see the following error.

```
$ packstats intel
Traceback (most recent call last):
  File "/home/stonecharioteer/code/tools/anaconda3/envs/py36/lib/python3.6/runpy.py", line 193, in _run_module_as_main
    "__main__", mod_spec)
  File "/home/stonecharioteer/code/tools/anaconda3/envs/py36/lib/python3.6/runpy.py", line 85, in _run_code
    exec(code, run_globals)
  File "/home/stonecharioteer/code/interview/canonical/packstats/__main__.py", line 5, in <module>
    cli_main()
  File "/home/stonecharioteer/code/interview/canonical/packstats/packstats.py", line 218, in cli_main
    reuse_if_exists=args.reuse_if_exists,
  File "/home/stonecharioteer/code/interview/canonical/packstats/packstats.py", line 146, in main
    f"{arch} was not found in the given mirror. Available architectures are: {found_architectures}")
packstats.exceptions.ContentIndexForArchitectureNotFound: intel was not found in the given mirror. Available architectures are: amd64, arm64, armel, armhf, i386, mips, mips64el, mipsel, ppc64el, s390x, source
```


## Testing

The core functions of `packstats` have tests.

```
$ python setup.py test
running test
running egg_info
writing canonical_vinay_packstats.egg-info/PKG-INFO
writing dependency_links to canonical_vinay_packstats.egg-info/dependency_links.txt
writing top-level names to canonical_vinay_packstats.egg-info/top_level.txt
reading manifest file 'canonical_vinay_packstats.egg-info/SOURCES.txt'
writing manifest file 'canonical_vinay_packstats.egg-info/SOURCES.txt'
running build_ext
test_downloads_content_file (tests.test_packstats.TestPackStats)
the application can download the right contents file given an architecture ... ok
test_get_content_index_file_url (tests.test_packstats.TestPackStats)
the application can get the content index file url given the architecture and whether or not udeb files are needed ... ok
test_get_content_index_file_url_with_udeb (tests.test_packstats.TestPackStats)
the application can get the content index file url for both the base arch ... ok
test_gets_package_data_from_contents (tests.test_packstats.TestPackStats)
the application can get the package data from a contents file ... ok
test_lists_architectures (tests.test_packstats.TestPackStats)
the application can list the architectures in the provided debian mirror ... ok

----------------------------------------------------------------------
Ran 5 tests in 35.787s

OK
```

The tests can also be run with `pytest`, should you choose to install it.


## Profiling with `py-spy`

`py-spy` offers a great report for the profiling. Note that `py-spy` needs to be installed separately using `pip`.

```
$ py-spy top -- python package_statistics.py amd64

Collecting samples from 'python package_statistics.py amd64' (python v3.6.10)
Total Samples 2600
GIL: 100.00%, Active: 100.00%, Threads: 1

  %Own   %Total  OwnTime  TotalTime  Function (filename:line)
 53.00%  53.00%    5.30s     5.30s   parse_contents_index (packstats/packstats.py:111)
  0.00%   0.00%    2.10s     2.10s   decode (codecs.py:321)
  0.00%   0.00%    1.89s     3.99s   parse_contents_index (packstats/packstats.py:101)
 14.00%  14.00%    1.80s     1.80s   parse_contents_index (packstats/packstats.py:114)
 13.00%  13.00%    1.49s     1.49s   parse_contents_index (packstats/packstats.py:112)
  0.00%   0.00%    1.45s     1.45s   read (gzip.py:471)
  0.00%   0.00%    1.17s     1.17s   parse_contents_index (packstats/packstats.py:103)
  7.00%   7.00%   0.680s    0.680s   parse_contents_index (packstats/packstats.py:118)
  5.00%   5.00%   0.630s    0.630s   parse_contents_index (packstats/packstats.py:106)
  0.00%   0.00%   0.590s    0.590s   _add_read_data (gzip.py:490)
  0.00%   0.00%   0.500s    0.500s   readinto (socket.py:586)
  0.00%   0.00%   0.400s     2.71s   read (gzip.py:276)
  4.00%   4.00%   0.320s    0.320s   parse_contents_index (packstats/packstats.py:113)
  0.00%   0.00%   0.320s    0.320s   parse_contents_index (packstats/packstats.py:116)
  3.00%   3.00%   0.260s    0.260s   parse_contents_index (packstats/packstats.py:110)
  1.00%   1.00%   0.230s    0.230s   parse_contents_index (packstats/packstats.py:105)
  0.00%   0.00%   0.100s    0.100s   read (gzip.py:91)
  0.00%   0.00%   0.060s    0.060s   download_contents_file (packstats/packstats.py:93)
  0.00%   0.00%   0.050s    0.060s   parse_contents_index (packstats/packstats.py:100)
  0.00%   0.00%   0.040s     3.48s   main (packstats/packstats.py:153)
  0.00%   0.00%   0.040s    0.040s   read (gzip.py:472)
  0.00%   0.00%   0.030s    0.030s   readinto (socket.py:580)
  0.00%   0.00%   0.030s    0.030s   create_connection (socket.py:713)
  0.00%   0.00%   0.030s    0.030s   read (gzip.py:83)
  0.00%   0.00%   0.020s    0.020s   __setitem__ (enum.py:90)
  0.00%   0.00%   0.020s    0.020s   download_contents_file (packstats/packstats.py:92)
  0.00%   0.00%   0.020s    0.020s   read (gzip.py:90)
  0.00%   0.00%   0.020s    0.030s   __instancecheck__ (abc.py:184)
  0.00%   0.00%   0.020s    0.610s   read (gzip.py:485)
  0.00%   0.00%   0.020s    0.020s   __instancecheck__ (abc.py:189)
  0.00%   0.00%   0.010s    0.010s   prepend (gzip.py:94)
  0.00%   0.00%   0.010s     2.72s   download_contents_file (packstats/packstats.py:91)
  0.00%   0.00%   0.010s    0.530s   _safe_read (http/client.py:622)
  0.00%   0.00%   0.010s    0.010s   download_contents_file (packstats/packstats.py:87)
  0.00%   0.00%   0.010s    0.010s   read (gzip.py:486)
  0.00%   0.00%   0.010s    0.060s   open (gzip.py:52)
  0.00%   0.00%   0.010s    0.010s   read (gzip.py:88)
  0.00%   0.00%   0.010s    0.010s   _compile (re.py:289)
  0.00%   0.00%   0.010s    0.010s   prepend (gzip.py:95)
  0.00%   0.00%   0.010s    0.010s   _is_descriptor (enum.py:25)
  0.00%   0.00%   0.010s    0.010s   open (gzip.py:51)
  0.00%   0.00%   0.010s    0.060s   _call_with_frames_removed (<frozen importlib._bootstrap>:219)

Press Control-C to quit, or ? for help.

process 85674 ended
```

The maximum time was spent within the `parse_contents_index` function, which can be optimized by using third-party packages such as `numba` or a different version of Python such as `PyPy`.

These performance metrics are from a desktop workstation with the following specs:

* CPU: Intel i5-2310 (4) @ 3.200GHz
* GPU: NVIDIA GeForce GTX 1060 3GB
* RAM: 15965MiB
