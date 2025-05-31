from PIL import Image, ImageDraw, ImageFont
import os

# 创建保存目录
os.makedirs('/home/ubuntu/powerautomation_integration/docs/images', exist_ok=True)

# 设置图像尺寸和背景
width, height = 1600, 1800
image = Image.new('RGB', (width, height), color='white')
draw = ImageDraw.Draw(image)

# 尝试加载字体，如果失败则使用默认字体
try:
    title_font = ImageFont.truetype("Arial", 36)
    header_font = ImageFont.truetype("Arial", 28)
    normal_font = ImageFont.truetype("Arial", 22)
    small_font = ImageFont.truetype("Arial", 18)
except IOError:
    # 使用默认字体
    title_font = ImageFont.load_default()
    header_font = ImageFont.load_default()
    normal_font = ImageFont.load_default()
    small_font = ImageFont.load_default()

# 定义颜色
colors = {
    'agent_blue': (70, 130, 220),
    'core_green': (100, 180, 100),
    'enhancer_green': (120, 200, 120),
    'tool_adapter_orange': (240, 130, 80),
    'dev_tools_yellow': (240, 200, 80),
    'github_purple': (180, 120, 240),
    'rl_factory_blue': (60, 120, 190),
    'key_module_gray': (200, 200, 200),
    'feature_box_light': (240, 240, 240),
    'arrow': (80, 80, 80),
    'text': (0, 0, 0),
    'highlight': (255, 100, 100)
}

