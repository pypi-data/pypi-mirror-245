from add_one_babu import example
from pyclitable import pyCliTable

header_data = [
    {"Name":
        ["Babucarr", "Ali", "Omar"]},
    {"Surname":
        ["Badjie", "Bah", "Badjie Badjie Badjie Badjie"]},
    {"Gender":
        ["Male", "Female", "Male",]},
    {"Location": ["Tal", "Kotu", "Ba"]}]

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

print(example.add_one(3))
