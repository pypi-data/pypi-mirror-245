from setuptools import find_packages, setup

with open("requirements.txt", encoding="utf-8") as f:
    install_requires = [line for line in f.readlines() if "./" not in line]

with open("requirements-test.txt", encoding="utf-8") as f:
    test_requires = [line for line in f.readlines() if "./" not in line]


setup(
    name="lvp_plots",
    version="0.1.0",
    packages=find_packages(),
    install_requires=install_requires,
    extras_require={"test": test_requires},
)
