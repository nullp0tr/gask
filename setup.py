from setuptools import setup, find_packages

setup (
    name='gask',
    version='0.0.1',
    description='Gask CLI to manage tasks and time',
    url='https://github.com/nullp0tr/gask',
    author='nullp0tr',
    author_email='ahmed@shnaboo.com',
    license='MIT',
    py_modules=['gask'],
    packages=find_packages(),
    entry_points={
          'console_scripts': [
              'gask = gask.__main__:main'
          ]
      },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],

    keywords='tasks gask time management project',
    install_requires=[]
)
