from setuptools import setup, find_packages

setup(
    name='CEFT_Classifier_French',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        "pandas",
        "torch",
        "sentencepiece",
        "transformers",
        "torchvision",
        "stqdm",
        "streamlit",
        "scikit-learn",
        "wget",
    ],
    # Optional
    author='Jonathan Stefanov',
    author_email='jonathan.stefanov@ik.me',
    description='A French text classification package.',
    keywords='french text classification',
)
