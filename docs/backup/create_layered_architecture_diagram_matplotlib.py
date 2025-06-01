import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.patheffects as path_effects
import numpy as np
import os

# 创建保存目录
os.makedirs('/home/ubuntu/powerautomation_integration/docs/images', exist_ok=True)

# 设置中文字体支持
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans', 'Arial Unicode MS', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

# 设置图像尺寸
fig, ax = plt.subplots(figsize=(16, 18))
ax.set_xlim(0, 16)
ax.set_ylim(0, 18)

# 隐藏坐标轴
ax.axis('off')

# 定义颜色
colors = {
    'agent_blue': '#4682B4',
    'core_green': '#64A064',
    'enhancer_green': '#78C878',
    'tool_adapter_orange': '#F08050',
    'dev_tools_yellow': '#F0C850',
    'rl_factory_blue': '#3C78BE',
    'key_module_gray': '#C8C8C8',
    'github_purple': '#B478F0',
    'feature_box_light': '#F0F0F0',
    'arrow': '#505050',
    'text': '#000000',
    'highlight': '#FF6464'
}

# 绘制标题
ax.text(8, 17.5, "PowerAutomation 分层架构图", fontsize=24, ha='center', weight='bold')

# 定义层级和位置
layers = [
    {"name": "智能体层 (Agents)", "y": 16, "color": colors['agent_blue'], "height": 1.5},
    {"name": "MCP核心组件层", "y": 14, "color": colors['core_green'], "height": 1.5},
    {"name": "MCP增强组件层", "y": 12, "color": colors['enhancer_green'], "height": 1.5},
    {"name": "外部工具适配器层", "y": 10, "color": colors['tool_adapter_orange'], "height": 1.5},
    {"name": "开发工具层 (Dev Tools)", "y": 8, "color": colors['dev_tools_yellow'], "height": 1.5},
    {"name": "RL-Factory层", "y": 6, "color": colors['rl_factory_blue'], "height": 1.5},
    {"name": "关键模块层 (Key Modules)", "y": 4, "color": colors['key_module_gray'], "height": 1.5},
    {"name": "基础仓库层 (Base Repository)", "y": 2, "color": colors['github_purple'], "height": 1.5}
]

# 绘制层级框和标题
for layer in layers:
    # 绘制层级框
    rect = patches.Rectangle((2, layer["y"]), 12, layer["height"], 
                           facecolor=layer["color"], edgecolor='black', linewidth=1)
    ax.add_patch(rect)
    
    # 绘制层级名称
    text = ax.text(2.2, layer["y"] + layer["height"]/2, layer["name"], 
                 fontsize=16, va='center', weight='bold')
    text.set_path_effects([path_effects.withStroke(linewidth=3, foreground='white')])

# 绘制智能体层的组件
agents = [
    {"name": "PPT智能体", "x": 5, "width": 1.8},
    {"name": "网页智能体", "x": 7, "width": 1.8},
    {"name": "代码智能体", "x": 9, "width": 1.8},
    {"name": "通用智能体", "x": 11, "width": 1.8}
]

for agent in agents:
    y = layers[0]["y"] + 0.3
    rect = patches.Rectangle((agent["x"], y), agent["width"], 0.9, 
                           facecolor=colors['feature_box_light'], edgecolor='black', linewidth=1)
    ax.add_patch(rect)
    ax.text(agent["x"] + agent["width"]/2, y + 0.45, agent["name"], 
          fontsize=12, ha='center', va='center')

# 绘制MCP核心组件层的组件
core_components = [
    {"name": "MCP中央协调器", "x": 5, "width": 2},
    {"name": "MCP规划器", "x": 7.2, "width": 1.8},
    {"name": "MCP头脑风暴器", "x": 9.2, "width": 1.8},
    {"name": "mcp.so", "x": 11.2, "width": 1.2}
]

for comp in core_components:
    y = layers[1]["y"] + 0.3
    rect = patches.Rectangle((comp["x"], y), comp["width"], 0.9, 
                           facecolor=colors['feature_box_light'], edgecolor='black', linewidth=1)
    ax.add_patch(rect)
    ax.text(comp["x"] + comp["width"]/2, y + 0.45, comp["name"], 
          fontsize=12, ha='center', va='center')

# 绘制MCP增强组件层的组件
enhancers = [
    {"name": "Sequential Thinking适配器", "x": 4, "width": 2.4, "y_offset": 0},
    {"name": "Playwright适配器", "x": 6.6, "width": 1.8, "y_offset": 0},
    {"name": "WebAgentB增强适配器", "x": 8.6, "width": 2, "y_offset": 0},
    {"name": "增强版MCP规划器", "x": 4, "width": 2.4, "y_offset": 0.7},
    {"name": "增强版MCP头脑风暴器", "x": 6.6, "width": 2.4, "y_offset": 0.7},
    {"name": "Agent问题解决驱动器", "x": 9.2, "width": 2.2, "y_offset": 0.7},
    {"name": "RL增强器", "x": 11.6, "width": 1.4, "y_offset": 0.7}
]

