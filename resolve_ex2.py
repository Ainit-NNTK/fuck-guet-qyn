import json
import requests
import os
import time
all_json_responses = []

url="http://guettx3.gstar-info.com:6060/api/QuestionBank/GetQuesList?CourseExperId=64336e35985ed506e83b1561&CourseNo=TXYL-24%E5%B9%B4%E6%98%A5&QNumber=10&usageScenario=1"
question_array = []

with open("questions2.md", "w", encoding="utf-8") as file:
    for i in range(35):
        response = requests.get(url)
        if response.status_code == 200:
            # 解析JSON数据并存储到列表中
            json_data = response.json()
                # 遍历题目信息
            for question_info in json_data["Result"]:
                # 获取题目信息
                question = question_info["Question"]
                #time.sleep(1)
                if not question in question_array:
                    question_array.append(question)
                    if "有图" in question:
                        start_index = question.find("<p>") + 3
                        end_index = question.find("</p><p>", start_index)
                        question_sim = question[start_index:end_index]
                        #
                        #pic to markdown
                        start_index = question.find("src=\"") + 5
                        end_index = question.find("\"", start_index)
                        image_url = question[start_index:end_index]
                        image_name = os.path.basename(image_url)
                        print(f"question: {question}")
                        print(f"图片URL {image_url}")
                        #print(f"图片 {image_name}")
                        #file.write("question:" + question + "\n")
                        file.write("题目：" + question_sim + "\n")
                        file.write("![](./img/" + image_name + ")\n")
                        markdown_image_link = f"![alt text]({image_url})"
                        #   
                        if "http" in image_url:
                            response = requests.get(image_url)
                            with open(f"./img/{image_name}", "wb") as img_file:
                                img_file.write(response.content)
                            print(f"图片 {image_name} 已保存成功")
                        else:
                            print("no pic")
                    else:
                        question_sim=question
                        file.write("题目：" + question_sim + "\n")
                    options = {
                        "A": question_info["OptionA"],
                        "B": question_info["OptionB"],
                        "C": question_info["OptionC"],
                        "D": question_info["OptionD"]
                    }
                    answer = question_info["Answer"]

                    #file.write("选项：\n")
                    for option, text in options.items():
                        if not text:
                            file.write(f"{option}: {text}\n")
                        elif "<p>" in text:
                            start_index = text.find("<p>") + 3
                            end_index = text.find("</p>", start_index)
                            option_text = text[start_index:end_index]
                            file.write(f"{option}: {option_text}\n")
                        else:
                            file.write(f"{option}: {text}\n")
                    file.write("答案：" + answer + "\n\n")
        else:
            print(f"Request to {url} failed with status code: {response.status_code}")

