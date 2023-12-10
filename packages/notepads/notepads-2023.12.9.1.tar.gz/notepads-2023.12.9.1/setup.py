from setuptools import setup, find_packages
import pathlib

path_absolute: pathlib.Path = pathlib.Path(__file__).parent.absolute()

setup(
    name='notepads',
    version='2023.12.9.1',
    description='Create runtime folders, files, and code notes. All stored in notepads environment.',
    long_description=pathlib.Path(f"{path_absolute}/README.md").read_text(encoding="utf-8"),
    long_description_content_type='text/markdown',
    url='https://github.com',
    author='notepads',
    author_email='toolkitr.email@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='entry,entries',
    install_requires=[
    ],
    include_package_data=True,
    packages=find_packages()
)