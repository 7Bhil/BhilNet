"""Setup script for BhilNet."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="bhilnet",
    version="1.0.0",
    author="BhilNet Team",
    author_email="bhilnet@example.com",
    description="A terminal-based messaging application for local network communication",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bhilnet/bhilnet",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Communications :: Chat",
        "Topic :: System :: Networking",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "bhilnet=main:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
