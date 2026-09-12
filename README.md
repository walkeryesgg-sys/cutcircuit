# CutCircuit

**Source. Cut. Score. Repair.**

CutCircuit is a Codex plugin for evidence-led video production. Its original video workflow combines four installable skills:

- `cutcircuit` routes requests and runs the quality loop.
- `produce-social-video` plans, scripts, edits, renders, repairs, and delivers.
- `score-social-video` independently evaluates finished videos against measurable release gates.
- `youtube-research-downloader` downloads and verifies authorized YouTube research media.

The full workflow is:

```text
interview → script + structure + shot list + storyboard → user approval → source → produce → score → repair → rescore → deliver
```

CutCircuit does not begin production from a topic or URL alone. It first delivers a versioned professional pre-production plan covering the complete script, narrative structure, beat sheet, shot list, storyboard, sound and caption treatment, asset/rights plan, risks, delivery specification, and acceptance gates. Formal media acquisition, TTS, editing, animation, and rendering begin only after the user explicitly approves that plan version.

For source-led public videos, CutCircuit includes a reusable commentary template: full-screen real footage, Chinese narration alternating with complete original-audio evidence, failure or uncertainty before the midpoint, delayed visual payoff in the second half, and a horizontal full-bleed hero ending. The template keeps factual entity labels, subtitles, audio continuity, and final-shot composition inside the release gates.

Ordinary videos target 9.0/10, paid or member content targets 9.5/10, and premium work targets 9.8/10 plus a complete linear watch. CutCircuit reports the real result when a target is not met; it does not weaken quality gates to manufacture a pass.

CutCircuit also measures sampled video luminance and a blur/softness proxy alongside black/freeze/silence signals. These metrics are diagnostic rather than automatic style verdicts: nominally-HD or dark cinematic work passes only when faces, machinery, and evidence details remain visibly crisp and legible.
The probe also reports integrated LUFS and true peak dBTP so a file cannot pass merely because its average/sample volume looks reasonable.

Programmed motion follows a deterministic, seek-safe timeline contract derived from official GSAP practices: labeled beats, explicit start/end states, transform-first animation, restrained easing, full-resolution performance checks, and frame sampling across every animated interval. CutCircuit also carries a regression checklist learned from real revisions so TTS boundary errors, linear-playback silence, late-track noise, weak first frames, mistimed spectacle, and undersized final shots are not reintroduced by later repairs.

For `硬核火星人`, CutCircuit records two routing fields in every new production brief: `program_type` separates curriculum-based `member_original` work from free `public_story` work, while `edit_model` selects source-led, narration-led montage, or hybrid evidence-lesson cutting. The member profile uses the canonical lower-right Chinese-only `硬核火星人` orbit watermark.

`马斯克商业解读` member originals use a dedicated commercial-mystery template: a visible contradiction, one repeatable explanation engine, escalating evidence and incentives, a serious limit or counterargument, and an operational conclusion. The workflow integrates six Open Design motion-UI families—data overview, timeline, cost tree, causal chain, comparison matrix, and evidence card—while keeping real footage and primary evidence visually dominant. An explicit 98-point request means an independently audited score of at least 9.8/10, zero fatal gates, and a completed final linear watch; it is not a promise of views or sales.

## 自研技能目录 / Original skill collection

本仓库汇总日常研究、写作、图文和视频制作中沉淀的九个自研 skill。可单独安装所需目录；CutCircuit 视频总控不会自动执行公众号发布。现有视频规则和本次汇总的最新修订一起保留。

| Skill | 用途 |
|---|---|
| [cutcircuit](skills/cutcircuit/SKILL.md) | 视频总控、质量闭环 |
| [produce-social-video](skills/produce-social-video/SKILL.md) | 视频前期、制作、修复与交付 |
| [score-social-video](skills/score-social-video/SKILL.md) | 独立审片与发布门禁 |
| [youtube-research-downloader](skills/youtube-research-downloader/SKILL.md) | 授权媒体下载与文件核验 |
| [youtube-research-pipeline](skills/youtube-research-pipeline/SKILL.md) | 研究视频发现、评分、去重和队列 |
| [wechat-article-studio](skills/wechat-article-studio/SKILL.md) | 公众号选题、写作、Humanizer终审、图文包和自检 |
| [wechat-publish-article](skills/wechat-publish-article/SKILL.md) | 公众号发布包预检、草稿交付与回执 |
| [social-video-packaging](skills/social-video-packaging/SKILL.md) | 多平台口播、标题、描述与封面设计 |
| [social-image-posts](skills/social-image-posts/SKILL.md) | 多平台图文、剖面科普与配图包 |

### 配置与外部依赖

- 将文档中的 `<your-vault>` 配置为自己的 Obsidian 或项目目录；案例中的品牌、栏目和质量目标可按用户指令替换。
- Humanizer、baoyu 系列、HyperFrames、GSAP、Open Design 等是可选或工作流所需的第三方依赖，并非本仓库原创或附带安装。按具体 skill 的说明从原项目安装；使用其代码时遵守各自许可。公众号润色流程需要可用的 Humanizer。
- 图片生成需要相应运行环境提供原生图像工具；发布需要用户授权及自己的登录环境。不要提交密钥、Cookie、浏览器资料、账号后台数据或生成的内容资产。
- `wechat-publish-article/scripts/update_draft.ts` 是实验性旧稿更新器：目前不支持本地正文插图，且DOM赋值与草稿ID不足以证明编辑器状态和保存成功。使用前需适配当前后台，检查保存响应并重新打开逐项验证；不可作为无人值守生产入口。正文含图片或需更新封面时按技能的其他交付路径处理。
- 自评分是编辑诊断；脚本结构检查不能替代真实音画审片，也不保证推荐量、收益或平台审核。

## Install

Install the repository as a Codex plugin or copy the desired folders under `skills/` into your Codex skills directory. Restart or open a new Codex session after installation so the skills are discovered.

Start with:

```text
Use $cutcircuit to produce this video and run the quality loop.
```

The downloader only handles material you are authorized to obtain. Download success does not grant reuse rights.

## Requirements

The core scripts use Python 3 and probe media with FFmpeg/FFprobe. YouTube transfers additionally require yt-dlp. Production may use an installed rendering or editing toolchain selected for the project.

## License

MIT
