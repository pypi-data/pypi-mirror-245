from setuptools import setup,find_packages

long_description = "A python package about json, smarter, quicker and better!"
setup(
    name='smarterjson',
    version='1.3.5',
    description='A smarter than python json', 
    long_description = long_description, 
    url='https://github.com/0x22f1a6543a0/smarterjsons',
    author='Zhang Jiaqi',
    author_email='2953911716@qq.com',
    license='MIT',
    classifiers=[
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    packages=find_packages(),
    include_package_data = True,
)
