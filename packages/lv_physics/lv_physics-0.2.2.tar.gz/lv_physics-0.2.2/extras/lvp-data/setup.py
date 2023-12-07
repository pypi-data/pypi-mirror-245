from setuptools import find_packages, setup

setup(
    name="lvp_data",
    packages=find_packages(),
    install_requires=[
        "boto3",
        "cryptography",
        "dataclasses-json",
        "numpy",
        "psycopg2-binary",
        "pytz",
    ],
    setuptools_git_versioning={
        "enabled": True,
    },
    setup_requires=["setuptools_git_versioning<2"],
)
