from setuptools import setup

# Read deps
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='ivette',
    version='0.0.10',
    description='Python client for Ivette Computational chemistry and Bioinformatics project',
    author='Eduardo Bogado',
    py_modules=['run_ivette', 'ivette', 'ivette.fileIO_module', 'ivette.IO_module', 'ivette.load_module',
                'ivette.run_module', 'ivette.supabase_module'],  # Include 'ivette.py' as a module
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'ivette=run_ivette:main',
        ],
    },
)
