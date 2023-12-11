from setuptools import setup, find_packages

VERSION = '0.0.2' 
DESCRIPTION = 'SMS.to API wrapper'
LONG_DESCRIPTION = 'Manage SMS.to api via Python 3 easily'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="smsto", 
        version=VERSION,
        author="Evgeniy Finskiy",
        author_email="finskiy.ru@yandex.ru",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=['pydantic', 'requests'],
        url='https://github.com/BeyondUnderstanding/smsto_sdk' ,
        
        keywords=['python3', 'smsto', 'sms', 'api'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Developers",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.11",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
            "Operating System :: Unix",
            "Topic :: Communications",
            "Typing :: Typed"
        ]
)