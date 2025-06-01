"""
智能体六大特性定义模块

负责定义和管理四个智能体（PPT、网页、代码、通用）的六大特性
"""

class AgentFeatures:
    """智能体六大特性基类"""
    
    def __init__(self, agent_type):
        """初始化智能体六大特性
        
        Args:
            agent_type: 智能体类型，可选值：'ppt_agent', 'web_agent', 'code_agent', 'general_agent'
        """
        self.agent_type = agent_type
        self._features = {
            'platform_feature': '',  # 特性1: PowerAutomation自动化平台功能
            'ui_layout': '',         # 特性2: UI布局
            'prompt': '',            # 特性3: 提示词
            'thinking': '',          # 特性4: 思维
            'content': '',           # 特性5: 内容
            'memory': ''             # 特性6: 记忆长度
        }
        self._initialize_features()
    
    def _initialize_features(self):
        """初始化默认特性值"""
        self._features['platform_feature'] = f"{self.agent_type}的PowerAutomation自动化平台功能"
        self._features['ui_layout'] = f"{self.agent_type}的两栏布局设计"
        self._features['prompt'] = f"{self.agent_type}的提示词处理"
        self._features['thinking'] = f"{self.agent_type}的思考过程"
        self._features['content'] = f"{self.agent_type}的内容生成"
        self._features['memory'] = f"{self.agent_type}的无限上下文记忆"
    
    def get_feature(self, feature_name):
        """获取特性值
        
        Args:
            feature_name: 特性名称
            
        Returns:
            特性值
        """
        return self._features.get(feature_name, '')
    
    def set_feature(self, feature_name, value):
        """设置特性值
        
        Args:
            feature_name: 特性名称
            value: 特性值
            
        Returns:
            是否设置成功
        """
        if feature_name in self._features:
            self._features[feature_name] = value
            return True
        return False
    
    def get_all_features(self):
        """获取所有特性
        
        Returns:
            所有特性的字典
        """
        return self._features.copy()
    
    def update_features(self, features_dict):
        """批量更新特性
        
        Args:
            features_dict: 特性字典
            
        Returns:
            更新的特性数量
        """
        count = 0
        for name, value in features_dict.items():
            if name in self._features:
                self._features[name] = value
                count += 1
        return count
    
    def to_dict(self):
        """转换为字典
        
        Returns:
            特性字典
        """
        return {
            'agent_type': self.agent_type,
            'features': self.get_all_features()
        }
    
    @classmethod
    def from_dict(cls, data):
        """从字典创建实例
        
        Args:
            data: 特性字典
            
        Returns:
            AgentFeatures实例
        """
        instance = cls(data.get('agent_type', 'unknown'))
        features = data.get('features', {})
        instance.update_features(features)
        return instance


class PPTAgentFeatures(AgentFeatures):
    """PPT智能体六大特性"""
    
    def __init__(self):
        """初始化PPT智能体六大特性"""
        super().__init__('ppt_agent')
        self._initialize_ppt_features()
    
    def _initialize_ppt_features(self):
        """初始化PPT智能体特有特性"""
        self._features['platform_feature'] = "PPT智能体的PowerAutomation自动化平台功能：智能体选择与后端通信，实现了智能体选择逻辑，创建了API接口封装"
        self._features['ui_layout'] = "PPT智能体的两栏布局设计：左侧为Sidebar导航栏，右侧为主内容区，包含Header、智能体卡片、输入区和案例展示"
        self._features['prompt'] = "PPT智能体的提示词处理：分析用户输入，提取PPT相关需求和参数"
        self._features['thinking'] = "PPT智能体的思考过程：分析PPT结构、内容组织和视觉设计，生成最佳演示方案"
        self._features['content'] = "PPT智能体的内容生成：创建专业、美观的演示文稿，包含合理的结构、清晰的逻辑和吸引人的视觉效果"
        self._features['memory'] = "PPT智能体的无限上下文记忆：记录用户偏好、历史交互和设计风格，确保连贯一致的演示体验"


