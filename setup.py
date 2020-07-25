
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="canonical-vinay-packstats", # Replace with your own username
    version="1.0",
    author="Vinay Keerthi",
    author_email="ktvkvinaykeerthi+canonical@gmail.com",
    description="A CLI tool to get the package statistics from a debian mirror, for a given arch.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    entry_points={
    'console_scripts': [
        'packstats=packstats.packstats:cli_main',
    ],
},
)
