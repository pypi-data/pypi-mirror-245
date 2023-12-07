from setuptools import setup, find_packages

setup(
    name='exem-logs',
    version='1.1.11',
    description='Powerfull but simplest way to log your python application.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://gitlab.com/exem2/libraries/logs',
    author='Félix BOULE--REIFF',
    author_email='boulereiff@exem.fr',
    license='BSD 2-clause',
    install_requires=[
        'google-cloud',
        'google-cloud-logging',
        'google-cloud-error-reporting'
    ],
    py_modules=[
        'Log',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: BSD License'
    ],
)
