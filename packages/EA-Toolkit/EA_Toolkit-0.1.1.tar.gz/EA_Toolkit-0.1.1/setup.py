from setuptools import setup, find_packages


setup(
    name='EA_Toolkit',
    version='0.1.1',
    packages=find_packages(),
    description='Some Utils for Entity Alignment and GCN.',
    author='Cody',
    author_email='615760263@qq.com',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    # Add other dependencies in here
    install_requires=[
        'numpy',
        'igraph'
    ]
)
