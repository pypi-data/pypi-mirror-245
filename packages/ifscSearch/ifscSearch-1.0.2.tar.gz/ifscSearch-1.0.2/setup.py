from setuptools import setup, find_packages

setup(
    name='ifscSearch',
    version='1.0.2',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'ifsc-search=ifscSearch.ifsc_search:main',
        ],
    },
    author='Amey Pandit',
    description='A module to search IFSC codes.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/panditamey/ifscSearch',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
)
