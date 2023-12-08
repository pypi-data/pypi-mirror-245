from setuptools import setup, find_packages

setup (
    name = "pyjeb",
    long_description_content_type="text/x-rst",
    long_description="A package to help on configuration file",
    version = "0.1",
    packages = find_packages(),
    install_requires = [
        "pyyaml==6.0.1"
    ]
)