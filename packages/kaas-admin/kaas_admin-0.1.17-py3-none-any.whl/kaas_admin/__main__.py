from setuptools import setup, find_packages

setup(
    name="kaas-admin",
    version="0.1.17",
    py_modules=["kaas-admin"],
    entry_points={
        "console_scripts": [
            "kaas-admin = kaas_admin.__main__:main"
        ]
    }
    ,
    packages=find_packages(),
    install_requires=[
        "pyyaml",
        "pytest",
        "ansible-tower-cli == 3.3.0",
        "shutil"
    ]
)
