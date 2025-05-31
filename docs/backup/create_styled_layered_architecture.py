import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.font_manager as fm
import os
import numpy as np
from matplotlib import font_manager
from matplotlib.path import Path

# 检查可用字体
print("检查系统中可用的中文字体...")
chinese_fonts = []
for font in font_manager.fontManager.ttflist:
    if any(name in font.name.lower() for name in ['heiti', 'hei', 'simhei', 'noto sans cjk', 'source han sans', 'microsoft yahei']):
        chinese_fonts.append(font.name)
        print(f"找到中文字体: {font.name}")

# 创建保存目录
os.makedirs("images", exist_ok=True)

# 设置中文字体支持 - 优先使用系统中找到的中文字体
if chinese_fonts:
    plt.rcParams['font.sans-serif'] = chinese_fonts + ['DejaVu Sans', 'Arial Unicode MS']
else:
    plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans', 'Arial Unicode MS']
    
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.family'] = 'sans-serif'

# 设置图形大小
fig, ax = plt.subplots(figsize=(16, 18))

# 定义颜色 - 使用附件风格的配色
colors = {
    "background": "#FFFFFF",
    "title": "#333333",
    "layer_border": "#CCCCCC",
    "text": "#333333",
    "line": "#AAAAAA",
    "icon_bg": "#8BC34A",
    
    # 层级颜色 - 使用附件风格的蓝色渐变
    "agent_layer": "#E3F2FD",
    "mcp_core_layer": "#BBDEFB",
    "mcp_enhancer_layer": "#90CAF9",
    "adapter_layer": "#64B5F6",
    "dev_tools_layer": "#42A5F5",
    "rl_factory_layer": "#2196F3",
    "key_modules_layer": "#1E88E5",
    "base_repo_layer": "#1976D2",
    
    # 功能区块颜色
    "features_border": "#CCCCCC",
    "features_bg": "#FFFFFF"
}

# 设置背景色
ax.set_facecolor(colors["background"])

# 定义各层的位置和大小
layer_height = 1.2
layer_width = 10
layer_margin = 0.4
layer_start_y = 16
layer_x = 3

# 绘制标题
ax.text(layer_x + layer_width/2, 17.2, "PowerAutomation 分层架构图", 
        fontsize=22, fontweight='bold', ha='center', color=colors["title"])

# 定义圆角矩形函数
def rounded_rectangle(x, y, width, height, radius=0.3):
    """
    创建圆角矩形路径
    """
    # 定义圆角矩形的顶点和连接方式
    verts = [
        (x + radius, y),  # 左下角后的点
        (x + width - radius, y),  # 右下角前的点
        (x + width, y + radius),  # 右下角后的点
        (x + width, y + height - radius),  # 右上角前的点
        (x + width - radius, y + height),  # 右上角后的点
        (x + radius, y + height),  # 左上角前的点
        (x, y + height - radius),  # 左上角后的点
        (x, y + radius),  # 左下角前的点
        (x + radius, y),  # 回到起点
    ]
    
    codes = [
        Path.MOVETO,  # 移动到起点
        Path.LINETO,  # 画直线到右下角前的点
        Path.CURVE3,  # 二次贝塞尔曲线
        Path.LINETO,  # 画直线到右上角前的点
        Path.CURVE3,  # 二次贝塞尔曲线
        Path.LINETO,  # 画直线到左上角前的点
        Path.CURVE3,  # 二次贝塞尔曲线
        Path.CURVE3,  # 二次贝塞尔曲线
        Path.CLOSEPOLY,  # 闭合路径
    ]
    
    return Path(verts, codes)

# 绘制小图标函数
def draw_icon(x, y, size=0.3):
    """
    在指定位置绘制小图标
    """
    circle = plt.Circle((x, y), size, color=colors["icon_bg"], alpha=0.9)
    ax.add_patch(circle)

# 绘制各层
layers = [
    {"name": "智能体层 (Agents)", "color": colors["agent_layer"], "components": [
        "PPT智能体, 网页智能体, 代码智能体, 通用智能体"
    ]},
    {"name": "MCP核心组件层", "color": colors["mcp_core_layer"], "components": [
        "MCP中央协调器, MCP规划器, MCP头脑风暴器"
    ]},
    {"name": "MCP增强组件层", "color": colors["mcp_enhancer_layer"], "components": [
        "Sequential Thinking适配器, Playwright适配器, WebAgent增强适配器,",
        "增强版MCP规划器, 增强版MCP头脑风暴器, 主动问题解决器, RL增强器"
    ]},
    {"name": "外部工具适配器层", "color": colors["adapter_layer"], "components": [
        "无限上下文适配器, MCP.so适配器, GitHub Actions适配器, ACI.dev适配器, WebUI工具构建器"
    ]},
    {"name": "开发工具层 (Dev Tools)", "color": colors["dev_tools_layer"], "components": [
        "思考与操作记录器, Agent问题解决驱动器, Release Manager, GitHub Actions"
    ]},
    {"name": "RL-Factory层", "color": colors["rl_factory_layer"], "components": [
        "思考过程结构化, 混合学习架构, 多层次奖励机制, 能力迁移"
    ]},
    {"name": "关键模块层 (Key Modules)", "color": colors["key_modules_layer"], "components": [
        "工具使用 (Tool Use), RL训练 (RL-Training), Web界面 (WebUI)"
    ]},
    {"name": "基础仓库层 (Base Repository)", "color": colors["base_repo_layer"], "components": [
        "PeterGriffinJin/Search-R1, volcengine/veRL, QwenLM/Qwen-Agent"
    ]}
]

