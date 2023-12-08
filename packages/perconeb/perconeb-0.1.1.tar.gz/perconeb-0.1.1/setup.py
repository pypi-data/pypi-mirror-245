import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
     name='perconeb',  
     version='0.1.1',
     py_modules = ["perconeb"],
     install_requires = [
                         "ase",
                         "numpy",
                         'networkx',
			             'spglib',
                         'scipy'
                         ],
     author="Artem Dembitskiy",
     author_email="art.dembitskiy@gmail.com",
     description="A tool for finding percolation pathways in crystals",
     key_words = ['percolation', 'neb', 'migration'],
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/dembart/perconeb",
     package_data={"perconeb": ["*.txt", "*.rst", '*.md', "*"], 
     },
     classifiers=[
         "Programming Language :: Python :: 3.6",
         "Programming Language :: Python :: 3.7",
         "Programming Language :: Python :: 3.8",
         "Programming Language :: Python :: 3.9",
         "Programming Language :: Python :: 3.10",
         "Programming Language :: Python :: 3.11",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
    include_package_data=True,
    packages=setuptools.find_packages(),
 )





