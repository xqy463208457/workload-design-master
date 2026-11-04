# -*- coding: utf-8 -*-
"""读取需求文档（.doc / .docx / .txt），并可直接抽取“业务功能”条目。

用法：
  python doc_read.py 需求说明书.doc                     # 打印全文前 3000 字
  python doc_read.py 需求说明书.doc --out full.txt       # 导出全文
  python doc_read.py 需求说明书.doc --modules            # 只列业务功能条目
"""
import argparse
import os
import re
import struct
import sys

CN_NUM = "一二三四五六七八九十"


def read_doc(path):
    """解析 Word 97-2003 二进制格式（OLE2 + 片段表）。"""
    import olefile
    ole = olefile.OleFileIO(path)
    try:
        wd = ole.openstream("WordDocument").read()
        flags = struct.unpack_from("<H", wd, 0x0A)[0]
        tbl_name = "1Table" if (flags & 0x0200) else "0Table"
        if not ole.exists(tbl_name):
            tbl_name = "1Table" if ole.exists("1Table") else "0Table"
        tbl = ole.openstream(tbl_name).read()
        fc_clx, lcb_clx = struct.unpack_from("<II", wd, 0x01A2)
        clx = tbl[fc_clx:fc_clx + lcb_clx]
        i = 0
        while i < len(clx) and clx[i] == 0x01:
            cb = struct.unpack_from("<h", clx, i + 1)[0]
            i += 3 + cb
        if clx[i] != 0x02:
            raise ValueError("文档片段表格式异常，可能是 Word 6.0/95 格式")
        lcb_pt = struct.unpack_from("<I", clx, i + 1)[0]
        pt = clx[i + 5:i + 5 + lcb_pt]
        n = (len(pt) - 4) // 12
        cps = [struct.unpack_from("<I", pt, 4 * k)[0] for k in range(n + 1)]
        out = []
        for k in range(n):
            off = 4 * (n + 1) + 8 * k
            fc = struct.unpack_from("<I", pt, off + 2)[0]
            ncp = cps[k + 1] - cps[k]
            if fc & 0x40000000:
                fc = (fc & ~0x40000000) // 2
                out.append(wd[fc:fc + ncp].decode("cp936", errors="replace"))
            else:
                out.append(wd[fc:fc + ncp * 2].decode("utf-16-le", errors="replace"))
    finally:
        ole.close()
    text = "".join(out)
    text = (text.replace("\r", "\n").replace("\x07", "\t")
            .replace("\x0b", "\n").replace("\x0c", "\n"))
    return re.sub(r"[\x00-\x08\x0e-\x1f]", "", text)


def read_docx(path):
    import docx
    d = docx.Document(path)
    parts = [p.text for p in d.paragraphs]
    for t in d.tables:
        for row in t.rows:
            parts.append("\t".join(c.text.strip() for c in row.cells))
    return "\n".join(parts)


def read_text(path):
    ext = os.path.splitext(path)[1].lower()
    if ext == ".doc":
        head = open(path, "rb").read(8)
        if head[:4] == b"PK\x03\x04":
            return read_docx(path)          # 实际是 docx，只是扩展名写成了 doc
        return read_doc(path)
    if ext == ".docx":
        head = open(path, "rb").read(8)
        if head[:4] == b"\xd0\xcf\x11\xe0":
            return read_doc(path)           # 实际是 doc，只是扩展名写成了 docx
        return read_docx(path)
    with open(path, encoding="utf-8", errors="replace") as fh:
        return fh.read()


def extract_modules(text):
    """抽取“业务功能N：标题”，返回去重后的标题列表（保持文档顺序）。"""
    pattern = re.compile(r"业务功能([%s]+)\s*[：:]\s*([^\n\t]{2,80})" % CN_NUM)
    seen, out = set(), []
    for m in pattern.finditer(text):
        name = m.group(2).strip().rstrip("。，,；;")
        if not name or len(name) < 2:
            continue
        key = name
        if key in seen:
            continue
        # 目录行带 PAGEREF，跳过
        tail = text[m.end():m.end() + 12]
        if "PAGEREF" in tail or "\\h" in tail:
            continue
        seen.add(key)
        out.append(name)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--out", default="")
    ap.add_argument("--modules", action="store_true")
    ap.add_argument("--chars", type=int, default=3000)
    a = ap.parse_args()

    text = read_text(a.file)
    if a.modules:
        mods = extract_modules(text)
        print("业务功能条目 %d 个：" % len(mods))
        for i, m in enumerate(mods, 1):
            print("  %2d. %s" % (i, m))
        return 0
    if a.out:
        with open(a.out, "w", encoding="utf-8") as fh:
            fh.write(text)
        print("已导出 %d 字到 %s" % (len(text), a.out))
        return 0
    print(text[:a.chars])
    print("\n... 全文 %d 字" % len(text))
    return 0


if __name__ == "__main__":
    sys.exit(main())
