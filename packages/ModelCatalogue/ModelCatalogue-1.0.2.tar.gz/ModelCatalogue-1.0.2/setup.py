from setuptools import setup, find_packages
import os
from ModelCatalogue import __version__

# See: https://wiki.disneystreaming.com/display/DEVX/2021/01/26/Python+Package+Publishing+Step+Available+in+Norfolk
pypi_prefix: str = os.getenv("PYPI_PREFIX")
package_name: str = (
    f"{pypi_prefix}.ModelCatalogue" if pypi_prefix else "ModelCatalogue"
)


setup(
    name=package_name,
    packages=find_packages(),
    version=__version__,
    description="Convenient tools for the Data Science Subscriber team.",
    long_description="Check out the README.md!",
    python_requires='>=3.7',
    author='Huijae (Jay) Kim',
    author_email='huijae.kim@disneystreaming.com'
)

