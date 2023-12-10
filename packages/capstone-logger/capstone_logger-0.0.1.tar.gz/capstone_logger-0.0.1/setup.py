from setuptools import setup

setup(
    name="capstone_logger",
    version="0.0.1",
    author="Author",
    author_email="rootproxy@duck.com",
    description="Logger for Capstone",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/proxyserver2023/capstone_logger",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.12",
    install_requires=[
        "python-json-logger>=2.0.7",
        "python-logstash>=0.4.8",
    ],
)
