from setuptools import setup
def readme():
  with open('TestMyFirstProjectLibrary/readme.md', 'r') as f:
    return f.read()

setup(name='TestMyFirstProjectLibrary',
      long_description=readme(),
      long_description_content_type='text/markdown',
      version='0.0.6.0',
      description='None',
      packages=['TestMyFirstProjectLibrary'],
      author_email='akim.petbu@gmail.com')