# 绘制标题
draw.text((width//2, 50), "PowerAutomation 分层架构图", fill=colors['text'], font=title_font, anchor="mm")

# 定义层级和位置
layers = [
    {"name": "智能体层 (Agents)", "y": 200, "color": colors['agent_blue'], "height": 100},
    {"name": "MCP核心组件层", "y": 400, "color": colors['core_green'], "height": 100},
    {"name": "MCP增强组件层", "y": 600, "color": colors['enhancer_green'], "height": 100},
    {"name": "外部工具适配器层", "y": 800, "color": colors['tool_adapter_orange'], "height": 100},
    {"name": "开发工具层 (Dev Tools)", "y": 1000, "color": colors['dev_tools_yellow'], "height": 100},
    {"name": "RL-Factory层", "y": 1200, "color": colors['rl_factory_blue'], "height": 100},
    {"name": "关键模块层 (Key Modules)", "y": 1400, "color": colors['key_module_gray'], "height": 100},
    {"name": "基础仓库层 (Base Repository)", "y": 1600, "color": colors['github_purple'], "height": 100}
]

# 绘制层级框和标题
for layer in layers:
    # 绘制层级框
    draw.rectangle([(200, layer["y"]), (width-200, layer["y"]+layer["height"])], 
                  fill=layer["color"], outline=(0, 0, 0))
    
    # 绘制层级名称
    draw.text((220, layer["y"]+layer["height"]//2), layer["name"], 
              fill=colors['text'], font=header_font, anchor="lm")

# 绘制智能体层的组件
agents = [
    {"name": "PPT智能体", "x": 500, "width": 180},
    {"name": "网页智能体", "x": 700, "width": 180},
    {"name": "代码智能体", "x": 900, "width": 180},
    {"name": "通用智能体", "x": 1100, "width": 180}
]

for agent in agents:
    y = layers[0]["y"] + 20
    draw.rectangle([(agent["x"], y), (agent["x"]+agent["width"], y+60)], 
                  fill=colors['feature_box_light'], outline=(0, 0, 0))
    draw.text((agent["x"]+agent["width"]//2, y+30), agent["name"], 
              fill=colors['text'], font=normal_font, anchor="mm")

# 绘制MCP核心组件层的组件
core_components = [
    {"name": "MCP中央协调器", "x": 500, "width": 200},
    {"name": "MCP规划器", "x": 720, "width": 180},
    {"name": "MCP头脑风暴器", "x": 920, "width": 180},
    {"name": "mcp.so", "x": 1120, "width": 120}
]

for comp in core_components:
    y = layers[1]["y"] + 20
    draw.rectangle([(comp["x"], y), (comp["x"]+comp["width"], y+60)], 
                  fill=colors['feature_box_light'], outline=(0, 0, 0))
    draw.text((comp["x"]+comp["width"]//2, y+30), comp["name"], 
              fill=colors['text'], font=normal_font, anchor="mm")

# 绘制MCP增强组件层的组件
enhancers = [
    {"name": "Sequential Thinking适配器", "x": 400, "width": 240},
    {"name": "Playwright适配器", "x": 660, "width": 180},
    {"name": "WebAgentB增强适配器", "x": 860, "width": 200},
    {"name": "增强版MCP规划器", "x": 400, "width": 240, "y_offset": 70},
    {"name": "增强版MCP头脑风暴器", "x": 660, "width": 240, "y_offset": 70},
    {"name": "Agent问题解决驱动器", "x": 920, "width": 220, "y_offset": 70},
    {"name": "RL增强器", "x": 1160, "width": 140, "y_offset": 70}
]

for enhancer in enhancers:
    y_offset = enhancer.get("y_offset", 0)
    y = layers[2]["y"] + 15 + y_offset
    draw.rectangle([(enhancer["x"], y), (enhancer["x"]+enhancer["width"], y+40)], 
                  fill=colors['feature_box_light'], outline=(0, 0, 0))
    draw.text((enhancer["x"]+enhancer["width"]//2, y+20), enhancer["name"], 
              fill=colors['text'], font=small_font, anchor="mm")

# 绘制外部工具适配器层的组件
adapters = [
    {"name": "无限上下文适配器", "x": 500, "width": 200},
    {"name": "MCP.so适配器", "x": 720, "width": 180},
    {"name": "GitHub Actions适配器", "x": 920, "width": 200},
    {"name": "浏览器自动化适配器", "x": 1140, "width": 200}
]

for adapter in adapters:
    y = layers[3]["y"] + 20
    draw.rectangle([(adapter["x"], y), (adapter["x"]+adapter["width"], y+60)], 
                  fill=colors['feature_box_light'], outline=(0, 0, 0))
    draw.text((adapter["x"]+adapter["width"]//2, y+30), adapter["name"], 
              fill=colors['text'], font=normal_font, anchor="mm")

# 绘制开发工具层的组件
dev_tools = [
    {"name": "思考与操作记录器", "x": 500, "width": 200},
    {"name": "Agent问题解决驱动器", "x": 720, "width": 220},
    {"name": "Release管理器", "x": 960, "width": 180},
    {"name": "测试与问题收集器", "x": 1160, "width": 200}
]

for tool in dev_tools:
    y = layers[4]["y"] + 20
    draw.rectangle([(tool["x"], y), (tool["x"]+tool["width"], y+60)], 
                  fill=colors['feature_box_light'], outline=(0, 0, 0))
    draw.text((tool["x"]+tool["width"]//2, y+30), tool["name"], 
              fill=colors['text'], font=normal_font, anchor="mm")

# 绘制RL-Factory层的组件
rl_factory_components = [
    {"name": "思考过程结构化", "x": 500, "width": 180},
    {"name": "混合学习架构", "x": 700, "width": 180},
    {"name": "多层次奖励机制", "x": 900, "width": 180},
    {"name": "能力迁移模块", "x": 1100, "width": 180}
]

for comp in rl_factory_components:
    y = layers[5]["y"] + 20
    draw.rectangle([(comp["x"], y), (comp["x"]+comp["width"], y+60)], 
                  fill=colors['feature_box_light'], outline=(0, 0, 0))
    draw.text((comp["x"]+comp["width"]//2, y+30), comp["name"], 
              fill=colors['text'], font=normal_font, anchor="mm")

# 绘制关键模块层的组件
key_modules = [
    {"name": "工具使用 (Tool Use)", "x": 500, "width": 200},
    {"name": "RL训练 (RL-Training)", "x": 750, "width": 200},
    {"name": "Web界面 (WebUI)", "x": 1000, "width": 200}
]

for module in key_modules:
    y = layers[6]["y"] + 20
    draw.rectangle([(module["x"], y), (module["x"]+module["width"], y+60)], 
                  fill=colors['feature_box_light'], outline=(0, 0, 0))
    draw.text((module["x"]+module["width"]//2, y+30), module["name"], 
              fill=colors['text'], font=normal_font, anchor="mm")

# 绘制基础仓库层的组件
base_repos = [
    {"name": "PeterGriffinJn/Search-R1", "x": 450, "width": 250},
    {"name": "volcengine/veRL", "x": 750, "width": 200},
    {"name": "QwenLM/Qwen-Agent", "x": 1000, "width": 200}
]

for repo in base_repos:
    y = layers[7]["y"] + 20
    draw.rectangle([(repo["x"], y), (repo["x"]+repo["width"], y+60)], 
                  fill=colors['feature_box_light'], outline=(0, 0, 0))
    draw.text((repo["x"]+repo["width"]//2, y+30), repo["name"], 
              fill=colors['text'], font=small_font, anchor="mm")

# 绘制功能分组
feature_groups = [
    {"name": "效率 (Efficiency)", "x": 1350, "y": 200, "items": ["Async LLMEngine", "工具结果缓存", "高并发支持"]},
    {"name": "对话 (Conversation)", "x": 1350, "y": 300, "items": ["LLM对话模拟", "多智能体RL训练", "上下文管理"]},
    {"name": "工具池 (Tool Pool)", "x": 1350, "y": 400, "items": ["与ACI.dev集成", "WebUI工具构建", "工具版本管理"]},
    {"name": "性能 (Performance)", "x": 1350, "y": 500, "items": ["过程奖励训练", "新RL算法", "极限长上下文"]},
    {"name": "兼容性 (Compatibility)", "x": 1350, "y": 600, "items": ["更多模型支持", "多平台测试", "发布到PyPI"]},
    {"name": "接口 (Interface)", "x": 1350, "y": 700, "items": ["图形界面", "提示优化", "项目管理"]}
]

for group in feature_groups:
    # 绘制分组框
    draw.rectangle([(group["x"], group["y"]), (group["x"]+220, group["y"]+80)], 
                  fill=colors['feature_box_light'], outline=(0, 0, 0))
    
    # 绘制分组标题
    draw.text((group["x"]+110, group["y"]+20), group["name"], 
              fill=colors['text'], font=normal_font, anchor="mm")
    
    # 绘制分组项目
    for i, item in enumerate(group["items"]):
        draw.text((group["x"]+20, group["y"]+40+i*15), f"• {item}", 
                  fill=colors['text'], font=small_font)

# 绘制连接线
# 智能体层 -> MCP核心组件层
draw.line([(width//2, layers[0]["y"]+layers[0]["height"]), 
           (width//2, layers[1]["y"])], 
          fill=colors['arrow'], width=3)

# MCP核心组件层 -> MCP增强组件层
draw.line([(width//2, layers[1]["y"]+layers[1]["height"]), 
           (width//2, layers[2]["y"])], 
          fill=colors['arrow'], width=3)

# MCP增强组件层 -> 外部工具适配器层
draw.line([(width//2, layers[2]["y"]+layers[2]["height"]), 
           (width//2, layers[3]["y"])], 
          fill=colors['arrow'], width=3)

# MCP核心组件层 <-> 开发工具层
draw.line([(layers[1]["y"]+layers[1]["height"]//2, layers[1]["y"]+layers[1]["height"]//2), 
           (width-300, layers[1]["y"]+layers[1]["height"]//2),
           (width-300, layers[4]["y"]+layers[4]["height"]//2),
           (width-200, layers[4]["y"]+layers[4]["height"]//2)], 
          fill=colors['arrow'], width=3)

# RL-Factory层 -> 关键模块层
for x in [600, 800, 1000]:
    draw.line([(x, layers[5]["y"]+layers[5]["height"]), 
               (x, layers[6]["y"])], 
              fill=colors['arrow'], width=2)

# 关键模块层 -> 现有功能
draw.text((400, layers[6]["y"]-30), "现有功能 (Existing Features)", 
          fill=colors['text'], font=normal_font)

# 功能分组 -> 未来功能
draw.text((1350, 150), "未来功能 (Upcoming Features)", 
          fill=colors['text'], font=normal_font)

# 基础仓库层 -> RL-Factory层
for x in [550, 750, 1000]:
    draw.line([(x, layers[7]["y"]), 
               (x, layers[5]["y"]+layers[5]["height"])], 
              fill=colors['arrow'], width=2)

# 添加RL增强器与MCP增强组件的关系说明
draw.text((1160+70, layers[2]["y"]+15+70+50), "RL增强器集成", 
          fill=colors['highlight'], font=small_font, anchor="mm")
draw.line([(1160+70, layers[2]["y"]+15+70+40), 
           (1160+70, layers[5]["y"])], 
          fill=colors['highlight'], width=2)

# 添加GitHub Actions与Release Manager的关系说明
draw.line([(920+100, layers[3]["y"]+60), 
           (920+100, layers[3]["y"]+80),
           (960+90, layers[3]["y"]+80),
           (960+90, layers[4]["y"])], 
          fill=colors['highlight'], width=2)
draw.text((960+90, layers[3]["y"]+90), "CI/CD集成", 
          fill=colors['highlight'], font=small_font, anchor="mm")

# 保存图像
image.save('/home/ubuntu/powerautomation_integration/docs/images/powerautomation_layered_architecture.png')
print("分层架构图已保存到 /home/ubuntu/powerautomation_integration/docs/images/powerautomation_layered_architecture.png")
