from setuptools import setup, find_packages

setup(
    name='tieui',
    version='0.2.21',
    packages=find_packages(),
    package_data={
        'tieui': ['local-version/*', 'local-version/**/*']
    },
    install_requires=[
        'flask_cors',
        'flask_socketio',
        'flask',
        'gunicorn',
        'eventlet',
        'sendgrid',
        'websocket-client',
    ],
    author='TieUi',
    author_email='info@tieUi.com',
    description='Tie Ui package for local development',
    url='https://tieui.app',
)