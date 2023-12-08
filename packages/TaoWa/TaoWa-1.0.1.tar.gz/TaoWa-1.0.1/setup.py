from setuptools import setup



from setuptools import setup, find_packages

setup(
    name='TaoWa',
    version='1.0.1',
    description='中文模块',
    long_description_content_type='text/markdown',
    author='陈炳强',
    author_email='99396686@qq.com',
    url='https://github.com/ChenBingQiangi/-',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.1',
    # 如果有依赖包，可以在此处添加
    install_requires=[
        'wxPython',
        'requests',
        'PyExecjs',
        'web3',
        'pywin32',
    ],
)