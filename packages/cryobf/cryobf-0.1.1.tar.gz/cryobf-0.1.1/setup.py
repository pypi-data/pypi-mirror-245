import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cryobf",
    version="0.1.1",
    author="Patrick Menschel",
    author_email="menschel.p@posteo.de",
    description="A python 3 unpacker for .bf files.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/menschel/cryobf",
    packages=setuptools.find_packages(exclude=["tests", "scripts", ]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3 :: Only",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development :: Embedded Systems",
    ],
    python_requires=">=3.9",
    keywords="game data cryo bf",
    scripts=["bin/cryobf"],
    data_files=[('etc/bash_completion.d', ['bin/cryobf.bash-completion'])]
)
