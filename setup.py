import setuptools
from os import path, sep

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, "README.rst"), encoding="utf-8") as f:
    readme = f.read()

with open("requirements.txt") as f:
    required = f.read().splitlines()

setup_requirements = ['setuptools_scm','pytest-runner', ]

test_requirements = ['pytest>=3', ]

about = {}
with open(
    path.join(here, "plugins/pds_plugin", "_version.py"),
    encoding="utf-8",
) as f:
    exec(f.read(), about)

setuptools.setup(
    use_scm_version=True,
    name=about["__name_soft__"],
    description=about["__description__"],
    long_description=readme,
    author=about["__author__"],
    author_email=about["__author_email__"],
    url=about["__url__"],
    license=about["__license__"],
    long_description_content_type="text/markdown",
    include_package_data=True,
    packages=setuptools.find_packages(),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=required,
)
