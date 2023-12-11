from setuptools import setup, find_packages


def readme():
  with open('README.md', 'r') as f:
    return f.read()


setup(
  name='firstlib',
  version='0.1',
  author='antrisole',
  author_email='gleb.zar.03@mail.ru',
  description='This is myh first module on python.',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='https://github.com/Mun-Robbery',
  packages=find_packages(),
  install_requires=['requests>=2.25.1'],
  classifiers=[
    'Programming Language :: Python :: 3.11',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='files speedfiles ',
  project_urls={
    'GitHub': 'https://github.com/Mun-Robbery'
  },
  python_requires='>=3.6'
)