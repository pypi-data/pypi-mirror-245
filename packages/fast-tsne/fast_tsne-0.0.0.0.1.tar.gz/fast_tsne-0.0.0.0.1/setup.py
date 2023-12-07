import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fast_tsne",
    version="0.0.0.0.1",
    author="Wangchen",
    author_email="wch_bioinformatics@163.com",
    description="fast-tsne: A mainfold method for visualizing single-cell data .",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wangzichenbioinformatics/fast-tsne",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
)
