from setuptools import setup

setup(name='extended-algo',
      version='0.1',
      description='wrapper for creating event and vector algo that supports the extended-chart',
      url='https://github.com/karunkrishna/poc_lightweight_charts',
      author='Karun Krishna',
      author_email='karun.krishna@gmail.com',
      license='MIT',
      packages=['extended_algo', 'extended_algo.engine', 'extended_algo.market', 'extended_algo.market'],
      install_requires=['pandas', 'python-dotenv'],
      zip_safe=False
      )