# 绘制层和组件
for i, layer in enumerate(layers):
    y = layer_start_y - i * (layer_height + layer_margin)
    
    # 绘制圆角矩形层背景
    path = rounded_rectangle(layer_x, y - layer_height, layer_width, layer_height)
    patch = patches.PathPatch(path, facecolor=layer["color"], edgecolor=colors["layer_border"], linewidth=1.0)
    ax.add_patch(patch)
    
    # 绘制层名称
    ax.text(layer_x + 0.4, y - 0.3, layer["name"], 
            fontsize=14, fontweight='bold', color=colors["text"])
    
    # 绘制图标
    draw_icon(layer_x + layer_width - 0.6, y - 0.3)
    
    # 绘制组件
    for j, component in enumerate(layer["components"]):
        ax.text(layer_x + 0.4, y - 0.6 - j * 0.25, component, 
                fontsize=11, color=colors["text"])

# 绘制连接线和标签
for i in range(len(layers) - 1):
    start_y = layer_start_y - i * (layer_height + layer_margin) - layer_height
    end_y = start_y - layer_margin
    
    # 绘制连接线
    mid_x = layer_x + layer_width / 2
    ax.plot([mid_x, mid_x], [start_y, end_y], color=colors["line"], linewidth=1.5, linestyle='--')
    
    # 添加连接标签
    if i == 0:
        label = "任务派发"
    elif i == 1:
        label = "能力调用"
    elif i == 2:
        label = "工具适配"
    elif i == 3:
        label = "开发支持"
    elif i == 4:
        label = "能力提升"
    elif i == 5:
        label = "功能支持"
    elif i == 6:
        label = "基础依赖"
    else:
        label = ""
    
    # 绘制标签文本
    ax.text(mid_x, (start_y + end_y) / 2, label, 
            fontsize=10, ha='center', va='center', color=colors["text"],
            bbox=dict(facecolor='white', alpha=0.7, edgecolor='none', boxstyle='round,pad=0.3'))

# 添加现有功能区块 - 放在分层架构正下方
feature_start_x = layer_x
feature_width = layer_width
feature_height = 4
feature_y = layer_start_y - len(layers) * (layer_height + layer_margin) - 0.8  # 放在最后一层下方

# 现有功能 - 使用圆角矩形
path = rounded_rectangle(feature_start_x, feature_y - feature_height, feature_width, feature_height)
patch = patches.PathPatch(path, facecolor=colors["features_bg"], edgecolor=colors["features_border"], linewidth=1.0)
ax.add_patch(patch)

ax.text(feature_start_x + feature_width / 2, feature_y - 0.4, 
        "现有功能 (Existing Features)", 
        fontsize=14, fontweight='bold', ha='center', color=colors["text"])

# 绘制图标
draw_icon(feature_start_x + feature_width - 0.6, feature_y - 0.4)

existing_features = [
    "多轮对话 (Multi-Turn):",
    "- 高效对话、掩码训练、异步工具使用",
    "",
    "更多工具 (More Tools):",
    "- MCP工具、自定义工具",
    "",
    "奖励机制 (Reward):",
    "- 规则奖励、模型评判、工具验证",
    "",
    "应用 (Application):",
    "- SOTA深度搜索、添加功能"
]

for i, line in enumerate(existing_features):
    ax.text(feature_start_x + 0.4, feature_y - 0.8 - i * 0.3,  # 增加行间距
            line, fontsize=11, color=colors["text"])

# 添加代码图标和箭头
# 左侧代码图标
code_icon_x = layer_x - 1.5
for i in range(3):
    y_pos = layer_start_y - i * 3 - 1
    ax.text(code_icon_x, y_pos, "</> ", fontsize=16, color="#64B5F6", fontweight='bold')
    # 箭头连接到相应层
    arrow_y = layer_start_y - i * 3 - 0.5
    ax.arrow(code_icon_x + 0.5, arrow_y, 0.8, 0, head_width=0.2, head_length=0.2, 
             fc='#BBDEFB', ec='#BBDEFB', linewidth=1.5)

# 右侧代码图标
code_icon_x = layer_x + layer_width + 1.5
for i in range(3):
    y_pos = layer_start_y - i * 3 - 1
    ax.text(code_icon_x, y_pos, " </>", fontsize=16, color="#64B5F6", fontweight='bold')
    # 箭头连接到相应层
    arrow_y = layer_start_y - i * 3 - 0.5
    ax.arrow(code_icon_x - 0.5, arrow_y, -0.8, 0, head_width=0.2, head_length=0.2, 
             fc='#BBDEFB', ec='#BBDEFB', linewidth=1.5)

# 设置坐标轴
ax.set_xlim(0, 16)
ax.set_ylim(0, 18)
ax.axis('off')

# 保存图像
output_path = "images/powerautomation_layered_architecture_styled.png"
plt.savefig(output_path, dpi=300, bbox_inches='tight')
plt.close()
print(f"风格化架构图已保存到 {output_path}")
