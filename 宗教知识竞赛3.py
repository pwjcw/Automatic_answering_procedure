import re
import json
from bs4 import BeautifulSoup
from lxml import etree
from selenium import webdriver
import demjson
from jsonpath import jsonpath
import difflib    #比较字符串的库
import time
dirve=webdriver.Chrome(executable_path="chromedriver.exe")
def replaceSpace(str):
    # 剔除字符串的
    try:
        return str.replace(' ', '').replace('\n', '').replace('\r', '').replace('\t', '')
    except Exception as e:
        return str
def get_equal_rate_1(str1, str2):        #定义比较字符串相似度的函数
   return difflib.SequenceMatcher(None, str1, str2).quick_ratio()
with open("F:\桌面文件\python宗教知识答题\河南省大学生中国特色社会主义民族宗教理论知识竞赛系统2.html",encoding='utf-8') as f:
    data=f.read()
    # print("{}".format(data))
    html = etree.HTML(data)
    soup = BeautifulSoup(data, 'lxml')
    list_id=[]
    m =soup.find_all('tr')   #获取网页中存储题目id的标签
    # all_font=soup.find_all('font')   #获取网页中的题目
    # for i in all_font:
    #     font=i.string
    #     print(font)
    all_problem=[]
    all_name_problem=html.xpath("//div[@class=\"widget-right-con\"]/div/table/tbody/tr/th/font/text()")   #通过xpath获取所有题目
    for i in all_name_problem:
        name_problem=replaceSpace(i)     #删除列表中的多余元素
        all_problem.append(name_problem)        #将处理后的题目添加到all_problem列表中
    # print(all_problem)
    for n in m:
        c=n.get('id')     #获取标签中对应的id属性
        # print(c)
        list_id.append(c)
    list_id=list(set(list_id))     #删除id中的重复元素
    list_id.pop(81)    #删除多余元素None
    # print(list_id)
obj = json.load(open("F:\桌面文件\python宗教知识答题\民族宗教答案.json", 'r', encoding='utf8'))   #导入题库
id=jsonpath(obj,"$..id")   #获取答案中题号中的id
name=jsonpath(obj,"$..question_txt")   #获取题库中的题目字段
answer_txt=jsonpath(obj,"$..answer_txt")    #获取题库中正确答案的字段
answer0=jsonpath(obj,"$..answer")   #获取答案中的选项
# print(name)
def selenium_choice():
    Serial_number = html.xpath("/html/body/div[2]/div[2]/div/div/div[2]/ul/li/text()")   #获取到题的序号
    dirve.get("F:\桌面文件\python宗教知识答题\河南省大学生中国特色社会主义民族宗教理论知识竞赛系统2.html")  #调用selenium进行点击
    dirve.maximize_window()     #将浏览器最大化
    sum2 = 1
    while sum2 <= 10:
        dirve.find_element_by_xpath("/html/body/div[2]/div[2]/div/div/div[2]/ul/li[{}]".format(sum2)).click()   #依次点击题号跳转到题目，这样才能进行点击操作
        for i in all_problem:
            for n in name:  # 遍历网页中的题目与题库中的题，然后去对比字符串的相似度，大于80%则认为是同一题
                sum = get_equal_rate_1(i, n)
                if sum >= 0.8:
                    # print(n)
                    sum3=name.index(n)  #获取题库中该题目对应的下标
                    # print(sum3)
                    answer1=answer0[sum3]          #通过该下标找到该题对应的选项
                    # print(answer1)
                    dirve.find_element_by_xpath("//*[@id=\"hmui-grid\"]/tbody/tr//td[@width=\"30\"]/input[@value=\"{}\"]".format(answer1)).click()      #找到该选项对应的点击按钮进行点击
        sum2 += 1
        # time.sleep(2)

selenium_choice()

