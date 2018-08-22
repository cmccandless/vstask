import setuptools
from vstask.__version__ import VERSION

if __name__ == '__main__':
    with open("README.md", "r") as fh:
        long_description = fh.read()

    setuptools.setup(
        name="vstask",
        version=VERSION,
        author="Corey McCandless",
        author_email="crm1994@gmail.com",
        description=(
            "CLI for VSCode tasks"
        ),
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/cmccandless/vstask",
        packages=setuptools.find_packages(),
        classifiers=(
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ),
        entry_points={
            'console_scripts': [
                'vstask = vstask.vstask:main'
            ],
        },
        install_requires=[],
        include_package_data=True
    )
