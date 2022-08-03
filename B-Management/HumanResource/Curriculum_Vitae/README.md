# 简历自动生成工具

工具链接：[curriculum_viate_markdown_generator.py](curriculum_viate_markdown_generator.py)

## 使用指南

```
usage: curriculum_viate_markdown_generator.py [-h] [--cv-json CV_JSON]
                                              [--example] [--lang LANG]
                                              [--public]
                                              [--hide-education-misc]

optional arguments:
  -h, --help            show this help message and exit
  --cv-json CV_JSON, -c CV_JSON
                        CV json path, use --example to get CV json example
  --example
  --lang LANG
  --public              Show private information
  --hide-education-misc
                        hide education misc information
```

准备 json 格式的简历数据（可以用`curriculum_viate_markdown_generator.py --example`获取数据示例）。

数据格式简介：
- 联系信息中的 `github_user` 可省略不填
- 简历采用 STAR 法则，每个 project 需要填写`situation, task, action, result`四部分（也可省略某些部分不填）。
- 简历支持隐藏隐私信息（默认行为），在使用 `--public` 参数时才会打印敏感信息。
- 简历支持英文输出，使用 `--lang en` 开启，其中姓名和地区将显示双语，当然 json 中的数据还是要自己写英文版。

其他功能：
1. 支持从 GitHub 爬取最新的信息，包括：
   - follower: 在简历中相应位置加入`{github_followers,username}`即可爬取`username`的follower数量
   - star: `{github_star,username,project_name}`
   - fork: `{github_fork,username,project_name}`
2. 使用 `pandoc` 转换为 html: `pandoc cv.md -t html5 -o cv.html --self-contained --css=cv.css`，其中 `css` 文件可以在[这里](cv.css)获取。可以用浏览器的打印功能把 html 打印成 pdf，当然也能用 word 打开 html 继续编辑。
