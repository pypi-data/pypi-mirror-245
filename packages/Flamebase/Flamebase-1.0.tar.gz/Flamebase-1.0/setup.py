from setuptools import setup

setup(
    name='Flamebase',
    version='1.0',
    description='Simple library to create a clone of Firebase Realtime database with almost the same api. Database uses json file format to keep data.',
    author='Michael Chess',
    author_email='codm.cheater@gmail.com',
    packages=['packages'],
    install_requires=['ngrok-api', 'flask', 'ngrok'],
)