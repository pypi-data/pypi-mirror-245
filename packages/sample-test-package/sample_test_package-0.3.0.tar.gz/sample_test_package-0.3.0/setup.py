from setuptools import setup, find_packages

setup(
    name='sample_test_package',
    version='0.3.0',
    author='Suraj Patidar',
    author_email='suraj.pysquad@gmail.com',
    description='this is a test package',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
