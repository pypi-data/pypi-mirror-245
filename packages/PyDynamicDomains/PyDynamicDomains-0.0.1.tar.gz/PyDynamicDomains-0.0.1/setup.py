from setuptools import setup

with open("README.md", "r") as fh:
    long_desc = fh.read()

setup(
    name='PyDynamicDomains',
    version="0.0.1",
    packages=["pydynamicdomains"],
    package_dir={'': "src"},
    scripts=['scripts/pydynamicdomains'],
    author="Impostor",
    author_email="drpresq@gmail.com",
    description="PyDynamicDomains - A Dynamic Domain Name System Record Updater for Google Domains",
    long_description=long_desc,
    long_description_content_type="text/markdown",
    url="https://github.com/drpresq/pydynamicdomains",
    install_requires=[
        'requests>=2.31.0'
    ],
    extras_require={
            'dev': [
                'pytest>=7.3.0'
            ]
    },
    keywords="",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: End Users/Desktop',
        'License :: Other/Proprietary License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)
