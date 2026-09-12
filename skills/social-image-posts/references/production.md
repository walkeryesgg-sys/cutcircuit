# 图像生成与交付协议

## 模式

- `copy`：只写文案，交付来源、编排、规则检查、各平台配文。
- `prompts`：另加逐张完整提示词，不要求图片。
- `full`：包括实际图片、各平台发布包与检查。用户要求成品时默认此模式。

不要为了演示技能自行生成与用户无关的整套内容。创建技能的验收可以用明确标识的文案/规划案例，不宣称图片生成已通过实测。

## 原生图像工具流程

1. 读取当前可用 `imagegen` 技能，遵守其实际工具参数。默认内置工具；只有用户明确选择CLI/API路径才启用对应路径，不为文件保存控制自动切换付费后端。
2. 每张先存完整提示词，指定精确中文、生成的事实边界与用途。不只写“同上”或“跟上一张一样”。
3. 生成一张风格锚图，检查通过再生成后续。参考锚图用于统一风格，不强行重复主体构图；需不同结构的页面明确新增关系。
4. 保存工具实际返回的文件。内置工具通常把文件存到Codex生成目录，生成后复制进项目；不假设工具接受输出路径参数。后续有本地参考图先用 `view_image` 查看，按实际工具支持的路径或最近图像引用。
5. 检查中文、结构、关键箭头和阅读。把问题写入新版本提示词，通过图像编辑/重新生成定向修正。已有生成图的文字不要自行用代码涂盖；除非用户明确要求其他编辑方式，否则继续使用图像工具。若连续两次针对同一个问题仍失败，降低单页复杂度/拆页，保留成功资产并说明真实缺口。
6. 需要裁切或重排生成图时使用图像编辑工具并检查，不将9:16强行拉伸成3:4。不通过去标识、重新截图等方式隐匿AI属性。
7. 每个平台按真实需要交付独立图片；相同内页可以复用。保留来源和原创品牌，不带其他平台下载水印、二维码、假按钮和作者标识。对精确图表或已有矢量设计可走相应原生排版工具，但不能以简陋SVG充当用户要求的写实3D配图。

## 每张提示词的完整结构

用中文或英文描述画面均可；中文成品文字逐字引用。以下是字段合同，不是后端参数：

```text
Use case: scientific-educational
Platform / page purpose: [平台、页码、读者要懂什么]
Subject and evidence: [对象、版本、关键事实、已知/未知]
Scene: [视角、真实层级、结构关系、标注起终点]
Visual hierarchy: [主视觉、局部放大、留白、尺寸/比例目标]
Text verbatim: [完整标题、每个标签、结论、页码、示意声明]
Style: [背景、材料、色板、光照、字体层级]
Reference images: [锚图=风格；结构图=关系；实际引用方式另看工具]
Constraints: [必须保持的机制、数量、方向、几何关系]
Avoid: [虚构内部部件、无来源数字、乱码、假实拍、装饰噪声]
```

不默认加英文副标题。不要往内置工具塞 `--seed`、`--v`、`--q` 等其他工具参数。像素目标写进提示词但最终以文件实测为准，不称“8K成品”除非文件确实达到。

## 文件和清单

```text
<package>/
  sources.md
  storyboard.md
  platform-check.md
  prompts/                 # prompts/full
  xiaohongshu/post.md
  xiaohongshu/01-cover.png  # full，其余图按页序
  wechat-channels/post.md
  douyin/post.md
  manifest.json
  review.md
```

只创建用户要求的平台。各 `post.md` 包含：推荐标题与另外2个候选、封面短句、正文首句、完整正文、相关话题、可选讨论问题、图片顺序、AI声明及发布端待验项。不同平台的具体差异写入 `review.md`。完整来源放 `sources.md`，公开文案选择适合平台的出处表达。

`manifest.json` 示例（示意，不是真实成品）：

```json
{
  "mode": "full",
  "platforms": ["xiaohongshu", "wechat-channels", "douyin"],
  "pages": [
    {"platform": "xiaohongshu", "order": 1,
     "prompt": "prompts/xhs-01.md", "image": "xiaohongshu/01-cover.png",
     "width": 1080, "height": 1440,
     "ai_generated": true, "disclosure": "AI生成·原理示意",
     "visual_review": "passed"}
  ]
}
```

列出实际全部页面而不是只复制这一行；`copy`模式 `pages` 可空；`prompts`模式每页须有prompt但可无image；`full`必须图片存在可解码、尺寸等于记录且 `visual_review=passed`。未检查填 `pending`，不能为过校验写passed。图片生成标记依据实际来源，混合素材含生成内容也记true。

运行 `python3 <skill-dir>/scripts/validate_package.py <package-dir>`；图片解码需要Pillow。缺依赖时只说明如何安装，不能退化为仅检查扩展名而报告通过。

校验不替代视觉检查。`review.md`记录真实检查方式、问题/修复、成品是否完整、发布入口是否实测。草稿缺图片可保持在项目，但不作为完整成品交付。不要把上传数量未知或后台未登录误标成图片没做完，也不要宣称已被平台接受。
