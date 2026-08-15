# 🧾 Resume Screener / 简历筛选官

> AI 帮你熬夜，HR 早点下班。
> Let AI pull the all-nighter, so you can clock out on time.

一个给 HR 用的 Codex skill：丢一份 JD 和一堆简历进来，它帮你拆标准、读简历、打分、写点评，最后吐出一张 Excel 总表。

A Codex skill for HR folks: throw in a job description and a pile of resumes, and it breaks down the requirements, reads every resume, scores them, writes evidence-based comments, and hands you back one clean Excel sheet.

---

## 🤔 这是什么 / What is this

简历筛选官是一个 **技能（Skill）**，不是一个独立软件。装进 Codex 之后，你只需要说一句话，比如：

> "按这份 JD 筛一下这个文件夹里的简历"

它就会自动完成从读简历到出报告的全过程。核心思路是：**AI 负责琐碎的"读"和"记"，你负责关键的"拍板"。**

It's a **skill**, not a standalone app. Once installed into Codex, you just say something like *"screen the resumes in this folder against this JD"*, and it handles everything from reading files to generating the report. The philosophy: **AI does the tedious reading, you do the real deciding.**

## 💡 为什么做它 / Why we built it

作者是一名 HR 招聘实习生，曾为了 30 份简历熬夜到凌晨三点——不是在看简历，是在数简历。于是决定：

- 让 AI 先把"看"这件事干完；
- 让判断标准统一，不再"今天心情好就多看一眼"；
- 让每一份淘汰都有理有据，面试官问起来不心虚。

The author is an HR recruiting intern who once stayed up until 3 a.m. with 30 resumes — not reading them, just counting them. So we decided to:

- Let AI do the "reading" first;
- Make screening criteria consistent instead of "I feel like it today";
- Make every rejection defensible, so you never panic when a hiring manager asks "why not this one?"

## ✨ 它能干什么 / What it can do

- **📄 多格式兼容**：PDF、Word 都能读；扫描版图片 PDF 自动 OCR 识别（中文也认识）。
- **📋 JD 拆解**：把 JD 拆成硬性要求、加分项、模糊项，先给你过目再开工。
- **🧮 匹配度打分**：0-100 分 + 通过 / 待定 / 淘汰 三档结论。
- **🔍 证据化点评**：每条判断都引用简历原文——"JD 要 3 年经验 ↔ 简历第 2 页写了 2021-2024"。
- **❓ 待核实清单**：每个候选人附 1-3 个最值得追问的问题，面试前直接抄作业。
- **📊 一键出表**：筛选总表 + 逐份点评 + JD 拆解，全部塞进一份 Excel。
- **👯 去重雷达**：同一份简历换了个名字投两次？它当场举报。

- **📄 Multi-format**: PDF and Word; scanned PDFs are handled with built-in OCR (Chinese-friendly).
- **📋 JD parsing**: breaks the JD into hard requirements, bonus points, and fuzzy asks — and shows you the list before starting.
- **🧮 Matching score**: 0-100 + Pass / Hold / Reject.
- **🔍 Evidence-based comments**: every judgment cites the resume — "JD wants 3 yrs experience ↔ resume page 2 says 2021-2024".
- **❓ Verification list**: 1-3 key questions per candidate. Steal them for interviews.
- **📊 One-click Excel**: summary table + detailed review + JD breakdown in a single workbook.
- **👯 Duplicate radar**: same resume under a different name? Snitches immediately.

## 🎯 给谁用 / Who it's for

- **HR 实习生**：批量初筛神器，救命恩人，评语担当。
- **招聘专员 / HRBP**：把重复劳动外包给 AI，把时间留给候选人。
- **面试官**：拿着待核实清单去面试，比候选人还懂他的简历。
- **求职者（友情模式）**：想提前知道自己的简历在 HR 眼里值几分？也可以拿它自测。

- **HR interns**: batch-screening lifesaver and comment-section MVP.
- **Recruiters / HRBPs**: outsource the grunt work, keep the human touch.
- **Interviewers**: walk in with a verification list and know the resume better than the candidate.
- **Job seekers (friends mode)**: curious how your resume scores in the eyes of HR? Run it on yourself.

## 🚀 怎么用 / How to use

完整说明见 [SKILL.md](SKILL.md)。一句话版：

1. 给 Codex 一份 JD（粘贴或文件）；
2. 丢一个简历文件夹（PDF / Word / 扫描件都行，建议每批 ≤30 份）；
3. 等它出 Excel，你看一眼，有异议就改，改完定稿。

Full instructions live in [SKILL.md](SKILL.md). The short version:

1. Give Codex a JD (paste or file);
2. Drop in a resume folder (PDF / Word / scanned OK, ≤30 per batch recommended);
3. Wait for the Excel, review it, raise objections if any, finalize.

## 🗺️ 未来更新 / Roadmap

现役版本很好用，但作者还想让它更卷：

- 多份 JD 横向对比（一人投仨岗位，一次看全）；
- 面试问题自动生成（从"关注点"进化成完整追问清单）；
- 拒信/邀约模板生成（HR 的深夜文案救星）；
- 人才库模式：把历史简历存起来，下次招人直接搜；
- 多语言简历支持；
- 手机端"边喝咖啡边刷结果"模式（画饼中）。

It works well today, but we're not done being ambitious:

- Compare multiple JDs side by side (one candidate, three roles, one view);
- Auto-generated interview question banks (upgrade from "focus points" to full scripts);
- Rejection / invitation email templates (the HR late-night writing lifesaver);
- Talent-pool mode: archive screened resumes, search them for the next role;
- Multi-language resume support;
- "Sip coffee while scrolling results on your phone" mode (roadmap pie).

## ⚠️ 免责声明 / Disclaimer

匹配度只是参考，不是圣旨。AI 会帮你省时间，但不会替你背锅——**最终用人决定权永远在你手里**。

The score is a reference, not a verdict. AI saves you time, but won't take the blame for you — **the final hiring call is always yours**.

---

Made with 🧋 + ☕ by an HR intern who just wanted to sleep.
