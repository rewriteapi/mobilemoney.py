from setuptools import setup

requirements = []
with open('requirements.txt') as f:
  requirements = f.read().splitlines()

readme = ''
with open('README.rst') as f:
    readme = f.read()

packages = [
  'mobilemoney',
  'mobilemoney.request',
  'mobilemoney.errors',
  'mobilemoney.utils'
  ]

setup(name='mobilemoney.py',
      author='rewriteapi',
      url='https://rewriteapi.cm/momo',
      author_email="<support@rewriteapi.cm>",
      project_urls={
        "Documentation": "https://momopy.rewriteapi.cm",
        "Website":"https://rewriteapi.cm",
        "Repository":"https://github.com/rewriteapi/mobilemoney.py"
      },
      version='0.1.2',
      packages=packages,
      long_description=readme,
      long_description_content_type="text/markdown",
      license='MIT',
      description='A Python wrapper for the MoMo Open API',
      include_package_data=True,
      install_requires=requirements,
      keywords=['python', 'mobilemoney', 'MTN Money', 'rewriteapi', 'MTN API', 'mobilemoney-py'],
      python_requires='>=3.8.0',
      classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
        'Typing :: Typed',
      ]

)