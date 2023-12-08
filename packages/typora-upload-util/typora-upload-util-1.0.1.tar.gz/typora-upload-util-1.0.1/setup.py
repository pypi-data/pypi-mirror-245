from setuptools import setup, find_packages

setup(
    name             = 'typora-upload-util',
    version          = '1.0.1',
    description      = 'Uploader Plugins for Typora',
    author           = 'Revi1337',
    author_email     = 'david122123@gmail.com',
    url              = '',
    download_url     = '',
    install_requires = ['requests'],
	include_package_data=True,
	packages=find_packages(),
    keywords         = ['TYPORA UPLOADER', 'typora uploader'],
    python_requires  = '>=3',
    zip_safe=False,
    classifiers      = [
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows"
    ]
)
