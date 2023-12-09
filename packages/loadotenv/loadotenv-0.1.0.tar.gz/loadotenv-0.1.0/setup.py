from setuptools import setup, find_packages

with open("README.md") as readme_file:
    long_desc = readme_file.read()

setup(
    name="loadotenv",
    version="0.1.0",
    author="Jarlem Red J. de Peralta",
    author_email="lmoa.jhdp@gmail.com",
    description="Reinventing the wheel to load .env variables",
    long_description=long_desc,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    python_requires=">=3.6",
    keywords=".env environment utility"
)
