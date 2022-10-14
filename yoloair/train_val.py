# 南京邮电大学
# 韩世豪
# 开发时间: 2022/9/21 17:24
import random

f = open('all_country.txt', "r")
image_list = f.readlines()
f.close()
f = open('val.txt', "w")
val_percent = 0.1
num = len(image_list)
list_index = range(num)
val_num = int(num * val_percent)
val_index = random.sample(list_index, val_num)
for i in val_index:
    f.write(image_list[i])
f.close()
print('success')
