import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="st-mongo-connection",
    version="1.0.0",
    author="Moris Doratiotto",
    author_email="moris.doratiotto@gmail.com",
    description="Streamlit MongoDB Connector: An efficient connector for interfacing MongoDB with Streamlit apps",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Mortafix/streamlit-mongo",
    packages=setuptools.find_packages(),
    install_requires=[
        "streamlit>=1.29.0",
        "pymongo>=4.6.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
    ],
    python_requires=">=3.9",
    keywords=["icons", "icons8", "download"],
    entry_points={"console_scripts": ["i8-downloader=i8_downloader.downloader:main"]},
)
