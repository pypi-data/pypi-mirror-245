from setuptools import find_packages, setup

setup(
    name="facebookrequests",
    version="0.0.1",
    description="A Python package for handling API interactions with Facebook, utilizing the Python requests package.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Dan Norwood",
    author_email="norwood.dan@gmail.com",
    url="https://your.package.url",  # Replace with your package's URL, if available
    packages=find_packages(),
    install_requires=[
        "requests",
        "Pillow",  # PIL is included in the Pillow package
    ],
    python_requires=">=3.11",  # Specify the minimum Python version required
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",  # Replace with your chosen license
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
    ],
)
