from setuptools import setup

setup(
    name='lektor-minification',
    description='A simple Lektor plugin to minify images at build time.',
    version='1.1',
    author=u'Pierre-Julien Grizel',
    author_email='pjgrizel@numericube.com',
    url='https://github.com/numericube/lektor-minification',
    license='GNU GPLv3',
    platforms='any',
    py_modules=['lektor_minification'],
    entry_points={
        'lektor.plugins': [
            'minification = lektor_minification:MinificationPlugin',
        ]
    },
    install_requires=[
        'Lektor',
        'Pillow',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP :: Site Management',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
