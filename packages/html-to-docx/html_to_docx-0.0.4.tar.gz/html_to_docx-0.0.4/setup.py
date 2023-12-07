from setuptools import setup, find_packages

requirements = [
    'pandas',
    'python-docx'
]

setup(
    name='html-to-docx',
    version='0.0.4',
    description='HTML file to DOCX',
    packages=find_packages("html_to_docx"),
    entry_points={
        'console_scripts': [
            'html_to_docx=src.app:run',
        ],
    },
    install_requires=requirements
)
