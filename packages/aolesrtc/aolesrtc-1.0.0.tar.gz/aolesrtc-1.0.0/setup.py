from distutils.core import setup
from setuptools import find_packages

with open("README.md", "r") as f:
  long_description = f.read()

setup(name='aolesrtc',
      version='1.0.0',
      description='A easy & simple rtc library supporting janus & p2p',
      long_description=long_description,
      author='aoles',
      author_email='young.aoles@qq.com',
      url='',
      install_requires=[],
      license='MIT License',
      packages=find_packages(),
      platforms=["macosx_arm64"],
      python_requires="==3.10.13",
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.10',
          'Topic :: Software Development :: Libraries',
          'Operating System :: MacOS'
      ],
    )
