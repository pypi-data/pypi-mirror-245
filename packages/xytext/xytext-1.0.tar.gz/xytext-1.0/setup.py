from setuptools import setup, find_packages

setup(
    name='xytext',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    author='Xytext',
    author_email='hello@xytext.com',
    description='API Wrapper for Xytext - LLM Interfaces for Production.',
    # long_description=open('README.md').read(),
    # long_description_content_type='text/markdown',
    url='https://github.com/xytext-ai/xytext',
)
