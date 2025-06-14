from setuptools import setup, find_packages

setup(
    name="zakat-app",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Flask==3.0.0",
        "Flask-SQLAlchemy==3.1.1",
        "SQLAlchemy==2.0.23",
        "Werkzeug==3.0.1",
        "Jinja2==3.1.2",
        "itsdangerous==2.1.2",
        "click==8.1.7",
    ],
    python_requires=">=3.7",
) 