---
name: filter-gesture-interaction-prompt
description: 用 MediaPipe + Canvas 2D 做浏览器端 AR 双手手势交互滤镜特效的提示词（禁框架、单文件）。当用户要用 AI 做一个实时摄像头手势滤镜网页时使用。
agent_created: true
---

# Codex 制作滤镜手势交互效果提示词

来源（飞书）：https://ccnope4jr4h4.feishu.cn/wiki/K4lLwtuCjikCqTkf6phcp7x6n3c

## 提示词原文（可直接使用，部分）
```
你是一位顶级的 Web 前端互动视觉工程师和 WebGL/Canvas 性能优化专家。
请为我编写一个可以直接运行的浏览器端 AR 双手手势交互特效。

核心技术栈（严格遵守）
- 原生 HTML、CSS、JavaScript (ES6+)
- 原生 HTML5 Canvas 2D API
- MediaPipe Tasks Vision API（必须使用最新版 @mediapipe/tasks-vision，通过 jsDelivr 或 unpkg CDN 引入）
- 绝对禁止使用任何前端框架（Vue/React）或图形库（Three.js/Pixi.js）。
- 所有逻辑包含在一个完整的项目中。

核心交互与视觉逻辑
- 数据获取与排序：调用摄像头（镜像显示）。同时运行 HandLandmarker 和 ImageSegmenter。获取手部 21 个关键点，必须根据手掌中心的 X 坐标（而不是 handedness）在画面中区分“左侧手”和“右侧手”。提取指尖关键点：拇指(4)、食指(8)、中指(12)、小指(20)。
- 连线与多边形生成：必须找到左右手，将对应指尖连接成三个四边形区域（Quad）：
  【区域 A】：左拇指-右拇指-右食指-左食指
  【区域 B】：左食指-右食指-右中指-左中指
  【区域 C】：左中指-右中指-右小指-左小指
  对四边形顶点进行简单的插值平滑处理（Lerp），减少画面抖动。
- 视觉滤镜渲染：使用 ctx.save() -> ctx.beginPath()（绘制四边形路径）-> ctx.clip() 创建遮罩窗口。在裁剪区域内重新绘制当前视频帧，应用强烈的 ctx.filter 和 globalCompositeOperation 模拟特效。
  红区（区域 A）：应用高对比度、复古偏红色调（如 contrast(200%) sepia(100%) hue-rotate(-50deg)），并叠加半透明红色网点或噪点图案（用 Canvas API 动态生成 pattern 并 fill）。
```

> 文档中红/绿/蓝三区（A/B/C）各有不同滤镜参数，内容较长。请在能登录飞书时补全到 `references/filter-gesture-full.md`。

## 在 WorkBuddy 中的使用方式
可直接把上述提示词发给 WorkBuddy，让其生成一个单文件 HTML 手势滤镜特效；补全完整三区参数后效果更完整。
