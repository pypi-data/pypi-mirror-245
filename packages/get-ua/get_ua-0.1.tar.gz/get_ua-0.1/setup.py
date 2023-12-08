from setuptools import setup, find_packages

setup(
    name='get_ua',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        # No external dependencies for now
    ],
    author='Dmitriy Kotenko',
    author_email='antevertapro@gmail.com',
    description='A Python library for generating random user agents',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/anteverta/get_user_agent',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
)
