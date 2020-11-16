from setuptools import find_packages, setup
setup(
    name='py_slack_notify',
    packages=find_packages(include=['py_slack_notify']),
    version='0.1.1',
    description='Python package for sending notification to Slack in thread with emoji',
    author='binhqd',
    license='MIT',
    install_requires=[],
    setup_requires=[],
    tests_require=[],
    test_suite='',
)