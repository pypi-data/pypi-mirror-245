from setuptools import setup, find_packages

requirements = [
    'pandas',
    'python-docx'
]

setup(
    name='htmlToDocxItgelt',
    version='0.0.6',
    description='HTML file to DOCX',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'htmlToDocxItgelt=src.app:run',
        ],
    },
    install_requires=requirements
)
