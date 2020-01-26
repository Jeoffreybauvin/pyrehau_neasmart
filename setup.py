import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyrehau_neasmart", # Replace with your own username
    version="0.0.4",
    author="Jeoffrey BAUVIN",
    author_email="jeoffrey.bauvin@gmail.com",
    description="A python package to interact with Rehaut Nea Smart interface",
    long_description="A python package to interact with Rehaut Nea Smart interface",
    long_description_content_type="text/markdown",
    url="https://github.com/Jeoffreybauvin/pyrehau_neasmart",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
          'requests',
      ],
    python_requires='>=3.6',
)
