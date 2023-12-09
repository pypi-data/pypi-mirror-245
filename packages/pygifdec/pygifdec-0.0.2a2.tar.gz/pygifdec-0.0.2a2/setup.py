from setuptools import setup, Extension

pygifdec = Extension('pygifdec',
                     sources=['./src/pygifdec.c', './src/gifdec.c'],
                     include_dirs=['./src'],
                     )

with open('README.md', 'r', encoding='utf-8') as f:
    readme = f.read()

setup(name='pygifdec',
      version='0.0.2a2',
      author='alingse',
      author_email='alingse@foxmail.com',
      description='a python gifdec wrapper',
      long_description=readme,
      long_description_content_type='text/markdown',
      url='https://github.com/alingse/pygifdec',
      ext_modules=[pygifdec],
      packages=['src'],
      package_data={'src': ['gifdec.h']},
      )
