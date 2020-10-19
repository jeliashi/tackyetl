from setuptools import find_packages, setup

if __name__ == "__main__":
    # (TODO) figure out why version can't be detected from attr in cfg
    setup(
        version="0.0.0",
        packages=find_packages(),
    )
