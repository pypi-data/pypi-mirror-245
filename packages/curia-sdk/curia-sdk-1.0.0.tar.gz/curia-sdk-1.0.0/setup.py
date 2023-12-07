import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="curia-sdk",
    version="1.0.0",
    author="Nick Bucheleres",
    author_email="nick@curia.us",
    description="Curia Python SDK",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Curia-co/curia-sdk",
    project_urls={
        "Bug Tracker": "https://github.com/Curia-co/curia-sdk",
        "Documentation": "https://docs.curia.co"
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=['curia-sdk'],
    install_requires=['requests'],
    python_requires=">=3.11")