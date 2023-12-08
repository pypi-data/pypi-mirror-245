from setuptools import setup, find_packages


with open("README.md", encoding="UTF-8") as f:
    readme = f.read()

setup(
    name = 'colorAw',
    version = '0.0.2',
    author='MohammadRezaFirouzi',
    author_email = 'mrfirouziii@gmail.com',
    description = 'This is an Color Library for Terminal',
    long_description = readme,
    python_requires="~=3.7",
    long_description_content_type = 'text/markdown',
    url = 'https://rubika.ir/Mohamadreza_firouzi',
    packages = find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
)
