from setuptools import setup, find_packages

with open('README.md', encoding='utf-8') as f: # README.md 내용 읽어오기
	  long_description = f.read()

setup(
    name='prstat',
    version='1.0.3',
    license='MIT',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    url='https://github.com/karinysis/prstat',
    author='youngjae lee',
    author_email='leeyoungjae@pusan.ac.kr',
    description='tools for pnu probabilities and statistics class',
    packages=find_packages(),    
    install_requires=['sympy'],
)

"""
python setup.py sdist bdist_wheel
twine upload dist/*
"""