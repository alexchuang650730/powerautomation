from PIL import Image, ImageDraw, ImageFont
import os

# 创建一个大画布
width, height = 1500, 1000
image = Image.new('RGB', (width, height), color='white')
draw = ImageDraw.Draw(image)

# 尝试加载中文字体，按优先级尝试
font_paths = [
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",  # Ubuntu常见路径
    "/usr/share/fonts/noto-cjk/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/wqy-microhei/wqy-microhei.ttc",  # 文泉驿微米黑
    "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
    "DejaVuSans.ttf"  # 默认字体
]

# 尝试加载字体
font_title = None
font_label = None
font_small = None
font_submodule = None

for font_path in font_paths:
    try:
        if os.path.exists(font_path):
            print(f"尝试加载字体: {font_path}")
            font_title = ImageFont.truetype(font_path, 24)
            font_label = ImageFont.truetype(font_path, 16)
            font_small = ImageFont.truetype(font_path, 12)
            font_submodule = ImageFont.truetype(font_path, 10)
            print(f"成功加载字体: {font_path}")
            break
    except Exception as e:
        print(f"加载字体 {font_path} 失败: {e}")

# 如果所有字体都加载失败，使用默认字体
if font_title is None:
    print("所有字体加载失败，使用默认字体")
    font_title = ImageFont.load_default()
    font_label = ImageFont.load_default()
    font_small = ImageFont.load_default()
    font_submodule = font_small

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
    'agent': (52, 152, 219),  # 智能体
    'tool': (76, 175, 80),  # 开发工具 - 改为绿色，避免使用紫色
}

# 绘制标题
draw.text((width/2, 30), "PowerAutomation 系统架构图", fill=(0, 0, 0), font=font_title, anchor="mm")

