from setuptools import find_packages, setup

setup(
    name="pygif_converter_test",
    version="1.0.0",
    description="Test package for distribution",
    author="quasarhub",
    author_email="quasarhub@gmail.com",
    url="",
    download_url="",
    install_requires=["pillow"],
    include_package_data=True,
    packages=find_packages(),
    keywords=["GIFCONVERTER", "gifconverter"],
    python_requires=">=3",
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
