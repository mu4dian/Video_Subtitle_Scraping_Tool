import os
import json
import requests

# 模拟浏览器请求头
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
}


def fetch_json(url, timeout=10):
    """
    根据给定 URL 下载 JSON 数据并解析为 Python 对象，
    出错时返回 None。
    """
    try:
        response = requests.get(url, headers=HEADERS, timeout=timeout)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"下载或解析 {url} 时出错：{e}")
        return None


def process_subtitles(json_data):
    """
    从 JSON 数据中提取字幕内容：
      - 遍历 JSON 数据中 "body" 列表，取出每条记录的 "content"。
      - 如果字幕末尾没有标点（“，”、“。”、“！”、“？”），则自动添加句号。
      - 将所有字幕内容用空格连接成一段文本。
    返回处理后的字幕文本。
    """
    if not json_data:
        return ""
    body = json_data.get("body", [])
    subtitles = []
    for item in body:
        content = item.get("content", "").strip()
        if content:
            if content[-1] not in "，。！？":
                content += "。"
            subtitles.append(content)
    return " ".join(subtitles)


def main():
    input_file = "input.txt"
    output_file = "output.txt"

    if not os.path.exists(input_file):
        print(f"文件 {input_file} 不存在。")
        return

    # 从 input.txt 中读取每个 URL（忽略空行）
    with open(input_file, 'r', encoding='utf-8') as f:
        urls = [line.strip() for line in f if line.strip()]

    results = []  # 保存每个 URL 处理后的段落
    for idx, url in enumerate(urls, start=1):
        print(f"正在处理第 {idx} 个 URL：{url}")
        json_data = fetch_json(url)
        subtitle_text = process_subtitles(json_data)
        if subtitle_text:
            # 在整个段落前添加序号
            block = f"{idx}. {subtitle_text}"
            results.append(block)
        else:
            print(f"未从 {url} 提取到字幕文本。")

    # 将所有段落写入 output.txt，每个段落一行
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("\n".join(results))
        print(f"所有字幕已整理并保存到 {output_file}")
    except Exception as e:
        print(f"写入文件 {output_file} 时出错：{e}")


if __name__ == "__main__":
    main()
