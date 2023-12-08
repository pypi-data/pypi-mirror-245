# docx-2-html

A package to convert docx files to html with added features on top of mammoth library.

Developed by Paras Jain (c) 2023

## Features

- Added support for all-types of images.
- Images like .emf are converted to .png type.
- Image dimensions present in the file are converted for html with preset same width and height.

**Note**
To convert .emf image types to .png, linux env is necessary with inkscape installed.

## Examples of How To Use

Convert docx to html

```python
from docx2html.convert import docx_to_html

html = docx_to_html("your_docx_filepath_here", is_convert)
```

- your_docx_filepath_here: Your docx file path
- is_convert: is a boolean to convert .emf imgs to .png
