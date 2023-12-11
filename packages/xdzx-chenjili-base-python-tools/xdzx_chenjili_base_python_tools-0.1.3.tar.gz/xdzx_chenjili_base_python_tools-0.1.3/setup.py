from setuptools import setup

setup(
    name='xdzx_chenjili_base_python_tools',
    version='0.1.3',
    description='a base python tools package',
    author='AuspiciousChan',
    author_email='AuspiciousChan@163.com',
    url='https://gitee.com/AuspiciousChan/base-python-tools',
    packages=['xdzx_chenjili_base_python_tools', 'xdzx_chenjili_base_python_tools.base', 'xdzx_chenjili_base_python_tools.log'],
    install_requires=[
        'datetime',
        'requests',
        'uuid',
    ],
)
