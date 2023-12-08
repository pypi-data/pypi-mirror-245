from setuptools import setup, find_packages

VERSION = "0.0.1"
DESCRIPTION = "Convert docx files to html"

# Setting up
setup(
    name="html4docx",
    version=VERSION,
    author="Paras Jain",
    author_email="<paras.2426@gmail.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=["mammoth", "beautifulsoup4", "python-docx"],
    keywords=[
        "python",
        "docx",
        "html",
        "docx-2-html",
        "docx2html",
        "docx-to-html",
        "convert",
        "docx_to_html",
        "html4docx"
    ],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
)
