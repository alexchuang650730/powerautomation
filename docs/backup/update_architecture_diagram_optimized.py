import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# 创建图形和坐标轴
fig, ax = plt.subplots(figsize=(12, 8), dpi=100)

# 设置背景色为白色
fig.patch.set_facecolor('white')
ax.set_facecolor('white')

# 移除坐标轴
ax.set_axis_off()

# 设置标题
plt.title('PowerAutomation MCP 系统架构图', fontsize=16, pad=20)

# 定义颜色
colors = {
    'central': '#5DADE2',  # 中央协调器
    'planner': '#5DADE2',  # 规划器
    'brainstorm': '#48C9B0',  # 头脑风暴器
    'recorder': '#EC7063',  # 记录器
    'release': '#F5B041',  # Release管理器
    'collector': '#E67E22',  # 测试收集器
    'solver': '#AF7AC5',  # 问题解决器
    'external': '#ABB2B9',  # 外部系统
    'submodule': '#ABB2B9',  # 子模块
}

# 定义节点位置和大小，确保灰色模块有足够大的尺寸
nodes = {
    # 中央协调器
    'central': {'pos': (7, 8), 'width': 4, 'height': 2, 'color': colors['central'], 'label': 'MCP中央协调器\n(MCPCentralCoordinator)'},
    
    # 规划器和头脑风暴器
    'planner': {'pos': (3, 5), 'width': 3, 'height': 1.5, 'color': colors['planner'], 'label': 'MCP规划器\n(MCPPlanner)'},
    'brainstorm': {'pos': (11, 5), 'width': 3, 'height': 1.5, 'color': colors['brainstorm'], 'label': 'MCP头脑风暴器\n(MCPBrainstorm)'},
    
    # 工具模块
    'recorder': {'pos': (2, 2), 'width': 3, 'height': 1.5, 'color': colors['recorder'], 'label': '思考与操作记录器\n(ThoughtActionRecorder)'},
    'release': {'pos': (6, 2), 'width': 3, 'height': 1.5, 'color': colors['release'], 'label': 'Release管理器\n(ReleaseManager)'},
    'collector': {'pos': (10, 2), 'width': 3, 'height': 1.5, 'color': colors['collector'], 'label': '测试与问题收集器\n(TestAndIssueCollector)'},
    'solver': {'pos': (14, 2), 'width': 3, 'height': 1.5, 'color': colors['solver'], 'label': 'Agent问题解决驱动器\n(AgentProblemSolver)'},
    
    # 外部系统
    'mcp_so': {'pos': (1, 8), 'width': 2, 'height': 1, 'color': colors['external'], 'label': 'mcp.so'},
    'github': {'pos': (13, 8), 'width': 2, 'height': 1, 'color': colors['external'], 'label': 'GitHub'},
    
    # 子模块 - 规划器 (增加宽度以适应文本)
    'matcher': {'pos': (1.5, 3.8), 'width': 2.0, 'height': 0.8, 'color': colors['submodule'], 'label': 'MCPMatcher'},
    'executor': {'pos': (3.5, 3.8), 'width': 2.0, 'height': 0.8, 'color': colors['submodule'], 'label': 'MCPExecutor'},
    'cache': {'pos': (1.5, 3), 'width': 2.5, 'height': 0.8, 'color': colors['submodule'], 'label': 'MCPCacheManager'},
    'currency': {'pos': (4, 3), 'width': 2.5, 'height': 0.8, 'color': colors['submodule'], 'label': 'CurrencyController'},
    
    # 子模块 - 头脑风暴器 (增加宽度以适应文本)
    'analyzer': {'pos': (9.5, 3.8), 'width': 2.5, 'height': 0.8, 'color': colors['submodule'], 'label': 'CapabilityAnalyzer'},
    'converter': {'pos': (12, 3.8), 'width': 2.5, 'height': 0.8, 'color': colors['submodule'], 'label': 'MCPConverter'},
    'enhancer': {'pos': (10.5, 3), 'width': 2.5, 'height': 0.8, 'color': colors['submodule'], 'label': 'SearchEnhancer'},
    
    # 子模块 - 记录器 (增加宽度以适应文本)
    'visual': {'pos': (1, 0.8), 'width': 3.0, 'height': 0.8, 'color': colors['submodule'], 'label': 'VisualThoughtRecorder'},
    'enhanced': {'pos': (4, 0.8), 'width': 3.0, 'height': 0.8, 'color': colors['submodule'], 'label': 'EnhancedThoughtRecorder'},
    
    # 子模块 - Release管理器 (增加宽度以适应文本)
    'rules': {'pos': (6, 0.8), 'width': 3.0, 'height': 0.8, 'color': colors['submodule'], 'label': 'ReleaseRulesChecker'},
    
    # 子模块 - 测试收集器 (增加宽度以适应文本)
    'updater': {'pos': (10, 0.8), 'width': 3.0, 'height': 0.8, 'color': colors['submodule'], 'label': 'TestReadmeUpdater'},
    
    # 子模块 - 问题解决器 (增加宽度以适应文本)
    'manager': {'pos': (13, 0.8), 'width': 3.0, 'height': 0.8, 'color': colors['submodule'], 'label': 'SessionSavePointManager'},
    'rollback': {'pos': (16, 0.8), 'width': 2.5, 'height': 0.8, 'color': colors['submodule'], 'label': 'RollbackExecutor'},
}

