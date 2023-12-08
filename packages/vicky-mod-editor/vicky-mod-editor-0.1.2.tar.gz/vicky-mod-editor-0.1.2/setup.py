from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='vicky-mod-editor',
    version='0.1.2',
    packages=find_packages(),
    install_requires=[
        'ClauseWizard',
        'pyparsing',
    ],
    entry_points={
        'console_scripts': [
            # List any command-line scripts here
        ],
    },
    # Other metadata like author, description, etc.
    author='supamap',
    description='Vicky Mod Editor',
    long_description=long_description,
    long_description_content_type="text/markdown",  # Use "text/plain" for plain text README
    url='https://github.com/supamap/vicky-mod-editor',
)