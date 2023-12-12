from setuptools import setup

setup(name='ansaotuvi',
      version='0.1.22',
      description='Chương trình an sao tử vi mã nguồn mở',
      url='https://github.com/hieudo-ursa/ansaotuvi',
      author='hieu.do',
      author_email='hieu.do@ursa.vn',
      license='MIT',
      packages=['ansaotuvi'],
      setup_requires=['pytest-runner'],
      tests_require=['pytest'],
      install_requires=[
          "attrs==19.2.0",
          "ephem==3.7.6.0  ; sys_platform == 'linux'",
          "more-itertools==4.1.0",
          "mypy==1.7.1",
          "pluggy==0.13.1",
          "py==1.10.0",
          "pytest==5.4.0",
          "six==1.12.0",
          "typed-ast==1.4.3"
      ],
      zip_safe=False)