for enhancer in enhancers:
    y_offset = enhancer.get("y_offset", 0)
    y = layers[2]["y"] + 0.3 + y_offset
    rect = patches.Rectangle((enhancer["x"], y), enhancer["width"], 0.6, 
                           facecolor=colors['feature_box_light'], edgecolor='black', linewidth=1)
    ax.add_patch(rect)
    ax.text(enhancer["x"] + enhancer["width"]/2, y + 0.3, enhancer["name"], 
          fontsize=10, ha='center', va='center')

# 绘制外部工具适配器层的组件
adapters = [
    {"name": "无限上下文适配器", "x": 5, "width": 2},
    {"name": "MCP.so适配器", "x": 7.2, "width": 1.8},
    {"name": "GitHub Actions适配器", "x": 9.2, "width": 2},
    {"name": "浏览器自动化适配器", "x": 11.4, "width": 2}
]

for adapter in adapters:
    y = layers[3]["y"] + 0.3
    rect = patches.Rectangle((adapter["x"], y), adapter["width"], 0.9, 
                           facecolor=colors['feature_box_light'], edgecolor='black', linewidth=1)
    ax.add_patch(rect)
    ax.text(adapter["x"] + adapter["width"]/2, y + 0.45, adapter["name"], 
          fontsize=12, ha='center', va='center')

# 绘制开发工具层的组件
dev_tools = [
    {"name": "思考与操作记录器", "x": 5, "width": 2},
    {"name": "Agent问题解决驱动器", "x": 7.2, "width": 2.2},
    {"name": "Release管理器", "x": 9.6, "width": 1.8},
    {"name": "测试与问题收集器", "x": 11.6, "width": 2}
]

for tool in dev_tools:
    y = layers[4]["y"] + 0.3
    rect = patches.Rectangle((tool["x"], y), tool["width"], 0.9, 
                           facecolor=colors['feature_box_light'], edgecolor='black', linewidth=1)
    ax.add_patch(rect)
    ax.text(tool["x"] + tool["width"]/2, y + 0.45, tool["name"], 
          fontsize=12, ha='center', va='center')

# 绘制RL-Factory层的组件
rl_factory_components = [
    {"name": "思考过程结构化", "x": 5, "width": 1.8},
    {"name": "混合学习架构", "x": 7, "width": 1.8},
    {"name": "多层次奖励机制", "x": 9, "width": 1.8},
    {"name": "能力迁移模块", "x": 11, "width": 1.8}
]

for comp in rl_factory_components:
    y = layers[5]["y"] + 0.3
    rect = patches.Rectangle((comp["x"], y), comp["width"], 0.9, 
                           facecolor=colors['feature_box_light'], edgecolor='black', linewidth=1)
    ax.add_patch(rect)
    ax.text(comp["x"] + comp["width"]/2, y + 0.45, comp["name"], 
          fontsize=12, ha='center', va='center')

# 绘制关键模块层的组件
key_modules = [
    {"name": "工具使用 (Tool Use)", "x": 5, "width": 2},
    {"name": "RL训练 (RL-Training)", "x": 7.5, "width": 2},
    {"name": "Web界面 (WebUI)", "x": 10, "width": 2}
]

for module in key_modules:
    y = layers[6]["y"] + 0.3
    rect = patches.Rectangle((module["x"], y), module["width"], 0.9, 
                           facecolor=colors['feature_box_light'], edgecolor='black', linewidth=1)
    ax.add_patch(rect)
    ax.text(module["x"] + module["width"]/2, y + 0.45, module["name"], 
          fontsize=12, ha='center', va='center')

# 绘制基础仓库层的组件
base_repos = [
    {"name": "PeterGriffinJn/Search-R1", "x": 4.5, "width": 2.5},
    {"name": "volcengine/veRL", "x": 7.5, "width": 2},
    {"name": "QwenLM/Qwen-Agent", "x": 10, "width": 2}
]

for repo in base_repos:
    y = layers[7]["y"] + 0.3
    rect = patches.Rectangle((repo["x"], y), repo["width"], 0.9, 
                           facecolor=colors['feature_box_light'], edgecolor='black', linewidth=1)
    ax.add_patch(rect)
    ax.text(repo["x"] + repo["width"]/2, y + 0.45, repo["name"], 
          fontsize=10, ha='center', va='center')

# 绘制功能分组
feature_groups = [
    {"name": "效率 (Efficiency)", "x": 13.5, "y": 16, "items": ["Async LLMEngine", "工具结果缓存", "高并发支持"]},
    {"name": "对话 (Conversation)", "x": 13.5, "y": 14.5, "items": ["LLM对话模拟", "多智能体RL训练", "上下文管理"]},
    {"name": "工具池 (Tool Pool)", "x": 13.5, "y": 13, "items": ["与ACI.dev集成", "WebUI工具构建", "工具版本管理"]},
    {"name": "性能 (Performance)", "x": 13.5, "y": 11.5, "items": ["过程奖励训练", "新RL算法", "极限长上下文"]},
    {"name": "兼容性 (Compatibility)", "x": 13.5, "y": 10, "items": ["更多模型支持", "多平台测试", "发布到PyPI"]},
    {"name": "接口 (Interface)", "x": 13.5, "y": 8.5, "items": ["图形界面", "提示优化", "项目管理"]}
]

