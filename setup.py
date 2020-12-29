import setuptools

from Rare import __version__ as version

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Rare",
    version=version,
    author="Dummerle",
    author_email="lennardbaeumer@gmail.com",
    license="GPL-3",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Dummerle/Rare",
    packages=["Rare", "Rare.Styles", "Rare.utils", "Rare.Tabs", "Rare.Tabs.Settings", "Rare.Tabs.GamesInstalled", "Rare.Tabs.GamesUninstalled"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        "Operating System :: OS Independent"
    ],
    python_requires=">=3.8",
    entry_points=dict(console_scripts=["rare=Rare.Main:main"]),
    install_requires=[
        "legendary-gl",
        "requests<3.0",
        "pillow",
        "pyqtwebengine",
        "setuptools",
        "wheel"
    ]
)
