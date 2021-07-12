import requests
import pymysql
import json
import time
import re
import os

url = "https://mnks.jxedt.com/get_question?r=0.46514869467754005&index={}"
db = pymysql.connect(host="", user="", password="", database="")
cursor = db.cursor()

def loads_str(data_str):
    try:
        result = json.loads(data_str)
        print("最终json加载结果：{}".format(result))
        return result
    except Exception as e:
        print("异常信息e：{}".format(e))
        error_index = re.findall(r"char (\d+)\)", str(e))
        if error_index:
            error_str = data_str[int(error_index[0])]
            data_str = data_str.replace(error_str, "<?>")
            print("替换异常字符串{} 后的文本内容{}".format(error_str, data_str))
            # 该处将处理结果继续递归处理
            return loads_str(data_str)

for i in range(1, 3934):
    # 请求链接
    response = requests.get(url.format(i))
    # 加载数据，过滤escape
    question_data = loads_str(response.text)
    print("正在爬取链接：{}".format(url.format(i)))

    # 如果题目中有图片，进行图片的爬取
    if question_data["imageurl"]:
        print("监测到题目中含有图片，正在爬取...")
        pic_response = requests.get(question_data["imageurl"])
        pic_name = question_data["imageurl"].split("/")[-1][0:-4]
        with open("/www/wwwroot/qr.nothamor.cn/questions/{}.jpg".format(pic_name), "wb+") as pic:
            pic.write(pic_response.content)
        question_data["imageurl"] = "https://xxx.com/{}.jpg".format(pic_name)

    print("正在爬取第{}道题，id为{}, 题目为{}, 答案为：{}".format(i, question_data["id"], question_data["question"], question_data["ta"]))
    sql = """insert into questions(question, a, b, c, d, ta, imageurl, bestanswer, bestanswerid, type, sinaimg, options)
    values("{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}")
    ;""".format(question_data["question"], question_data["a"], question_data["b"], question_data["c"], question_data["d"], question_data["ta"], question_data["imageurl"], question_data["bestanswer"], question_data["bestanswerid"], question_data["Type"], question_data["sinaimg"], question_data["options"])
    # with open("./question{}.json".format(i), "wb+") as file:
    #     file.write(response.text.encode())
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
    except:
        # 如果发生错误则回滚
        db.rollback()