from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'a package for easyensemble whose basemodel is dnn'

# 配置
setup(
    name="dnneasyensemble",
    version=VERSION,
    author="VCz",
    license='MIT',
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=[
        'numpy>=1.18.0',
        'scikit-learn>=0.22.0',
        'tensorflow>=2.0.0',
        'imbalanced_learn>=0.10.1',
        'imblearn'
    ]
)