from setuptools import setup, find_packages

setup(
    name="fitgirl_cli",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["rich", "httpx"],
    
    entry_points={
        "console_scripts": ["fitgirl=main:main"],
    },
    author="Your Name",
    description="A terminal-based CLI for FitGirl Repacks links",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