class WebAgentFeatures(AgentFeatures):
    """网页智能体六大特性"""
    
    def __init__(self):
        """初始化网页智能体六大特性"""
        super().__init__('web_agent')
        self._initialize_web_features()
    
    def _initialize_web_features(self):
        """初始化网页智能体特有特性"""
        self._features['platform_feature'] = "网页智能体的PowerAutomation自动化平台功能：智能体选择与后端通信，实现了智能体选择逻辑，创建了API接口封装"
        self._features['ui_layout'] = "网页智能体的两栏布局设计：左侧为Sidebar导航栏，右侧为主内容区，包含Header、智能体卡片、输入区和案例展示"
        self._features['prompt'] = "网页智能体的提示词处理：分析用户输入，提取网页设计和开发相关需求"
        self._features['thinking'] = "网页智能体的思考过程：分析网页结构、交互逻辑和视觉设计，生成最佳网页方案"
        self._features['content'] = "网页智能体的内容生成：创建响应式、美观、功能完善的网页，包含合理的结构、清晰的导航和优秀的用户体验"
        self._features['memory'] = "网页智能体的无限上下文记忆：记录用户偏好、历史交互和设计风格，确保连贯一致的网页开发体验"


class CodeAgentFeatures(AgentFeatures):
    """代码智能体六大特性"""
    
    def __init__(self):
        """初始化代码智能体六大特性"""
        super().__init__('code_agent')
        self._initialize_code_features()
    
    def _initialize_code_features(self):
        """初始化代码智能体特有特性"""
        self._features['platform_feature'] = "代码智能体的PowerAutomation自动化平台功能：智能体选择与后端通信，实现了智能体选择逻辑，创建了API接口封装"
        self._features['ui_layout'] = "代码智能体的两栏布局设计：左侧为Sidebar导航栏，右侧为主内容区，包含Header、智能体卡片、输入区和案例展示"
        self._features['prompt'] = "代码智能体的提示词处理：分析用户输入，提取编程需求、语言偏好和功能要求"
        self._features['thinking'] = "代码智能体的思考过程：分析问题、设计算法、选择数据结构，生成最佳代码方案"
        self._features['content'] = "代码智能体的内容生成：创建高质量、可维护的代码，包含清晰的注释、合理的结构和优秀的性能"
        self._features['memory'] = "代码智能体的无限上下文记忆：记录用户编程风格、历史交互和代码片段，确保连贯一致的编程体验"


class GeneralAgentFeatures(AgentFeatures):
    """通用智能体六大特性"""
    
    def __init__(self):
        """初始化通用智能体六大特性"""
        super().__init__('general_agent')
        self._initialize_general_features()
    
    def _initialize_general_features(self):
        """初始化通用智能体特有特性"""
        self._features['platform_feature'] = "通用智能体的PowerAutomation自动化平台功能：智能体选择与后端通信，实现了智能体选择逻辑，创建了API接口封装"
        self._features['ui_layout'] = "通用智能体的两栏布局设计：左侧为Sidebar导航栏，右侧为主内容区，包含Header、智能体卡片、输入区和案例展示"
        self._features['prompt'] = "通用智能体的提示词处理：分析用户输入，提取核心需求和意图"
        self._features['thinking'] = "通用智能体的思考过程：全面分析问题，综合考虑多种解决方案，选择最佳路径"
        self._features['content'] = "通用智能体的内容生成：创建全面、准确、有价值的回应，满足用户多样化需求"
        self._features['memory'] = "通用智能体的无限上下文记忆：记录用户偏好、历史交互和关键信息，确保连贯一致的对话体验"


def create_agent_features(agent_type):
    """创建智能体六大特性实例
    
    Args:
        agent_type: 智能体类型
        
    Returns:
        AgentFeatures实例
    """
    if agent_type == 'ppt_agent':
        return PPTAgentFeatures()
    elif agent_type == 'web_agent':
        return WebAgentFeatures()
    elif agent_type == 'code_agent':
        return CodeAgentFeatures()
    elif agent_type == 'general_agent':
        return GeneralAgentFeatures()
    else:
        return AgentFeatures(agent_type)


def get_agent_features(agent_type):
    """获取智能体六大特性
    
    Args:
        agent_type: 智能体类型
        
    Returns:
        特性字典
    """
    features = create_agent_features(agent_type)
    return features.get_all_features()


def update_agent_features(agent_type, features_dict):
    """更新智能体六大特性
    
    Args:
        agent_type: 智能体类型
        features_dict: 特性字典
        
    Returns:
        更新结果
    """
    features = create_agent_features(agent_type)
    count = features.update_features(features_dict)
    return {
        'agent_type': agent_type,
        'updated_count': count,
        'features': features.get_all_features()
    }
