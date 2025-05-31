import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from matplotlib.path import Path

# 设置中文字体支持
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

# 创建图形和坐标轴
fig, ax = plt.subplots(figsize=(12, 8))

# 定义模块颜色
colors = {
    'agent': '#4B89DC',  # 蓝色
    'mcp': '#8CC152',    # 绿色
    'tool': '#F6BB42',   # 黄色
    'external': '#E9573F'  # 红色
}

# 绘制主要模块框
def draw_box(x, y, width, height, label, color, alpha=0.8):
    rect = patches.Rectangle((x, y), width, height, linewidth=2, 
                            edgecolor=color, facecolor=color, alpha=alpha)
    ax.add_patch(rect)
    ax.text(x + width/2, y + height/2, label, ha='center', va='center', 
            fontsize=12, fontweight='bold')

# 绘制箭头
def draw_arrow(start, end, color='black', style='->', width=1.5):
    ax.annotate('', xy=end, xytext=start,
                arrowprops=dict(arrowstyle=style, color=color, lw=width))

# 绘制智能体模块
draw_box(1, 7, 3, 1, '智能体 (Agents)', colors['agent'])

# 绘制MCP核心组件
draw_box(1, 5, 3, 1, 'MCP核心组件', colors['mcp'])

# 绘制MCP增强组件
draw_box(1, 3, 3, 1, 'MCP增强组件', colors['mcp'], 0.6)

# 绘制外部工具适配器
draw_box(1, 1, 3, 1, '外部工具适配器', colors['external'])

# 绘制开发工具
draw_box(7, 5, 3, 1, '开发工具 (Dev Tools)', colors['tool'])

# 绘制连接线
draw_arrow((2.5, 7), (2.5, 6))  # 智能体 -> MCP核心
draw_arrow((2.5, 5), (2.5, 4))  # MCP核心 -> MCP增强
draw_arrow((2.5, 3), (2.5, 2))  # MCP增强 -> 外部适配器
draw_arrow((4, 5.5), (7, 5.5))  # MCP核心 -> 开发工具
draw_arrow((7, 5.5), (4, 5.5))  # 开发工具 -> MCP核心

# 添加MCP增强组件详情
components = [
    'Sequential Thinking适配器',
    'Playwright适配器',
    'WebAgentB增强适配器',
    '增强版MCP规划器',
    '增强版MCP头脑风暴器',
    '主动问题解决器'
]

# 在右侧添加组件列表
for i, comp in enumerate(components):
    y_pos = 3.5 - i * 0.3
    ax.text(5, y_pos, f'• {comp}', fontsize=10)
    if i == 0:
        draw_arrow((4, 3.5), (4.8, 3.5), style='-', width=1)

# 设置坐标轴
ax.set_xlim(0, 11)
ax.set_ylim(0, 9)
ax.axis('off')  # 隐藏坐标轴

# 添加标题
ax.set_title('PowerAutomation MCP模块关系图', fontsize=16, pad=20)

# 保存图像
plt.tight_layout()
plt.savefig('/home/ubuntu/powerautomation_integration/docs/module_relationship.png', dpi=300, bbox_inches='tight')
plt.close()

print("模块关系图已生成: /home/ubuntu/powerautomation_integration/docs/module_relationship.png")
