from add_one_babu import example
# from pyclitable import pyCliTable
import pyCliTable

header_data = [
    {"Name":
        [
            "Alice", "Bob", "Clara", "David", "Emma", "Frank", "Grace", "Henry", "Ivy", "Jack",
            "Victor", "Wendy", "Xavier", "Yara", "Zach", "Ava", "Ethan", "Sophia", "Mason", "Isabella"
        ]},
    {"Surname":
        [
            "Smith", "Johnson", "Williams", "Jones", "Brown", "Davis", "Miller", "Wilson", "Moore", "Taylor",
            "Anderson", "Thomas", "Jackson", "White", "Harris", "Martin", "Thompson", "Garcia", "Martinez", "Lee"
        ]},
    {"Gender":
        [
            "Male", "Female", "Male", "Female", "Male", "Female", "Male", "Female", "Male", "Female",
            "Male", "Female", "Male", "Female", "Male", "Female", "Male", "Female", "Male", "Female"
        ]},
    {"Location": [
        "New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia", "San Antonio", "San Diego",
        "Dallas", "San Jose", "Austin", "Jacksonville", "San Francisco", "Indianapolis", "Seattle", "Denver",
        "Washington", "Boston", "El Paso", "Nashville"
    ]},
    {"INTRODUCTION": [
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed placerat ",
        "Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis ",
        "Cras vitae sapien velit. Fusce ullamcorper, eros ut hendrerit rhoncus, risus risus convallis massa,",
        "Nulla facilisi. Integer hendrerit nulla et arcu venenatis, eget pellentesque arcu ",
        "Vestibulum eu mauris nec ligula pulvinar suscipit vitae ac lorem. Maecenas efficitur  dictum.",
        "Fusce vehicula placerat risus, sed ultricies purus gravida ac. Suspendisse at mi a ex in euismod est.",
        "Praesent vestibulum velit nec leo condimentum, a tincidunt metus cursus. Donec consec orci eget erat .",
        "Ut sit amet commodo odio. Integer fermentum lobortis libero nec vestibulum. Curabitur.",
        "In hac habitasse platea dictumst. Vivamus eget mi dignissim, fermentum purus vitae, c odio.",
        "Etiam id massa ac sapien placerat vestibulum. Vestibulum ac urna fringilla, condiment dolor at  .",
        "Morbi rhoncus dolor vitae justo varius, eget hendrerit odio consequat. Integer eget i sed tempo .",
        "Nam ornare fermentum dui, quis placerat est interdum nec. Aliquam a dui vel ipsum ele ante. Sed.",
        "Aliquam erat volutpat. Integer lacinia, lacus vitae bibendum lobortis, odio elit conv urna.  feugiat.",
        "Vestibulum hendrerit, felis sit amet tempor varius, nulla mi ultricies urna, quis con in ris, congue nulla.",
        "Mauris euismod eros sed libero fringilla, id rhoncus mauris sagittis. Proin .",
        "Fusce quis luctus quam. Sed et elit eu nunc vestibulum feugiat. Sed commodo",
        "Suspendisse potenti. Sed vel fermentum felis. Integer malesuada urna velit,  efficitur.",
        "Efficitur viverra. Curabitur sit amet elit nec ni. Integer malesuada urna velit,  efficitur.",
        "Praesent eget mi ac elit efficitur viverra. Curabitur sit amet elit nec nisi efficitur faucibus, .",
        "Vivamus in consequat libero. Nulla facilisi. Sed a metus vel dolor efficitur venenatis sapien cur .",
    ]
    }]

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


config = ["Cyan", "italic"]
header_config = ["bold", "Magenta", 'italic']
result = pyCliTable.table(
    data=header_data, header_config=header_config, word_space=1)
print(result)
