import os
import setuptools

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

classifiers = [
    "Development Status :: 4 - Beta",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Operating System :: OS Independent",
]

main = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(main, "requirements.txt"), "r", encoding="utf-8") as f:
    requirements = f.read().splitlines()

about = {}
with open(
    os.path.join(main, "tumblr_scraper", "__version__.py"), "r", encoding="utf-8"
) as f:
    exec(f.read(), about)

setuptools.setup(
    name=about["__title__"],
    version=about["__version__"],
    author=about["__author__"],
    author_email=about["__author_email__"],
    description=about["__description__"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=about["__url__"],
    license=about["__license__"],
    packages=setuptools.find_packages(),
    classifiers=classifiers,
    keywords=["tumblr", "scraper", "download", "images", "videos"],
    install_requires=requirements,
    python_requires=">=3.7",
    zip_safe=False,
    entry_points={"console_scripts": ["tumblr-scraper=tumblr_scraper.main:main"]},
    project_urls={"Source": "https://github.com/giosali/tumblr-scraper"},
)
