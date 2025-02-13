import os
import time
import threading
import concurrent.futures
from openai import OpenAI
from tqdm import tqdm  # 用于显示进度条

# -------------------------------
# 参数设置：请根据实际情况调整
# -------------------------------
SUBTITLES_FILE = 'subtitles.txt'  # 字幕文件路径，每行对应一条字幕（即一集视频的字幕）
OUTPUT_MARKDOWN = 'tutorial_notes.md'  # 最终生成的 Markdown 文件路径
MAX_WORKERS = 12  # 并发线程数，利用20核 CPU

# 限流参数（每分钟调用次数和 Token 消耗上限）
QPM_LIMIT = 12000
TPM_LIMIT = 900000

# -------------------------------
# 初始化 OpenAI 客户端（远程调用 deepseek-r1 模型）
# -------------------------------
client = OpenAI(
    api_key="sk-fda0f63f9d8c484a911ca6b34d718013",  # 请确保已配置环境变量中的 API Key
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)


# -------------------------------
# 速率控制器：限制每分钟的 API 调用次数和 Token 消耗
# -------------------------------
class RateLimiter:
    def __init__(self, qpm, tpm):
        self.qpm = qpm
        self.tpm = tpm
        self.lock = threading.Lock()
        self.start_time = time.time()
        self.calls = 0
        self.tokens_used = 0

    def check_limit(self, tokens_needed):
        with self.lock:
            current_time = time.time()
            elapsed = current_time - self.start_time
            if elapsed > 60:
                self.start_time = current_time
                self.calls = 0
                self.tokens_used = 0
            if self.calls >= self.qpm or (self.tokens_used + tokens_needed) > self.tpm:
                sleep_time = 60 - elapsed
                print(f"[{time.strftime('%H:%M:%S')}] 达到限流条件，暂停 {sleep_time:.2f} 秒")
                time.sleep(sleep_time)
                self.start_time = time.time()
                self.calls = 0
                self.tokens_used = 0
            self.calls += 1
            self.tokens_used += tokens_needed


# 全局速率控制器
rate_limiter = RateLimiter(QPM_LIMIT, TPM_LIMIT)


# -------------------------------
# 读取字幕文件
# -------------------------------
def read_subtitles(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        subtitles = [line.strip() for line in f if line.strip()]
    print(f"[{time.strftime('%H:%M:%S')}] 检测到 {len(subtitles)} 条字幕")
    return subtitles


# -------------------------------
# 调用 deepseek-r1 模型生成笔记（流式输出）
# -------------------------------
def generate_notes(subtitle):
    # 输出正在处理的字幕简要信息（仅打印前30个字符）
    print(f"[{time.strftime('%H:%M:%S')}] 正在处理字幕: {subtitle[:30]}...")
    # 简单以词数估计 Token 数量（可根据需要替换为更准确的分词方式）
    tokens_estimate = len(subtitle.split())
    rate_limiter.check_limit(tokens_estimate)

    messages = [{'role': 'user', 'content': subtitle}]

    # 发起流式调用
    stream = client.chat.completions.create(
        model="deepseek-r1",
        messages=messages,
        stream=True
    )

    reasoning_content = ""
    answer_content = ""

    try:
        for chunk in stream:
            delta = chunk.choices[0].delta
            if hasattr(delta, 'reasoning_content') and delta.reasoning_content:
                reasoning_content += delta.reasoning_content
            if hasattr(delta, 'content') and delta.content:
                answer_content += delta.content
    except Exception as e:
        print(f"[{time.strftime('%H:%M:%S')}] 处理字幕时发生异常: {subtitle[:30]}... 异常信息: {e}")

    # 这里返回的字典中包含推理过程和最终生成的笔记
    return {"summary": reasoning_content, "notes": answer_content}


# -------------------------------
# 整合所有生成的笔记，保存为 Markdown 文件
# -------------------------------
def generate_markdown(notes_list, output_file):
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("# 视频教程合集笔记\n\n")
        for idx, notes in enumerate(notes_list, start=1):
            f.write(f"## 第{idx}集：视频标题\n")
            f.write("### 概要\n")
            f.write(f"{notes['summary']}\n")
            f.write("### 笔记\n")
            f.write(f"{notes['notes']}\n\n")
    print(f"[{time.strftime('%H:%M:%S')}] 所有视频笔记已整合到 Markdown 文件：{output_file}")


# -------------------------------
# 主函数：启动程序并显示实时进度
# -------------------------------
def main():
    print(f"[{time.strftime('%H:%M:%S')}] 程序开始运行...")
    subtitles = read_subtitles(SUBTITLES_FILE)
    if not subtitles:
        print("字幕文件为空，请检查文件内容。")
        return

    notes_list = [None] * len(subtitles)

    # 使用 ThreadPoolExecutor 并结合 tqdm 显示整体进度
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        future_to_index = {executor.submit(generate_notes, subtitle): i for i, subtitle in enumerate(subtitles)}
        for future in tqdm(concurrent.futures.as_completed(future_to_index), total=len(subtitles), desc="处理进度"):
            index = future_to_index[future]
            try:
                notes = future.result()
                notes_list[index] = notes
            except Exception as exc:
                print(f"[{time.strftime('%H:%M:%S')}] 字幕处理发生异常: {subtitles[index][:30]}... 异常信息: {exc}")

    generate_markdown(notes_list, OUTPUT_MARKDOWN)
    print(f"[{time.strftime('%H:%M:%S')}] 处理完成。")


if __name__ == '__main__':
    main()
