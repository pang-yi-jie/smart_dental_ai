"""深度分析家长端交互展示 HTML：结构、配色、排版、子页面、素材。"""

import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HTML = r"C:\Users\Administrator\Documents\xwechat_files\wxid_lw4lrvwf20th22_19f8\msg\attach\7f3cf2d6b50f9ece4da87dbbc76e31cb\2026-10\Rec\3f3d46a34d85e81d\F\8\家长端口腔评估交互展示 (1).html"

raw = Path(HTML).read_text(encoding="utf-8", errors="replace")
print(f"HTML 总大小: {len(raw)} 字符")

# 1. 去掉 base64 图片数据（很大）
raw_noimg = re.sub(r"data:image/[^\"']+", "[IMG]", raw)
print(f"去掉图片后: {len(raw_noimg)} 字符")

# 2. 提取 <style> 里的 CSS
styles = re.findall(r"<style[^>]*>(.*?)</style>", raw, flags=re.S | re.I)
print(f"\n=== 找到 {len(styles)} 个 <style> 块 ===")

# 提取所有颜色值
all_css = "\n".join(styles)
colors = re.findall(r"#[0-9a-fA-F]{3,8}\b", all_css)
from collections import Counter
color_freq = Counter(c.upper() for c in colors)
print("\n=== 使用频率最高的 25 个颜色 ===")
for c, n in color_freq.most_common(25):
    print(f"  {c}  x{n}")

# 字体
fonts = re.findall(r"font-family\s*:\s*([^;]+)", all_css)
print("\n=== font-family ===")
for f in set(fonts):
    print(f"  {f.strip()}")

# 3. 提取 class 名（结构）
classes = re.findall(r'class="([^"]+)"', raw_noimg)
class_counter = Counter()
for c in classes:
    for cls in c.split():
        class_counter[cls] += 1
print("\n=== 出现最多的 40 个 class 名 ===")
for cls, n in class_counter.most_common(40):
    print(f"  .{cls}  x{n}")

# 4. 提取 body 内纯文本（保留结构）
body = re.sub(r"<script[^>]*>.*?</script>", " ", raw_noimg, flags=re.S | re.I)
body = re.sub(r"<style[^>]*>.*?</style>", " ", body, flags=re.S | re.I)
body = re.sub(r"<(br|/p|/div|/h[1-6]|/li|/section|/tr)[^>]*>", "\n", body, flags=re.I)
body = re.sub(r"<[^>]+>", "", body)
body = re.sub(r"\n\s*\n+", "\n", body)
body = re.sub(r"[ \t]+", " ", body)
lines = [l.strip() for l in body.split("\n") if l.strip()]
print(f"\n=== 纯文本 {len(lines)} 行 ===")
Path(r"D:\SmartDentalAI\_ref\html_analysis.txt").write_text(
    "\n".join([f"{i+1}: {l}" for i, l in enumerate(lines)]), encoding="utf-8"
)
print("已保存到 _ref/html_analysis.txt")
