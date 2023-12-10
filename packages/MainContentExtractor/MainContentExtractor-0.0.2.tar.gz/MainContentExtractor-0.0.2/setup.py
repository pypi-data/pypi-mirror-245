from setuptools import setup, find_packages

setup(
    name="MainContentExtractor",
    version="0.0.2",
    author="HawkClaws",
    packages=find_packages(),
    install_requires=[
        "trafilatura>=1.6.2",
        "html2text>=2020.1.16",
        "beautifulsoup4>=4.12.2",
    ],
    python_requires=">=3.6",
    include_package_data=True,
    url="https://github.com/HawkClaws/main_content_extractor",
    project_urls={"Source Code": "https://github.com/HawkClaws/main_content_extractor"},
    license="MIT",
)
