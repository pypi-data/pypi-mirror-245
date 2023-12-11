from setuptools import setup

setup(
    name='xdzx-chenjili-base-python-tools',
    version='0.1.0',
    description='a base python tools package',
    author='AuspiciousChan',
    author_email='AuspiciousChan@163.com',
    url='https://gitee.com/AuspiciousChan/base-python-tools',
    packages=['utils'],
    install_requires=[
        'datetime',
        'requests',
        'uuid',
    ],
)
