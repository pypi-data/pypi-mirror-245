from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as file:
    long_description = file.read()

setup(
    name='pyFIFA',
    version='0.2.0',
    packages=find_packages(),
    install_requires=[
        'pyfiglet>=0.8.post1',
    ],
    long_description=long_description,
    long_description_content_type='text/markdown',
    entry_points={
        'console_scripts': [
            'play = OOP_Fifa_In_Terminal.main:main',
        ],
    },

    # Other setup parameters...
)
