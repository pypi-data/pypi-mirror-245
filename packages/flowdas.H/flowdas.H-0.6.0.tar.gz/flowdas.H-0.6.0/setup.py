# Copyright 2023 Flowdas Inc. <prospero@flowdas.com>
from setuptools import setup

setup_requires = [
]

install_requires = [
    'falcon',
    'importlib_metadata;python_version<"3.10"',
    'nest-asyncio',
    'pyyaml',
    'typing-extensions;python_version<"3.9"',
    'uvicorn[standard]',
]

tests_require = [
]

dev_requires = tests_require + [
]

setup(
    name='flowdas.H',
    version=open('VERSION').read().strip(),
    url='https://pypi.org/project/flowdas.H/',
    description='Flowdas H',
    author='Flowdas',
    author_email='prospero@flowdas.com',
    packages=[
        'flowdas.boot',
        'flowdas.function',
        'flowdas.http',
        'flowdas.jsonrpc',
        'flowdas.runner',
        'typeable',
    ],
    install_requires=install_requires,
    setup_requires=setup_requires,
    tests_require=tests_require,
    extras_require={
        'dev': dev_requires,
    },
    scripts=[],
    entry_points={
        'console_scripts': [
            'f=flowdas.boot.main:main',
        ],
        'flowdas.boot': [
            'plugin.http=flowdas.http.boot',
            'plugin.runner=flowdas.runner.boot',
        ],
    },
    zip_safe=True,
    python_requires=">=3.10",
    keywords=[],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Internet',
        'Topic :: Utilities',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
