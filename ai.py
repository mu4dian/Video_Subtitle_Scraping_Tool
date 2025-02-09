import os
import json
import requests


def download_json(url, timeout=10):
    """
    下载指定 URL 的 JSON 数据并解析成 Python 对象。

    参数：
        url: 字幕 JSON 文件的 URL 地址
        timeout: 请求超时时间（单位：秒）
    返回：
        解析后的 JSON 数据（字典），下载或解析出错时返回 None。
    """
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()  # 检查请求状态
        data = response.json()
        return data
    except Exception as e:
        print(f"下载或解析 {url} 时出错：{e}")
        return None


def extract_subtitles(data):
    """
    从 JSON 数据中提取字幕文本。

    参数：
        data: JSON 数据（字典），要求存在 "body" 字段，其值为字幕条目列表，
              每个条目中包含 "content" 字段。
    返回：
        提取出的字幕文本列表（每个元素为一条字幕）。
    """
    subtitles = []
    if not data:
        return subtitles
    body = data.get("body", [])
    for item in body:
        content = item.get("content", "").strip()
        if content:
            subtitles.append(content)
    return subtitles


def batch_download_and_extract(url_list):
    """
    批量下载多个 JSON 字幕文件，并提取每个文件中的字幕文本。

    每个 JSON 文件生成的字幕文本（内部各字幕以逗号连接）作为一行，
    最终返回一个包含所有行的列表。

    参数：
        url_list: 字幕 JSON 文件 URL 的列表
    返回：
        每个 JSON 文件生成的字幕文本列表，每个元素对应一行文本。
    """
    lines = []  # 保存每个 JSON 文件生成的一行字幕文本
    for url in url_list:
        print(f"正在处理：{url}")
        data = download_json(url)
        subtitles = extract_subtitles(data)
        if subtitles:
            # 将当前 JSON 文件的所有字幕用逗号连接
            line_text = ",".join(subtitles)
            lines.append(line_text)
        else:
            print(f"未从 {url} 提取到字幕文本。")
    return lines


def save_text_to_file(text, output_file):
    """
    将文本保存到指定文件中。

    参数：
        text: 要保存的文本内容
        output_file: 输出文件路径
    """
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f"字幕文本已成功保存到：{output_file}")
    except Exception as e:
        print(f"保存文件 {output_file} 时出错：{e}")


