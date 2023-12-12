from setuptools import find_packages, setup

setup(
    name="fprlib",
    version="0.0.7",
    description="Knjižnica za FPR",
    package_dir={"": "app"},
    packages=find_packages(where="app"),
    long_description="README.md",
    long_description_content_type="text/markdown",
    url="https://github.com/DrKvass/fprlib",
    author="Dr.Kvass",
    classifiers=[
        "Programming Language :: Python :: 3.11",
    ],
    install_requires=["numpy","scipy","matplotlib","statistics","uncertainties"],
    python_required=">=3.11",
)