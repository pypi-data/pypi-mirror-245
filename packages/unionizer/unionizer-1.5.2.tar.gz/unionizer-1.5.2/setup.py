from setuptools import setup, find_packages
import pathlib

path_absolute: pathlib.Path = pathlib.Path(__file__).parent.absolute()

setup(
    name='unionizer',
    version='1.5.2',
    description='Unionizer helps developers pair objects together.',
    long_description=pathlib.Path(f"{path_absolute}/README.md").read_text(encoding="utf-8"),
    long_description_content_type='text/markdown',
    url='https://github.com',
    author='unionizer',
    author_email='toolkitr.email@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Development Status :: 2 - Pre-Alpha',
        'Development Status :: 3 - Alpha',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='unionizer, union, unions',
    include_package_data=True,
    packages=find_packages()
)