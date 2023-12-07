from setuptools import setup

with open("README.md") as readme:
    long_description = readme.read()

setup(
    name="memhack",
    version="1.0.0",
    py_modules=["memhack"],
    license="MIT",
    platforms=["any"],
    description="Arbitrary RAM Access",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Szabolcs Dombi",
    author_email="szabolcs@szabolcsdombi.com",
    url="https://github.com/szabolcsdombi/memhack/",
    project_urls={
        "Source": "https://github.com/szabolcsdombi/memhack/",
        "Bug Tracker": "https://github.com/szabolcsdombi/memhack/issues/",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
        "Topic :: Software Development",
        "Topic :: Software Development :: Debuggers",
        "Topic :: Utilities",
    ],
    keywords=[
        "ram",
        "memory",
        "mem",
        "pointer",
        "ptr",
        "heap",
    ],
)