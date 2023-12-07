from setuptools import setup, find_packages

with open("README.md") as f:
    readme = f.read()

setup(
    name="fslog",
    version="0.1.3",
    author="Federico Sossai",
    author_email="federico.sossai@gmail.com",
    url="http://github.com/fsossai/fslog",
    description="Customizable log formatter that supports recursive log sections",
    long_description=readme,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[]
)

