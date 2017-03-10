from setuptools import setup

setup(name='verato_scp',
      version='0.1',
      description='Utility to help scp file with commands and run on host (local -> jump -> provisioner -> host)'
      url='https://git-codecommit.us-east-1.amazonaws.com/v1/repos/veratoDTS',
      author='Olzhas Shaikenov',
      author_email='olzhas.shaikenov@verato.com',
      license='MIT',
      packages=['verato_scp'],
      zip_safe=False)
