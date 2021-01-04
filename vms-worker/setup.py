from setuptools import setup, find_packages

setup(
    name='VMs Worker',
    packages=find_packages("src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=[
        'flask==1.1.2',
        'shutils==0.1.0',
        'pytest==6.0.1',
        'mock==4.0.2',
        'requests==2.23.0',
        'flask-restplus==0.13.0',
        'werkzeug==0.16.1',
        'schedule==0.6.0',
        'zipfile37==0.1.3'
    ],
    test_suite="tests",
    tests_require=['pytest'],
    setup_requires=['pytest-runner'],
)
