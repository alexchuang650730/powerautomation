import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.font_manager as fm
import os
import numpy as np
from matplotlib import font_manager

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

# 设置图形大小 - 减小高度使整体更紧凑
fig, ax = plt.subplots(figsize=(14, 14))

# 定义颜色
colors = {
    "agent_blue": "#4169E1",      # 深蓝色
    "mcp_core_blue": "#6495ED",   # 浅蓝色
    "mcp_enhancer_green": "#90EE90",  # 浅绿色
    "external_adapter_coral": "#FF7F50",  # 珊瑚色
    "dev_tools_gold": "#FFD700",   # 金色
    "rl_factory_teal": "#008080",  # 蓝绿色
    "key_modules_purple": "#9370DB",  # 紫色
    "base_repo_gray": "#A9A9A9",  # 灰色
    "text_black": "#000000",      # 黑色
    "line_gray": "#808080",       # 灰色
    "box_border": "#646464",      # 深灰色
    "background": "#FFFFFF"       # 白色
}

# 设置背景色
ax.set_facecolor(colors["background"])

# 定义各层的位置和大小 - 减小高度和间距使整体更紧凑
layer_height = 0.9  # 减小高度
layer_width = 8  # 保持宽度
layer_margin = 0.3  # 减小间距
layer_start_y = 14  # 调整起始位置
layer_x = 3

# 绘制标题
ax.text(layer_x + layer_width/2, 15.2, "PowerAutomation 分层架构图", 
        fontsize=18, fontweight='bold', ha='center')

# 绘制各层
layers = [
    {"name": "智能体层 (Agents)", "color": colors["agent_blue"], "components": [
        "PPT智能体, 网页智能体, 代码智能体, 通用智能体"
    ]},
    {"name": "MCP核心组件层", "color": colors["mcp_core_blue"], "components": [
        "MCP中央协调器, MCP规划器, MCP头脑风暴器"
    ]},
    {"name": "MCP增强组件层", "color": colors["mcp_enhancer_green"], "components": [
        "Sequential Thinking适配器, Playwright适配器, WebAgent增强适配器,",
        "增强版MCP规划器, 增强版MCP头脑风暴器, 主动问题解决器, RL增强器"
    ]},
    {"name": "外部工具适配器层", "color": colors["external_adapter_coral"], "components": [
        "无限上下文适配器, MCP.so适配器, GitHub Actions适配器, ACI.dev适配器, WebUI工具构建器"
    ]},
    {"name": "开发工具层 (Dev Tools)", "color": colors["dev_tools_gold"], "components": [
        "思考与操作记录器, Agent问题解决驱动器, Release Manager, GitHub Actions"
    ]},
    {"name": "RL-Factory层", "color": colors["rl_factory_teal"], "components": [
        "思考过程结构化, 混合学习架构, 多层次奖励机制, 能力迁移"
    ]},
    {"name": "关键模块层 (Key Modules)", "color": colors["key_modules_purple"], "components": [
        "工具使用 (Tool Use), RL训练 (RL-Training), Web界面 (WebUI)"
    ]},
    {"name": "基础仓库层 (Base Repository)", "color": colors["base_repo_gray"], "components": [
        "PeterGriffinJin/Search-R1, volcengine/veRL, QwenLM/Qwen-Agent"
    ]}
]

# 绘制层和组件
for i, layer in enumerate(layers):
    y = layer_start_y - i * (layer_height + layer_margin)
    
    # 绘制层背景
    rect = patches.Rectangle((layer_x, y - layer_height), layer_width, layer_height, 
                           facecolor=layer["color"], edgecolor=colors["box_border"], linewidth=1.5)
    ax.add_patch(rect)
    
    # 绘制层名称 - 不添加白色背景
    ax.text(layer_x + 0.2, y - 0.3, layer["name"], 
            fontsize=12, fontweight='bold', color='black')
    
    # 绘制组件 - 不添加白色背景
    for j, component in enumerate(layer["components"]):
        ax.text(layer_x + 0.2, y - 0.6 - j * 0.25, component, 
                fontsize=10, color='black')

# 绘制连接线和标签
for i in range(len(layers) - 1):
    start_y = layer_start_y - i * (layer_height + layer_margin) - layer_height
    end_y = start_y - layer_margin
    
    # 绘制连接线
    mid_x = layer_x + layer_width / 2
    ax.plot([mid_x, mid_x], [start_y, end_y], color=colors["line_gray"], linewidth=2)
    
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
    
    # 绘制标签文本 - 不添加白色背景
    ax.text(mid_x, (start_y + end_y) / 2, label, 
            fontsize=9, ha='center', va='center', color='black')

# 添加现有功能区块 - 放在分层架构正下方
feature_start_x = layer_x
feature_width = layer_width
feature_height = 4
feature_y = layer_start_y - len(layers) * (layer_height + layer_margin) - 0.5  # 放在最后一层下方

# 现有功能
rect_existing = patches.Rectangle((feature_start_x, feature_y - feature_height), 
                                feature_width, feature_height, 
                                facecolor='none', edgecolor=colors["box_border"], linewidth=1.5)
ax.add_patch(rect_existing)

ax.text(feature_start_x + feature_width / 2, feature_y - 0.3, 
        "现有功能 (Existing Features)", 
        fontsize=12, fontweight='bold', ha='center')

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
    ax.text(feature_start_x + 0.2, feature_y - 0.6 - i * 0.3,  # 增加行间距
            line, fontsize=9)

# 设置坐标轴
ax.set_xlim(0, 15)
ax.set_ylim(0, 16)
ax.axis('off')

# 保存图像
output_path = "images/powerautomation_layered_architecture_simplified.png"
plt.savefig(output_path, dpi=300, bbox_inches='tight')
plt.close()
print(f"架构图已保存到 {output_path}")
