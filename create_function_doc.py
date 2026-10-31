# -*- coding: utf-8 -*-
"""生成《口腔AI检测系统-功能说明文档》Word（面向医院，覆盖整个软件）。"""

from docx import Document
from docx.oxml.ns import qn
from docx.shared import Pt

FONT = "微软雅黑"
OUT = r"D:\SmartDentalAI\口腔AI检测系统-功能说明文档.docx"


def set_fonts(doc):
    for sname in ["Normal", "Heading 1", "Heading 2", "Heading 3", "Title"]:
        st = doc.styles[sname]
        st.font.name = FONT
        rpr = st.element.get_or_add_rPr()
        rfonts = rpr.get_or_add_rFonts()
        rfonts.set(qn("w:eastAsia"), FONT)
    doc.styles["Normal"].font.size = Pt(11)


def body(doc, text):
    p = doc.add_paragraph(text)
    p.paragraph_format.space_after = Pt(6)
    return p


def bullet(doc, text):
    p = doc.add_paragraph(text, style="List Bullet")
    p.paragraph_format.space_after = Pt(4)
    return p


def numbered(doc, text):
    p = doc.add_paragraph(text, style="List Number")
    p.paragraph_format.space_after = Pt(4)
    return p


doc = Document()
set_fonts(doc)

# ===== 标题 =====
doc.add_heading("口腔 AI 检测系统", level=0)
p = doc.add_paragraph("功能说明文档")
p.runs[0].font.size = Pt(14)

body(doc, "本系统为口腔医疗机构定制，实现「患者拍照 → AI 自动识别牙位并标注 → 医生在线复核 → 生成检测报告」的完整流程。")

# ===== 一、系统概述 =====
doc.add_heading("一、系统概述", level=1)
body(doc, "系统由三部分组成，分别面向不同使用者：")

t = doc.add_table(rows=1, cols=4)
t.style = "Table Grid"
hdr = t.rows[0].cells
for i, h in enumerate(["端", "使用人", "形态", "核心功能"]):
    hdr[i].text = h
for cell in hdr:
    for run in cell.paragraphs[0].runs:
        run.font.bold = True

rows = [
    ("患者端", "患者", "微信小程序", "拍照检测、查看报告、历史记录、好物推荐"),
    ("医生端", "医生", "网页(Web)", "病例复核、修改诊断、定稿、驳回重拍"),
    ("管理端", "平台管理员", "网页(Web)", "诊所管理、医生账号、商品管理"),
]
for r in rows:
    cells = t.add_row().cells
    for i, v in enumerate(r):
        cells[i].text = v

# ===== 二、患者端功能 =====
doc.add_heading("二、患者端功能（微信小程序）", level=1)

doc.add_heading("2.1 手机号登录", level=2)
bullet(doc, "微信一键授权手机号，无需注册、无需填表")
bullet(doc, "手机号是唯一身份，自动关联所有历史记录")

doc.add_heading("2.2 拍照检测", level=2)
bullet(doc, "选择检测视角：咬合面 / 唇颊面")
bullet(doc, "填写牙位编号（如 16）")
bullet(doc, "调用手机摄像头拍照并上传")

doc.add_heading("2.3 查看报告", level=2)
bullet(doc, "AI 标注图（牙位画框 + 标签）")
bullet(doc, "检测结果明细（标签 + 置信度）")
bullet(doc, "检测状态（分析中 / 待审核 / 已定稿 / 已驳回）")

doc.add_heading("2.4 历史记录", level=2)
bullet(doc, "查看自己所有历史检测记录")
bullet(doc, "个人自测和去诊所检测的结果都能看到")

doc.add_heading("2.5 好物推荐", level=2)
bullet(doc, "展示检测设备、牙膏、牙刷等推荐商品")
bullet(doc, "一键复制淘口令跳转购买")

# ===== 三、医生端功能 =====
doc.add_heading("三、医生端功能（Web 后台）", level=1)

doc.add_heading("3.1 登录", level=2)
bullet(doc, "账号 + 密码登录")

doc.add_heading("3.2 病例列表", level=2)
bullet(doc, "按状态筛选：待审核 / 已定稿 / 已驳回 / 全部")
bullet(doc, "每个医生只能看到「自己名下」的病例")

doc.add_heading("3.3 病例详情", level=2)
bullet(doc, "AI 标注图（可点击放大）")
bullet(doc, "检测明细（每个标签 + 置信度百分比）")

doc.add_heading("3.4 诊断意见", level=2)
bullet(doc, "医生填写文字意见，可保存、可修改")

doc.add_heading("3.5 定稿 / 驳回重拍", level=2)
bullet(doc, "定稿：确认无误后发布最终报告")
bullet(doc, "驳回重拍：照片模糊、没拍全时，驳回让患者重新拍")

doc.add_heading("3.6 修改留痕", level=2)
bullet(doc, "医生每次修改都有记录，可追溯、可审计")

# ===== 四、管理端功能 =====
doc.add_heading("四、管理端功能（Web 后台）", level=1)
bullet(doc, "诊所管理：诊所入驻、开通、停用")
bullet(doc, "医生账号管理：创建医生账号、分配到诊所")
bullet(doc, "商品管理：好物推荐的上架、下架、编辑")

# ===== 五、AI 检测能力 =====
doc.add_heading("五、AI 检测能力", level=1)
bullet(doc, "咬合面检测（从牙齿上方拍）：识别 12 类牙位标签（A、B、C、D、E、1~7）")
bullet(doc, "唇颊面检测（从牙齿侧面拍）：识别 2 类标签（B、C）")
bullet(doc, "后续扩展：病灶分类（自动判断龋坏、牙周等问题）")

# ===== 六、完整业务流程 =====
doc.add_heading("六、完整业务流程", level=1)

doc.add_heading("6.1 患者自测", level=2)
body(doc, "患者打开小程序 → 授权手机号 → 选牙位拍照 → 上传 → AI 自动分析 → 查看报告 → 医生复核定稿 → 患者查看最终报告")

doc.add_heading("6.2 诊所代测", level=2)
body(doc, "诊所相机拍摄 → 收患者手机号备案 → 建病例 → AI 自动分析 → 医生复核 → 定稿；患者用同一手机号登录小程序即可看到该结果")

# ===== 七、数据与权限 =====
doc.add_heading("七、数据与权限", level=1)
bullet(doc, "多诊所隔离：每个诊所只能看到自己的数据")
bullet(doc, "医生只能处理「自己名下」的病例")
bullet(doc, "医生修改全程留痕，可追溯")

# ===== 八、想请医院/医生提建议的几点 =====
doc.add_heading("八、想请医院/医生提建议的几点", level=1)
numbered(doc, "「诊断意见」您更习惯哪种方式？A. 直接写文字；B. 逐颗牙点选 + 预置话术（如「16 龋坏，建议补牙」）")
numbered(doc, "AI 标注图这样标注，能否一眼看出是哪颗牙？标签方式要不要调整？")
numbered(doc, "检测结果里的「置信度百分比」对您有用吗？")
numbered(doc, "除了「定稿 / 驳回重拍」，还需要什么操作？（如加急、转诊、历史对比、报告打印等）")
numbered(doc, "最终报告给患者看，您最希望包含哪些内容？")
numbered(doc, "好物推荐模块，您希望推荐哪些类别的商品？")

doc.save(OUT)
print("已生成:", OUT)
