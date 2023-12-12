#  _____      _                         _      _____ _____   _____                       _ _   _
# /  ___|    | |                       | |    |_   _|_   _| /  __ \                     | | | (_)
# \ `--.  ___| |__  _ __ ___   ___  ___| | __   | |   | |   | /  \/ ___  _ __  ___ _   _| | |_ _ _ __   __ _
#  `--. \/ __| '_ \| '__/ _ \ / _ \/ __| |/ /   | |   | |   | |    / _ \| '_ \/ __| | | | | __| | '_ \ / _` |
# /\__/ / (__| | | | | | (_) |  __/ (__|   <   _| |_  | |   | \__/\ (_) | | | \__ \ |_| | | |_| | | | | (_| |
# \____/ \___|_| |_|_|  \___/ \___|\___|_|\_\  \___/  \_/    \____/\___/|_| |_|___/\__,_|_|\__|_|_| |_|\__, |
#                                                                                                       __/ |
#                                                                                                      |___/


import io
import os
from version import version
from setuptools import find_packages, setup

requirements = open("requirements.txt").read().split("\n")



setup(
    name="fastapi_oauth_client",
    version=version,
    description="FastAPI Authorization Framework",
    long_description=io.open("README.md", encoding="utf8").read()+ "\n",
    long_description_content_type='text/markdown',
    #+ io.open(os.path.join("docs", "source", "HISTORY.rst"), encoding="utf8").read(),
    # Get more strings from
    # http://www.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    author="Schroeck IT-Consulting GbR",
    author_email="hello@schroeck-consulting.de",
    url="http://pypi.python.org/projects/xxxx",
    license="GPL",
    packages=find_packages(exclude=["ez_setup"]),
    include_package_data=True,
    zip_safe=False,
    tests_require=["pytest"],
    test_suite="tests",
    entry_points={
    },
    install_requires=requirements,
)
