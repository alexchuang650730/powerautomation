from PIL import Image, ImageDraw, ImageFont
import os

# 创建一个大画布
width, height = 1200, 800
image = Image.new('RGB', (width, height), color='white')
draw = ImageDraw.Draw(image)

# 尝试加载字体，如果失败则使用默认字体
try:
    font_title = ImageFont.truetype("DejaVuSans.ttf", 24)
    font_label = ImageFont.truetype("DejaVuSans.ttf", 14)
    font_small = ImageFont.truetype("DejaVuSans.ttf", 12)
except IOError:
    font_title = ImageFont.load_default()
    font_label = ImageFont.load_default()
    font_small = ImageFont.load_default()

# 定义颜色
colors = {
    'central': (93, 173, 226),  # 中央协调器
    'planner': (93, 173, 226),  # 规划器
    'brainstorm': (72, 201, 176),  # 头脑风暴器
    'recorder': (236, 112, 99),  # 记录器
    'release': (245, 176, 65),  # Release管理器
    'collector': (230, 126, 34),  # 测试收集器
    'solver': (175, 122, 197),  # 问题解决器
    'external': (171, 178, 185),  # 外部系统
    'submodule': (171, 178, 185),  # 子模块
}

# 绘制标题
draw.text((width/2, 30), "PowerAutomation MCP 系统架构图", fill=(0, 0, 0), font=font_title, anchor="mm")

# 定义节点位置和大小
nodes = {
    # 中央协调器
    'central': {'pos': (600, 150), 'width': 300, 'height': 80, 'color': colors['central'], 'label': 'MCP中央协调器\n(MCPCentralCoordinator)'},
    
    # 规划器和头脑风暴器
    'planner': {'pos': (300, 300), 'width': 200, 'height': 60, 'color': colors['planner'], 'label': 'MCP规划器\n(MCPPlanner)'},
    'brainstorm': {'pos': (900, 300), 'width': 200, 'height': 60, 'color': colors['brainstorm'], 'label': 'MCP头脑风暴器\n(MCPBrainstorm)'},
    
    # 工具模块
    'recorder': {'pos': (150, 450), 'width': 200, 'height': 60, 'color': colors['recorder'], 'label': '思考与操作记录器\n(ThoughtActionRecorder)'},
    'release': {'pos': (400, 450), 'width': 200, 'height': 60, 'color': colors['release'], 'label': 'Release管理器\n(ReleaseManager)'},
    'collector': {'pos': (650, 450), 'width': 200, 'height': 60, 'color': colors['collector'], 'label': '测试与问题收集器\n(TestAndIssueCollector)'},
    'solver': {'pos': (900, 450), 'width': 200, 'height': 60, 'color': colors['solver'], 'label': 'Agent问题解决驱动器\n(AgentProblemSolver)'},
    
    # 外部系统
    'mcp_so': {'pos': (100, 150), 'width': 120, 'height': 40, 'color': colors['external'], 'label': 'mcp.so'},
    'github': {'pos': (1100, 150), 'width': 120, 'height': 40, 'color': colors['external'], 'label': 'GitHub'},
    
    # 子模块 - 规划器 (确保足够宽以容纳文本)
    'matcher': {'pos': (200, 370), 'width': 120, 'height': 30, 'color': colors['submodule'], 'label': 'MCPMatcher'},
    'executor': {'pos': (350, 370), 'width': 120, 'height': 30, 'color': colors['submodule'], 'label': 'MCPExecutor'},
    'cache': {'pos': (200, 400), 'width': 150, 'height': 30, 'color': colors['submodule'], 'label': 'MCPCacheManager'},
    'currency': {'pos': (350, 400), 'width': 150, 'height': 30, 'color': colors['submodule'], 'label': 'CurrencyController'},
    
    # 子模块 - 头脑风暴器 (确保足够宽以容纳文本)
    'analyzer': {'pos': (800, 370), 'width': 150, 'height': 30, 'color': colors['submodule'], 'label': 'CapabilityAnalyzer'},
    'converter': {'pos': (980, 370), 'width': 150, 'height': 30, 'color': colors['submodule'], 'label': 'MCPConverter'},
    'enhancer': {'pos': (900, 400), 'width': 150, 'height': 30, 'color': colors['submodule'], 'label': 'SearchEnhancer'},
    
    # 子模块 - 记录器 (确保足够宽以容纳文本)
    'visual': {'pos': (100, 550), 'width': 180, 'height': 30, 'color': colors['submodule'], 'label': 'VisualThoughtRecorder'},
    'enhanced': {'pos': (300, 550), 'width': 180, 'height': 30, 'color': colors['submodule'], 'label': 'EnhancedThoughtRecorder'},
    
    # 子模块 - Release管理器 (确保足够宽以容纳文本)
    'rules': {'pos': (400, 550), 'width': 180, 'height': 30, 'color': colors['submodule'], 'label': 'ReleaseRulesChecker'},
    
    # 子模块 - 测试收集器 (确保足够宽以容纳文本)
    'updater': {'pos': (650, 550), 'width': 180, 'height': 30, 'color': colors['submodule'], 'label': 'TestReadmeUpdater'},
    
    # 子模块 - 问题解决器 (确保足够宽以容纳文本)
    'manager': {'pos': (850, 550), 'width': 180, 'height': 30, 'color': colors['submodule'], 'label': 'SessionSavePointManager'},
    'rollback': {'pos': (1050, 550), 'width': 150, 'height': 30, 'color': colors['submodule'], 'label': 'RollbackExecutor'},
}

