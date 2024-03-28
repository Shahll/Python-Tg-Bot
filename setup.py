from setuptools import setup

sourceFile = ['bot/bot.py']

setup(
    name='book_searching_app',
    version='1.0',
    description='A book searching application',
    author='Shahll',
    author_email='shahll.git@email.com',
    py_modules=['bot.bot'], 
    install_requires=[
        'python-telegram-bot',
        'python-dotenv',
        'requests'
    ],
)