from setuptools import setup, find_packages

setup(
    name='llm_datatech',
    version='0.1.0',
    author='datatech',
    author_email='tdf@totalenergies.com',
    description='RAG llm datatech',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)