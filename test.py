import os

content = ""

with open('./test.md') as f:
    content = f.read()

result = "sknkdsnck"
content = "content=f\"" + content + "\""
print(content)
# content = f"{reslut}"
exec(content)
print(content)
