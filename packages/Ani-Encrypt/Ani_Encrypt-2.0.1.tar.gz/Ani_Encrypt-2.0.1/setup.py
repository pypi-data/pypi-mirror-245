from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="Ani_Encrypt",
    version="2.0.1",
    description="A Python package to encrypt and decrypt data.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="",
    author="Aniket Dubey",
    author_email="daniket182@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["enc_dec"],
    include_package_data=True,
    install_requires=["requests"],
    entry_points={
        "console_scripts": [
            "Ani_Encrypt=enc_dec.encoder_decoder:ED",
        ]
    },
)