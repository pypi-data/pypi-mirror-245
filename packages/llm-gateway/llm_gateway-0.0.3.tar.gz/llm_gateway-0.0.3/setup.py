from setuptools import find_packages, setup

PACKAGE_NAME = "llm_gateway"

setup(
    name=PACKAGE_NAME,
    version="0.0.3",
    description="This is LLM Gateway package",
    packages=find_packages(),
    entry_points={
        "package_tools": ["llm_gateway_tool = llm_gateway.tools.utils:list_package_tools"],
    },
    include_package_data=True,   # This line tells setuptools to include files from MANIFEST.in
    extras_require={
        "azure": [
            "azure-ai-ml>=1.11.0,<2.0.0"
        ]
    },
)