# 定义节点位置和大小
nodes = {
    # 中央协调器
    'central': {'pos': (width/2, 150), 'width': 400, 'height': 80, 'color': colors['central'], 'label': 'MCP中央协调器\n(MCPCentralCoordinator)', 'font': font_label},
    
    # 规划器和头脑风暴器
    'planner': {'pos': (width/2 - 300, 300), 'width': 250, 'height': 70, 'color': colors['planner'], 'label': 'MCP规划器\n(MCPPlanner)', 'font': font_label},
    'brainstorm': {'pos': (width/2 + 300, 300), 'width': 250, 'height': 70, 'color': colors['brainstorm'], 'label': 'MCP头脑风暴器\n(MCPBrainstorm)', 'font': font_label},
    
    # 智能体
    'ppt_agent': {'pos': (200, 150), 'width': 180, 'height': 60, 'color': colors['agent'], 'label': 'PPT智能体\n(PPTAgent)', 'font': font_label},
    'web_agent': {'pos': (200, 230), 'width': 180, 'height': 60, 'color': colors['agent'], 'label': '网页智能体\n(WebAgent)', 'font': font_label},
    'code_agent': {'pos': (200, 310), 'width': 180, 'height': 60, 'color': colors['agent'], 'label': '代码智能体\n(CodeAgent)', 'font': font_label},
    'general_agent': {'pos': (200, 390), 'width': 180, 'height': 60, 'color': colors['agent'], 'label': '通用智能体\n(GeneralAgent)', 'font': font_label},
    
    # 工具模块
    'recorder': {'pos': (width/2 - 450, 450), 'width': 220, 'height': 70, 'color': colors['recorder'], 'label': '思考与操作记录器\n(ThoughtActionRecorder)', 'font': font_label},
    'release': {'pos': (width/2 - 150, 450), 'width': 220, 'height': 70, 'color': colors['release'], 'label': 'Release管理器\n(ReleaseManager)', 'font': font_label},
    'collector': {'pos': (width/2 + 150, 450), 'width': 220, 'height': 70, 'color': colors['collector'], 'label': '测试与问题收集器\n(TestAndIssueCollector)', 'font': font_label},
    'solver': {'pos': (width/2 + 450, 450), 'width': 220, 'height': 70, 'color': colors['solver'], 'label': 'Agent问题解决驱动器\n(AgentProblemSolver)', 'font': font_label},
    
    # 外部系统
    'mcp_so': {'pos': (100, 150), 'width': 120, 'height': 50, 'color': colors['external'], 'label': 'mcp.so', 'font': font_label},
    'github': {'pos': (width - 100, 150), 'width': 120, 'height': 50, 'color': colors['external'], 'label': 'GitHub', 'font': font_label},
    
    # MCP增强模块
    'sequential': {'pos': (width/2 - 450, 600), 'width': 220, 'height': 70, 'color': colors['tool'], 'label': 'Sequential Thinking适配器', 'font': font_label},
    'playwright': {'pos': (width/2 - 150, 600), 'width': 220, 'height': 70, 'color': colors['tool'], 'label': 'Playwright适配器', 'font': font_label},
    'webagent': {'pos': (width/2 + 150, 600), 'width': 220, 'height': 70, 'color': colors['tool'], 'label': 'WebAgentB增强适配器', 'font': font_label},
    'enhanced_planner': {'pos': (width/2 - 300, 700), 'width': 220, 'height': 70, 'color': colors['tool'], 'label': '增强版MCP规划器', 'font': font_label},
    'enhanced_brainstorm': {'pos': (width/2, 700), 'width': 220, 'height': 70, 'color': colors['tool'], 'label': '增强版MCP头脑风暴器', 'font': font_label},
    'problem_solver': {'pos': (width/2 + 300, 700), 'width': 220, 'height': 70, 'color': colors['tool'], 'label': '主动问题解决器', 'font': font_label},
    
    # 子模块 - 规划器
    'matcher': {'pos': (width/2 - 380, 370), 'width': 120, 'height': 30, 'color': colors['submodule'], 'label': 'MCPMatcher', 'font': font_submodule},
    'executor': {'pos': (width/2 - 250, 370), 'width': 120, 'height': 30, 'color': colors['submodule'], 'label': 'MCPExecutor', 'font': font_submodule},
    'cache': {'pos': (width/2 - 380, 400), 'width': 150, 'height': 30, 'color': colors['submodule'], 'label': 'MCPCacheManager', 'font': font_submodule},
    'currency': {'pos': (width/2 - 230, 400), 'width': 150, 'height': 30, 'color': colors['submodule'], 'label': 'CurrencyController', 'font': font_submodule},
    
    # 子模块 - 头脑风暴器
    'analyzer': {'pos': (width/2 + 230, 370), 'width': 150, 'height': 30, 'color': colors['submodule'], 'label': 'CapabilityAnalyzer', 'font': font_submodule},
    'converter': {'pos': (width/2 + 380, 370), 'width': 150, 'height': 30, 'color': colors['submodule'], 'label': 'MCPConverter', 'font': font_submodule},
    'enhancer': {'pos': (width/2 + 300, 400), 'width': 150, 'height': 30, 'color': colors['submodule'], 'label': 'SearchEnhancer', 'font': font_submodule},
    
    # 子模块 - 记录器
    'visual': {'pos': (width/2 - 520, 520), 'width': 180, 'height': 30, 'color': colors['submodule'], 'label': 'VisualThoughtRecorder', 'font': font_submodule},
    'enhanced': {'pos': (width/2 - 340, 520), 'width': 180, 'height': 30, 'color': colors['submodule'], 'label': 'EnhancedThoughtRecorder', 'font': font_submodule},
    
    # 子模块 - Release管理器
    'rules': {'pos': (width/2 - 150, 520), 'width': 180, 'height': 30, 'color': colors['submodule'], 'label': 'ReleaseRulesChecker', 'font': font_submodule},
    
    # 子模块 - 测试收集器
    'updater': {'pos': (width/2 + 150, 520), 'width': 180, 'height': 30, 'color': colors['submodule'], 'label': 'TestReadmeUpdater', 'font': font_submodule},
    
    # 子模块 - 问题解决器
    'manager': {'pos': (width/2 + 380, 520), 'width': 180, 'height': 30, 'color': colors['submodule'], 'label': 'SessionSavePointManager', 'font': font_submodule},
    'rollback': {'pos': (width/2 + 560, 520), 'width': 150, 'height': 30, 'color': colors['submodule'], 'label': 'RollbackExecutor', 'font': font_submodule},
}

# 绘制节点
for node_id, node in nodes.items():
    x, y = node['pos']
    width_node, height_node = node['width'], node['height']
    color = node['color']
    label = node['label']
    font = node['font']
    
    # 绘制矩形
    draw.rectangle([(x - width_node/2, y - height_node/2), (x + width_node/2, y + height_node/2)], 
                  fill=color, outline=(0, 0, 0))
    
    # 添加标签
    draw.text((x, y), label, fill=(0, 0, 0), font=font, anchor="mm")

