from setuptools import setup, find_packages

setup(
    name='gitlab-manager',
    version='0.1',
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