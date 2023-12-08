# Introduction

"pyCliTable" is a Python package designed to simplify the display of data in a tabular format within the command-line interface (CLI). This package offers an intuitive and user-friendly way to present structured data, making it easy for developers and users to visualize information neatly organized into rows and columns. With customizable styling options, "pyCliTable" streamlines the process of creating tables, enhancing the readability and presentation of data for CLI applications.

### Installation:
`pip install pyCliTable`

### Example:
```
from pyclitable import pyCliTable

data = [
    {
        "ID": ["1", "2", "3"]
    },
    {
        "NAME": ["John", "Doe", "Quick"]
    },
    {
        "LOCATION": ["Foobar Foobar Foobar", "Foobar Foobar", "Foobar"]
    },
    {
        "INTRODUCTION": [
            "Hello! My name is John Doe and I'm from the bustling city of New York.",
            "I have a passion for technology and enjoy exploring the diverse cultures that thrive in this vibrant city.",
            "As a software engineer, I'm dedicated to creating innovative solutions that impact people's lives positively."
        ]
    }
]

config = ["Green", "italic"]
header_config = ["bold", "red"]
result = pyCliTable.table(data=data, header_config=header_config, word_space=1)
print(result)
```

The following are the valid values for `config` and and `header_config` arguments.
```
config = ["red", "green", "yellow", "blue", "magenta", "cyan", "white", "underline", "bold", "italy"]
```