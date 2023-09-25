import json
from bs4 import BeautifulSoup

# Your JSON array
json_array = [
    {'StrContent': 'This is a valid entry', 'StrTalker': 'user1'},
    {'StrContent': '<?xml version="1.0"?><msg><img>', 'StrTalker': 'user2'},
    {'StrContent': '<div>This is another invalid entry</div>', 'StrTalker': 'user3'},
    {'StrContent': 'Another valid entry', 'StrTalker': 'user4'},
]

# List to store valid entries
valid_entries = []

for item in json_array:
    content = item['StrContent']
    soup = BeautifulSoup(content, 'html.parser')
    if not soup.find():
        valid_entries.append(item)

# Print valid entries
for item in valid_entries:
    print(item)