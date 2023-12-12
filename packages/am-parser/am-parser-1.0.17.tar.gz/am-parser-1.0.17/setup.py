import setuptools


setuptools.setup(
    name="am-parser",
    version="1.0.17",
    author="casual-aimer",
    license="GNU GPLv3",
    description="Simple asciimath parser",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=["am_parser"],
    include_package_data=True,
    platforms="any",
    python_requires=">=3.9",
)
