import os
import re

from setuptools import setup, find_packages

from custom_bgr import version


def read(filename: str):
    filepath = os.path.join(os.path.dirname(__file__), filename)
    file = open(filepath, "r", encoding="utf-8")
    return file.read()


def req_file(filename: str, folder: str = "."):
    with open(os.path.join(folder, filename), encoding="utf-8") as f:
        content = f.readlines()
    # you may also want to remove whitespace characters
    # Example: `\n` at the end of each line
    return [x.strip() for x in content]


setup(
    name="custom_bgr",
    version=version,
    author="Rishabh Dwivedi",
    author_email="dwivedi.rishabh95@gmail.com",
    description="Customized background removal app",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    keywords=[
        "unet background removal",
        "pretrained background removal",
        "background removal",
        "remove background",
        "deep learning app",
        "machine learning app",
    ],

    url="https://github.com/Rishabh20539011/Custom_BGR_APP",
    packages=find_packages(),
    scripts=[],
    install_requires=req_file("requirements.txt"),
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.10.4",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
)
