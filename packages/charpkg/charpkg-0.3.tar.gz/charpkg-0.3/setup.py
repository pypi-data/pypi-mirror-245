from setuptools import setup, find_packages

setup(
    name='charpkg',
    version='0.3',
    author='James Evans',
    author_email='joesaysahoy@gmail.com',
    description='A framework for creating RPGs',
    license='MIT',
    keywords='RPG',
    url='https://github.com/primal-coder/Char',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'CharActor==0.9.8',
        'CharObj',
        'CharTask',
        'CharCore',
        'gridengine_framework',
        'entyty',
        'dicepy',
        'screeninfo',
        'colorama'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Games/Entertainment :: Role-Playing',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
    ]
)