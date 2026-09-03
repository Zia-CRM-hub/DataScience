from setuptools import setup, find_packages

setup(
    name="employee-events",
    version="1.0.0",
    description="Employee Events Management System",
    author="Zia-CRM-hub",
    author_email="contact@example.com",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "pandas>=1.3.0",
        "python-fasthtml>=0.14.0",
    ],
    package_data={
        "employee_events": ["employee_events.db"],
    },
)
