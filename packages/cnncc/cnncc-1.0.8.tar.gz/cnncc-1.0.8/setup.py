from setuptools import setup, find_packages

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='cnncc',
    version='1.0.8',
    packages=find_packages(),
    description='A simple CNN for cell-cycle phase classification',
    author='F.Dumoncel, E.Billard, S. Boudouh',
    install_requires=required,
    package_data={
        'cnncc': ['models/resnet/*.pt', 'models/resnet/*.pth', 'models/logreg/*.joblib'],
    },
    entry_points={
        'console_scripts': [
            'cnncc = cnncc:main'
        ]
    }
)