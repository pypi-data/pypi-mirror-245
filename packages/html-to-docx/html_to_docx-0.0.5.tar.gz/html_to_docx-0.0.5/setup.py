from setuptools import setup, find_packages

requirements = [
    'pandas',
    'python-docx'
]

setup(
    name='html_to_docx',
    version='0.0.5',
    description='HTML file to DOCX',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'html_to_docx=src.app:run',
        ],
    },
    install_requires=requirements
)
