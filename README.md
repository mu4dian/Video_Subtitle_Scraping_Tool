### 这是一个可以把B站上视频字幕爬取下来的程序
1.在开始之前需要先打开bilibili的网页版中的视频
![image](https://github.com/user-attachments/assets/21888db0-45f1-4dbb-a968-405bf2ac1edd)
2.然后按下键盘上的F12或通过其他方式进入开发者模式，在网络选项中搜索“ai_subtitlle”，刷新页面，左侧会出现找到的AI字幕请求，右键复制URL即可
![image](https://github.com/user-attachments/assets/74d9e97f-e1d3-4150-9253-870d5722b775)
3.拉取仓库
```
gitclone https://github.com/mu4dian/Video_Subtitle_Scraping_Tool.git
```
4.在代码中找到填写url的部分替换为刚刚复制的链接，运行程序，即可在项目根目录下生成subtile.txt文件
可以在此处粘贴多条链接，只需要在浏览器中保持页面不刷新，连续跳转至其他视频即可收集多条字幕请求
![image](https://github.com/user-attachments/assets/0804a85c-0127-4022-ad37-eb1104a88c23)

###### 其中的GetJSON.py文件可以得到请求中的json文件
