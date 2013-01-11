from setuptools import setup, find_packages
setup(
    name = "actiontec-utils",
    author = 'Lars Kellogg-Stedman',
    author_email = 'lars@oddbit.com',
    url = 'http://github.com/larsks/actiontec-utils',
    version = "1",
    packages = find_packages(),
    install_requires=open('requirements.txt').readlines(),

    entry_points = {
        'console_scripts': [
            'actiontec = actiontec.main:main',
            ],
        },
)

