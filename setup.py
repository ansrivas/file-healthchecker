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
    with open('app/__init__.py') as version_file:
        return re.search(r"""__version__\s+=\s+(['"])(?P<version>.+?)\1""",
                         version_file.read()).group('version')


test_requires = ['pytest', 'pytest-sugar', 'pytest-asyncio', 'pytest-cov', ]
REQUIRES_PYTHON = ">=3.6.0"

setup(
    name='healthcheck',
    description="Check health of static, long running applications",
    long_description=long_description,
    py_modules=['app'],
    long_description_content_type="text/markdown",
    version=get_version(),
    python_requires=REQUIRES_PYTHON,
    include_package_data=True,
    tests_require=test_requires,
    packages=find_packages(),
    zip_safe=False,
    entry_points={
        "console_scripts": [
            "healthcheck.py=app.cmd.entrypoint:health_check"
        ],
    },
    author="Ankur Srivastava",
    author_email="ankur.srivastava@email.de",
    download_url="github.com/ansrivas/healthcheck/{}.tar.gz".format(get_version()),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ]
)
