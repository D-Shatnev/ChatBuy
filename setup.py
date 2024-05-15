"""
This module contains the setup for the application.
"""

import io
import os
import re
import sys

import setuptools

VERSION = "0.0.1"


def get_long_description() -> str:
    """
    Retrieves the long description of the application.

    Returns:
        str: The long description of the application.
    """
    base_dir = os.path.abspath(os.path.dirname(__file__))
    with io.open(os.path.join(base_dir, "README.md"), encoding="utf-8") as file:
        return file.read()


def parse_requirements(fname="requirements.txt", with_version=True) -> list[str]:
    """
    Parses a requirements text file and returns a list of packages.

    Args:
        fname (str): The path to the requirements text file. Defaults to "requirements.txt".
        with_version (bool): Whether to include the version information for each package. Defaults to True.

    Returns:
        list: A list of packages. Each package is represented as a string.
    """
    require_fpath = fname

    def parse_line(line):
        """
        Parses a line and yields information about the line.

        Args:
            line (str): The line to be parsed.

        Yields:
            dict: A dictionary containing information about the line.
            The dictionary has the following keys:
                - "line" (str): The original line.
                - "package" (str): The package name extracted from the line.
                - "version_operator" (str): The version operator extracted from the line.
                - "version" (str): The version extracted from the line.
                - "platform_deps" (str): The platform-specific dependencies extracted from the line.
        """
        if line.startswith("-r "):
            # Allow specifying requirements in other files
            target = line.split(" ")[1]
            for info in parse_require_file(target):
                yield info
        else:
            info = {"line": line}
            if line.startswith("-e "):
                info["package"] = line.split("#egg=")[1]
            elif "@git+" in line:
                info["package"] = line
            else:
                # Remove versioning from the package
                pat = "(" + "|".join([">=", "==", ">"]) + ")"
                parts = re.split(pat, line, maxsplit=1)
                parts = [p.strip() for p in parts]

                info["package"] = parts[0]
                if len(parts) > 1:
                    version_operator, rest = parts[1:]
                    if ";" in rest:
                        # Handle platform specific dependencies
                        # http://setuptools.readthedocs.io/en/latest/setuptools.html#declaring-platform-specific-dependencies
                        version, platform_deps = map(str.strip, rest.split(";"))
                        info["platform_deps"] = platform_deps
                    else:
                        version = rest  # NOQA
                    info["version"] = (version_operator, version)
            yield info

    def parse_require_file(fpath):
        """
        Parses a require file and yields information about each line.

        Args:
            fpath (str): The path to the require file.

        Yields:
            str: Information about each line in the require file.
        """
        with open(fpath, "r", encoding="utf-8") as file:
            for line in file.readlines():
                line = line.strip()
                if line and not line.startswith("#"):
                    for info in parse_line(line):
                        yield info

    def gen_packages_items():
        """
        Generate the items of the packages based on the requirements file.

        Returns:
            A generator that yields the items of the packages.

        Raises:
            FileNotFoundError: If the requirements file does not exist.
        """
        if os.path.exists(require_fpath):
            for info in parse_require_file(require_fpath):
                parts = [info["package"]]
                if with_version and "version" in info:
                    parts.extend(info["version"])
                if not sys.version.startswith("3.4"):
                    # apparently package_deps are broken in 3.4
                    platform_deps = info.get("platform_deps")
                    if platform_deps is not None:
                        parts.append(";" + platform_deps)
                item = "".join(parts)
                yield item

    packages = list(gen_packages_items())
    return packages


setuptools.setup(
    name="ChatBuy",
    version=VERSION,
    description="A project consisting of several AI agents that help the user to make a shopping experience",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/D-Shatnev/ChatBuy.git",
    packages=setuptools.find_packages(),
    install_requires=parse_requirements(),
    extras_require={"dev": parse_requirements(fname="requirements-dev.txt")},
    python_requires=">=3.10",
)