# 定义连接线
connections = [
    # 中央协调器连接
    {'from': 'central', 'to': 'planner', 'color': (0, 0, 255), 'label': '协调'},
    {'from': 'central', 'to': 'brainstorm', 'color': (0, 0, 255), 'label': '协调'},
    
    # 智能体连接
    {'from': 'ppt_agent', 'to': 'central', 'color': (0, 128, 0), 'label': '调用'},
    {'from': 'web_agent', 'to': 'central', 'color': (0, 128, 0), 'label': '调用'},
    {'from': 'code_agent', 'to': 'central', 'color': (0, 128, 0), 'label': '调用'},
    {'from': 'general_agent', 'to': 'central', 'color': (0, 128, 0), 'label': '调用'},
    
    # 规划器连接
    {'from': 'planner', 'to': 'matcher', 'color': (0, 128, 0), 'label': '调用'},
    {'from': 'planner', 'to': 'executor', 'color': (0, 128, 0), 'label': '调用'},
    {'from': 'planner', 'to': 'cache', 'color': (0, 128, 0), 'label': '调用'},
    {'from': 'planner', 'to': 'currency', 'color': (0, 128, 0), 'label': '调用'},
    
    # 头脑风暴器连接
    {'from': 'brainstorm', 'to': 'analyzer', 'color': (0, 128, 0), 'label': '调用'},
    {'from': 'brainstorm', 'to': 'converter', 'color': (0, 128, 0), 'label': '调用'},
    {'from': 'brainstorm', 'to': 'enhancer', 'color': (0, 128, 0), 'label': '调用'},
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
    {'from': 'planner', 'to': 'recorder', 'color': (0, 128, 0), 'label': '调用'},
    {'from': 'planner', 'to': 'collector', 'color': (0, 128, 0), 'label': '调用'},
    
    # MCP增强模块连接
    {'from': 'sequential', 'to': 'enhanced_planner', 'color': (128, 0, 128), 'label': '增强'},
    {'from': 'playwright', 'to': 'enhanced_brainstorm', 'color': (128, 0, 128), 'label': '增强'},
    {'from': 'webagent', 'to': 'enhanced_brainstorm', 'color': (128, 0, 128), 'label': '增强'},
    {'from': 'sequential', 'to': 'problem_solver', 'color': (128, 0, 128), 'label': '增强'},
    {'from': 'webagent', 'to': 'problem_solver', 'color': (128, 0, 128), 'label': '增强'},
    
    # 增强模块到核心模块的连接
    {'from': 'enhanced_planner', 'to': 'planner', 'color': (255, 0, 0), 'label': '优化'},
    {'from': 'enhanced_brainstorm', 'to': 'brainstorm', 'color': (255, 0, 0), 'label': '优化'},
    {'from': 'problem_solver', 'to': 'solver', 'color': (255, 0, 0), 'label': '优化'},
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
    
    # 添加标签 - 使用白色背景确保可见性
    if conn['label']:
        mid_x = (from_x + to_x) / 2
        mid_y = (from_y + to_y) / 2
        
        # 计算文本大小
        text_width = len(conn['label']) * 10
        text_height = 20
        
        # 绘制白色背景
        draw.rectangle([(mid_x - text_width/2, mid_y - text_height/2), 
                        (mid_x + text_width/2, mid_y + text_height/2)], 
                      fill=(255, 255, 255), outline=(0, 0, 0))
        
        # 绘制文本
        draw.text((mid_x, mid_y), conn['label'], fill=(0, 0, 0), font=font_small, anchor="mm")

# 添加图例
legend_items = [
    {'color': colors['central'], 'label': '中央协调器'},
    {'color': colors['planner'], 'label': '规划器'},
    {'color': colors['brainstorm'], 'label': '头脑风暴器'},
    {'color': colors['agent'], 'label': '智能体'},
    {'color': colors['recorder'], 'label': '记录器'},
    {'color': colors['release'], 'label': 'Release管理器'},
    {'color': colors['collector'], 'label': '测试收集器'},
    {'color': colors['solver'], 'label': '问题解决器'},
    {'color': colors['tool'], 'label': 'MCP增强模块'},
    {'color': colors['external'], 'label': '外部系统'},
    {'color': colors['submodule'], 'label': '子模块'},
]

# 绘制图例
legend_x = 100
legend_y = 850
legend_width = 20
legend_height = 20
legend_spacing = 120  # 图例项之间的间距

for item in legend_items:
    # 绘制图例方块
    draw.rectangle([(legend_x, legend_y), (legend_x + legend_width, legend_y + legend_height)], 
                  fill=item['color'], outline=(0, 0, 0))
    # 绘制图例文字
    draw.text((legend_x + legend_width + 5, legend_y + legend_height/2), item['label'], 
              fill=(0, 0, 0), font=font_small, anchor="lm")
    
    # 更新下一个图例项的位置
    legend_x += legend_spacing
    if legend_x > width - 150:  # 换行
        legend_x = 100
        legend_y += 30

# 确保目录存在
os.makedirs('/home/ubuntu/powerautomation_integration/docs/images', exist_ok=True)

# 保存图像
output_path = '/home/ubuntu/powerautomation_integration/docs/images/powerautomation_complete_architecture.png'
image.save(output_path)

print(f"完整架构图已生成并保存到 {output_path}")
