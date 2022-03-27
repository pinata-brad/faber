import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="faber-ml", 
    version="0.0.6",
    author="Bradley Nobbs",
    author_email="bradleynobbs@gmail.com",
    description="Quick start ml experimentation pipelines",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    entry_points ={
        'console_scripts': [
            'faber = faber.cli:main'
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    include_package_data = True
)
