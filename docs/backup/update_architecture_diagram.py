import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# 设置中文字体支持
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

# 创建图形和坐标轴
fig, ax = plt.subplots(figsize=(12, 10))

# 定义颜色
colors = {
    'central': '#5DADE2',  # 中央协调器 - 蓝色
    'planner': '#5499C7',  # 规划器 - 深蓝色
    'brainstorm': '#48C9B0',  # 头脑风暴器 - 绿色
    'recorder': '#EC7063',  # 记录器 - 红色
    'release': '#F5B041',  # Release管理器 - 橙色
    'test': '#E67E22',  # 测试收集器 - 深橙色
    'solver': '#AF7AC5',  # 问题解决器 - 紫色
    'external': '#BDC3C7',  # 外部系统 - 灰色
    'submodule': '#BDC3C7',  # 子模块 - 灰色
}

# 绘制中央协调器
central = patches.Rectangle((4, 7), 4, 2, linewidth=1, edgecolor='black', facecolor=colors['central'])
ax.add_patch(central)
ax.text(6, 8, 'MCP中央协调器\n(MCPCentralCoordinator)', ha='center', va='center', fontsize=12, color='white')

# 绘制规划器
planner = patches.Rectangle((2, 4), 4, 2, linewidth=1, edgecolor='black', facecolor=colors['planner'])
ax.add_patch(planner)
ax.text(4, 5, 'MCP规划器\n(MCPPlanner)', ha='center', va='center', fontsize=12, color='white')

# 绘制头脑风暴器
brainstorm = patches.Rectangle((8, 4), 4, 2, linewidth=1, edgecolor='black', facecolor=colors['brainstorm'])
ax.add_patch(brainstorm)
ax.text(10, 5, 'MCP头脑风暴器\n(MCPBrainstorm)', ha='center', va='center', fontsize=12, color='white')

# 绘制思考与操作记录器
recorder = patches.Rectangle((1, 1), 3, 2, linewidth=1, edgecolor='black', facecolor=colors['recorder'])
ax.add_patch(recorder)
ax.text(2.5, 2, '思考与操作记录器\n(ThoughtActionRecorder)', ha='center', va='center', fontsize=10, color='white')

# 绘制Release管理器
release = patches.Rectangle((5, 1), 3, 2, linewidth=1, edgecolor='black', facecolor=colors['release'])
ax.add_patch(release)
ax.text(6.5, 2, 'Release管理器\n(ReleaseManager)', ha='center', va='center', fontsize=10, color='white')

# 绘制测试与问题收集器
test = patches.Rectangle((9, 1), 3, 2, linewidth=1, edgecolor='black', facecolor=colors['test'])
ax.add_patch(test)
ax.text(10.5, 2, '测试与问题收集器\n(TestAndIssueCollector)', ha='center', va='center', fontsize=10, color='white')

# 绘制Manus问题解决驱动器
solver = patches.Rectangle((13, 1), 3, 2, linewidth=1, edgecolor='black', facecolor=colors['solver'])
ax.add_patch(solver)
ax.text(14.5, 2, 'Manus问题解决驱动器\n(ManusProblemSolver)', ha='center', va='center', fontsize=10, color='white')

# 绘制外部系统 - mcp.so
mcp_so = patches.Rectangle((1, 8), 2, 1.5, linewidth=1, edgecolor='black', facecolor=colors['external'])
ax.add_patch(mcp_so)
ax.text(2, 8.75, 'mcp.so', ha='center', va='center', fontsize=10, color='white')

# 绘制外部系统 - GitHub
github = patches.Rectangle((9, 8), 2, 1.5, linewidth=1, edgecolor='black', facecolor=colors['external'])
ax.add_patch(github)
ax.text(10, 8.75, 'GitHub', ha='center', va='center', fontsize=10, color='white')

# 绘制子模块
submodules = [
    # 规划器子模块
    {'name': 'MCPMatcher', 'x': 1.5, 'y': 3.2},
    {'name': 'MCPExecutor', 'x': 2.5, 'y': 3.2},
    {'name': 'MCPCacheManager', 'x': 1.5, 'y': 2.7},
    {'name': 'CurrencyController', 'x': 2.5, 'y': 2.7},
    
    # 头脑风暴器子模块
    {'name': 'CapabilityAnalyzer', 'x': 8.5, 'y': 3.2},
    {'name': 'MCPConverter', 'x': 9.5, 'y': 3.2},
    {'name': 'SearchEnhancer', 'x': 9, 'y': 2.7},
    
    # 记录器子模块
    {'name': 'VisualThoughtRecorder', 'x': 1, 'y': 0.3},
    {'name': 'EnhancedThoughtRecorder', 'x': 2.5, 'y': 0.3},
    
    # Release管理器子模块
    {'name': 'ReleaseRulesChecker', 'x': 6.5, 'y': 0.3},
    
    # 测试收集器子模块
    {'name': 'TestReadmeUpdater', 'x': 10.5, 'y': 0.3},
    
    # 问题解决器子模块
    {'name': 'SessionSavePointManager', 'x': 13.5, 'y': 0.3},
    {'name': 'RollbackExecutor', 'x': 15, 'y': 0.3},
]

