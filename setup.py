from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name='passphera-core',
    version='0.34.0',
    author='Fathi Abdelmalek',
    author_email='passphera@imfathi.com',
    url='https://github.com/passphera/core',
    description='The core of passphera project',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    python_requires='>=3',
    install_requires=['cipherspy'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: Security",
        "Topic :: Security :: Cryptography",
    ]
)
