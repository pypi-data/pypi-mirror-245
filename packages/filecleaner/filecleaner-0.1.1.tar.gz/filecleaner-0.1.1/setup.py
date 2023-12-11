from setuptools import setup

with open("requirements.txt", "r") as r:
    install_requires = r.readlines()

with open("README.md", "r") as readme:
    long_description = readme.read()

setup(
    name="filecleaner",
    version="0.1.1",
    description="A simple command line utility that organises files in a directory into subdirectories.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Tim Nwungang",
    author_email="timnw.dev@gmail.com",
    url="https://github.com/timnw2000/File-Manager",
    requires=["setuptools"],
    install_requires=install_requires,
    license="MIT",
    maintainer_email="timnw.dev@gmail.com",
    project_urls={
        "Documentation": "https://github.com/timnw2000/File-Manager/blob/creating_gui/README.md",
    },
    entry_points={
        "console_scripts": [
            "cleanup = file_manager:main"
        ]
    }
)