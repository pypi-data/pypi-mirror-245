from setuptools import setup, find_packages
import pathlib

setup(
    name='libr',
    version='0.0.0',
    description='libr',
    long_description=pathlib.Path('README.md').read_text(),
    long_description_content_type='text/markdown',
    url='https://github.com/',
    author='libr',
    license='MIT',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='libr',
    packages=find_packages(),
    install_requires=[]
)