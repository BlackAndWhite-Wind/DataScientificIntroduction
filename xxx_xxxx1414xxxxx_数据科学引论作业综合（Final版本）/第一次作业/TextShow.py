import pandas as pd  # 导入pandas包

data = pd.read_csv("txttest.csv")  # 读取csv文件
print(data)  # 打印所有文件

# 使用pandas读取结果（跟excel好像。。）
#   name1 name2 name3
# 0   aaa   bbb   ccc
# 1   xxx   yyy   zzz



import csv

with open('txttest.csv', 'r') as f:
    reader = csv.reader(f)
    print(type(reader))

    for row in reader:
        print(row)

# 使用csv读取结果
# ['name1', 'name2', 'name3']
# ['aaa', 'bbb', 'ccc']
# ['xxx', 'yyy', 'zzz']
