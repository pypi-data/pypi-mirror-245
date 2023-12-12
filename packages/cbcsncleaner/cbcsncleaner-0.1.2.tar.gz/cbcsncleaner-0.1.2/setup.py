from setuptools import setup, find_packages

setup(
    name='cbcsncleaner',
    version='0.1.2',
    description='A system for cleaning and organizing the output of generated SQL queries from Snowflake.',
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Intended Audience :: Developers",
        "Development Status :: 4 - Beta"
    ],
    python_requires='>=3.10',
    install_requires=[
        'python-dotenv',
        'wordninja'
    ],
    entry_points={
        'console_scripts': [
            'cbcsncleaner=sql_model_cleaner.main:cli_function',
        ],
    },
)

