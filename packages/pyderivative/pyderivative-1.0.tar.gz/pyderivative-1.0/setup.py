from setuptools import setup, find_packages


def readme():
  with open('README.md', 'r') as f:
    return f.read()


setup(
  name='pyderivative',
  version='1.0',
  author='antrisole',
  author_email='gleb.zar.03@mail.ru',
  description='This module destined to calculation of derivatives using numerical methods.',
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
  keywords='numerical derivative',
  project_urls={
    'GitHub': 'https://github.com/Mun-Robbery/pyder'
  },
  python_requires='>=3.6'
)