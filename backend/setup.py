from setuptools import setup, find_packages

setup(
    name='Virtual Lab Manager',
    packages=find_packages("src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=[
        'flask==1.1.2',
        'requests==2.23.0',
        'pytest==6.0.1',
        'mock==4.0.2',
        'flask-restplus==0.13.0',
        'werkzeug==0.16.1',
        'flask-cors==3.0.9',
        'pyjwt==1.7.1',
        'bcrypt==3.2.0',
        'wiremock==2.1.3',
        'psycopg2-binary==2.8.6',
        'SQLAlchemy==1.4.2'
    ],
    test_suite="tests",
    tests_require=['pytest'],
    setup_requires=['pytest-runner'],
)