# 绘制节点
for node_id, node in nodes.items():
    x, y = node['pos']
    width, height = node['width'], node['height']
    color = node['color']
    label = node['label']
    
    # 绘制矩形
    rect = patches.Rectangle((x - width/2, y - height/2), width, height, 
                             linewidth=1, edgecolor='black', facecolor=color)
    ax.add_patch(rect)
    
    # 添加标签，为子模块使用更小的字体
    if node_id in ['matcher', 'executor', 'cache', 'currency', 'analyzer', 'converter', 'enhancer', 'visual', 'enhanced', 'rules', 'updater', 'manager', 'rollback']:
        fontsize = 8  # 子模块使用更小的字体
    else:
        fontsize = 10  # 主要模块使用正常字体
    
    ax.text(x, y, label, ha='center', va='center', fontsize=fontsize)

# 定义连接线
connections = [
    # 中央协调器连接
    {'from': 'central', 'to': 'planner', 'color': 'blue', 'label': '协调'},
    {'from': 'central', 'to': 'brainstorm', 'color': 'blue', 'label': '协调'},
    
    # 规划器连接
    {'from': 'planner', 'to': 'matcher', 'color': 'green', 'label': '调用'},
    {'from': 'planner', 'to': 'executor', 'color': 'green', 'label': '调用'},
    {'from': 'planner', 'to': 'analyzer', 'color': 'green', 'label': '调用'},
    {'from': 'planner', 'to': 'enhancer', 'color': 'green', 'label': '调用'},
    
    # 头脑风暴器连接
    {'from': 'brainstorm', 'to': 'planner', 'color': 'purple', 'label': '能力提升'},
    
    # 外部系统连接
    {'from': 'mcp_so', 'to': 'central', 'color': 'gray', 'label': '集成'},
    {'from': 'central', 'to': 'github', 'color': 'gray', 'label': '同步'},
    
    # 工具模块连接
    {'from': 'recorder', 'to': 'visual', 'color': 'blue', 'label': '记录'},
    {'from': 'recorder', 'to': 'enhanced', 'color': 'blue', 'label': '记录'},
    {'from': 'release', 'to': 'rules', 'color': 'blue', 'label': '检查'},
    {'from': 'collector', 'to': 'updater', 'color': 'blue', 'label': '收集'},
    {'from': 'solver', 'to': 'manager', 'color': 'blue', 'label': '解决'},
    {'from': 'solver', 'to': 'rollback', 'color': 'blue', 'label': '回滚'},
    
    # 工具模块间连接
    {'from': 'recorder', 'to': 'release', 'color': 'orange', 'label': '更新'},
    {'from': 'release', 'to': 'collector', 'color': 'orange', 'label': '测试'},
    {'from': 'collector', 'to': 'solver', 'color': 'orange', 'label': '问题'},
    
    # 规划器到工具模块的连接
    {'from': 'planner', 'to': 'recorder', 'color': 'green', 'label': ''},
    {'from': 'planner', 'to': 'collector', 'color': 'green', 'label': ''},
]

# 绘制连接线
for conn in connections:
    from_node = nodes[conn['from']]
    to_node = nodes[conn['to']]
    
    from_x, from_y = from_node['pos']
    to_x, to_y = to_node['pos']
    
    # 计算连接点
    if from_y > to_y:  # 从上到下
        from_y -= from_node['height']/2
        to_y += to_node['height']/2
    elif from_y < to_y:  # 从下到上
        from_y += from_node['height']/2
        to_y -= to_node['height']/2
    elif from_x > to_x:  # 从右到左
        from_x -= from_node['width']/2
        to_x += to_node['width']/2
    else:  # 从左到右
        from_x += from_node['width']/2
        to_x -= to_node['width']/2
    
    # 绘制箭头
    ax.annotate('', xy=(to_x, to_y), xytext=(from_x, from_y),
                arrowprops=dict(arrowstyle='->', color=conn['color'], lw=1.5))
    
    # 添加标签
    if conn['label']:
        mid_x = (from_x + to_x) / 2
        mid_y = (from_y + to_y) / 2
        ax.text(mid_x, mid_y, conn['label'], ha='center', va='center', 
                bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'), fontsize=9)

# 添加图例
legend_elements = [
    patches.Patch(facecolor=colors['central'], edgecolor='black', label='中央协调器'),
    patches.Patch(facecolor=colors['planner'], edgecolor='black', label='规划器'),
    patches.Patch(facecolor=colors['brainstorm'], edgecolor='black', label='头脑风暴器'),
    patches.Patch(facecolor=colors['release'], edgecolor='black', label='Release管理器'),
    patches.Patch(facecolor=colors['recorder'], edgecolor='black', label='记录器'),
    patches.Patch(facecolor=colors['collector'], edgecolor='black', label='测试收集器'),
    patches.Patch(facecolor=colors['solver'], edgecolor='black', label='问题解决器'),
    patches.Patch(facecolor=colors['external'], edgecolor='black', label='外部系统'),
    patches.Patch(facecolor=colors['submodule'], edgecolor='black', label='子模块'),
]

# 放置图例在底部
ax.legend(handles=legend_elements, loc='lower center', bbox_to_anchor=(0.5, -0.05),
          ncol=3, frameon=True, fontsize=9)

# 调整布局
plt.tight_layout()
plt.subplots_adjust(bottom=0.15)

# 保存图像
plt.savefig('/home/ubuntu/powerautomation_integration/docs/images/mcp_architecture_updated.png', dpi=150, bbox_inches='tight')

print("架构图已生成并保存到 /home/ubuntu/powerautomation_integration/docs/images/mcp_architecture_updated.png")
