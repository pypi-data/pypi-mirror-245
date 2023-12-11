from setuptools import find_packages, setup

from wavecount_cli import PACKAGE_NAME, VERSION

with open("README.md", "r") as fh:
    long_description = fh.read()

DEPENDENCIES = [
    "requests",
    "click",
    "halo",
    "pyfiglet",
    "inquirer",
    "pydash",
]

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description="Wavecount cli",
    author="Navid Ahrary",
    author_email="N.Ahrary@domil.io",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="ISC",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Environment :: Console",
        "License :: OSI Approved :: ISC License (ISCL)",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(exclude=["test*", ".vscode"]),
    install_requires=DEPENDENCIES,
    python_requires=">=3.11",
    entry_points="""
        [console_scripts]
        wave=wavecount_cli.wave:main
    """,
)
