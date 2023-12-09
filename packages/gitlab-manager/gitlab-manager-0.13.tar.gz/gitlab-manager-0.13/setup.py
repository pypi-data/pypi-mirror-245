from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='gitlab-manager',
    version='0.13',
    readme = "README.md",
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[
        'python-dotenv',
        'requests',
        'python-gitlab'
    ],
    entry_points={
        'console_scripts': [
            'gitlab-manager = gitlab_manager.main:main',
        ],
    },
)