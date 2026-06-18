from setuptools import setup, find_packages

setup(
    name="employee-events",
    version="1.0.0",
    description="Employee Events Management System",
    author="Your Name",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "python-fasthtml>=0.14.0",
    ]
)
