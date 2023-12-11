from pathlib import Path
from setuptools import setup





setup(
    name='robocraft',
    version='1.2.0',
    description='Fix of neumond Computercraft',
    author='Artem Robocodovich',
    author_email='garo109696@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Education',
        'Topic :: Games/Entertainment',
    ],
    keywords='robocraft minecraft',
    package_data={'computercraft': ['back.lua']},
    packages=['computercraft', 'computercraft.subapis'],
    install_requires=['aiohttp == 3.8.5', 'greenlet'],
    entry_points={
        'console_scripts': ['robocraft = computercraft.server:main'],
    },
)
