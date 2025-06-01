import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.font_manager as fm
import os

# 创建保存目录
os.makedirs("images", exist_ok=True)

# 设置中文字体支持
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial Unicode MS', 'SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 设置图形大小
fig, ax = plt.subplots(figsize=(14, 18))

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

# 定义各层的位置和大小
layer_height = 1.2
layer_width = 8
layer_margin = 0.5
layer_start_y = 16
layer_x = 3

# 绘制标题
ax.text(layer_x + layer_width/2, 17.5, "PowerAutomation 分层架构图", 
        fontsize=20, fontweight='bold', ha='center')

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
    
    # 绘制层名称
    ax.text(layer_x + 0.2, y - 0.3, layer["name"], 
            fontsize=14, fontweight='bold')
    
    # 绘制组件
    for j, component in enumerate(layer["components"]):
        ax.text(layer_x + 0.2, y - 0.6 - j * 0.3, component, 
                fontsize=12)

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
    
    # 绘制标签背景
    text_bg = patches.Rectangle((mid_x - 0.5, (start_y + end_y) / 2 - 0.15), 1, 0.3, 
                              facecolor=colors["background"], edgecolor=None)
    ax.add_patch(text_bg)
    
    # 绘制标签文本
    ax.text(mid_x, (start_y + end_y) / 2, label, 
            fontsize=10, ha='center', va='center')

# 添加横向功能分组 - 现有功能
feature_start_x = 0.5
feature_width = 3
feature_height = 4
feature_y = layer_start_y - 2 * (layer_height + layer_margin) - 0.5

# 现有功能
rect_existing = patches.Rectangle((feature_start_x, feature_y - feature_height), 
                                feature_width, feature_height, 
                                facecolor='none', edgecolor=colors["box_border"], linewidth=1.5)
ax.add_patch(rect_existing)
ax.text(feature_start_x + feature_width / 2, feature_y - 0.3, 
        "现有功能 (Existing Features)", 
        fontsize=14, fontweight='bold', ha='center')

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
    ax.text(feature_start_x + 0.2, feature_y - 0.6 - i * 0.3, 
            line, fontsize=10)

# 未来功能
future_start_x = layer_x + layer_width + 0.5
rect_future = patches.Rectangle((future_start_x, feature_y - feature_height), 
                              feature_width, feature_height, 
                              facecolor='none', edgecolor=colors["box_border"], linewidth=1.5)
ax.add_patch(rect_future)
ax.text(future_start_x + feature_width / 2, feature_y - 0.3, 
        "未来功能 (Upcoming Features)", 
        fontsize=14, fontweight='bold', ha='center')

upcoming_features = [
    "效率 (Efficiency):",
    "- 异步LLM引擎、工具结果缓存、高并发",
    "",
    "对话 (Conversation):",
    "- LLM对话模拟、多智能体RL训练",
    "",
    "工具池 (Tool Pool):",
    "- 与ACI.dev集成、WebUI工具构建",
    "",
    "性能 (Performance):",
    "- 过程奖励训练、新RL算法、极限长上下文",
    "",
    "兼容性 (Compatibility):",
    "- 更多模型支持、多平台测试、发布到pypi",
    "",
    "接口 (Interface):",
    "- 图形界面、提示优化、项目管理"
]

for i, line in enumerate(upcoming_features):
    ax.text(future_start_x + 0.2, feature_y - 0.6 - i * 0.25, 
            line, fontsize=10)

# 设置坐标轴
ax.set_xlim(0, 15)
ax.set_ylim(5, 18)
ax.axis('off')

# 保存图像
output_path = "images/powerautomation_layered_architecture_fixed.png"
plt.savefig(output_path, dpi=300, bbox_inches='tight')
plt.close()
print(f"架构图已保存到 {output_path}")
