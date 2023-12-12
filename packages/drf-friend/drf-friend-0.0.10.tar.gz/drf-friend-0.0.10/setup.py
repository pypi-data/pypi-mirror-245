from setuptools import setup, find_packages

def read(f):
    with open(f, 'r', encoding='utf-8') as file:
        return file.read()
    
setup(
    # Package metadata
    name='drf-friend',
    version='0.0.10',
    url='https://drf-friend.code4mk.org/',
    author='Mostafa Kamal',
    author_email='hiremostafa@gmail.com',
    description='A utility package for Django Rest Framework (DRF) that makes API development easier for developers.',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    
    # Package configuration
    packages=find_packages(exclude=['tests*']),
    
    # Dependencies
    install_requires=[
        # List your dependencies here
        # For example, 'Django>=3.0' or 'djangorestframework>=3.12.0'
    ],

    # Classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    project_urls={
        'Source': 'https://github.com/code4mk/drf-friend',
        'Changelog': 'https://github.com/code4mk/drf-friend',
    },
)
