import setuptools
#a  comment
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tagnet", # Replace with your own username
    version="0.0.1",
    author="John Torr",
    author_email="john@cantab.net",
    description="A neural network supertagger",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/xxxxx/xxxxx",#COMPLETE THIS!!!!!!!!!
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)