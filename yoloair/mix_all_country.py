# 南京邮电大学
# 韩世豪
# 开发时间: 2022/10/2 18:01
import os
import pandas as pd
import glob

csv_list = glob.glob('*.csv')  # 查看同文件夹下的csv文件数
print(u'共发现%s个CSV文件' % len(csv_list))
print(u'正在处理............')
for i in csv_list:  # 循环读取同文件夹下的csv文件
    fr = open(i, 'rb').read()
    with open('result.csv', 'ab') as f:  # 将结果保存为result.csv
        f.write(fr)
print(u'合并完毕！')
