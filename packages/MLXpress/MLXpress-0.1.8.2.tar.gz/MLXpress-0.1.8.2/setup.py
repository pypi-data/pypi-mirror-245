from setuptools import setup, find_packages
with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='MLXpress',
    version='0.1.8.2',
    author='vinilg7',
    author_email='vinilg7@gmail.com',
    description='A powerful and user-friendly machine learning toolkit for data science and ML professionals to accelerate their workflow',
    long_description=long_description,
    long_description_content_type='text/markdown',


    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
    ],
    install_requires=[
        'scikit-learn',
        'pandas',
        'seaborn',
        'matplotlib',
        'numpy',
        'scipy'

    ],
)
