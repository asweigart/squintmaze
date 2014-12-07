from setuptools import setup


setup(
    name='Squint Maze',
    version='0.9.0',
    url='https://github.com/asweigart/squintmaze',
    author='Al Sweigart',
    author_email='al@inventwithpython.com',
    description=('A maze game that will ruin your eyesight. Built with Pygame for Ludum Dare 31.'),
    license='BSD',
    packages=['squintmaze'],
    test_suite='',
    install_requires=[],
    keywords="maze game pygame",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Win32 (MS Windows)',
        'Environment :: X11 Applications',
        'Environment :: MacOS X',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.2',
    ],
)