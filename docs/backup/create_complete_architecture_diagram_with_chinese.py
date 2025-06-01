import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib.patches as patches
import numpy as np
import os

# 检查可用字体
fonts = [f.name for f in fm.fontManager.ttflist]
print("可用字体列表:")
for font in sorted(fonts):
    if "sans" in font.lower() or "noto" in font.lower() or "source" in font.lower():
        print(f"- {font}")

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans', 'Arial Unicode MS', 'Noto Sans CJK SC', 'Source Han Sans CN']
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# 创建图形和坐标轴
fig, ax = plt.subplots(figsize=(15, 10), dpi=100)

# 设置背景色为白色
fig.patch.set_facecolor('white')
ax.set_facecolor('white')

# 移除坐标轴
ax.set_axis_off()

# 设置标题
plt.title('PowerAutomation 系统架构图', fontsize=20, pad=20)

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
    'agent': '#3498DB',  # 智能体
    'tool': '#9B59B6',  # 开发工具
}

# 定义节点位置和大小
nodes = {
    # 中央协调器
    'central': {'pos': (7.5, 8), 'width': 4, 'height': 1.5, 'color': colors['central'], 'label': 'MCP中央协调器\n(MCPCentralCoordinator)'},
    
    # 规划器和头脑风暴器
    'planner': {'pos': (4.5, 5.5), 'width': 3, 'height': 1.5, 'color': colors['planner'], 'label': 'MCP规划器\n(MCPPlanner)'},
    'brainstorm': {'pos': (10.5, 5.5), 'width': 3, 'height': 1.5, 'color': colors['brainstorm'], 'label': 'MCP头脑风暴器\n(MCPBrainstorm)'},
    
    # 智能体
    'ppt_agent': {'pos': (2, 8), 'width': 2, 'height': 1, 'color': colors['agent'], 'label': 'PPT智能体\n(PPTAgent)'},
    'web_agent': {'pos': (2, 6.5), 'width': 2, 'height': 1, 'color': colors['agent'], 'label': '网页智能体\n(WebAgent)'},
    'code_agent': {'pos': (2, 5), 'width': 2, 'height': 1, 'color': colors['agent'], 'label': '代码智能体\n(CodeAgent)'},
    'general_agent': {'pos': (2, 3.5), 'width': 2, 'height': 1, 'color': colors['agent'], 'label': '通用智能体\n(GeneralAgent)'},
    
    # 工具模块
    'recorder': {'pos': (3, 3), 'width': 2.5, 'height': 1.2, 'color': colors['recorder'], 'label': '思考与操作记录器\n(ThoughtActionRecorder)'},
    'release': {'pos': (6, 3), 'width': 2.5, 'height': 1.2, 'color': colors['release'], 'label': 'Release管理器\n(ReleaseManager)'},
    'collector': {'pos': (9, 3), 'width': 2.5, 'height': 1.2, 'color': colors['collector'], 'label': '测试与问题收集器\n(TestAndIssueCollector)'},
    'solver': {'pos': (12, 3), 'width': 2.5, 'height': 1.2, 'color': colors['solver'], 'label': 'Agent问题解决驱动器\n(AgentProblemSolver)'},
    
    # 外部系统
    'mcp_so': {'pos': (1, 8), 'width': 1.5, 'height': 1, 'color': colors['external'], 'label': 'mcp.so'},
    'github': {'pos': (14, 8), 'width': 1.5, 'height': 1, 'color': colors['external'], 'label': 'GitHub'},
    
    # MCP增强模块
    'sequential': {'pos': (3, 1.5), 'width': 2.5, 'height': 1, 'color': colors['tool'], 'label': 'Sequential Thinking适配器'},
    'playwright': {'pos': (6, 1.5), 'width': 2.5, 'height': 1, 'color': colors['tool'], 'label': 'Playwright适配器'},
    'webagent': {'pos': (9, 1.5), 'width': 2.5, 'height': 1, 'color': colors['tool'], 'label': 'WebAgentB增强适配器'},
    'enhanced_planner': {'pos': (4, 0.5), 'width': 2.5, 'height': 1, 'color': colors['tool'], 'label': '增强版MCP规划器'},
    'enhanced_brainstorm': {'pos': (7.5, 0.5), 'width': 2.5, 'height': 1, 'color': colors['tool'], 'label': '增强版MCP头脑风暴器'},
    'problem_solver': {'pos': (11, 0.5), 'width': 2.5, 'height': 1, 'color': colors['tool'], 'label': '主动问题解决器'},
    
    # 子模块 - 规划器
    'matcher': {'pos': (3.5, 4.5), 'width': 1.5, 'height': 0.6, 'color': colors['submodule'], 'label': 'MCPMatcher'},
    'executor': {'pos': (5.5, 4.5), 'width': 1.5, 'height': 0.6, 'color': colors['submodule'], 'label': 'MCPExecutor'},
    'cache': {'pos': (3.5, 3.9), 'width': 1.5, 'height': 0.6, 'color': colors['submodule'], 'label': 'MCPCacheManager'},
    'currency': {'pos': (5.5, 3.9), 'width': 1.5, 'height': 0.6, 'color': colors['submodule'], 'label': 'CurrencyController'},
    
    # 子模块 - 头脑风暴器
    'analyzer': {'pos': (9.5, 4.5), 'width': 1.5, 'height': 0.6, 'color': colors['submodule'], 'label': 'CapabilityAnalyzer'},
    'converter': {'pos': (11.5, 4.5), 'width': 1.5, 'height': 0.6, 'color': colors['submodule'], 'label': 'MCPConverter'},
    'enhancer': {'pos': (10.5, 3.9), 'width': 1.5, 'height': 0.6, 'color': colors['submodule'], 'label': 'SearchEnhancer'},
    
    # 子模块 - 记录器
    'visual': {'pos': (2, 2), 'width': 1.8, 'height': 0.6, 'color': colors['submodule'], 'label': 'VisualThoughtRecorder'},
    'enhanced': {'pos': (4, 2), 'width': 1.8, 'height': 0.6, 'color': colors['submodule'], 'label': 'EnhancedThoughtRecorder'},
    
    # 子模块 - Release管理器
    'rules': {'pos': (6, 2), 'width': 1.8, 'height': 0.6, 'color': colors['submodule'], 'label': 'ReleaseRulesChecker'},
    
    # 子模块 - 测试收集器
    'updater': {'pos': (9, 2), 'width': 1.8, 'height': 0.6, 'color': colors['submodule'], 'label': 'TestReadmeUpdater'},
    
    # 子模块 - 问题解决器
    'manager': {'pos': (11, 2), 'width': 1.8, 'height': 0.6, 'color': colors['submodule'], 'label': 'SessionSavePointManager'},
    'rollback': {'pos': (13, 2), 'width': 1.8, 'height': 0.6, 'color': colors['submodule'], 'label': 'RollbackExecutor'},
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
    
    # 智能体连接
    {'from': 'ppt_agent', 'to': 'central', 'color': 'green', 'label': '调用'},
    {'from': 'web_agent', 'to': 'central', 'color': 'green', 'label': '调用'},
    {'from': 'code_agent', 'to': 'central', 'color': 'green', 'label': '调用'},
    {'from': 'general_agent', 'to': 'central', 'color': 'green', 'label': '调用'},
    
    # 规划器连接
    {'from': 'planner', 'to': 'matcher', 'color': 'green', 'label': '调用'},
    {'from': 'planner', 'to': 'executor', 'color': 'green', 'label': '调用'},
    {'from': 'planner', 'to': 'cache', 'color': 'green', 'label': '调用'},
    {'from': 'planner', 'to': 'currency', 'color': 'green', 'label': '调用'},
    
    # 头脑风暴器连接
    {'from': 'brainstorm', 'to': 'analyzer', 'color': 'green', 'label': '调用'},
    {'from': 'brainstorm', 'to': 'converter', 'color': 'green', 'label': '调用'},
    {'from': 'brainstorm', 'to': 'enhancer', 'color': 'green', 'label': '调用'},
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
    {'from': 'release', 'to': 'collector', 'color': 'orange', 'label': '测试'},
    {'from': 'collector', 'to': 'solver', 'color': 'orange', 'label': '问题'},
    {'from': 'recorder', 'to': 'release', 'color': 'orange', 'label': '更新'},
    
    # 规划器到工具模块的连接
    {'from': 'planner', 'to': 'recorder', 'color': 'green', 'label': '调用'},
    {'from': 'planner', 'to': 'collector', 'color': 'green', 'label': '调用'},
    
    # MCP增强模块连接
    {'from': 'sequential', 'to': 'enhanced_planner', 'color': 'purple', 'label': '增强'},
    {'from': 'playwright', 'to': 'enhanced_brainstorm', 'color': 'purple', 'label': '增强'},
    {'from': 'webagent', 'to': 'enhanced_brainstorm', 'color': 'purple', 'label': '增强'},
    {'from': 'sequential', 'to': 'problem_solver', 'color': 'purple', 'label': '增强'},
    {'from': 'webagent', 'to': 'problem_solver', 'color': 'purple', 'label': '增强'},
    
    # 增强模块到核心模块的连接
    {'from': 'enhanced_planner', 'to': 'planner', 'color': 'red', 'label': '优化'},
    {'from': 'enhanced_brainstorm', 'to': 'brainstorm', 'color': 'red', 'label': '优化'},
    {'from': 'problem_solver', 'to': 'solver', 'color': 'red', 'label': '优化'},
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
        
        # 绘制白色背景使文字更清晰
        bbox_props = dict(boxstyle="round,pad=0.3", fc="white", ec="black", alpha=0.8)
        ax.text(mid_x, mid_y, conn['label'], ha='center', va='center', 
                bbox=bbox_props, fontsize=9)

# 添加图例
legend_elements = [
    patches.Patch(facecolor=colors['central'], edgecolor='black', label='中央协调器'),
    patches.Patch(facecolor=colors['planner'], edgecolor='black', label='规划器'),
    patches.Patch(facecolor=colors['brainstorm'], edgecolor='black', label='头脑风暴器'),
    patches.Patch(facecolor=colors['agent'], edgecolor='black', label='智能体'),
    patches.Patch(facecolor=colors['recorder'], edgecolor='black', label='记录器'),
    patches.Patch(facecolor=colors['release'], edgecolor='black', label='Release管理器'),
    patches.Patch(facecolor=colors['collector'], edgecolor='black', label='测试收集器'),
    patches.Patch(facecolor=colors['solver'], edgecolor='black', label='问题解决器'),
    patches.Patch(facecolor=colors['tool'], edgecolor='black', label='MCP增强模块'),
    patches.Patch(facecolor=colors['external'], edgecolor='black', label='外部系统'),
    patches.Patch(facecolor=colors['submodule'], edgecolor='black', label='子模块'),
]

# 放置图例在底部
ax.legend(handles=legend_elements, loc='lower center', bbox_to_anchor=(0.5, -0.05),
          ncol=4, frameon=True, fontsize=9)

# 调整布局
plt.tight_layout()
plt.subplots_adjust(bottom=0.15)

# 确保目录存在
os.makedirs('/home/ubuntu/powerautomation_integration/docs/images', exist_ok=True)

# 保存图像
output_path = '/home/ubuntu/powerautomation_integration/docs/images/powerautomation_complete_architecture.png'
plt.savefig(output_path, dpi=150, bbox_inches='tight')

print(f"完整架构图已生成并保存到 {output_path}")
