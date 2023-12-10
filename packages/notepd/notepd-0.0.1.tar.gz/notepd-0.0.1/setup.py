from setuptools import setup, find_packages
import pathlib

path_absolute: pathlib.Path = pathlib.Path(__file__).parent.absolute()

setup(
    name='notepd',
    version='0.0.1',
    description='',
    long_description=pathlib.Path(f"{path_absolute}/README.md").read_text(encoding="utf-8"),
    long_description_content_type='text/markdown',
    url='https://github.com',
    author='notepd',
    author_email='toolkitr.email@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='entry,entries',
    include_package_data=True,
    packages=find_packages()
)