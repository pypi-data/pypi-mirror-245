import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="genome_automl", # Replace with your own username
    version="0.9.32",
    license='MIT',
    author="Endr Del",
    description="library for building extreme scale, millions of models and intelligent agent pipelines, and evaluations, on AWS, Google Cloud",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/edeliu2000/genome",
    package_dir={"": "./"},
    packages=setuptools.find_packages(exclude=["test.*", "test"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
