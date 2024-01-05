import requests
from config import user, project
'''
    很奇怪，v1的版本和去掉v1后的URL返回的JSON内容不一样
    同时，我理解的pulls.json是一个总体的PR信息
    而pulls/1.json是第一个PR的信息
    但是pulls/1.json和pulls.json列表的第一个内容不一样

    我发现pulls.json列表是按照时间顺序进行的，并且最多可以显示20个PR
    所以我决定只用pulls.json的内容
'''

def get_pr_len(user, project):
    # 获取PR的数量
    url = f'https://www.gitlink.org.cn/api/{user}/{project}/pulls.json'
    response = requests.get(url).json()
    issues = response["issues"]
    return len(issues)

def get_pr_time(user, project):
    # 获取PR的创建时间，单位是秒，返回一个列表
    len = get_pr_len(user, project)
    pr_time = []
    url = f'https://www.gitlink.org.cn/api/{user}/{project}/pulls.json'
    response = requests.get(url).json()
    for id in range(len):
        raw_pr_time = response["issues"][id]["pr_time"]
        if("秒前" in raw_pr_time):
            real_pr_time = int(raw_pr_time.replace("秒前", ""))
        elif("分钟前" in raw_pr_time):
            real_pr_time = int(raw_pr_time.replace("分钟前", "")) * 60
        elif("小时前" in raw_pr_time):
            real_pr_time = int(raw_pr_time.replace("小时前", "")) * 60 * 60
        elif("天前" in raw_pr_time):
            real_pr_time = int(raw_pr_time.replace("天前", "")) * 60 * 60 * 24
        elif("个月前" in raw_pr_time):
            real_pr_time = int(raw_pr_time.replace("个月前", "")) * 60 * 60 * 24 * 30
        elif("年前" in raw_pr_time):
            real_pr_time = int(raw_pr_time.replace("年前", "")) * 60 * 60 * 24 * 30 * 12
        pr_time.append(real_pr_time)
    return pr_time


if __name__ == "__main__":
    url = f'https://www.gitlink.org.cn/api/{user}/{project}/pulls.json'
    print(get_pr_time(user, project))

