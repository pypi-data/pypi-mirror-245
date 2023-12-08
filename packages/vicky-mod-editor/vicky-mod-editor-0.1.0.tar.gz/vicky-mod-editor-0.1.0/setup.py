from setuptools import setup, find_packages

setup(
    name='vicky-mod-editor',
    version='0.1.0',
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
    url='https://github.com/yourusername/your-package-name',
)