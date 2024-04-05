from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='passphera-core',
    version='0.1.0',
    author='Fathi Abdelmalek',
    author_email='abdelmalek.fathi.2001@gmail.com',
    url='',
    description='',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=['passphera_core'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 Only",
        "Topic :: Security",
        "Topic :: Security :: Cryptography",
    ]
)
