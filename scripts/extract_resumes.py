#!/usr/bin/env python3
"""Extract text from resume files (PDF / DOCX, including scanned PDFs via OCR).

Usage:
    python extract_resumes.py <input> -o extracted.json [--no-ocr]

<input> may be a folder or a single .pdf / .docx file.

Output JSON has one entry per supported file:
{
  "files": [
    {
      "file": "张三-产品.pdf",
      "path": "C:/.../张三-产品.pdf",
      "method": "pdf_text" | "docx" | "ocr" | "ocr_required" | "failed",
      "error": null | "message",
      "pages": 3,
      "chars": 1200,
      "text": "...",
      "text_hash": "...",
      "low_text": false
    }
  ]
}

method "ocr" means the PDF was treated as scanned and recognized via OCR.
method "ocr_required" means the PDF looks scanned but rapidocr-onnxruntime is
not installed; run `pip install rapidocr-onnxruntime` and rerun.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

SUPPORTED = {".pdf", ".docx"}
UNSUPPORTED = {".doc"}


def normalize(text: str) -> str:
    return re.sub(r"\s+", "", text or "")


def text_hash(text: str) -> str:
    return hashlib.sha256(normalize(text).encode("utf-8")).hexdigest()


def find_files(input_path: Path) -> tuple[list[Path], list[Path]]:
    """Return (supported_files, unsupported_old_doc_files)."""
    if input_path.is_file():
        ext = input_path.suffix.lower()
        if ext in SUPPORTED:
            return [input_path], []
        if ext in UNSUPPORTED:
            return [], [input_path]
        return [], []
    files, unsupported = [], []
    for p in sorted(input_path.rglob("*")):
        if not p.is_file():
            continue
        ext = p.suffix.lower()
        if ext in SUPPORTED:
            files.append(p)
        elif ext in UNSUPPORTED:
            unsupported.append(p)
    return files, unsupported


def extract_pdf_text(path: Path) -> tuple[str, int]:
    import pdfplumber

    parts = []
    with pdfplumber.open(str(path)) as pdf:
        page_count = len(pdf.pages)
        for page in pdf.pages:
            parts.append(page.extract_text() or "")
    return "\n".join(parts), page_count


def extract_docx_text(path: Path) -> str:
    from docx import Document
    from docx.table import Table
    from docx.text.paragraph import Paragraph

    doc = Document(str(path))
    parts = []
    for child in doc.element.body.iterchildren():
        tag = child.tag
        if tag.endswith("}p"):
            parts.append(Paragraph(child, doc).text)
        elif tag.endswith("}tbl"):
            table = Table(child, doc)
            for row in table.rows:
                cells = [c.text.strip().replace("\n", " ") for c in row.cells]
                parts.append(" | ".join(cells))
    return "\n".join(parts)


def looks_scanned(text: str, pages: int, min_chars_per_page: int) -> bool:
    if not text.strip():
        return True
    if pages <= 0:
        return True
    return len(normalize(text)) / pages < min_chars_per_page


_OCR_ENGINE = None


def get_ocr_engine():
    global _OCR_ENGINE
    if _OCR_ENGINE is None:
        from rapidocr_onnxruntime import RapidOCR

        _OCR_ENGINE = RapidOCR()
    return _OCR_ENGINE


def ocr_pdf(path: Path, scale: float) -> str:
    import numpy as np
    import pypdfium2 as pdfium

    engine = get_ocr_engine()
    pdf = pdfium.PdfDocument(str(path))
    parts = []
    try:
        for page in pdf:
            bitmap = page.render(scale=scale)
            img = np.array(bitmap.to_pil().convert("RGB"))
            result, _ = engine(img)
            if result:
                parts.append("\n".join(item[1] for item in result))
    finally:
        pdf.close()
    return "\n".join(parts)


def extract_one(path: Path, use_ocr: bool, ocr_scale: float, min_chars_per_page: int) -> dict:
    entry = {
        "file": path.name,
        "path": str(path),
        "method": "failed",
        "error": None,
        "pages": 0,
        "chars": 0,
        "text": "",
        "text_hash": None,
        "low_text": False,
    }
    try:
        ext = path.suffix.lower()
        if ext == ".pdf":
            text, page_count = extract_pdf_text(path)
            entry["pages"] = page_count
            scanned = looks_scanned(text, page_count, min_chars_per_page)
            if scanned and use_ocr:
                try:
                    text = ocr_pdf(path, ocr_scale)
                    entry["method"] = "ocr"
                except ImportError:
                    entry["method"] = "ocr_required"
                    entry["error"] = (
                        "扫描版 PDF 需要 OCR 依赖，请先安装：pip install rapidocr-onnxruntime"
                    )
                    return entry
                except Exception as exc:  # noqa: BLE001 - report any OCR failure
                    entry["method"] = "ocr_failed"
                    entry["error"] = f"OCR 失败: {exc}"
                    return entry
            else:
                entry["method"] = "pdf_text"
        elif ext == ".docx":
            text = extract_docx_text(path)
            entry["method"] = "docx"
        entry["low_text"] = looks_scanned(text, max(entry["pages"], 1), min_chars_per_page)
        entry["text"] = text
        entry["chars"] = len(normalize(text))
        entry["text_hash"] = text_hash(text)
    except Exception as exc:  # noqa: BLE001 - record per-file failure
        entry["error"] = f"{type(exc).__name__}: {exc}"
    return entry


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract text from resume PDFs/DOCX.")
    parser.add_argument("input", help="Folder or single file containing resumes")
    parser.add_argument("-o", "--output", default="extracted.json", help="Output JSON path")
    parser.add_argument(
        "--no-ocr", action="store_true", help="Skip OCR for scanned PDFs (marks them low_text)"
    )
    parser.add_argument("--ocr-scale", type=float, default=2.0, help="Render scale for OCR (default 2.0)")
    parser.add_argument(
        "--min-chars-per-page",
        type=int,
        default=15,
        help="Below this avg chars/page, treat PDF as scanned (default 15)",
    )
    args = parser.parse_args()

    if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"[ERROR] 路径不存在: {input_path}", file=sys.stderr)
        return 2

    files, unsupported = find_files(input_path)
    if not files and not unsupported:
        print("[ERROR] 未找到 .pdf / .docx 文件。", file=sys.stderr)
        return 1
    for doc in unsupported:
        print(f"[SKIP] 旧版 .doc 不支持（请另存为 .docx）：{doc.name}", file=sys.stderr)

    results = []
    for idx, path in enumerate(files, 1):
        entry = extract_one(path, not args.no_ocr, args.ocr_scale, args.min_chars_per_page)
        status = {
            "ocr": "OCR(扫描件)",
            "pdf_text": "PDF文字",
            "docx": "Word",
            "failed": "失败",
            "ocr_required": "需装OCR",
            "ocr_failed": "OCR失败",
        }.get(entry["method"], entry["method"])
        print(f"[{idx}/{len(files)}] {status} {entry['file']} (chars={entry['chars']})")
        if entry["error"]:
            print(f"          错误: {entry['error']}")
        results.append(entry)

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps({"files": results}, ensure_ascii=False, indent=2), encoding="utf-8")

    ok = [r for r in results if r["method"] != "failed"]
    failed = [r for r in results if r["method"] == "failed"]
    scanned = [r for r in results if r["method"] == "ocr"]
    low_text = [r for r in results if r.get("low_text")]
    print(f"\n完成：{len(results)} 份，成功 {len(ok)} 份，失败 {len(failed)} 份。")
    if scanned:
        print(f"扫描件 OCR：{len(scanned)} 份")
    if low_text:
        print(f"[注意] 以下文件提取文本偏少，建议人工复核：{', '.join(r['file'] for r in low_text)}")

    by_hash: dict[str, list[str]] = {}
    for r in results:
        if r["text_hash"]:
            by_hash.setdefault(r["text_hash"], []).append(r["file"])
    dups = {h: names for h, names in by_hash.items() if len(names) > 1}
    if dups:
        print("[提示] 检测到内容完全相同的简历（疑似重复投递）：")
        for names in dups.values():
            print(f"  - {' / '.join(names)}")

    print(f"已写入: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
