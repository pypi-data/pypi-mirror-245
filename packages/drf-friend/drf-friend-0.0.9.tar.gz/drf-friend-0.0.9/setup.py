from setuptools import setup, find_packages

setup(
    # Package metadata
    name='drf-friend',
    version='0.0.9',
    author='Mostafa Kamal',
    author_email='hiremostafa@gmail.com',
    description='A utility package for Django Rest Framework (DRF) that makes API development easier for developers.',
    long_description='''\
    drf-friend is a collection of utilities and enhancements for Django Rest Framework (DRF), aiming to simplify and streamline the process of building RESTful APIs. It provides convenience functions, tools, and patterns to help developers write clean, efficient, and maintainable code when working with DRF.
    
    Features:
    
    - Enhanced core components for common tasks in API development.
    - Customized Django Rest Framework core classes for improved functionality.
    - Utility functions and mixins to handle common API patterns.
    - Simplifies pagination, routing, and data serialization tasks.
    
    Check the project repository for detailed documentation, examples, and updates: https://github.com/code4mk/drf-friend
    Doc: https://drf-friend.code4mk.org
    ''',
    
    # Package configuration
    packages=find_packages(),
    
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
)
