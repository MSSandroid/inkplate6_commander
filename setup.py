import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='inkplate6_commander',
    version="0.1",
    author="Michael Schuldes",
    author_email="schuldes@pm.me",
    description="Send UART commands to Inkplate6",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MSSandroid/inkplate6_commander",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: MIT",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=[
        'parse',
        'serial',
    ])

