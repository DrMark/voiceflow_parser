from setuptools import setup, find_packages

setup(
    name="voiceflow_parser",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "click>=8.1.3",
        "rich>=13.4.2",
        "pydantic>=2.4.0",
    ],
    entry_points={
        "console_scripts": [
            "voiceflow-parser=voiceflow_parser.cli:cli",
        ],
    },
    python_requires=">=3.8",
    description="A tool to parse Voiceflow exports and generate project files",
)
