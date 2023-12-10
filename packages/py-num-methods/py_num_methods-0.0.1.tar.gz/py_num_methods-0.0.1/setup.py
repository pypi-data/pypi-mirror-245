from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 11',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='py_num_methods',
  version='0.0.1',
  description='Numerical Methods Library in Python',
  long_description_content_type = 'text/markdown',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='JaidevSK',
  author_email='jaidevkhalane@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='Numerical Methods', 
  packages=find_packages(),
  install_requires=['numpy', 'matplotlib'] 
)
