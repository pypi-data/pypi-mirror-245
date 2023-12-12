from setuptools import setup, find_packages

setup(
    name='api-typewith',
    version='0.1.0',
    author='Roberto Mello',
    author_email='roberto.mello@typewith.ai',
    description='API with VDB SDK by Typewtih AI',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: Other/Proprietary License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)