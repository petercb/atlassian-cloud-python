import sys
from setuptools import setup

assert sys.version_info >= (3, 2), 'Python 3.2+ required.'

setup(
    name='atlassian-cloud-python',
    description='Python Atlassian Cloud REST API and utils',
    license='Apache License 2.0',
    version='0.1.0',
    download_url='https://github.com/petercb/atlassian-cloud-python',

    author='Peter Burns',
    author_email='pcburns@outlook.com',
    url='https://github.com/petercb',

    packages=['atlassiancloud'],
    package_data={
        '': [
            'LICENSE',
            'README.md'
        ],
    },
    package_dir={'atlassiancloud': 'lib/atlassiancloud'},
    scripts=[
        'bin/upload_attachments.py'
    ],
    install_requires=['requests', 'python-magic'],

    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Utilities'
    ]
)