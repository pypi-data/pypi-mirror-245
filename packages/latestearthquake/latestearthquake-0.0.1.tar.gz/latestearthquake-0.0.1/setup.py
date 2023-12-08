
import pathlib
import setuptools

setuptools.setup(
    name="latestearthquake",
    version="0.0.1",
    author="Nur Arif",
    author_email="nurarif0151@gmail.com",
    description="This package will get the latest earthquake from BMKG",
    long_description=pathlib.Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    url="https://github.com/teolloDEV/Indonesia-last-earthquake",
    license = "The Unlicense",
    project_urls={
        "Website": "https://nurarif.com",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
    ],
    # package_dir={"": "src"},
    # packages=setuptools.find_packages(where="src"),
    packages=setuptools.find_packages(),
    python_requires=">=3.8",


)