# 绘制节点
for node_id, node in nodes.items():
    x, y = node['pos']
    width, height = node['width'], node['height']
    color = node['color']
    label = node['label']
    
    # 绘制矩形
    draw.rectangle([(x - width/2, y - height/2), (x + width/2, y + height/2)], 
                  fill=color, outline=(0, 0, 0))
    
    # 添加标签
    draw.text((x, y), label, fill=(0, 0, 0), font=font_label, anchor="mm")

# 定义连接线
connections = [
    # 中央协调器连接
    {'from': 'central', 'to': 'planner', 'color': (0, 0, 255), 'label': '协调'},
    {'from': 'central', 'to': 'brainstorm', 'color': (0, 0, 255), 'label': '协调'},
    
    # 规划器连接
    {'from': 'planner', 'to': 'matcher', 'color': (0, 128, 0), 'label': '调用'},
    {'from': 'planner', 'to': 'executor', 'color': (0, 128, 0), 'label': '调用'},
    {'from': 'planner', 'to': 'analyzer', 'color': (0, 128, 0), 'label': '调用'},
    {'from': 'planner', 'to': 'enhancer', 'color': (0, 128, 0), 'label': '调用'},
    
    # 头脑风暴器连接
    {'from': 'brainstorm', 'to': 'planner', 'color': (128, 0, 128), 'label': '能力提升'},
    
    # 外部系统连接
    {'from': 'mcp_so', 'to': 'central', 'color': (128, 128, 128), 'label': '集成'},
    {'from': 'central', 'to': 'github', 'color': (128, 128, 128), 'label': '同步'},
    
    # 工具模块连接
    {'from': 'recorder', 'to': 'visual', 'color': (0, 0, 255), 'label': '记录'},
    {'from': 'recorder', 'to': 'enhanced', 'color': (0, 0, 255), 'label': '记录'},
    {'from': 'release', 'to': 'rules', 'color': (0, 0, 255), 'label': '检查'},
    {'from': 'collector', 'to': 'updater', 'color': (0, 0, 255), 'label': '收集'},
    {'from': 'solver', 'to': 'manager', 'color': (0, 0, 255), 'label': '解决'},
    {'from': 'solver', 'to': 'rollback', 'color': (0, 0, 255), 'label': '回滚'},
    
    # 工具模块间连接
    {'from': 'release', 'to': 'collector', 'color': (255, 165, 0), 'label': '测试'},
    {'from': 'collector', 'to': 'solver', 'color': (255, 165, 0), 'label': '问题'},
    {'from': 'recorder', 'to': 'release', 'color': (255, 165, 0), 'label': '更新'},
    
    # 规划器到工具模块的连接
    {'from': 'planner', 'to': 'recorder', 'color': (0, 128, 0), 'label': ''},
    {'from': 'planner', 'to': 'collector', 'color': (0, 128, 0), 'label': ''},
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
    
    # 绘制箭头线
    draw.line([(from_x, from_y), (to_x, to_y)], fill=conn['color'], width=2)
    
    # 添加箭头
    if to_x > from_x:
        arrow_x = to_x - 10
        dx = -10
    else:
        arrow_x = to_x + 10
        dx = 10
        
    if to_y > from_y:
        arrow_y = to_y - 10
        dy = -10
    else:
        arrow_y = to_y + 10
        dy = 10
        
    # 简单箭头
    draw.polygon([(to_x, to_y), (arrow_x, arrow_y), (arrow_x + dy/2, arrow_y + dx/2)], fill=conn['color'])
    
    # 添加标签
    if conn['label']:
        mid_x = (from_x + to_x) / 2
        mid_y = (from_y + to_y) / 2
        # 绘制白色背景使文字更清晰
        text_width = len(conn['label']) * 7
        draw.rectangle([(mid_x - text_width/2, mid_y - 10), (mid_x + text_width/2, mid_y + 10)], 
                      fill=(255, 255, 255, 128))
        draw.text((mid_x, mid_y), conn['label'], fill=(0, 0, 0), font=font_small, anchor="mm")

# 添加图例
legend_items = [
    {'color': colors['central'], 'label': '中央协调器'},
    {'color': colors['brainstorm'], 'label': '头脑风暴器'},
    {'color': colors['release'], 'label': 'Release管理器'},
    {'color': colors['solver'], 'label': '问题解决器'},
    {'color': colors['external'], 'label': '外部系统'},
    {'color': colors['submodule'], 'label': '子模块'},
]

# 绘制图例
legend_x = 100
legend_y = 650
for item in legend_items:
    # 绘制图例方块
    draw.rectangle([(legend_x, legend_y), (legend_x + 20, legend_y + 20)], 
                  fill=item['color'], outline=(0, 0, 0))
    # 绘制图例文字
    draw.text((legend_x + 30, legend_y + 10), item['label'], fill=(0, 0, 0), font=font_small, anchor="lm")
    legend_x += 180
    if legend_x > 900:  # 换行
        legend_x = 100
        legend_y += 30

# 确保目录存在
os.makedirs('/home/ubuntu/powerautomation_integration/docs/images', exist_ok=True)

# 保存图像
image.save('/home/ubuntu/powerautomation_integration/docs/images/mcp_architecture_updated.png')

print("架构图已生成并保存到 /home/ubuntu/powerautomation_integration/docs/images/mcp_architecture_updated.png")
