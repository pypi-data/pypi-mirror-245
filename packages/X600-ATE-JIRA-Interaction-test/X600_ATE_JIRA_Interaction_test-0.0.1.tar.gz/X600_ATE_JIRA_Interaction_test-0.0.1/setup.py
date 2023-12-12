from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = 'Allow interaction between ATE and JIRA'
LONG_DESCRIPTION = 'Allow the ATE to automatically create JIRA tickets'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="X600_ATE_JIRA_Interaction_test", 
        version=VERSION,
        author="Houssem Eddine Amor",
        author_email="<youremail@email.com>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python', 'first package'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)