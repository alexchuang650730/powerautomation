import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from matplotlib.path import Path

# 设置中文字体支持
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

# 创建图形和坐标轴
fig, ax = plt.subplots(figsize=(12, 8))

# 定义层级和颜色
layers = [
    {"name": "智能体层 (Agents)", "color": "#4287f5", "y": 7},
    {"name": "MCP核心组件层", "color": "#42c5f5", "y": 6},
    {"name": "MCP增强组件层", "color": "#42f5a7", "y": 5},
    {"name": "外部工具适配器层", "color": "#f5a742", "y": 4},
    {"name": "开发工具层 (Dev Tools)", "color": "#f542a7", "y": 3},
    {"name": "RL-Factory层", "color": "#a742f5", "y": 2},
    {"name": "关键模块层 (Key Modules)", "color": "#42f5f5", "y": 1},
    {"name": "基础仓库层 (Base Repository)", "color": "#c5c5c5", "y": 0}
]

# 定义每层的内容
layer_contents = {
    "智能体层 (Agents)": [
        "PPT智能体\n(PPTAgent)",
        "网页智能体\n(WebAgent)",
        "代码智能体\n(CodeAgent)",
        "通用智能体\n(GeneralAgent)"
    ],
    "MCP核心组件层": [
        "MCP中央协调器\n(MCPCentralCoordinator)",
        "MCP规划器\n(MCPPlanner)",
        "MCP头脑风暴器\n(MCPBrainstorm)"
    ],
    "MCP增强组件层": [
        "思考与操作记录器\n(ThoughtActionRecorder)",
        "Release管理器\n(ReleaseManager)",
        "测试与问题收集器\n(TestAndIssueCollector)",
        "Agent问题解决驱动器\n(AgentProblemSolver)"
    ],
    "外部工具适配器层": [
        "无限上下文适配器, MCP.so适配器, GitHub Actions适配器, ACI.dev适配器, WebUI工具构建器"
    ],
    "开发工具层 (Dev Tools)": [
        "VisualTester",
        "InfiniteContextAdapter",
        "ThoughtRecorder",
        "ReleaseRuleChecker",
        "TestNameUpdater",
        "SessionSavePointManager",
        "RollbackLocator"
    ],
    "RL-Factory层": [
        "Sequential Thinking适配器",
        "Playwright适配器",
        "WebAgentB增强适配器",
        "增强版MCP规划器",
        "增强版MCP头脑风暴器",
        "主动问题解决器"
    ],
    "关键模块层 (Key Modules)": [
        "监督学习\n(Supervised Learning)",
        "强化学习\n(Reinforcement Learning)",
        "对比学习\n(Contrastive Learning)",
        "混合学习\n(Hybrid Learning)"
    ],
    "基础仓库层 (Base Repository)": [
        "PowerAutomation 基础仓库"
    ]
}

# 定义层级之间的连接标签
connections = [
    {"from": "智能体层 (Agents)", "to": "MCP核心组件层", "label": "任务派发"},
    {"from": "MCP核心组件层", "to": "MCP增强组件层", "label": "协调"},
    {"from": "MCP增强组件层", "to": "外部工具适配器层", "label": "调用"},
    {"from": "外部工具适配器层", "to": "开发工具层 (Dev Tools)", "label": "集成"},
    {"from": "开发工具层 (Dev Tools)", "to": "RL-Factory层", "label": "能力提升"},
    {"from": "RL-Factory层", "to": "关键模块层 (Key Modules)", "label": "学习"},
    {"from": "关键模块层 (Key Modules)", "to": "基础仓库层 (Base Repository)", "label": "依赖"}
]

# 绘制层级
for layer in layers:
    rect = patches.Rectangle((0.1, layer["y"] - 0.4), 0.8, 0.8, 
                            linewidth=1, edgecolor='black', 
                            facecolor=layer["color"], alpha=0.7)
    ax.add_patch(rect)
    ax.text(0.5, layer["y"], layer["name"], ha='center', va='center', 
            fontsize=12, fontweight='bold')

    # 绘制每层的内容
    contents = layer_contents[layer["name"]]
    n_contents = len(contents)
    
    for i, content in enumerate(contents):
        x_pos = 0.1 + (i + 0.5) * 0.8 / max(n_contents, 1)
        y_pos = layer["y"] - 0.25
        ax.text(x_pos, y_pos, content, ha='center', va='center', 
                fontsize=9, wrap=True)

# 绘制连接
for connection in connections:
    from_layer = next(layer for layer in layers if layer["name"] == connection["from"])
    to_layer = next(layer for layer in layers if layer["name"] == connection["to"])
    
    # 绘制箭头
    ax.annotate("", 
                xy=(0.5, to_layer["y"] + 0.4), 
                xytext=(0.5, from_layer["y"] - 0.4),
                arrowprops=dict(arrowstyle="->", lw=1.5, color="green"))
    
    # 添加连接标签
    mid_y = (from_layer["y"] - 0.4 + to_layer["y"] + 0.4) / 2
    ax.text(0.55, mid_y, connection["label"], ha='left', va='center', 
            fontsize=9, color='blue')

# 设置坐标轴
ax.set_xlim(0, 1)
ax.set_ylim(-0.5, 8)
ax.axis('off')

# 添加标题
ax.set_title('PowerAutomation 分层架构图', fontsize=16, pad=20)

# 保存图像
plt.tight_layout()
plt.savefig('/home/ubuntu/powerautomation_integration/docs/images/powerautomation_refactored_architecture.png', dpi=300, bbox_inches='tight')
plt.close()

print("重构后的PowerAutomation分层架构图已生成")
