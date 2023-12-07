from setuptools import setup, find_packages

setup(
    name="pexels_async_api",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "aiohttp",
        "backoff",
    ],
    author="Cagin Polat",
    author_email="caginpolat@notrino.com",
    description="An Asynchronous Python Client for the Pexels API",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/darkcurrent/pexels_async_api",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