for group in feature_groups:
    # 绘制分组框
    rect = patches.Rectangle((group["x"], group["y"]), 2.2, 1.2, 
                           facecolor=colors['feature_box_light'], edgecolor='black', linewidth=1)
    ax.add_patch(rect)
    
    # 绘制分组标题
    ax.text(group["x"] + 1.1, group["y"] + 1, group["name"], 
          fontsize=12, ha='center', va='center', weight='bold')
    
    # 绘制分组项目
    for i, item in enumerate(group["items"]):
        ax.text(group["x"] + 0.2, group["y"] + 0.8 - i*0.25, f"• {item}", 
              fontsize=8)

# 绘制"未来功能"标题
ax.text(13.5, 17, "未来功能 (Upcoming Features)", fontsize=12, weight='bold')

# 绘制"现有功能"标题
ax.text(4, layers[6]["y"] + 1.7, "现有功能 (Existing Features)", fontsize=12, weight='bold')

# 绘制连接线
# 智能体层 -> MCP核心组件层
arrow = patches.FancyArrowPatch((8, layers[0]["y"]), (8, layers[1]["y"] + layers[1]["height"]),
                              arrowstyle='->', color=colors['arrow'], linewidth=2,
                              connectionstyle="arc3,rad=0")
ax.add_patch(arrow)

# MCP核心组件层 -> MCP增强组件层
arrow = patches.FancyArrowPatch((8, layers[1]["y"]), (8, layers[2]["y"] + layers[2]["height"]),
                              arrowstyle='->', color=colors['arrow'], linewidth=2,
                              connectionstyle="arc3,rad=0")
ax.add_patch(arrow)

# MCP增强组件层 -> 外部工具适配器层
arrow = patches.FancyArrowPatch((8, layers[2]["y"]), (8, layers[3]["y"] + layers[3]["height"]),
                              arrowstyle='->', color=colors['arrow'], linewidth=2,
                              connectionstyle="arc3,rad=0")
ax.add_patch(arrow)

# MCP核心组件层 <-> 开发工具层
arrow = patches.FancyArrowPatch((14, layers[1]["y"] + layers[1]["height"]/2), 
                              (14, layers[4]["y"] + layers[4]["height"]/2),
                              arrowstyle='<->', color=colors['arrow'], linewidth=2,
                              connectionstyle="arc3,rad=0")
ax.add_patch(arrow)

# RL-Factory层 -> 关键模块层
for x in [6, 8, 10]:
    arrow = patches.FancyArrowPatch((x, layers[5]["y"]), (x, layers[6]["y"] + layers[6]["height"]),
                                  arrowstyle='->', color=colors['arrow'], linewidth=1.5,
                                  connectionstyle="arc3,rad=0")
    ax.add_patch(arrow)

# 基础仓库层 -> RL-Factory层
for x in [5.5, 7.5, 10]:
    arrow = patches.FancyArrowPatch((x, layers[7]["y"] + layers[7]["height"]), (x, layers[5]["y"]),
                                  arrowstyle='->', color=colors['arrow'], linewidth=1.5,
                                  connectionstyle="arc3,rad=0")
    ax.add_patch(arrow)

# 添加RL增强器与MCP增强组件的关系说明
arrow = patches.FancyArrowPatch((12.3, layers[2]["y"] + 1), (12.3, layers[5]["y"] + layers[5]["height"]),
                              arrowstyle='->', color=colors['highlight'], linewidth=2,
                              connectionstyle="arc3,rad=0")
ax.add_patch(arrow)
ax.text(12.3, layers[2]["y"] + 1.2, "RL增强器集成", fontsize=10, ha='center', color=colors['highlight'], weight='bold')

# 添加GitHub Actions与Release Manager的关系说明
arrow = patches.FancyArrowPatch((10.2, layers[3]["y"] + 0.3), (10.2, layers[4]["y"] + 1.2),
                              arrowstyle='<->', color=colors['highlight'], linewidth=2,
                              connectionstyle="arc3,rad=0")
ax.add_patch(arrow)
ax.text(10.2, (layers[3]["y"] + 0.3 + layers[4]["y"] + 1.2)/2, "CI/CD集成", 
      fontsize=10, ha='center', color=colors['highlight'], weight='bold')

# 保存图像
plt.tight_layout()
plt.savefig('/home/ubuntu/powerautomation_integration/docs/images/powerautomation_layered_architecture.png', dpi=300, bbox_inches='tight')
print("分层架构图已保存到 /home/ubuntu/powerautomation_integration/docs/images/powerautomation_layered_architecture.png")
