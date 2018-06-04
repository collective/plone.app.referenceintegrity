from setuptools import setup, find_packages
import os

version = '0.2.dev0'

setup(name='plone.app.referenceintegrity',
      version=version,
      description="Protect reference targets to be deleted",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        ],
      keywords='',
      author='',
      author_email='',
      url='http://svn.plone.org/svn/collective/',
      license='GPL',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      namespace_packages=['plone', 'plone.app'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'Plone',
          'plone.app.linkintegrity',
          'plone.app.registry',
      ],
      extras_require={'test': [
        'plone.app.testing',
      ]},
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
