from setuptools import setup, find_packages
from os.path import dirname, join

setup(
    name='zvolvAuth',
    version='0.0.13',
    license='MIT',
    description='Official Zvolv Arithmetic Python SDK',
    long_description_content_type="text/markdown",
    long_description= open(join('README.md'), encoding='utf-8').read(),  
    packages=find_packages(),
    author = 'Yogesh Jadhav',
    author_email = 'support@zvolv.com',
    python_requires=">=3.0.1",
    url = '',
    download_url = '',
    keywords = ['zvolv', 'zvolv-api', 'web-api', 'sdk', 'rest-api-client'],
    install_requires=[],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        "Operating System :: OS Independent",
        'License :: OSI Approved :: MIT License',  
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
     project_urls={
        'Source': 'https://github.com/yogeshjadhav22/python-sdk0.0.1',
    },
)