import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description=fh.read()

setuptools.setup(
    name="llm-caiche",
    version="0.1.1",
    author="Structuraize",
    author_email="info@structuraize.com",
    description="Unified Language Model Cache.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/structuraize/caiche",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.20.0",
    ]
)
