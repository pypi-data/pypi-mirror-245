from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read() 

INSTALL_REQUIRES = []

def doSetup(install_requires):
    setup(
        name='crispr_array_generator',
        version='0.1',
        author='Willow Chernoske',
        author_email='wachern@uw.edu',
        url='https://github.com/wachern/crispr_array_generator',
        description='A tool to automate the design of CRISPR Cas12 arrays',
        long_description=long_description,
        long_description_content_type='text/markdown',
        packages=['crispr_array_generator'],
        package_dir={'crispr_array_generator':
            'crispr_array_generator'},
        install_requires = install_requires,
        include_package_data=True,
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Intended Audience :: Science/Research',
            'Topic :: Scientific/Engineering',
            'License :: OSI Approved :: MIT License', 
            'Programming Language :: Python :: 3.9',
            'Programming Language :: Python :: 3.10',
            'Programming Language :: Python :: 3.11',
        ],
    )

if __name__ == '__main__':
  doSetup(INSTALL_REQUIRES)