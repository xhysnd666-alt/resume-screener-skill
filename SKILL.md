---
name: resume-screener
description: 按用户提供的 JD 批量筛选简历：解析 PDF/Word（含扫描版，OCR 兜底）简历，按硬性/加分/模糊标准逐份评估，输出匹配度、证据化点评、缺口与待核实问题，并生成单份 Excel 汇总表供人工核实。当用户说"筛简历/筛选简历/帮我看看这些简历/按这份 JD 筛选/这批简历匹配度怎么样/输出简历筛选结果"并给出简历文件或文件夹（.pdf/.docx）时使用。也适用于候选人初筛、简历匹配度打分、简历点评、投递归档整理等场景。
---

# Resume Screener（简历筛选）

批量筛选 PDF/Word 简历（含扫描版），按 JD 逐份评估，产出「筛选总表 + 逐份点评 + JD 拆解」一份 Excel，供 HR 核实后决策。

## 工作流

### Step 1 获取并确认 JD

1. 请用户提供 JD：粘贴文字或给出文件路径均可。
2. 按 [evaluation_guide.md](references/evaluation_guide.md) 拆解为：硬性要求 / 加分项 / 模糊项，每条注明 JD 原文。
3. 把清单展示给用户确认；用户补充的内部要求（如"不接受频繁跳槽"）一并记入并标注"用户补充"。

### Step 2 收集简历

- 接受一个文件夹或若干文件，格式 `.pdf` / `.docx`。
- 旧版 `.doc` 不支持：提示用户另存为 `.docx` 后重新提供。
- 每批建议 ≤30 份，超过则分批处理。

### Step 3 提取文本

1. 确定 Python 解释器：桌面版 Codex 优先调用 `load_workspace_dependencies` 返回的自带 Python；不可用时退回 `python` / `py -3`。运行前确认依赖：`pdfplumber`、`python-docx`、`openpyxl`、`pypdfium2`；扫描件还需 `rapidocr-onnxruntime`（缺失时安装；国内网络慢可用清华镜像：`pip install rapidocr-onnxruntime -i https://pypi.tuna.tsinghua.edu.cn/simple`）。
2. 运行：
   ```bash
   python scripts/extract_resumes.py <简历文件夹> -o extracted.json
   ```
3. 检查输出：
   - `method=ocr` → 扫描件识别成功；`low_text=true` 的条目要人工复核。
   - `method=ocr_required` / `failed` → 处理依赖或报错后重跑；失败文件如实告知用户。
   - 相同 `text_hash` → 重复投递，评估时标注。

### Step 4 逐份评估

1. 复制 [evaluation_template.json](assets/evaluation_template.json) 为 `evaluation.json`，按其中 schema 填写。
2. 对每份简历，严格按 [evaluation_guide.md](references/evaluation_guide.md) 评估：逐条核对硬性要求、加分项、模糊项；每条结论引用简历原文。
3. 写出 `evaluation.json`（UTF-8）。
4. 自查后再写文件：结论与分数一致；每条匹配/缺口都有证据；不脑补未提及内容。

### Step 5 生成 Excel

```bash
python scripts/build_report.py evaluation.json -o 简历筛选结果.xlsx
```

生成后快速核对：候选人数量一致、结论分布与 evaluation.json 一致。

### Step 6 用户核实

1. 向用户展示总表摘要：结论分布、排名前几、待定/淘汰中值得复议的对象、重复投递。
2. 用户反馈调整（改结论、改分数、补要求）后，修改 evaluation.json 并重新生成 Excel，直到用户满意。
3. 把最终 Excel 放到用户指定的输出位置（如 `outputs/`），并说明每张表的内容。

## JSON 输出规范

`evaluation.json` 结构见 [evaluation_template.json](assets/evaluation_template.json)：

- `jd_breakdown`: `hard_requirements` / `bonus` / `ambiguous`，与用户确认后的清单。
- `candidates[]`:
  - `file` / `name`
  - `conclusion`: `通过` | `待定` | `淘汰`
  - `score`: 0-100 整数
  - `match_summary`: 一句话结论
  - `evidence[]`: `{jd_requirement, resume_snippet, assessment}`，assessment ∈ `完全匹配` | `部分匹配` | `未提及`
  - `gaps[]`: 缺口
  - `questions[]`: 待核实问题（1-3 个最有价值的）
  - `interview_focus[]`: 面试建议关注点
  - `notes`: 备注（如"重复投递"、"用户放宽学历要求"）

## 资源

- `scripts/extract_resumes.py` — 批量提取 PDF/DOCX 文本，扫描件自动 OCR，输出 `extracted.json`。
- `scripts/build_report.py` — 把 `evaluation.json` 渲染成单份 Excel（筛选总表 / 逐份点评 / JD 拆解）。
- `assets/evaluation_template.json` — evaluation.json 的结构模板。
- `references/evaluation_guide.md` — JD 拆解、评分、证据引用、核查注意点等完整方法论。
