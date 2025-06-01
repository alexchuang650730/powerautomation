"""
代码智能体六大特性定义文档
更新日期：2025-06-01
"""

class CodeAgentFeatures:
    """
    代码智能体六大特性定义类
    包含平台特性、UI布局特性、提示词特性、思维特性、内容特性和记忆特性
    """
    
    def __init__(self):
        """初始化代码智能体六大特性"""
        # 初始化六大特性
        self.platform_features = self._init_platform_features()
        self.ui_layout_features = self._init_ui_layout_features()
        self.prompt_features = self._init_prompt_features()
        self.thinking_features = self._init_thinking_features()
        self.content_features = self._init_content_features()
        self.memory_features = self._init_memory_features()
    
    def _init_platform_features(self):
        """初始化平台特性"""
        return {
            "ide_integration": {
                "name": "IDE集成能力",
                "description": "支持与主流IDE（VSCode、IntelliJ等）的无缝集成",
                "enabled": True,
                "config": {
                    "vscode_extension": True,
                    "intellij_plugin": True,
                    "eclipse_plugin": True
                }
            },
            "version_control_support": {
                "name": "版本控制支持",
                "description": "与Git、SVN等版本控制系统集成，支持代码提交、分支管理等操作",
                "enabled": True,
                "config": {
                    "git_support": True,
                    "svn_support": True,
                    "branch_management": True
                }
            },
            "build_system_integration": {
                "name": "构建系统集成",
                "description": "支持Maven、Gradle、npm等构建系统，自动处理依赖和构建流程",
                "enabled": True,
                "config": {
                    "maven_support": True,
                    "gradle_support": True,
                    "npm_support": True
                }
            }
        }
    
    def _init_ui_layout_features(self):
        """初始化UI布局特性"""
        return {
            "two_column_layout": {
                "name": "两栏式布局",
                "description": "左侧展示任务进度和ThoughtActionRecorder思考过程，右侧展示代码和画面回放",
                "enabled": True,
                "config": {
                    "left_column_width_percentage": 40,
                    "right_column_width_percentage": 60,
                    "min_column_width": 300
                }
            },
            "task_progress_display": {
                "name": "任务进度展示",
                "description": "可视化展示当前任务进度、已完成步骤和待完成步骤",
                "enabled": True,
                "config": {
                    "progress_bar": True,
                    "step_indicators": True,
                    "completion_percentage": True
                }
            },
            "code_playback": {
                "name": "代码回放",
                "description": "支持代码生成过程的回放，展示思考和编写过程",
                "enabled": True,
                "config": {
                    "playback_speed_control": True,
                    "step_by_step_mode": True,
                    "annotation_display": True
                }
            },
            "code_editor_integration": {
                "name": "代码编辑器集成",
                "description": "内置代码编辑器，支持语法高亮、自动补全和错误提示",
                "enabled": True,
                "config": {
                    "syntax_highlighting": True,
                    "auto_completion": True,
                    "error_highlighting": True,
                    "code_folding": True
                }
            }
        }
    
    def _init_prompt_features(self):
        """初始化提示词特性"""
        return {
            "code_intent_recognition": {
                "name": "代码意图识别",
                "description": "准确理解用户的编程需求和意图",
                "enabled": True,
                "config": {
                    "natural_language_parsing": True,
                    "technical_requirement_extraction": True,
                    "ambiguity_resolution": True
                }
            },
            "language_specific_prompting": {
                "name": "特定语言提示",
                "description": "根据目标编程语言调整提示策略",
                "enabled": True,
                "config": {
                    "supported_languages": ["python", "javascript", "java", "c++", "go"],
                    "language_idiom_awareness": True,
                    "best_practice_suggestions": True
                }
            },
            "architecture_guidance": {
                "name": "架构引导",
                "description": "提供架构级别的指导和建议",
                "enabled": True,
                "config": {
                    "design_pattern_suggestions": True,
                    "scalability_considerations": True,
                    "maintainability_focus": True
                }
            }
        }
    
    def _init_thinking_features(self):
        """初始化思维特性"""
        return {
            "algorithm_selection": {
                "name": "算法选择",
                "description": "根据问题特性选择最适合的算法",
                "enabled": True,
                "config": {
                    "complexity_analysis": True,
                    "performance_optimization": True,
                    "space_time_tradeoff": True
                }
            },
            "code_structure_planning": {
                "name": "代码结构规划",
                "description": "设计清晰、模块化的代码结构",
                "enabled": True,
                "config": {
                    "module_organization": True,
                    "interface_design": True,
                    "dependency_management": True
                }
            },
            "edge_case_consideration": {
                "name": "边缘情况考虑",
                "description": "全面考虑各种边缘情况和异常处理",
                "enabled": True,
                "config": {
                    "input_validation": True,
                    "error_handling": True,
                    "boundary_condition_testing": True
                }
            },
            "refactoring_analysis": {
                "name": "重构分析",
                "description": "识别代码中的改进机会并提供重构建议",
                "enabled": True,
                "config": {
                    "code_smell_detection": True,
                    "technical_debt_assessment": True,
                    "refactoring_suggestion": True
                }
            }
        }
    
    def _init_content_features(self):
        """初始化内容特性"""
        return {
            "clean_code_generation": {
                "name": "清晰代码生成",
                "description": "生成符合最佳实践的清晰、可维护代码",
                "enabled": True,
                "config": {
                    "naming_convention_adherence": True,
                    "consistent_formatting": True,
                    "code_simplicity": True
                }
            },
            "documentation_generation": {
                "name": "文档生成",
                "description": "自动生成代码文档、注释和使用说明",
                "enabled": True,
                "config": {
                    "inline_comments": True,
                    "api_documentation": True,
                    "usage_examples": True
                }
            },
            "test_case_creation": {
                "name": "测试用例创建",
                "description": "为代码生成全面的单元测试和集成测试",
                "enabled": True,
                "config": {
                    "unit_test_coverage": True,
                    "integration_test_scenarios": True,
                    "test_data_generation": True
                }
            },
            "performance_optimization": {
                "name": "性能优化",
                "description": "识别并解决性能瓶颈，提供优化建议",
                "enabled": True,
                "config": {
                    "hotspot_identification": True,
                    "optimization_suggestions": True,
                    "benchmark_comparison": True
                }
            }
        }
    
    def _init_memory_features(self):
        """初始化记忆特性"""
        return {
            "codebase_understanding": {
                "name": "代码库理解",
                "description": "全面理解和记忆项目代码库的结构和关系",
                "enabled": True,
                "config": {
                    "dependency_graph_building": True,
                    "class_hierarchy_tracking": True,
                    "api_usage_patterns": True
                }
            },
            "coding_style_adaptation": {
                "name": "编码风格适应",
                "description": "记忆并适应用户的编码风格和偏好",
                "enabled": True,
                "config": {
                    "style_pattern_recognition": True,
                    "consistency_enforcement": True,
                    "personalization_level": "high"
                }
            },
            "solution_reuse": {
                "name": "解决方案复用",
                "description": "记录并复用成功的代码解决方案",
                "enabled": True,
                "config": {
                    "solution_cataloging": True,
                    "context_based_retrieval": True,
                    "adaptation_to_new_contexts": True
                }
            },
            "project_history_tracking": {
                "name": "项目历史追踪",
                "description": "记录项目演变历史，理解代码变更原因",
                "enabled": True,
                "config": {
                    "commit_history_analysis": True,
                    "change_pattern_recognition": True,
                    "developer_intent_inference": True
                }
            }
        }
    
    def get_all_features(self):
        """获取所有特性"""
        return {
            "platform_features": self.platform_features,
            "ui_layout_features": self.ui_layout_features,
            "prompt_features": self.prompt_features,
            "thinking_features": self.thinking_features,
            "content_features": self.content_features,
            "memory_features": self.memory_features
        }
    
    def update_feature(self, category, feature_id, updates):
        """更新特定特性的配置"""
        if category not in self.__dict__:
            raise ValueError(f"特性类别 '{category}' 不存在")
        
        category_dict = self.__dict__[category]
        if feature_id not in category_dict:
            raise ValueError(f"特性 '{feature_id}' 在类别 '{category}' 中不存在")
        
        # 更新特性配置
        for key, value in updates.items():
            if key in category_dict[feature_id]:
                category_dict[feature_id][key] = value
            elif key == "config" and isinstance(value, dict):
                # 递归更新配置字典
                self._update_config_dict(category_dict[feature_id]["config"], value)
            else:
                category_dict[feature_id][key] = value
    
    def _update_config_dict(self, current_config, new_config):
        """递归更新配置字典"""
        for key, value in new_config.items():
            if key in current_config and isinstance(current_config[key], dict) and isinstance(value, dict):
                self._update_config_dict(current_config[key], value)
            else:
                current_config[key] = value
    
    def to_dict(self):
        """将特性转换为字典格式"""
        return {
            "platform_features": self.platform_features,
            "ui_layout_features": self.ui_layout_features,
            "prompt_features": self.prompt_features,
            "thinking_features": self.thinking_features,
            "content_features": self.content_features,
            "memory_features": self.memory_features
        }
    
    def to_json(self):
        """将特性转换为JSON格式"""
        import json
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)
    
    def save_to_file(self, filepath):
        """将特性保存到文件"""
        import json
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, ensure_ascii=False, indent=2)
    
    @classmethod
    def load_from_file(cls, filepath):
        """从文件加载特性"""
        import json
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        instance = cls()
        for category, features in data.items():
            if category in instance.__dict__:
                instance.__dict__[category] = features
        
        return instance


# 使用示例
if __name__ == "__main__":
    # 创建代码智能体六大特性实例
    features = CodeAgentFeatures()
    
    # 保存到文件
    features.save_to_file("code_agent_features.json")
    
    # 更新特性示例
    features.update_feature("ui_layout_features", "two_column_layout", {
        "config": {
            "left_column_width_percentage": 35,
            "right_column_width_percentage": 65
        }
    })
    
    # 输出更新后的特性
    print(features.to_json())
