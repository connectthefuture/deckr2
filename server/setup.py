from setuptools import setup

setup(name='deckr',
    version='0.1',
    description='The core deckr server',
    author='Tristan Rasmussen',
    license='MIT',
    packages=['deckr'],
    zip_safe=False,
    install_requires=[
      'twisted',
    ],
    # Test configuration
    test_suite='nose.collector',
    tests_require=[
    'nose',
    'mock'
    ],
)
