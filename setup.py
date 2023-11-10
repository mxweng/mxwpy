from setuptools import setup, find_packages

setup(
    name='mxwpy',  # 包名
    version='0.1.1',  # 版本
    author='Mingxing Weng',  # 作者名
    author_email='2431141461@qq.com',  # 作者邮箱
    description='efficient numerical schemes',  # 简短描述
    long_description=open('README.md').read(),  # 长描述，通常是你的README
    long_description_content_type='text/markdown',  # 长描述的格式，如果是Markdown，就是'text/markdown'
    url='https://github.com/mxweng/mxwpy',  # 项目的主页
    packages=find_packages(),  # 自动发现所有包
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],  # 分类器列表
    python_requires='>=3.6',  # Python版本要求
)