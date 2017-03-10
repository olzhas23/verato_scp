from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()


setup(name='verato_scp',
      version='0.1',
      description='Utility to help scp file with commands and run on host (local -> jump -> provisioner -> host)',
      long_description='This utility is useful when you have a setup when you need to run some code on multiple machines',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 2.7',
          'Topic :: System :: Distributed Computing',
      ],
      url='https://github.com/olzhas23/verato_scp.git',
      author='Olzhas Shaikenov',
      author_email='olzhas.shaikenov@verato.com',
      license='MIT',
      install_requires=["paramiko==2.0.2", ],
      packages=['verato_scp'],
      scripts=['scripts/vscp.py'],
      zip_safe=False)
