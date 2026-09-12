# 2026-09 制作复盘：从现象到门禁

案例：`videos/spacex-price-bet-rebuild`，前序为 `spacex-price-bet-full-12min`。当前候选 624.833 秒；用户认可完成度与连续旁白，但指出内容像流水账、重点不易记住。以下是工程记录与用户反馈，不是全片已达 9.8 分的证明。

| 踩坑 | 根因 / 后续动作 | 可核对证据 |
|---|---|---|
| 两套字幕 | 带烧录字幕的引导片叠加新字幕。逐素材记录 baked/native/overlay 所有者，交付只留指定的一套；采集 TTS 用的 SRT 不是交付字幕时钟。 | 制作对话；audio-repair；CAPTION-REVIEW |
| 音频接缝拖沓 | 原生停顿外又加留白。停顿范围指最终听到的总间隔，不是额外 padding。按真实波形拼接、连续试听；保留已确认音轨，不盲目清零自然停顿。 | audio-repair/continuous-timing.json；USER-LISTENING-APPROVAL.md |
| 字幕与声音开口不齐、长句布局误判 | ASR 起点可能为零但实际尚未开口；CSS 与 ASS 字号不等于同样可见字高。以波形定位，以实际输出量字宽、字高；保持完整 cue，内部换行不另切时间。 | qa/CAPTION-REVIEW.md；scripts/check_captions.py |
| 白字幕、白水印在亮景消失 | 模板合规不代表该背景可读。对所有亮/繁杂场景及替换片检查首中尾；预先解决构图或批准的对比度变体，不把事后叠字补丁当通用品牌模板。 | qa/WATERMARK-REPAIR.md；qa/CAPTION-REVIEW.md |
| 水印几乎看不见、片尾拿错 | 全画布 SVG 被当局部 logo 缩放；文件名不能证明是批准母版。核对 viewBox、实际字形尺寸与位置；片尾绑定批准参考及哈希。 | scripts/build_film.mjs；素材与片尾选择记录 |
| 镜头中段对题、尾部跑题 | 只看代表帧忽略源窗口内切镜。检查完整源时间窗、首中尾和正常速度运动；换素材后重查。 | qa/REVIEW-LIMITS.md；镜头替换记录 |
| 渲染版本 / 滤镜不兼容、快速捕获回退重跑 | 先核验本机实际版本、ASS/drawtext 等必需能力以及短段捕获，锁定本项目验证过的配置。不要把某次有效版本、安装路径或 fast 模式固化为永远有效。 | 渲染日志；scripts/finish_candidate.mjs |
| 单声道转立体声后音量变化 | 显式确认声道路由与混音增益；检测最终总线，不从源音量推断。案例使用双单声道路由，但不对原生立体声强套该处理。 | scripts/finish_candidate.mjs；qa/final-technical-report.json |
| 分章拼接累计帧数误差 | 用 round(end×fps)−round(start×fps) 分配共享时钟帧数，不逐章 ceil。验证实际解码帧数；禁止用长尾补帧掩盖缺失媒体。 | scripts/finish_candidate.mjs；最终 18745 帧检查 |
| 局部修好就宣称全片完成 | 哈希、解码、抽帧只能证明各自范围。音频包哈希相同不等于已听完整混音；导出 MP4 不等于已导入剪映；局部评分不能归一化冒充总分。 | qa/REVIEW-LIMITS.md；qa/WATERMARK-REPAIR.md；评分报告 |
| 信息全但人记不住 | 六章、89 个解释状态覆盖多个并列问题；信息回报表不能证明主次、因果和迁移。先缩小问题、删支线、测试无提示复述，再生成声音和画面。 | editorial-states.tsv；用户 2026-09-09 反馈；five-minute-focus-and-recall.md |

以上工程防线要在短风险样段中覆盖高风险状态，避免到完整渲染后才发现。但技术通过与人类理解是两项独立验收，不相互代替。
