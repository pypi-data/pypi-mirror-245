import pathlib
from setuptools import setup, find_packages
here = pathlib.Path(__file__).parent.resolve()

long_description = (here / "README.md").read_text(encoding="utf-8")
setup(
    name='sample_test_package',
    version='0.7.0',
    author='Suraj Patidar',
    author_email='suraj.pysquad@gmail.com',
    description="Django Waffle Project",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[line.strip() for line in open("requirements.txt")],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Environment :: Web Environment",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3 :: Only",
        "Framework :: Django",
        "Framework :: Django :: 3.0",
        "Framework :: Django :: 3.1",
        "Framework :: Django :: 3.2",
        "Framework :: Django :: 4.0",
        "Framework :: Django :: 4.1",
        "Framework :: Django :: 4.2",
    ],
    keywords="django, waffle, feature flags, development",
    # packages=find_packages(exclude=("example")),
    python_requires=">=3.5",
    project_urls={
        "Bug Reports": "https://github.com/SurajPysquad/waffle-project/issues",
        "Source": "https://github.com/SurajPysquad/waffle-project",
    },
)
