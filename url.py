import os
import requests


def download_subtitle(url, output_dir):
    """
    下载单个字幕文件，并保存到指定文件夹中。

    参数：
        url: 字幕文件的 URL 地址
        output_dir: 保存下载文件的文件夹路径
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # 如果状态码不是200，则抛出异常
    except Exception as e:
        print(f"下载 {url} 时出错：{e}")
        return

    # 从 URL 中提取文件名：取 /prod/ 后到 ? 前的部分作为文件名
    try:
        filename = url.split("/prod/")[-1].split("?")[0]
        if not filename:
            filename = "subtitle"
    except Exception:
        filename = "subtitle"

    # 添加后缀名（这里默认为 .json）
    filename += ".json"
    file_path = os.path.join(output_dir, filename)

    try:
        with open(file_path, "wb") as f:
            f.write(response.content)
        print(f"成功下载：\n  {url}\n保存到：{file_path}\n")
    except Exception as e:
        print(f"保存文件 {file_path} 时出错：{e}")


def batch_download_subtitles(url_list, output_dir="subtitles"):
    """
    批量下载字幕文件，并保存到指定文件夹中。

    参数：
        url_list: 包含字幕文件 URL 的列表
        output_dir: 保存下载文件的文件夹（默认为 "subtitles"）
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for url in url_list:
        download_subtitle(url, output_dir)


