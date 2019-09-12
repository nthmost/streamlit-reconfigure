from setuptools import setup, find_packages

setup(
    name = 'streamlit-reconfigure',
    version = '0.0.1',
    description = 'Streamlit Reconfigurator CLI tool',
    url = 'https://github.com/nthmost/streamlit-reconfigure',
    author = 'Naomi Most',
    maintainer = 'Naomi Most',
    author_email = 'naomi@nthmost.com',
    maintainer_email = 'naomi@nthmost.com',
    license = 'Apache 2.0',
    packages = find_packages(),
    entry_points = { 'console_scripts': [
                        'streamlit-reconfigure = slreconfig.main:main',
                    ]
                   },
    install_requires = [
        'setuptools',
        'wheel',
        'toml',
        'streamlit',
        'click',
        ],
    )
