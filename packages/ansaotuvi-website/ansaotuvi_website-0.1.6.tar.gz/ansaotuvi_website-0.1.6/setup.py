from setuptools import setup

setup(name='ansaotuvi_website',
      version='0.1.6',
      description='Chương trình an sao tử vi mã nguồn mở sử dụng django',
      long_description="Chương trình an sao tử vi mã nguồn mở sử dụng django",
      long_description_content_type="text/markdown",
      url='https://github.com/hieudo-ursa/ansaotuvi-website',
      author='hieu.do',
      author_email='hieu.do@ursa.vn',
      license='MIT',
      packages=['ansaotuvi_website'],
      setup_requires=['pytest-runner'],
      tests_require=['pytest'],
      include_package_data=True,
      install_requires=[
          "Django==4.2.8",
          "more-itertools==4.1.0",
          "pytz==2020.1",
          "six==1.12.0",
          "docutils==0.17.0",
          "urllib3==1.26.0",
          "typed-ast==1.4.3",
          "ansaotuvi==0.1.2"
      ],
      zip_safe=False)
