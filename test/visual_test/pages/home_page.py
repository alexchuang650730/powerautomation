"""
端到端视觉自动化测试：页面对象模型
"""
class HomePage:
    """首页页面对象模型"""
    
    def __init__(self, page):
        self.page = page
        self.url = "/"
        self.agent_cards = page.locator(".agent-card")
        self.code_agent_card = page.locator("text=代码智能体")
        self.ppt_agent_card = page.locator("text=PPT智能体")
        self.web_agent_card = page.locator("text=网页智能体")
        self.general_agent_card = page.locator("text=通用智能体")
        self.input_field = page.locator("textarea[placeholder='请输入您的需求...']")
        self.send_button = page.locator("button.send-button")
        self.response_content = page.locator(".response-content")
    
    def navigate(self):
        """导航到首页"""
        self.page.goto(self.url)
        self.page.wait_for_load_state("networkidle")
        return self
    
    def select_agent(self, agent_name):
        """选择智能体"""
        if agent_name == "代码":
            self.code_agent_card.click()
        elif agent_name == "PPT":
            self.ppt_agent_card.click()
        elif agent_name == "网页":
            self.web_agent_card.click()
        elif agent_name == "通用":
            self.general_agent_card.click()
        else:
            raise ValueError(f"未知的智能体名称: {agent_name}")
        return self
    
    def send_query(self, query):
        """发送查询"""
        self.input_field.fill(query)
        self.send_button.click()
        return self
    
    def wait_for_response(self, timeout=30000):
        """等待响应"""
        self.response_content.wait_for(state="visible", timeout=timeout)
        return self.response_content.inner_text()
    
    def take_screenshot(self, path):
        """截取屏幕截图"""
        self.page.screenshot(path=path)
        return self
