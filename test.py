# sk-fda0f63f9d8c484a911ca6b34d718013

import os
from openai import OpenAI

client = OpenAI(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
    api_key="sk-fda0f63f9d8c484a911ca6b34d718013",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)
completion = client.chat.completions.create(
    model="deepseek-r1", # 此处以 deepseek-r1 为例，可按需更换模型名称。
    messages=[
        {'role': 'user', 'content': '生成一个零基础认识电子元器件的教程，注意，是完整的教程内容，不是大纲，不能省略中间章节，要包含每一个小结内容，用户是一个大学生，要尽可能的详细，内容由浅入深，内容尽可能的丰富，要生成完整的内容，要具有一定的专业性，文字不少于100000字，要包含以下的内容：01 基础元器件和电阻02 基础元器件：电容器03 基础元器件：电感04 基础元器件：保险05 基础元器件：二极管0608 基础元器件+蜂鸣器10 基础元器件+电阻提高篇11 基础元器件+电感提高篇-变压器12 基础元器件+二极管提高篇-整流桥13 基础元器件+IGBT14 基础元器件+电源转换器件15 基础元器件+晶振16 基础元器件+继电器17 基础元器件+光耦18 基础元器件+缓冲器19 基础元器件+触发器20 基础元器件+计数器21 基础元器件-AD DA转换器22 基础元器件+隔离放大器23 基础元器件+运放24 基础元器件+电压基准源25 基础元器件+555定时器'}
        ],
    stream=True
    )

# 定义完整思考过程
reasoning_content = ""
# 定义完整回复
answer_content = ""
for chunk in completion:
    # 获取思考过程
    reasoning_chunk = chunk.choices[0].delta.reasoning_content
    # 获取回复
    answer_chunk = chunk.choices[0].delta.content
    # 如果思考过程不为空，则打印思考过程
    if reasoning_chunk != "":
        print(reasoning_chunk,end="")
        reasoning_content += reasoning_chunk
    # 如果回复不为空，则打印回复。回复一般会在思考过程结束后返回
    elif answer_chunk != "":
        print(answer_chunk,end="")
        answer_content += answer_chunk
print(f"\n完整思考过程：{reasoning_content}")
print(f"完整的回复：{answer_content}")