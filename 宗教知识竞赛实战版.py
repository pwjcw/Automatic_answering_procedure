# coding=utf-8
import re
import json
from bs4 import BeautifulSoup
from lxml import etree
from selenium import webdriver
import demjson
from jsonpath import jsonpath
import difflib    #比较字符串的库
import time
from lxml.html import fromstring, tostring
dirve=webdriver.Chrome(executable_path="chromedriver.exe")
def replaceSpace(str):
    # 剔除字符串的
    try:
        return str.replace(' ', '').replace('\n', '').replace('\r', '').replace('\t', '')
    except Exception as e:
        return str
def get_equal_rate_1(str1, str2):        #定义比较字符串相似度的函数
   return difflib.SequenceMatcher(None, str1, str2).quick_ratio()
# with open("F:\桌面文件\河南省大学生中国特色社会主义民族宗教理论知识竞赛系统2.html",encoding='utf-8') as f:
#     data=f.read()
dirve.get("http://exam.hm86.cn/vip/login/login.php")  # 调用selenium进行点击
dirve.find_element_by_xpath("//*[@id=\"useraccount\"]").send_keys()   #填写账号
dirve.find_element_by_xpath("//*[@id=\"password\"]").send_keys("")   #填写密码
time.sleep(20)
data=dirve.page_source
html = etree.HTML(data)
all_name_problem = html.xpath(
        "//div[@class=\"widget-right-con\"]/div/table/tbody/tr/th/font/text()")  # 通过xpath获取所有题目
all_problem=[]
for i in all_name_problem:
    name_problem=replaceSpace(i)     #删除列表中的多余元素
    all_problem.append(name_problem)        #将处理后的题目添加到all_problem列表中
print(all_problem)
obj = json.load(open("F:\桌面文件\民族宗教答案.json", 'r', encoding='utf8'))  # 导入题库
name = jsonpath(obj, "$..question_txt")  # 获取题库中的题目字段
answer_txt = jsonpath(obj, "$..answer_txt")  # 获取题库中正确答案的字段
answer0 = jsonpath(obj, "$..answer")  # 获取答案中的选项
def selenium_click():
    dirve.maximize_window()  # 将浏览器最大化
    sum5=1
    sum6=0
    for i in all_problem:
        for m in name:
            Similarity=get_equal_rate_1(i,m)
            if Similarity>0.7:
                sum6+=1
                sum3 = name.index(m)  # 获取题库中该题目对应的下标
                answer1 = answer0[sum3]  # 通过该下标找到该题对应的选项
                answer1 = list(answer1)
                print(sum5,i,answer1)
                dirve.find_element_by_xpath(
                    "/html/body/div[2]/div[2]/div/div/div[2]/ul/li[{}]".format(sum5)).click()  # 依次点击题号跳转到题目，这样才能进行点击操作
                for answer2 in answer1:
                    dirve.find_element_by_xpath("//td[@width=\"30\"]/input[(@value=\"{}\") and @orderindex=\"{}\"]".format(answer2,sum5)).click()
                sum5+=1
                break
        else:
            dirve.find_element_by_xpath(
                "/html/body/div[2]/div[2]/div/div/div[2]/ul/li[{}]".format(sum5)).click()
            # print(sum2)
            sum5+=1
    print(sum6)
selenium_click()