from setuptools import setup, find_packages

setup(
    name='mxwpy',  # package name
    version='0.2.1',  # version
    author='Mingxing Weng',  # author name
    author_email='2431141461@qq.com',  # author email
    description='efficient numerical schemes',  # short description
    long_description=open('README.md').read(),  # long description, usually your README
    long_description_content_type='text/markdown',  # format of the long description, 'text/markdown' if it's Markdown
    url='https://github.com/mxweng/mxwpy',  # project homepage
    packages=find_packages(),  # automatically discover all packages
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],  # list of classifiers
    python_requires='>=3.6',  # Python version requirement
)