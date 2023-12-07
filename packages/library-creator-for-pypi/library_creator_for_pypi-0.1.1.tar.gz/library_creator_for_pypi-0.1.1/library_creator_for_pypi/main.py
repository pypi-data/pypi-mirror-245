import os

r"""
Script Description:

This script creates a new folder, copies the contents of a specified file into a 'main.py' file in the new folder,
creates an '__init__.py' file with an import statement, and generates a 'setup.py' file for packaging.

Usage:
- Run the script and provide the necessary parameters:
  - path: The path where the new folder will be created.
  - folder_name: The name of the new folder.
  - code_path: The path to the file whose contents will be copied.
  - name: The name of the package.
  - install_requires: A list of dependencies for the package.
  - version: The version number of the package.
  create(r"C:\Users\1\Desktop", "m_Folder", "./py.py", "my_name", [], "0.0.1")
"""


def create_folder(path, folder_name) -> str:
    full_path = os.path.join(path, folder_name)
    os.makedirs(full_path)
    return full_path


def create_s(name: str, install_requires: list, version: str):
    into = f"""
from setuptools import setup, find_packages

setup(
    name='{name}',
    version='{version}',
    packages=find_packages(),
    install_requires={str(install_requires)}
)
    """
    return into


def create(path, folder_name, code_path, name, install_requires: list, version):

    full_path1: str = create_folder(path, folder_name)
    full_path2: str = create_folder(os.path.join(path, folder_name), folder_name)

    with open(code_path, "r") as f1:
        main = f1.read()

    with open(os.path.join(full_path2, "main.py"), "w") as f:
        f.write(main)

    with open(os.path.join(full_path2, "__init__.py"), "w") as f:
        f.write(f"from .main import *")

    with open(os.path.join(full_path1, "setup.py"), "w") as f:
        f.write(create_s(name, install_requires, version))
