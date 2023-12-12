from time import time
import setuptools
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
setuptools.setup(
    name="proof-report-parser",
    version="0.9.8",
    author="happy2wh",
    author_email="no@gmail.com",
    description="解析”全国防雷减灾综合管理服务平台“的docx格式检测报告",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://pypi.org/project/proof-report-parser/",
    # project_urls={
    #     "Bug Tracker": "https://github.com/pypa/sampleproject/issues",
    # },
    install_requires=["python-docx"],
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)