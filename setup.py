import re
from os import path
from codecs import open  # To use a consistent encoding

from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


# Get version without importing, which avoids dependency issues
def get_version():
    with open('file_healthchecker/__init__.py') as version_file:
        return re.search(r"""__version__\s+=\s+(['"])(?P<version>.+?)\1""",
                         version_file.read()).group('version')


REQUIRES_PYTHON = ">=3.6.0"
TEST_REQUIRES = [
    "pytest==5.2.1",
    "pytest-sugar==0.9.2",
    "pytest-asyncio==0.10.0",
    "pytest-cov==2.8.1",
]

EXTRAS_REQUIRE = {
    "dev": ["python-language-server[all]", "black==19.3b0"],
    "test": TEST_REQUIRES,
}

setup(
    name='file-healthchecker',
    description="Check health of static, long running applications using generated files.",
    long_description=long_description,
    py_modules=['file_healthchecker*'],
    long_description_content_type="text/markdown",
    version=get_version(),
    python_requires=REQUIRES_PYTHON,
    extras_require=EXTRAS_REQUIRE,
    include_package_data=True,
    tests_require=TEST_REQUIRES,
    packages=find_packages(),
    zip_safe=False,
    entry_points={
        "console_scripts": [
            "checkhealth=file_healthchecker.entrypoint:health_check"
        ],
    },
    author="Ankur Srivastava",
    author_email="ankur.srivastava@email.de",
    download_url="https://github.com/ansrivas/healthchecker/{}.tar.gz".format(get_version()),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ]
)
