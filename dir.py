###  要修改线程(默认25),最大超时时间(7.5)等等之类的可以在 dirsearch项目中config.ini修改
### 需在同目录下创建读取目标的target.txt以及存放结果的 result目录

import os

# 读取目标文件并执行命令
def run():
    target = []
    with open("target.txt","r") as f:
            for line in f.readlines():
                line=line.strip('\n')
                target.append(line)
    for i in target:
        #文件保存到result/目标.csv
        url=f"python3 dirsearch.py -u '{i}' -i 200 201 400 403 500 -o ./result/{i}.csv --format=csv"
        #print(url)
        os.system(url)

if __name__=="__main__":
    run()
