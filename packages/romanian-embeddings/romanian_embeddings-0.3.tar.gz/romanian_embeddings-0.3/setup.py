from setuptools import setup, find_packages

setup(
    name='romanian_embeddings',
    version='0.3',
    packages=find_packages(),
    install_requires=[
        'transformers',
        'numpy',
        'onnxruntime',
    ],
    author='Mihai Ilie',
    author_email='ilie.mihai92@gmail.com',
    description='Romanian language embeddings using transformers and ONNX.',
    keywords='nlp transformers onnx romanian embeddings',
)

