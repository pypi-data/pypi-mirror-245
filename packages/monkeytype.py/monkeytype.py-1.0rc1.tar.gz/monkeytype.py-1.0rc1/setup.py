import setuptools

with open("./README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="monkeytype.py",
    version="1.0rc1",
    author="Maksims K.",
    author_email="contact@maksims.co.uk",
    description="🔧 A python wrapper built around the Monkeytype API.",
    license="MIT License",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/m2ksims/monkeytype.py",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    install_requires=["requests>=2.2.0", "ratelimit>=2.2.1"],
)
