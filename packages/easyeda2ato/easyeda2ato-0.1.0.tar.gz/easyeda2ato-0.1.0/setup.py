from setuptools import find_packages, setup

with open("README.md") as fh:
    long_description = fh.read()

production_dependencies = ["pydantic>=2.0.0", "requests>2.0.0"]

development_dependencies = [
    "pre-commit>=2.17.0",
]

with open("requirements.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(production_dependencies + development_dependencies))

setup(
    name="easyeda2ato",
    description=(
        "A Python package for converting electronic components from LCSC or EasyEDA to"
        " ato files, facilitating integration with Kicad libraries."
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    version="0.1.0",  # Updated version
    author="Narayan Powderly",
    author_email="napowderly@gmail.com",  # Consider adding your email
    url="https://github.com/your-username/easyeda2ato",  # Update your fork's URL
    project_urls={
        "Code": "https://github.com/your-username/easyeda2ato",  # Update your fork's URL
    },
    # download_url='',  # Optional: you can provide a direct download URL if desired
    license="AGPL-3.0",  # Ensure this is the license you want
    py_modules=["easyeda2ato"],  # Update module name if necessary
    platforms="any",
    packages=find_packages(exclude=["tests", "utils"]),
    package_dir={"easyeda2ato": "easyeda2ato"},  # Update if the directory structure has changed
    entry_points={"console_scripts": ["easyeda2ato = easyeda2ato.__main__:main"]},  # Update if the entry point has changed
    python_requires=">=3.6",
    install_requires=production_dependencies,
    extras_require={"dev": development_dependencies},
    zip_safe=False,
    keywords="easyeda ato kicad library conversion",  # Update keywords
    classifiers=[
        # Update classifiers if necessary
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Electronic Design Automation (EDA)",
    ],
)
