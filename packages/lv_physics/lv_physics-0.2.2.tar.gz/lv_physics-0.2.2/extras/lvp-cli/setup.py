from setuptools import find_packages, setup

setup(
    name="lvp_cli",
    packages=find_packages(),
    setuptools_git_versioning={
        "enabled": True,
    },
    setup_requires=["setuptools_git_versioning<2"],
    entry_points={
        "console_scripts": ["lvp = lvp_cli.__main__:main"],
    }
)
