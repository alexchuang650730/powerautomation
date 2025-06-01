from PIL import Image, ImageDraw, ImageFont
import os

# 创建保存目录
os.makedirs("images", exist_ok=True)

# 设置画布大小和颜色
width, height = 1200, 1600
image = Image.new("RGB", (width, height), "white")
draw = ImageDraw.Draw(image)

# 尝试加载字体，如果失败则使用默认字体
try:
    title_font = ImageFont.truetype("DejaVuSans-Bold.ttf", 36)
    header_font = ImageFont.truetype("DejaVuSans-Bold.ttf", 28)
    normal_font = ImageFont.truetype("DejaVuSans.ttf", 22)
    small_font = ImageFont.truetype("DejaVuSans.ttf", 18)
except IOError:
    title_font = ImageFont.load_default()
    header_font = ImageFont.load_default()
    normal_font = ImageFont.load_default()
    small_font = ImageFont.load_default()

# 定义颜色
colors = {
    "agent_blue": (65, 105, 225),      # 深蓝色
    "mcp_core_blue": (100, 149, 237),  # 浅蓝色
    "mcp_enhancer_green": (144, 238, 144),  # 浅绿色
    "external_adapter_coral": (255, 127, 80),  # 珊瑚色
    "dev_tools_gold": (255, 215, 0),   # 金色
    "rl_factory_teal": (0, 128, 128),  # 蓝绿色
    "key_modules_purple": (147, 112, 219),  # 紫色
    "base_repo_gray": (169, 169, 169), # 灰色
    "text_black": (0, 0, 0),           # 黑色
    "line_gray": (128, 128, 128),      # 灰色
    "box_border": (100, 100, 100),     # 深灰色
    "background": (255, 255, 255)      # 白色
}

# 绘制标题
draw.text((width//2, 50), "PowerAutomation 分层架构图", fill=colors["text_black"], font=title_font, anchor="mm")

# 定义各层的位置和大小
layer_height = 120
layer_width = 800
layer_margin = 40
layer_start_y = 150
layer_x = width // 2 - layer_width // 2

# 绘制各层
layers = [
    {"name": "智能体层 (Agents)", "color": colors["agent_blue"], "components": [
        "PPT智能体", "网页智能体", "代码智能体", "通用智能体"
    ]},
    {"name": "MCP核心组件层", "color": colors["mcp_core_blue"], "components": [
        "MCP中央协调器", "MCP规划器", "MCP头脑风暴器"
    ]},
    {"name": "MCP增强组件层", "color": colors["mcp_enhancer_green"], "components": [
        "Sequential Thinking适配器", "Playwright适配器", "WebAgent增强适配器",
        "增强版MCP规划器", "增强版MCP头脑风暴器", "主动问题解决器", "RL增强器"
    ]},
    {"name": "外部工具适配器层", "color": colors["external_adapter_coral"], "components": [
        "无限上下文适配器", "MCP.so适配器", "GitHub Actions适配器", "ACI.dev适配器", "WebUI工具构建器"
    ]},
    {"name": "开发工具层 (Dev Tools)", "color": colors["dev_tools_gold"], "components": [
        "思考与操作记录器", "Agent问题解决驱动器", "Release Manager", "GitHub Actions"
    ]},
    {"name": "RL-Factory层", "color": colors["rl_factory_teal"], "components": [
        "思考过程结构化", "混合学习架构", "多层次奖励机制", "能力迁移"
    ]},
    {"name": "关键模块层 (Key Modules)", "color": colors["key_modules_purple"], "components": [
        "工具使用 (Tool Use)", "RL训练 (RL-Training)", "Web界面 (WebUI)"
    ]},
    {"name": "基础仓库层 (Base Repository)", "color": colors["base_repo_gray"], "components": [
        "PeterGriffinJin/Search-R1", "volcengine/veRL", "QwenLM/Qwen-Agent"
    ]}
]

# 绘制层和组件
for i, layer in enumerate(layers):
    y = layer_start_y + i * (layer_height + layer_margin)
    
    # 绘制层背景
    draw.rectangle([(layer_x, y), (layer_x + layer_width, y + layer_height)], 
                  fill=layer["color"], outline=colors["box_border"], width=2)
    
    # 绘制层名称
    draw.text((layer_x + 20, y + 20), layer["name"], 
              fill=colors["text_black"], font=header_font)
    
    # 绘制组件
    components_text = ", ".join(layer["components"])
    # 文本换行处理
    max_width = layer_width - 40
    lines = []
    current_line = ""
    for word in components_text.split(", "):
        test_line = current_line + word + ", " if current_line else word + ", "
        text_width = draw.textlength(test_line, font=normal_font)
        if text_width <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word + ", "
    if current_line:
        lines.append(current_line)
    
    # 绘制组件文本
    for j, line in enumerate(lines):
        draw.text((layer_x + 20, y + 60 + j * 30), line, 
                  fill=colors["text_black"], font=normal_font)

# 绘制连接线和标签
for i in range(len(layers) - 1):
    start_y = layer_start_y + i * (layer_height + layer_margin) + layer_height
    end_y = start_y + layer_margin
    
    # 绘制连接线
    mid_x = layer_x + layer_width // 2
    draw.line([(mid_x, start_y), (mid_x, end_y)], 
              fill=colors["line_gray"], width=3)
    
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
    text_width = draw.textlength(label, font=small_font)
    text_height = small_font.size
    text_bg_x = mid_x - text_width // 2 - 5
    text_bg_y = start_y + (end_y - start_y) // 2 - text_height // 2 - 5
    draw.rectangle([(text_bg_x, text_bg_y), 
                   (text_bg_x + text_width + 10, text_bg_y + text_height + 10)], 
                  fill=colors["background"])
    
    # 绘制标签文本
    draw.text((mid_x, start_y + (end_y - start_y) // 2), 
              label, fill=colors["text_black"], font=small_font, anchor="mm")

# 添加横向功能分组
feature_start_x = 50
feature_width = 300
feature_height = 400
feature_y = layer_start_y + 2 * (layer_height + layer_margin)

# 现有功能
draw.rectangle([(feature_start_x, feature_y), 
               (feature_start_x + feature_width, feature_y + feature_height)], 
              outline=colors["box_border"], width=2)
draw.text((feature_start_x + feature_width // 2, feature_y + 30), 
          "现有功能 (Existing Features)", 
          fill=colors["text_black"], font=header_font, anchor="mm")

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
    draw.text((feature_start_x + 20, feature_y + 70 + i * 30), 
              line, fill=colors["text_black"], font=small_font)

# 未来功能
future_start_x = width - feature_start_x - feature_width
draw.rectangle([(future_start_x, feature_y), 
               (future_start_x + feature_width, feature_y + feature_height)], 
              outline=colors["box_border"], width=2)
draw.text((future_start_x + feature_width // 2, feature_y + 30), 
          "未来功能 (Upcoming Features)", 
          fill=colors["text_black"], font=header_font, anchor="mm")

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
    draw.text((future_start_x + 20, feature_y + 70 + i * 25), 
              line, fill=colors["text_black"], font=small_font)

# 保存图像
output_path = "images/powerautomation_layered_architecture_updated.png"
image.save(output_path)
print(f"架构图已保存到 {output_path}")
