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
        "https://aisubtitle.hdslb.com/bfs/ai_subtitle/prod/2069401553785984971a753d0a2ae81ecf620f9017556e94cb?auth_key=1739444989-14fe304e839a45af84c10face55e20b4-0-866dd59cfebb7370517c1c26aec85ab5"
        "https://aisubtitle.hdslb.com/bfs/ai_subtitle/prod/206940155383805647ba00d8334d260c7f494595121d33379f?auth_key=1739445015-d58190b459b84d1a8d0ba71366bee3fa-0-59e6e5cabec4d29456e4a1130a496d3d"
        "https://aisubtitle.hdslb.com/bfs/ai_subtitle/prod/20694015538380638851cc10bd9926cd54485806fa43eaecea?auth_key=1739445023-4161925ac8ac48c6ac00ce4d7b8467b1-0-0cfa5b248bf736a63ac67019d1499242"
        "https://aisubtitle.hdslb.com/bfs/ai_subtitle/prod/206940155388533478e4af94a43f72142e525356bf5eaa0e75?auth_key=1739445031-5150cceed7864a96a0408914098930be-0-c30875655888fe9529fcc47b189c7902"
        "https://aisubtitle.hdslb.com/bfs/ai_subtitle/prod/20694015539800716548716eb120bea4794b57710ef650ee00?auth_key=1739445035-c146c4fdef6b46adb97607073dcae8f5-0-b227380f91b9b5670a8fee89021eb44d"
        "https://aisubtitle.hdslb.com/bfs/ai_subtitle/prod/206940155403756948ccb7a86d2d61a5315e0adace049fe0a6?auth_key=1739445040-1bf562e302a2451095f13bba2394d5b7-0-50f01a954c1f5fb4283fa84013793928"
        "https://aisubtitle.hdslb.com/bfs/ai_subtitle/prod/20694015541174084722679df82a6f6c7f8c4b46c6f5dbe94d?auth_key=1739445051-34d8ec161fc748c39a2ddba91f7bca4a-0-a9f5fce02941f1a9b8605d20bbf74da2"
        "https://aisubtitle.hdslb.com/bfs/ai_subtitle/prod/206940155423021612bb4515b95c76b5883365c5b88706444b?auth_key=1739445056-9886e973cf7649f7ae83c2cba543607a-0-a0138c27cfdd934ebd6d4705492d8875"
        "https://aisubtitle.hdslb.com/bfs/ai_subtitle/prod/206940155432296816c55840e721fa09b81f01f1224cbf0886?auth_key=1739445062-1022533172ef40ceb1b08c1094af82cd-0-fa72b1d8e07b8a8eb44ced1fd5a2a0c7"
        "https://aisubtitle.hdslb.com/bfs/ai_subtitle/prod/2069401554322969666dee58188cfd662c9e6cc4119058cf09?auth_key=1739445067-7d659aa6207849e78f2102c191f88b77-0-0a66b44a8efc15dc0bd931eaef15c165"
        "https://aisubtitle.hdslb.com/bfs/ai_subtitle/prod/2069401554458960088ef40838d91310228573f3fb3f477f9d?auth_key=1739445072-ca7d9742d46c4525b584a0c2bcf0017a-0-5c17af3a87450b13268bbd0ea6915ce2"
        "https://aisubtitle.hdslb.com/bfs/ai_subtitle/prod/206940155460804006334291caf430257e43f8aa2f84216d71?auth_key=1739445078-2bd9dca1e5db47ec890efc0658877791-0-45ba9d777bd35670ced717ee0c8fcd41"
        "https://aisubtitle.hdslb.com/bfs/ai_subtitle/prod/2069401554886987586ca2644e58cbb797e226866f6bd8fbdb?auth_key=1739445084-afeda68855b549ceb43cd5915a949934-0-bc1d37f5789a84dfd403942cb86313f5"
        "https://aisubtitle.hdslb.com/bfs/ai_subtitle/prod/206940155497803687a815a2e3899b6a60bf3098a84f8459e1?auth_key=1739445091-31736a34d76e4d7abd6b11b42bf8a532-0-847a5a1ad90ad04da2f24b3438e71b21"
        "https://aisubtitle.hdslb.com/bfs/ai_subtitle/prod/206940155514686650a5b207990c222341f1b42e340caa8339?auth_key=1739445095-931a95e4dc354a8db8aee9a953112d1d-0-9dce462df476f59eb81905d0a517f437"
        "https://aisubtitle.hdslb.com/bfs/ai_subtitle/prod/206940155550982453246d29c0d545bba366a62823694bec61?auth_key=1739445102-6b67741f90c94c9883d8e7edcf8de2ac-0-476ab56a8c31f99f026d805a6ba498ea"
        "https://aisubtitle.hdslb.com/bfs/ai_subtitle/prod/206940155829087391d2621a096381dd6c14905d24ae36fa4a?auth_key=1739445112-f034b1c0077f43bcb7a404342bd40250-0-48f61656512ac82bf0b0b7e11e05e713"
        "https://aisubtitle.hdslb.com/bfs/ai_subtitle/prod/206940155845763452792aa032e20d05159cfc06a074e6c204?auth_key=1739445116-376c1681d1524b9a9f6c207f1c4c6d64-0-67101e7e89935befa9f1e5d9f7d37ce7"
        "https://aisubtitle.hdslb.com/bfs/ai_subtitle/prod/2069401558660538961ac21affcadbcf03749cb44a79dee691?auth_key=1739445121-fd300f26c9214383af6f7ecbf0815631-0-65260847e9d208075d87cc5a78da22e7"
        "https://aisubtitle.hdslb.com/bfs/ai_subtitle/prod/206940155866053986431a923883257eb656532dddc29a603d?auth_key=1739445125-de9eb0af56b840fba8e0ca073c25dd65-0-26dacec7fd68c0abba1cf63137578298"
        "https://aisubtitle.hdslb.com/bfs/ai_subtitle/prod/20694015556725902926bd27bdb69acad88c94e261a7e8dc6d?auth_key=1739445129-37b5f8f99ab74cbf92d47226c8b7386c-0-e919d42ab6f20979ce17bc84d79177e2"
        "https://aisubtitle.hdslb.com/bfs/ai_subtitle/prod/2069401555829540132b6675387c1fbaf74f9bba88133edd4d?auth_key=1739445132-f0f6249cefbf4144a2ad31d320f5e049-0-b23e1dd8ab417434ccce4fd4617b50ec"
        "https://aisubtitle.hdslb.com/bfs/ai_subtitle/prod/20694015571772715174dbc6fd06582bed98580208e7a982db?auth_key=1739445137-37d0364ce9504ea2be6fad1a6f617444-0-d3a2eeea77022bfef0b204d4ec8f9967"
        "https://aisubtitle.hdslb.com/bfs/ai_subtitle/prod/3e595cbc575c6cc51a81004abe3d27ef?auth_key=1739445141-c0ea0be71f3e4552a08e94f3f1a67d56-0-5dd5ab464738c61f0749bd95f62029a2"
        "https://aisubtitle.hdslb.com/bfs/ai_subtitle/prod/206940155753968397316896640a5d67d3b10041cb435ef531?auth_key=1739445146-0e298c0df94d4bd292441596ed2b43dc-0-92a3294b402d38d526bd456567f16399"
        "https://aisubtitle.hdslb.com/bfs/ai_subtitle/prod/6037f7abe8fba70774372c954d26fd0e?auth_key=1739445151-4d33bc719d254d218262109c954da995-0-0fde8103c613201bed31ef5eb7f9206c"
        "https://aisubtitle.hdslb.com/bfs/ai_subtitle/prod/206940155799369670b703c74587f9cb74f99abf1047638ea4?auth_key=1739445156-a42e0cac777241069d4be403bac85531-0-d4ed24cf6ffd70068b1b6a4748dcd981"
        "https://aisubtitle.hdslb.com/bfs/ai_subtitle/prod/206940155799365361b84bf2d56f0d403e26233d015c4d1be0?auth_key=1739445161-874905807da94d22b2cbf32cc2781317-0-cfa1820ca9d49558e8e7399fd1b3185a"
        "https://aisubtitle.hdslb.com/bfs/ai_subtitle/prod/206940155799365459bfa2bff0eca64004576abdcdb2a70357?auth_key=1739445168-2f37976ac3d14b29a935c51030c5aeac-0-2d22ad89f1ec77cb8a444828d43595c6"
        "https://aisubtitle.hdslb.com/bfs/ai_subtitle/prod/206940155811152198b409f9422b37de93c9dba25c5849d917?auth_key=1739445175-eaf7fadb96bf46e5bc7343cd9ecbb96a-0-4e810422effb3226666bfed0f41dbd1d"
        "https://aisubtitle.hdslb.com/bfs/ai_subtitle/prod/2069401558852359598e565ec09913a3dc00b38eafa485327d?auth_key=1739445182-d22002dab5824d079b90d25df32c3248-0-053b4576cc51c2b66f8fc4f863952705"
        "https://aisubtitle.hdslb.com/bfs/ai_subtitle/prod/2069401559082511810774921e045bec583989d26c83798b20?auth_key=1739445187-e53e0a2b2da2455b8e83fc8e17f513d9-0-1ae4a7ced254323f572df2e86f26d7a8"
        "https://aisubtitle.hdslb.com/bfs/ai_subtitle/prod/20694015593308735166d87de43cf71d18439d1c47e70c36fb?auth_key=1739445192-1a47dd4be695479998dc6778dc67f369-0-ed4abc2d2bdc22bc1f461b348f92e0e3"
        "https://aisubtitle.hdslb.com/bfs/ai_subtitle/prod/206940155962874876f31df1a61ee3941f9b3e2af449df63f7?auth_key=1739445196-e39f4ce6d9e2496fa4161dd8f498b18e-0-eb7e3e2a0f5e12ffd6f50318adc27dd3"
        "https://aisubtitle.hdslb.com/bfs/ai_subtitle/prod/206940155984567851436b51c56d6e618f03870a47c9b98cbb?auth_key=1739445204-fcd8f30ccd834e30bde1b6f9a80371da-0-efe6855f6715e9287208d2393b26a3da"
        "https://aisubtitle.hdslb.com/bfs/ai_subtitle/prod/2069401551019951602aa3dcf79476f72f34121dbbc799c0d9e?auth_key=1739445210-b99d110b1842479db9686a651bc79326-0-bffd1b4ecb2f2c52b11045d9a350fd8e"
        "https://aisubtitle.hdslb.com/bfs/ai_subtitle/prod/20694015510526785152568f8c0c3a8d011ccdf14fd27ab753e?auth_key=1739445215-a83c046151b54dd0b8b137c61e568f30-0-4cc1e912d31739b50f1d3013f42d49b5"
        "https://aisubtitle.hdslb.com/bfs/ai_subtitle/prod/2069401551080129354a78a2f5115e372da145e9bea6f4e686f?auth_key=1739445221-2b8c86845f3b45d68b7a08dad045b248-0-790e2dac2bf7decbfc228989e7ecc779"
        "https://aisubtitle.hdslb.com/bfs/ai_subtitle/prod/20694015511051541758db0fc63becdb766c8a198ead7715416?auth_key=1739445229-c6c857b944c4455787983647a8cc6ce3-0-c83663250c78603c93d4e6c492647365"
        "https://aisubtitle.hdslb.com/bfs/ai_subtitle/prod/2069401551129486892b400554f96518e6a586cce1a9fbf09d3?auth_key=1739445236-5fc1eee593824c36b5882f57ef884836-0-8fa9dbcaf85839da1a35b51c7c3ed43e"
        "https://aisubtitle.hdslb.com/bfs/ai_subtitle/prod/20694015511514517428ed48c556fa2ca42b7ba47df28aa119f?auth_key=1739445242-9d9c5926415a4cc3a749ab9730c7feee-0-ad70052d49d53d627846eb0ebb1ea432"
        "https://aisubtitle.hdslb.com/bfs/ai_subtitle/prod/2069401551175391823526c0125bffad9294195822ccedeef71?auth_key=1739445250-53c9b57e85294b9c9b1960a3c0bc1a9f-0-c9f6f8d743cad436eeb0b8110284ad69"
        "https://aisubtitle.hdslb.com/bfs/ai_subtitle/prod/206940155120004369807520c85046ee39569644b3590be549e?auth_key=1739445257-ae6cc45becaa4467976c917daed07d79-0-514cf54962ff3d1194911b8afafa5641"
        "https://aisubtitle.hdslb.com/bfs/ai_subtitle/prod/2069401551238492185e66a0ab98a7842a5464af730235a39a4?auth_key=1739445264-79ebc5934e0e4c96a4687046af2818f1-0-d5dc630cdaf6bd039cffddbf849e3e07"
        "https://aisubtitle.hdslb.com/bfs/ai_subtitle/prod/20694015512897576343b497ea56a7ee7c08f1b03fac9f8e45b?auth_key=1739445270-7e83a2cb2188433aac9d805848609d37-0-4529a61dc8ecc7d46da98f617d754192"
        "https://aisubtitle.hdslb.com/bfs/ai_subtitle/prod/2069401551260999250a026bfc503cca6d0d8508d742a353a77?auth_key=1739445277-9a45c3892b524dc09885ee2196a13b9f-0-4204aa9445bda4dfef71a0bd2ff602c3"
        "https://aisubtitle.hdslb.com/bfs/ai_subtitle/prod/206940155127447577042fec02e3273afb88a282ca8a66a0460?auth_key=1739445284-a518cee5f3634cf6a6b275086c195dfa-0-1845268f932515a508890b3fb8dfdf2b"
        "https://aisubtitle.hdslb.com/bfs/ai_subtitle/prod/20694015512877428920d0ab55fc60ab87731dcf67972e80e6d?auth_key=1739445291-d9197fc2320140feb9edd16251a23310-0-f74fa696a767f2bf6414a68e952e1a44"
        "https://aisubtitle.hdslb.com/bfs/ai_subtitle/prod/2069401551303334116b907660f8bb8e7884a58239179e1c259?auth_key=1739445298-95c3a0b3b9ca4728a39cc0b37f82b0d3-0-f78a2b32ccf19182162495465edcdb15"
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