if __name__ == "__main__":
    # 所有字幕文件的 URL 列表
    urls = [
        "https://aisubtitle.hdslb.com/bfs/ai_subtitle/prod/22253477595981291316caf1339e242e5f395ff104612b24d3?auth_key=1739106837-048a63abbac649d6995435a062ddae3f-0-b75fac084c1e6958a4215eb5f6a8e36b",
        "https://aisubtitle.hdslb.com/bfs/ai_subtitle/prod/2225347759598108510ccbaaa89106ccb093b18523a233af48?auth_key=1739107270-697654d2562b40148ae245f7cbc5a35f-0-104637fa6f27440db7eab22ec917e2e7",
        "https://aisubtitle.hdslb.com/bfs/ai_subtitle/prod/22253477595981864035cab7421bfe2911b1d3cd449bc795ab?auth_key=1739107275-054243bd2cfc446f9a29685c229c04f5-0-2a523ead658bd5bf3add5d07b369e09b",
        "https://aisubtitle.hdslb.com/bfs/ai_subtitle/prod/2225347759598110513870688650b9ece2db575ab68f60026a?auth_key=1739107281-a8bbbc2871b4433ab6b0bd3e621bc255-0-e48afbfd23db432ae7bd47c5074550d0",
        "https://aisubtitle.hdslb.com/bfs/ai_subtitle/prod/2225347759598122969257fdd0b1df54be1c1cb62f9f3962ac?auth_key=1739107285-3f0844b3aeff4d9b93ef79d63f8948c4-0-1a450cac8e92cd46b7ceadbd523fd074",
        "https://aisubtitle.hdslb.com/bfs/ai_subtitle/prod/2225347759598127041ab691e76b1139d007fdca607a215071?auth_key=1739107290-10a66e21210a4761a638295537958e20-0-71c861e18f4909815401fb3597aca4a3",
        "https://aisubtitle.hdslb.com/bfs/ai_subtitle/prod/222534775959812234af3d68bc4c8c252b17018546f1db6f83?auth_key=1739107294-56be4a35b0fa4c1da76f82caf77d41dd-0-b7e51649a27806a9fe1026488bcf35a2",
        "https://aisubtitle.hdslb.com/bfs/ai_subtitle/prod/22253477595981125900de509f6f2adb1fe6915bcd6a986ad4?auth_key=1739107299-f620875fcb084f3a9289ee3f43557d3e-0-f4fb77c76c74adc710229ab8fb62c615",
        "https://aisubtitle.hdslb.com/bfs/ai_subtitle/prod/2225347759598129877fe959d5f17af368d1a1e9be6f028889?auth_key=1739107305-27b470f5f9b44829b350da960d5ffed9-0-380fb055ea1c0a1f509a0a5e338f90d4",
        "https://aisubtitle.hdslb.com/bfs/ai_subtitle/prod/22253477595981291316caf1339e242e5f395ff104612b24d3?auth_key=1739107309-8759dd0a701048aa8bbd4fb4a1a54512-0-7877ed479abf188a8f131a96e83b96a0",
        "https://aisubtitle.hdslb.com/bfs/ai_subtitle/prod/222534775959813269209caeb88e11a1fdd3491ec06017d532?auth_key=1739107313-1133d862f0634a6bb7f43f9388bf80e0-0-f5095c87db2250b328d4258ae7e48c39",
        "https://aisubtitle.hdslb.com/bfs/ai_subtitle/prod/222534775959813503c3933ec1611c90fa853f78895e5181b6?auth_key=1739107319-b42922766d0b419cbcac676fb3f0993f-0-3125d6fc0a4610b0fe002f00d63749fa",
        "https://aisubtitle.hdslb.com/bfs/ai_subtitle/prod/222534775959814623764286d1573a133cd9e839b4c30565a0?auth_key=1739107324-813dbec6fb864f9793fe28aca3aaf527-0-7c60be2b79795b280c7a0a642a1f637e",
        "https://aisubtitle.hdslb.com/bfs/ai_subtitle/prod/2225347759598137296270f41c1e0a0eee04418f1f13ac4013?auth_key=1739107329-7a72785836754c469b2f0fba9efb6f3d-0-99605cd462d61a3e71d79735ae990358",
        "https://aisubtitle.hdslb.com/bfs/ai_subtitle/prod/222534775959813898066ba0e694ed6d601582c112f62212f3?auth_key=1739107334-8446ef952f9e469cbd7477d397be4b17-0-27cf1ba0187188d0795252d48dbf9a99",
        "https://aisubtitle.hdslb.com/bfs/ai_subtitle/prod/222534775959814665549a9484d5852988d839f78afae174a1?auth_key=1739107338-62dfa38b869a41238cc85ee5539d7f02-0-9a29a69bb334a1df0ab8ac04dea00255",
        "https://aisubtitle.hdslb.com/bfs/ai_subtitle/prod/222534775959816132dd60370e7bf337d5b2d01520d54dd8bd?auth_key=1739107343-2bbefab97078496fafa7e80acc501e05-0-cf03054e72456bcf98f9b8cd5f8bf117",
        "https://aisubtitle.hdslb.com/bfs/ai_subtitle/prod/2225347759598148678260bdd5efa1f0e64aa92eec2d321dca?auth_key=1739107349-3d9ba96b54634396addc7ca825b00f12-0-78b7427264bb014b6cfd3939c6b335e2",
        "https://aisubtitle.hdslb.com/bfs/ai_subtitle/prod/2225347759598151396fbea47f5bec52d4991fd4de37cd88bc?auth_key=1739107354-e43699e8b3c84dcd95ab424e205eeaa0-0-9cef9f822f1ff946509d3e03293e9701",
        "https://aisubtitle.hdslb.com/bfs/ai_subtitle/prod/222534775959815912fa58f109034392780f62724c0fb4c426?auth_key=1739107359-2e2b06bc16c6481c9b9a83f35110e6d0-0-f97ac4890eac03212289656f93eb480c",
        "https://aisubtitle.hdslb.com/bfs/ai_subtitle/prod/222534775959824487c2c6dcf94deb1e32687a8aee71324447?auth_key=1739107364-7c856033d30a4bd6874e9ad0e4c15bd4-0-04865f5c875cfefc0a48374b2f55493a",
        "https://aisubtitle.hdslb.com/bfs/ai_subtitle/prod/2225347751633443113f9a36b8b56405bc43fdc8b99947a53f1?auth_key=1739107369-e64ab2aab9a142e29febc4bae822f57f-0-094e68d452c05114fb1d84c86c73cefd",
        "https://aisubtitle.hdslb.com/bfs/ai_subtitle/prod/22253477516334432555fabc4af273da289eca19ac436397959?auth_key=1739107375-129c40c9a5c44e72adf0522eb8649fbb-0-668b509e409e5a0b7be01e5d4ffb6636",
        "https://aisubtitle.hdslb.com/bfs/ai_subtitle/prod/222534775163344329099f9d00c42158c8c7a697731a029a6c8?auth_key=1739107381-53a27451201443a397cd3936ea0acfc9-0-7b4435f6b36f5b98f35fddebaec4143b",
        "https://aisubtitle.hdslb.com/bfs/ai_subtitle/prod/222534775163344382883b28e7a3d4a0a50beb77b10820d20bc?auth_key=1739107387-94007385e4da462782a5bb57f3283170-0-3e418a4d2b78edd46abddb634cd99052"
    ]

    # 指定保存字幕文件的目录（默认会在当前目录创建一个 "subtitles" 文件夹）
    batch_download_subtitles(urls, output_dir="subtitles")
