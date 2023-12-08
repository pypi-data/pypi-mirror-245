from setuptools import setup

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='punjabi_stopwords',
    version='1.0.0', 
    py_modules=['punjabi_stopwords'],
    description='A Python library for Punjabi language stopwords.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Gurpej Singh',
    author_email='gurpejsingh462@gmail.com',
    url='https://github.com/gurpejsingh13/Punjabi_Stopwords.git',
    license='MIT',
    keywords=['stopwords', 'punjabi', 'nlp', 'punjabi language', 'natural language processing'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',  
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    python_requires='>=3.7',
)
