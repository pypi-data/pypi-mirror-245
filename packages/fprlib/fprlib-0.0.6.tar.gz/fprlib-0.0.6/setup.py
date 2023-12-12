from setuptools import find_packages, setup

#with open("app/README.md","r") as f:
#    long_description = f.read()

setup(
    name="fprlib",
    version="0.0.6",
    description="Knjižnica za FPR",
    package_dir={"": "app"},
    packages=find_packages(where="app"),
#    long_description=long_description,
    url="https://github.com/DrKvass/fprlib",
    author="Dr.Kvass",
    classifiers=[
        "Programming Language :: Python :: 3.11",
    ],
    install_requires=["numpy","scipy","matplotlib","statistics","uncertainties"],
    python_required=">=3.11",
)