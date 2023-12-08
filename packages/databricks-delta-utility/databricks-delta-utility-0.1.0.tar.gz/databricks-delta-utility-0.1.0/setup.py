from setuptools import setup, find_packages

setup(
    name="databricks-delta-utility",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "databricks-api",
        "delta-tables",
        # Add other dependencies as needed
    ],
    author="Sachin Dhiman",
    author_email="sachindhiman1@live.in",
    description="Utility package for managing Delta tables on Databricks",
    long_description="""\
    My Databricks Package is a Python package designed to simplify Delta table management on Databricks.
    It provides functionalities to create, read, update, and delete Delta tables, with parameterization for table names,
    prefix, and suffix. The package also auto-detects the Databricks workspace and current user.
    """,
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/databricks-delta-utility",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    keywords="databricks delta utility",
    project_urls={
        "Bug Reports": "https://github.com/your-username/databricks-delta-utility/issues",
        "Source": "https://github.com/your-username/databricks-delta-utility",
    },
    python_requires=">=3.6",
)
