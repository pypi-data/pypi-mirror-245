from setuptools import setup

setup(
    name='LingerGRN',
    version='1.1',
    description='Gene regulatory network inference',
    author='Kaya Yuan',
    author_email='qyyuan33@gmail.com',
    packages=['LingerGRN'],
    license = "MIT",
    url='https://github.com/Durenlab/LINGER',
    install_requires=['torch', 'scipy', 'numpy', 'pandas', 'shap', 'scikit-learn', 'joblib'],
)
