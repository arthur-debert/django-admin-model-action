import os
from setuptools import setup, find_packages

from adminmodelaction import VERSION


f = open(os.path.join(os.path.dirname(__file__), 'README.rst'))
readme = f.read()
f.close()

setup(
    name='django-admin-model-action',
    version=".".join(map(str, VERSION)),
    description='adds the hability to have action buttons on the admin chage view',
    long_description=readme,
    author='Arthur Debert',
    author_email='arthur@stimuli.com.br',
    url='http://github.com/arthur-debert/django-admin-model-action',
    packages=find_packages(),
    package_data={
        'adminmodelaction': ['templates/*.html',]
    },
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
)