# 添加子模块
for module in submodules:
    rect = patches.Rectangle((module['x']-0.5, module['y']-0.3), 1, 0.6, 
                            linewidth=1, edgecolor='black', facecolor=colors['submodule'])
    ax.add_patch(rect)
    ax.text(module['x'], module['y'], module['name'], ha='center', va='center', fontsize=8, color='black')

# 绘制连接线
# 中央协调器到规划器
ax.plot([4, 4], [7, 6], 'b-', linewidth=2)
ax.text(3.7, 6.5, '协调', fontsize=8)

# 中央协调器到头脑风暴器
ax.plot([8, 8], [7, 6], 'b-', linewidth=2)
ax.text(8.3, 6.5, '协调', fontsize=8)

# 规划器到头脑风暴器
ax.plot([6, 8], [5, 5], 'purple', linewidth=2)
ax.text(7, 5.2, '能力提升', fontsize=8)

# mcp.so到中央协调器
ax.plot([3, 4], [8.75, 8], 'gray', linewidth=1)
ax.text(3.3, 8.5, '集成', fontsize=8)

# 中央协调器到GitHub
ax.plot([8, 9], [8, 8.75], 'gray', linewidth=1)
ax.text(8.5, 8.5, '同步', fontsize=8)

# 规划器到子模块的连接
ax.plot([2, 2], [4, 3.5], 'g-', linewidth=1)
ax.text(1.8, 3.7, '调用', fontsize=8)

ax.plot([3, 3], [4, 3.5], 'g-', linewidth=1)
ax.text(3.2, 3.7, '调用', fontsize=8)

# 规划器到记录器
ax.plot([2, 2.5], [4, 3], 'g-', linewidth=1)

# 规划器到Release管理器
ax.plot([4, 6.5], [4, 3], 'g-', linewidth=1)

# 规划器到测试收集器
ax.plot([6, 10.5], [4, 3], 'g-', linewidth=1)
ax.text(8, 3.7, '调用', fontsize=8)

# 头脑风暴器到子模块的连接
ax.plot([9, 9], [4, 3.5], 'g-', linewidth=1)
ax.text(8.8, 3.7, '调用', fontsize=8)

# 头脑风暴器到测试收集器
ax.plot([10, 10.5], [4, 3], 'g-', linewidth=1)

# 记录器到子模块
ax.plot([1.5, 1], [1, 0.6], 'blue', linewidth=1)
ax.text(1.2, 0.8, '记录', fontsize=8)

ax.plot([2.5, 2.5], [1, 0.6], 'blue', linewidth=1)

# Release管理器到子模块
ax.plot([6.5, 6.5], [1, 0.6], 'blue', linewidth=1)
ax.text(6.7, 0.8, '检查', fontsize=8)

# 测试收集器到子模块
ax.plot([10.5, 10.5], [1, 0.6], 'blue', linewidth=1)
ax.text(10.7, 0.8, '收集', fontsize=8)

# 测试收集器到问题解决器
ax.plot([12, 13], [1.5, 1.5], 'orange', linewidth=1)
ax.text(12.5, 1.7, '问题', fontsize=8)

# 问题解决器到子模块
ax.plot([14, 13.5], [1, 0.6], 'blue', linewidth=1)
ax.text(13.7, 0.8, '解决', fontsize=8)

ax.plot([14.5, 15], [1, 0.6], 'blue', linewidth=1)

# 测试收集器到Release管理器的反馈
ax.plot([9, 6.5], [1.2, 0.8], 'r--', linewidth=1)

# 图例
legend_elements = [
    patches.Patch(facecolor=colors['central'], edgecolor='black', label='中央协调器'),
    patches.Patch(facecolor=colors['planner'], edgecolor='black', label='规划器'),
    patches.Patch(facecolor=colors['brainstorm'], edgecolor='black', label='头脑风暴器'),
    patches.Patch(facecolor=colors['release'], edgecolor='black', label='Release管理器'),
    patches.Patch(facecolor=colors['recorder'], edgecolor='black', label='记录器'),
    patches.Patch(facecolor=colors['test'], edgecolor='black', label='测试收集器'),
    patches.Patch(facecolor=colors['solver'], edgecolor='black', label='问题解决器'),
    patches.Patch(facecolor=colors['external'], edgecolor='black', label='外部系统'),
    patches.Patch(facecolor=colors['submodule'], edgecolor='black', label='子模块'),
]

ax.legend(handles=legend_elements, loc='lower center', bbox_to_anchor=(0.5, -0.05), 
          ncol=5, fontsize=8)

# 设置坐标轴
ax.set_xlim(0, 17)
ax.set_ylim(-0.5, 10)
ax.axis('off')

# 添加标题
plt.title('PowerAutomation MCP 系统架构图', fontsize=16, pad=20)

# 保存图像
plt.tight_layout()
plt.savefig('mcp_architecture_updated.png', dpi=300, bbox_inches='tight')
plt.close()

print("架构图已更新，灰色模块字体已调整")
