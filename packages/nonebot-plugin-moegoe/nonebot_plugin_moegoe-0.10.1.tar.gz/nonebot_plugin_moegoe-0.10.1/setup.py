# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_moegoe']

package_data = \
{'': ['*']}

install_requires = \
['gradio_client>=0.7.0,<0.8.0',
 'httpx>=0.23.0,<0.24.0',
 'nonebot-adapter-onebot>=2.1.1,<3.0.0',
 'nonebot2>=2.0.0b5,<3.0.0',
 'rtoml>=0.9.0,<0.10.0']

setup_kwargs = {
    'name': 'nonebot-plugin-moegoe',
    'version': '0.10.1',
    'description': 'VITS AI合成原神角色语音',
    'long_description': '<!--\n * @Author         : yiyuiii\n * @Date           : 2022-10-11 00:00:00\n * @LastEditors    : yiyuiii\n * @LastEditTime   : 2023-12-11 00:00:00\n * @Description    : None\n * @GitHub         : https://github.com/yiyuiii\n-->\n\n<!-- markdownlint-disable MD033 MD036 MD041 -->\n\n<p align="center">\n  <a href="https://v2.nonebot.dev/"><img src="https://v2.nonebot.dev/logo.png" width="200" height="200" alt="nonebot"></a>\n</p>\n\n<div align="center">\n\n# nonebot-plugin-moegoe\n\n用API让原神角色说话！\n\n_✨ AI（VITS）合成原神角色语音 by fumiama✨_\n\n搬运自ZeroBot-Plugin仓库：https://github.com/FloatTech/ZeroBot-Plugin/tree/master/plugin/moegoe\n\nhttps://github.com/fumiama/MoeGoe/tree/genshin\n\n</div>\n\n<p align="center">\n  <a href="https://raw.githubusercontent.com/Yiyuiii/nonebot-plugin-moegoe/master/LICENSE">\n    <img src="https://img.shields.io/github/license/Yiyuiii/nonebot-plugin-moegoe.svg" alt="license">\n  </a>\n  <a href="https://pypi.python.org/pypi/nonebot-plugin-moegoe">\n    <img src="https://img.shields.io/pypi/v/nonebot-plugin-moegoe.svg" alt="pypi">\n  </a>\n  <img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="python">\n</p>\n\n## :gear: 安装方法\n\n`nb plugin install nonebot_plugin_moegoe`\n或 `pip install nonebot_plugin_moegoe`\n\n## :rocket: 使用方式\n\n**在聊天中输入:**\n\n- **让**(中配|英配|日配)[角色]\\(以[参数])**说**(中文|英语|日语)(文本)\n- **让**[宁宁|爱瑠|芳乃|茉子|丛雨|小春|七海|妃爱|华乃|亚澄|诗樱|天梨|里|广梦|莉莉子]\\(以[参数])**说日语：**(日语)\n- **让**[Sua|Mimiru|Arin|Yeonhwa|Yuhwa|Seonbae]\\(以[参数])**说韩语：**(韩语)\n\n可选参数默认有语速、情绪、顿挫。\n\n例：\n\n- [让派蒙说你好！旅行者。](https://genshinvoice.top/api?speaker=%E6%B4%BE%E8%92%99_ZH&text=%E4%BD%A0%E5%A5%BD%EF%BC%81%E6%97%85%E8%A1%8C%E8%80%85%E3%80%82&format=wav&length=1&noise=0.5&noisew=0.9&sdp_ratio=0.2&language=ZH)\n- [让英配派蒙以情绪0.8长度1.8顿挫0.7说中文你好！旅行者。](https://genshinvoice.top/api?speaker=%E6%B4%BE%E8%92%99_EN&text=%E4%BD%A0%E5%A5%BD%EF%BC%81%E6%97%85%E8%A1%8C%E8%80%85%E3%80%82&format=wav&length=1.8&noise=0.8&noisew=0.7&sdp_ratio=0.2&language=ZH)\n- [让宁宁说日语：hello.](https://moegoe.azurewebsites.net/api/speak?text=hello!&id=0)\n- [让Sua说韩语：hello.](https://moegoe.azurewebsites.net/api/speakkr?text=hello!&id=0)\n\n**Bot返回语音**\n\n<!-- <p align="center">\n<audio src="https://genshinvoice.top/api?speaker=%E6%B4%BE%E8%92%99_ZH&text=%E4%BD%A0%E5%A5%BD%EF%BC%81%E6%97%85%E8%A1%8C%E8%80%85%E3%80%82&format=wav&length=1&noise=0.5&noisew=0.9&sdp_ratio=0.2&language=ZH"></audio>\n\n<audio src="https://genshinvoice.top/api?speaker=%E6%B4%BE%E8%92%99_EN&text=%E4%BD%A0%E5%A5%BD%EF%BC%81%E6%97%85%E8%A1%8C%E8%80%85%E3%80%82&format=wav&length=1.8&noise=0.8&noisew=0.7&sdp_ratio=0.2&language=ZH"></audio>\n\n<audio src="https://moegoe.azurewebsites.net/api/speak?text=hello!&id=0"></audio>\n\n<audio src="https://moegoe.azurewebsites.net/api/speakkr?text=hello!&id=0"></audio>\n</p> -->\n\n**在聊天中输入:**  \n\n- `moegoe load` 可以在线更新profile\n- `moegoe list` 可以看到cnapi角色列表（只有链接）\n- `moegoe xx` 可以看到上述说明\n\n## :wrench: 配置方法\n\n在插件初次联网成功运行后，可以发现 BOTROOT/data/moegoe/ 路径下有profile.toml文件，其中可以配置\n\n- 插件优先级 priority\n- 触发正则语句 regex\n\n等等。 修改后保存，重启生效。\n\n**注意：**\n\n插件主要通过调用网络api来获取合成语音。\n\n目前中文默认使用新的免费api：https://genshinvoice.top/ ，该api目前展现出稳定的良好表现，并正在持续更新。\n\n原付费api也可继续使用，在自行获取APIKey后，在配置文件的cnapi url末尾`"`前加上`&code=你的APIKey`，即可使用。参考[Issue 17](https://github.com/Yiyuiii/nonebot-plugin-moegoe/issues/17#issuecomment-1336317427)\n\n日文和韩文的API目前正常。\n\n当插件版本更新时新配置将覆盖旧配置，如果不希望被覆盖可以在profile.toml中把版本调高。\n\n## :speech_balloon: 常见问题\n\n<details>\n<summary>报错 ERROR: No matching distribution found for nonebot-plugin-moegoe</summary>\n\n[Issue 1](https://github.com/Yiyuiii/nonebot-plugin-moegoe/issues/1)\n\n - 注意安装的包名是带**下划线**的：nonebot_plugin_moegoe\n</details>\n\n<details>\n<summary>API不能正确生成语音</summary>\n\n[Issue 2](https://github.com/Yiyuiii/nonebot-plugin-moegoe/issues/2) | [Issue 4](https://github.com/Yiyuiii/nonebot-plugin-moegoe/issues/4)\n\n- 第一种情况：输入如果包含api无法处理的字符就会无法生成语音，请排查英文、叠词、奇怪标点符号等。\n- 第二种情况：当后台在报`encode silk failed: convert pcm file error: exec: "ffmpeg": executable file not found in %PATH% `错误时，表示go-cqhttp编码音频所依赖的ffmpeg包没有被安装，所以不能发送音频。**请自行安装ffmpeg**。*（不过ffmpeg可能不是必须的。如果有人在不安装ffmpeg时能正常使用，请向我反馈，这一点还没有经过测试。）*\n- 第三种情况：**本插件默认优先级为5**，若有其它的插件优先级比5强，且该插件有block截断，则本插件可能无法收到并处理消息。目前需要自行调整插件的优先级。\n</details>\n\n<details>\n<summary>API不能生成较长语音</summary>\n\n一些API生成较长语音的速度很慢（从数十秒到数分钟），为避免该类请求的并发造成资源阻塞，代码中限制了请求时长，可自行修改。\n\n`resp = await client.get(url, timeout=120)`\n</details>\n\n<details>\n<summary>API挂了</summary>\n\n[Issue 7](https://github.com/Yiyuiii/nonebot-plugin-moegoe/issues/7) | [Issue 15](https://github.com/Yiyuiii/nonebot-plugin-moegoe/issues/15)\n\n</details>\n\n\n## :clipboard: 更新日志\n\n#### 2023.12.11 > v0.10.1 :fire:\n\n- 跟随genshinvoice.top更新cnapi以及相关处理流程。\n- 优化版本控制代码和逻辑，考虑到minor版本更新经常带来profile和旧版本代码的不兼容问题，今后只会自动更新micro新版本的profile。\n\n#### 2023.11.09 > v0.9.1\n\n- 跟随genshinvoice.top更新cnapi以及相关处理流程。该API现在支持海量配音角色和中日英三种语言！\n- 更新镜像站为 https://mirror.ghproxy.com/\n\n#### 2023.08.30 > v0.8.1\n\n- 触发语句改动：加入可选的参数触发指令；顺便整理了代码。\n\n#### 2023.08.29 > v0.8.0\n\n- 更新了新的免费cnapi，和新的cnapi角色名单。\n\n#### 2023.06.17 > v0.7.8\n\n- 更新了cnapi的角色名单，并加入了一些api参数。\n\n#### 2023.02.08 > v0.7.6\n\n- 更新了新的中文api：yuanshenai.azurewebsites.net **（目前已失效）**\n- 增加了更多api配置选项，如果url中存在对应空位则生效，目前可以在profile.toml中修改。\n- 更新profile.toml时自动将原有文件备份为profile.bak。\n- 加入在线更新profile的指令 moegoe load。\n\n#### 2023.01.27 > v0.7.5 \n\n- 增加了回复形式的设置，详见profile.toml中[api]一栏。\n\n#### 2022.12.25 > v0.7.4\n\n- 应官方要求升级包依赖版本。\n\n#### 2022.12.18 > v0.7.1\n- 修复安装失败的BUG。profile.toml的位置改变，之前版本的配置可能无法自动更新profile.toml配置文件。\n\n#### 2022.11.29 > v0.7.0\n- 从__init__.py抽离一些配置组成profile.toml配置文件，现在可以自动从github上抓取url等配置的更新了。\n\n#### 2022.10.11 > v0.6.0\n- 同步更新中文原神语音api\n\n#### 2022.10.03 > v0.5.2\n- 增加包依赖的nonebot版本限制（仅此而已）\n\n#### 2022.08.24 > v0.5.1\n- 在`让xx说xx：`正则式中添加冒号的全角半角匹配`(：|:)`（此外，之前版本已经添加形如`(日语|日文|日本语)`的正则匹配）\n\n#### 2022.08.24 > v0.5.0\n- 添加日语speaker2的API，增加8名可选语音人物\n- 换用httpx以修正requests阻塞多协程的BUG\n- 在中文语音中，将输入文字中的英文符号和0-9数字预处理为中文\n- 优化报错提示\n- 整理代码\n',
    'author': 'yiyuiii',
    'author_email': 'yiyuiii@foxmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/yiyuiii/nonebot-plugin-moegoe',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
