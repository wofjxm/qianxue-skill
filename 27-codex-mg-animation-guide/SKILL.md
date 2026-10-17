---
name: codex-mg-animation-guide
description: Codex + HyperFrames 制作 MG 动画的流程规范与提示词（先出效果图再生成 AE 动效）。当用户要用 AI 做 MG/动效动画成片时使用。
agent_created: true
---

# Codex 使用及 MG 动画生成流程规范

来源（飞书）：https://ccnope4jr4h4.feishu.cn/wiki/N1ITwrkweiTWmykoNyRcMqGHnNd

## Codex 安装提示
Codex 安装其实很简单，但要保证 Win 系统版本正确；遇到安装问题通常是因为 Win 系统版本问题，需要更换电脑或换系统。
下载安装地址（官方）：https://chatgpt.com/zh-Hans-CN/codex/

## MG 动画生成流程
Codex 搭配 HyperFrames（by HeyGen）可以直接生成炫酷的 MG 动画，但由于提示词描述有时不准确，建议：
1. **先用生图工具生成想要的 MG 动画效果图**；
2. 再把效果图上传到 Codex，张贴提示词让其生成 MG 动画。

### 生图提示词（可替换为你的文字稿）
```
我要做一个AE流程动效，来演示“中转服务器就像一个‘大型分流器’。他们把总的官方API Key接入自己的面板，然后像切蛋糕一样，生成无数个新的‘子API’令牌卖出去。”，你先帮我理解我的演示意图，然后帮我生成一张演示的AE效果图，要精致好看，苹果极简风格，纯黑色背景。
```
（把引号内的内容替换成你想要生成的演示动画的文字稿片段，然后复制所有提示词到生图工具，目前效果比较好的是 image2，可自由选择生图工具）

### 生成动画
把生成的效果图上传到 Codex，张贴提示词：
```
帮我根据效果图，生成ae效果的mg动画。
```

## 在 WorkBuddy 中的使用方式
WorkBuddy 可参考该流程：先出静态效果图（用图片生成能力），再据图生成动画/视频；HyperFrames 为 Codex 生态插件，WorkBuddy 侧可用等效的视频生成能力替代。
