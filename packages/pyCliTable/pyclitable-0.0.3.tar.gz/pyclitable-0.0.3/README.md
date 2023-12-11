# Introduction

"pyCliTable" is a Python package designed to simplify the display of data in a tabular format within the command-line interface (CLI). This package offers an intuitive and user-friendly way to present structured data, making it easy for developers and users to visualize information neatly organized into rows and columns. With customizable styling options, "pyCliTable" streamlines the process of creating tables, enhancing the readability and presentation of data for CLI applications.

Additionally, the intelligent algorithm within pyCliTable detects missing data within a specific row and seamlessly replaces it with `*****`, ensuring a continuous, polished presentation of your data. This feature seamlessly integrates into its functionality, allowing pyCliTable to maintain its magic throughout.

![pyCliTable image example.](/images/img2.png)

### Installation:

`pip install pyCliTable`
Or see https://pypi.org/project/pyCliTable/

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

result = pyCliTable.table(data=data, config=config, table_color="red", header_config=header_config, word_space=1)

print(result)
```

The following are the valid values for `config` and and `header_config` arguments.

```
config = ["red", "green", "yellow", "blue", "magenta", "cyan", "white", "underline", "bold", "italy"]
```