if __name__ == "__main__":
    # 所有字幕 JSON 文件的 URL 列表
    urls = [
        "https://aisubtitle.hdslb.com/bfs/ai_subtitle/prod/61886000012779983401076fe3157d3f707c72e797ab5f4c6be?auth_key=1739107743-a26847cbb04740aaa55b32e2f80fc7cd-0-79466148edae2ba0c805fd913a003141",
        "https://aisubtitle.hdslb.com/bfs/ai_subtitle/prod/23379279912780387571d318a954bf7b70794f8d4d3f18efe42?auth_key=1739108003-6b91113e7a8e4fad98a8658450b16868-0-187b4f06dfd83207331cd07c9406ed19",
        "https://aisubtitle.hdslb.com/bfs/ai_subtitle/prod/23397065112783213266d2f62f3822104c9391f97cdf334cf5d?auth_key=1739108007-22fb118526b345c48c3e5dbc79855267-0-7c4febc433e446047ad39a876b7140d5",
        "https://aisubtitle.hdslb.com/bfs/ai_subtitle/prod/4913758751280688568e28d23c2c07a87855902c20b2c17d73d?auth_key=1739108010-3349ab46f1f347279a826b0b2269666f-0-c906713404d57b242b53bd57bdd6cce6",
        "https://aisubtitle.hdslb.com/bfs/ai_subtitle/prod/961572921128170110784883e69a851d2deee344ec01d03bc71?auth_key=1739108014-fe2e3ee5a9d740a19d912bee955dde81-0-d60c0246446f29b3171147c32203d843",
        "https://aisubtitle.hdslb.com/bfs/ai_subtitle/prod/4490891811282677149aba56e47e7fe7be7bc18c470dbb063d3?auth_key=1739108018-4b565a86cfb3484cba8a3db739229d41-0-0f349fb99b9cb7886e3ea3458743d774",
        "https://aisubtitle.hdslb.com/bfs/ai_subtitle/prod/2767016771287639874e33e0ecf2fd0583abef56f6245f08f34?auth_key=1739108022-e56bfa3a758643ac9955e6eb8dbfa62a-0-2b98026ae78de846864bef8dcbfcd734",
        "https://aisubtitle.hdslb.com/bfs/ai_subtitle/prod/91672919612876458690a63c3edd423504ec6e4d09337e09e6e?auth_key=1739108027-28eb364f0c194552a7abfd49b821f294-0-e58a4e64cc58b2b4f30513e8f568fecf",
        "https://aisubtitle.hdslb.com/bfs/ai_subtitle/prod/27674731812869935229c31fd00bb1c72ced423989e11f81787?auth_key=1739108030-d0ab34ee893a4e2b8fdd8e3e772ed9a5-0-36e3ca9586c06f793a6d647e9e759362",
        "https://aisubtitle.hdslb.com/bfs/ai_subtitle/prod/40669945412873208083e112a10d6d421f1eb259757c5eb9305?auth_key=1739108034-d5d06fbb48c14129a5adc898b0eb7e4a-0-672abc9be2f6972ac2bb84eb965b1dfd",
        "https://aisubtitle.hdslb.com/bfs/ai_subtitle/prod/49172758112876488700a5e46e91b23f5ef07deeb76ad3e1ef6?auth_key=1739108040-b8b2c9b751d344d4b41d8ee64d0b1a55-0-784fbc59a5781d3f845dac8c043a87de",
        "https://aisubtitle.hdslb.com/bfs/ai_subtitle/prod/7892947831288557110e93a23bb0deccf9ea95acff98900e945?auth_key=1739108044-1529ddd6a77e4188b22b1f6d6060a979-0-25cb956bf25b6802129417911ea5cc29",
        "https://aisubtitle.hdslb.com/bfs/ai_subtitle/prod/4918046861290147000c82701a76e3fdcb37c7b3fc31ee3fd46?auth_key=1739108049-566094f8995b419e9eabb80ed282dd2d-0-b57226bd06808dd1096f74ba1a3254b5",
        "https://aisubtitle.hdslb.com/bfs/ai_subtitle/prod/534343696129017714833f62cfb99934843e2481a2b041f236e?auth_key=1739108054-528cbf555d24465bbee27c277ab357ed-0-4cb476d64968f271e93e704009c74a0d",
        "https://aisubtitle.hdslb.com/bfs/ai_subtitle/prod/9592629221291036676b5a0eed92edea644f46755b91da446fc?auth_key=1739108058-6b8eac1e70774d838970e52927ec288d-0-6dd6551a711394461f78b5f38f36df58",
        "https://aisubtitle.hdslb.com/bfs/ai_subtitle/prod/74680835412910497206a70f81aa6026cce8f67ea74106f7103?auth_key=1739108063-7c55cf4393c4464aae8b9eb02d837199-0-6d3cc52c97452b5c62b0f6d24cfbdb85",
        "https://aisubtitle.hdslb.com/bfs/ai_subtitle/prod/4919585631292097599266f43464a469d0e74fd5729fcb351e5?auth_key=1739108068-547790f47f8e4c5d88bc00b5839882c7-0-cf7a219379ba884f779d8c4d501c0641",
        "https://aisubtitle.hdslb.com/bfs/ai_subtitle/prod/70438414112921039348c0414ed3f9ceef1bbc667f789a07d96?auth_key=1739108085-25a64c485efc45dfbdf9ad809dbfd11b-0-d5db25407a078b007c4c7a5b400644b0",
        "https://aisubtitle.hdslb.com/bfs/ai_subtitle/prod/44940880412926842909853892f6089a6739aafd52589bc0247?auth_key=1739108096-cfb7c27143ce419eb1e92a54c7c8ccea-0-1e9c53dcf6d7b56c686d791d6337d360",
        "https://aisubtitle.hdslb.com/bfs/ai_subtitle/prod/5769484901292695215b753881be43d5ab55c9b4a2045faf23c?auth_key=1739108103-3f94dcbef2e949f49f05f52148db2ad0-0-6c106f4c884a61936bec5f44fdb351d0",
        "https://aisubtitle.hdslb.com/bfs/ai_subtitle/prod/491911499129366008741429be3c0dc117f46f9d761935bf747?auth_key=1739108109-402febbef4a34fd2b17537be181699bb-0-662d7b8415ca57f638ae413d7cfee594",
        "https://aisubtitle.hdslb.com/bfs/ai_subtitle/prod/66198545212942451637b4ef23a892c965370babc263c7b10c5?auth_key=1739108178-970198e3d598493e96011fd396df0fcf-0-096ca098dd9449320638b8e0d90b95f0",
        "https://aisubtitle.hdslb.com/bfs/ai_subtitle/prod/2345177131295174477bec9eeef045802e1773e0a04b5bb54ae?auth_key=1739108188-1c91ec5464cc4316a5bf705d07e7620a-0-ae76e74da98babb177775950504f5606",
        "https://aisubtitle.hdslb.com/bfs/ai_subtitle/prod/40705524912951820745ce02e50668c8a52db837ea25861172d?auth_key=1739108192-08c6daea18f64908b2cec44aaab079fe-0-f422c03670307fd460f522cce07fe463",
        "https://aisubtitle.hdslb.com/bfs/ai_subtitle/prod/662104687129570458110e0221310ec02da6310a5bbc4bfc4f4?auth_key=1739108202-d9a35afb62ac4920b701ee5f45320583-0-06efa185b7c13d638afb91aa1c1b836f",
        "https://aisubtitle.hdslb.com/bfs/ai_subtitle/prod/449591956129577324062a389dd53fc5cea25378ff966e99fd8?auth_key=1739108209-602317ffdfee4724bc57ee433269b7f1-0-5da8255af3e565d769cba44dd0334503",
        "https://aisubtitle.hdslb.com/bfs/ai_subtitle/prod/959617896129700387141fd520a5dfb935f2c6912ab4cc97eff?auth_key=1739108215-fa0e25f009eb4247959e40328bff9df4-0-07ea1152d5c22a93a213b29002cec4c2",
        "https://aisubtitle.hdslb.com/bfs/ai_subtitle/prod/78956492412970292667e8816b9a76f4aeeb9c9e5a4aa2d1ad1?auth_key=1739108222-b0eb1e97cb2740a9aaff18f46ac27d44-0-94408a1e7ddaf6419ef67053ca30cca3",
        "https://aisubtitle.hdslb.com/bfs/ai_subtitle/prod/704609037129824476596f1fc37be2a605a1c0027e4a1298323?auth_key=1739108230-9e849f04ccf1430a853d1e9386c7145a-0-7796b8fe329cd68d2b025c36a3c3319c",
        "https://aisubtitle.hdslb.com/bfs/ai_subtitle/prod/31974782812982752464a46a0e30924decaab89026ed70c2591?auth_key=1739108236-b2660ae5f7804fff802ee0ddfae48c0d-0-70eea6ce718ec810fbb5349ad8c31c96",
        "https://aisubtitle.hdslb.com/bfs/ai_subtitle/prod/619700882129977142056d480ef7e6399c36e79f2fa91bfdfcf?auth_key=1739108244-5da9cd5b783445fd9d15c92bb99a38c9-0-1cd71f18358aa97abca6fb42af032ddd",
        "https://aisubtitle.hdslb.com/bfs/ai_subtitle/prod/9622493011299844708e4700aa99016cfee50cb9d806e6bbbf0?auth_key=1739108250-857dfed4e65646b994c5ded7cb5a300f-0-79ce5ca4b088546c00fbb196a2f1c22a",
        "https://aisubtitle.hdslb.com/bfs/ai_subtitle/prod/619682424130145210207ac374439bd98aab248e23e13b9b1fa?auth_key=1739108257-c242980abf574b3d8738b19571fd1ac5-0-f3c67472ea2a3bb15cb298c691e1536d",
        "https://aisubtitle.hdslb.com/bfs/ai_subtitle/prod/57722585113014679643e856a67d8fe97af173d1569d456c095?auth_key=1739108263-44477348c8d0467c86656fd8ea74f1d8-0-4f4bb9e2b247fb6b9a80150cf1d6034f"
    ]

    # 批量下载并提取每个 JSON 文件中的字幕文本（每个文件生成的字幕文本为一行）
    lines = batch_download_and_extract(urls)

    if not lines:
        print("没有提取到任何字幕文本。")
    else:
        # 将每个 JSON 文件生成的字幕文本用换行分隔拼接成最终文本
        final_text = "\n".join(lines)

        # 指定输出文件路径（可根据需要修改）
        output_txt = "all_subtitles.txt"
        save_text_to_file(final_text, output_txt)


