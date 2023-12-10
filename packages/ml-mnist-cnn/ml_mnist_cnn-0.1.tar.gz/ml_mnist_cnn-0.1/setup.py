from setuptools import setup, find_packages

setup(
    name='ml_mnist_cnn',
    version='0.1',
    packages=find_packages(),
    package_data={'ml_mnist_cnn': ['data/*']},
    include_package_data=True,
    description='Code for handwritten MNIST using CNN',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='davinci003',
    author_email='freegpt00@gmail.com',
    url='https://github.com/savioratharv/prac_testing',
    # Add more if needed
)