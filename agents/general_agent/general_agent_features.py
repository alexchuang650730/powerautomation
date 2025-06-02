"""
通用智能体六大特性定义文档
更新日期：2025-06-02
版本：1.3

核心治理原则：所有功能扩展将严格基于原本的文件结构进行，不会更改现有结构
"""

# 单例模式实现
_instance = None

def get_instance():
    """
    获取GeneralAgentFeatures单例实例
    
    Returns:
        GeneralAgentFeatures: 通用智能体六大特性定义类的单例实例
    """
    global _instance
    if _instance is None:
        _instance = GeneralAgentFeatures()
    return _instance

class GeneralAgentFeatures:
    """
    通用智能体六大特性定义类
    包含平台特性、UI布局特性、提示词特性、思维特性、内容特性和记忆特性
    
    核心治理原则：
    1. 结构保护原则：所有功能扩展将严格基于原本的文件结构进行，不会更改现有结构
    2. 兼容性原则：新增功能必须与现有功能保持向后兼容
    3. 空间利用原则：UI扩展只在空白区域进行，不影响原有控件和布局
    4. 模块化原则：新功能作为独立模块添加，不修改现有代码逻辑
    5. 一致性原则：保持与现有代码风格和架构的一致性
    """
    
    def __init__(self):
        """初始化通用智能体六大特性"""
        # 初始化六大特性
        self.platform_features = self._init_platform_features()
        self.ui_layout_features = self._init_ui_layout_features()
        self.prompt_features = self._init_prompt_features()
        self.thinking_features = self._init_thinking_features()
        self.content_features = self._init_content_features()
        self.memory_features = self._init_memory_features()
        
        # 核心治理原则
        self.governance_principles = {
            "structure_preservation": {
                "name": "结构保护原则",
                "description": "所有功能扩展将严格基于原本的文件结构进行，不会更改现有结构",
                "enabled": True,
                "config": {
                    "enforce_in_development": True,
                    "enforce_in_deployment": True,
                    "enforce_in_testing": True,
                    "validation_required": True
                }
            },
            "backward_compatibility": {
                "name": "兼容性原则",
                "description": "新增功能必须与现有功能保持向后兼容，确保系统稳定性",
                "enabled": True,
                "config": {
                    "compatibility_testing": True,
                    "legacy_support": True,
                    "version_control": True,
                    "migration_path_required": True
                }
            },
            "space_utilization": {
                "name": "空间利用原则",
                "description": "UI扩展只在空白区域进行，不影响原有控件和布局",
                "enabled": True,
                "config": {
                    "layout_preservation": True,
                    "component_isolation": True,
                    "responsive_adaptation": True,
                    "visual_harmony": True
                }
            },
            "modularity": {
                "name": "模块化原则",
                "description": "新功能作为独立模块添加，不修改现有代码逻辑",
                "enabled": True,
                "config": {
                    "component_encapsulation": True,
                    "interface_based_integration": True,
                    "dependency_injection": True,
                    "plugin_architecture": True
                }
            },
            "consistency": {
                "name": "一致性原则",
                "description": "保持与现有代码风格和架构的一致性",
                "enabled": True,
                "config": {
                    "style_guide_compliance": True,
                    "naming_convention_adherence": True,
                    "architectural_pattern_alignment": True,
                    "documentation_standards": True
                }
            }
        }
    
    def get_core_capabilities(self):
        """
        获取核心能力列表
        
        Returns:
            List[str]: 核心能力列表
        """
        return [
            "automated_testing",
            "version_rollback",
            "agent_manufacturing",
            "structure_based_extension",
            "integrated_workflow_management",
            "unified_interface_experience"
        ]
    
    def get_ui_features(self):
        """
        获取UI布局特性列表
        
        Returns:
            List[str]: UI布局特性列表
        """
        return [
            "two_column_layout",
            "responsive_design",
            "theme_customization",
            "agent_card_layout",
            "work_node_visualizer",
            "n8n_style_workflow_visualization",
            "integrated_input_area",
            "unified_work_node_workflow_view",
            "message_history_display"
        ]
    
    def get_memory_features(self):
        """
        获取记忆特性列表
        
        Returns:
            List[str]: 记忆特性列表
        """
        return [
            "checkpoint_management",
            "historical_data_analysis",
            "knowledge_graph_integration",
            "context_persistence",
            "workflow_state_persistence",
            "message_history_management"
        ]
    
    def _init_platform_features(self):
        """初始化平台特性"""
        return {
            "multi_platform_integration": {
                "name": "多平台集成能力",
                "description": "支持与GitHub、CI/CD平台、本地开发环境的无缝集成",
                "enabled": True,
                "config": {
                    "github_integration": True,
                    "cicd_integration": True,
                    "local_dev_integration": True
                }
            },
            "cross_environment_compatibility": {
                "name": "跨环境兼容性",
                "description": "在Windows、macOS和Linux环境下保持一致的功能表现",
                "enabled": True,
                "config": {
                    "windows_support": True,
                    "macos_support": True,
                    "linux_support": True
                }
            },
            "api_standardization": {
                "name": "API接口标准化",
                "description": "提供统一的REST API接口，支持第三方系统调用",
                "enabled": True,
                "config": {
                    "rest_api_enabled": True,
                    "swagger_docs": True,
                    "rate_limiting": True
                }
            },
            "automated_testing": {
                "name": "自动化测试",
                "description": "自动执行测试用例，收集测试结果，分析测试覆盖率，生成测试报告",
                "enabled": True,
                "config": {
                    "unit_testing": True,
                    "integration_testing": True,
                    "ui_testing": True,
                    "performance_testing": True,
                    "test_scheduling": {
                        "on_commit": True,
                        "nightly": True,
                        "weekly": True
                    },
                    "test_result_collection": True,
                    "coverage_analysis": True,
                    "report_generation": True,
                    "failure_notification": True
                }
            },
            "structure_based_extension": {
                "name": "基于原结构扩展",
                "description": "所有功能扩展严格基于原有文件结构，确保系统稳定性和一致性",
                "enabled": True,
                "config": {
                    "preserve_existing_files": True,
                    "extension_only_approach": True,
                    "compatibility_verification": True,
                    "structure_validation": True,
                    "file_structure_analysis": True,
                    "impact_assessment": True,
                    "extension_guidelines": {
                        "preserve_directory_structure": True,
                        "maintain_file_naming_conventions": True,
                        "respect_component_boundaries": True,
                        "follow_existing_patterns": True,
                        "document_all_extensions": True
                    }
                }
            },
            "integrated_workflow_management": {
                "name": "集成工作流管理",
                "description": "将工作节点和工作流程整合在统一界面，提供一致的用户体验",
                "enabled": True,
                "config": {
                    "unified_interface": True,
                    "real_time_status_updates": True,
                    "workflow_node_correlation": True,
                    "context_preservation": True,
                    "agent_mode_awareness": True,
                    "independent_module_implementation": True,
                    "style_isolation": True,
                    "state_management": {
                        "use_context_api": True,
                        "redux_integration": True,
                        "local_state_isolation": True
                    }
                }
            },
            "unified_interface_experience": {
                "name": "统一界面体验",
                "description": "提供一致的用户界面体验，整合输入区域、智能体选择、工作节点和工作流可视化",
                "enabled": True,
                "config": {
                    "component_integration": True,
                    "state_synchronization": True,
                    "visual_consistency": True,
                    "interaction_patterns": True,
                    "responsive_behavior": True,
                    "accessibility_compliance": True,
                    "theme_consistency": True
                }
            }
        }
    
    def _init_ui_layout_features(self):
        """初始化UI布局特性"""
        return {
            "two_column_layout": {
                "name": "两栏式布局",
                "description": "左侧为Sidebar导航栏，右侧为主内容区，包含Header、智能体卡片、输入区和案例展示",
                "enabled": True,
                "config": {
                    "left_column_width_percentage": 25,
                    "right_column_width_percentage": 75,
                    "min_column_width": 250
                }
            },
            "responsive_design": {
                "name": "响应式设计",
                "description": "自适应不同屏幕尺寸，确保在桌面和移动设备上的良好体验",
                "enabled": True,
                "config": {
                    "desktop_breakpoint": 1200,
                    "tablet_breakpoint": 768,
                    "mobile_breakpoint": 480,
                    "grid_columns": {
                        "desktop": 4,
                        "tablet": 2,
                        "mobile": 1
                    }
                }
            },
            "theme_customization": {
                "name": "主题定制",
                "description": "支持明暗主题切换和企业级视觉风格定制",
                "enabled": True,
                "config": {
                    "light_theme": True,
                    "dark_theme": True,
                    "custom_theme_support": True,
                    "brand_color_customization": True
                }
            },
            "agent_card_layout": {
                "name": "智能体卡片布局",
                "description": "横向四等分布局，展示四种智能体模式",
                "enabled": True,
                "config": {
                    "card_spacing": 20,
                    "card_border_radius": 8,
                    "card_shadow": True,
                    "highlight_selected": True
                }
            },
            "work_node_visualizer": {
                "name": "工作节点可视化",
                "description": "在首页智能体下方展示工作节点和测试部署状态，左侧显示任务进度和ThoughtActionRecorder思考过程，右侧显示代码和画面回放",
                "enabled": True,
                "config": {
                    "node_display_limit": 10,
                    "auto_refresh_interval": 5000,
                    "node_types": ["savepoint", "rollback", "test", "deploy", "error"],
                    "status_indicators": {
                        "success": "#4CAF50",
                        "pending": "#FFC107",
                        "failed": "#F44336",
                        "running": "#2196F3"
                    }
                }
            },
            "n8n_style_workflow_visualization": {
                "name": "n8n风格工作流可视化",
                "description": "在UI空白区域添加n8n风格的节点连接图，直观展示工作流程和数据流转",
                "enabled": True,
                "config": {
                    "node_types": {
                        "trigger": {
                            "color": "#61b8ff",
                            "icon": "play-circle"
                        },
                        "action": {
                            "color": "#27ae60",
                            "icon": "code-branch"
                        },
                        "condition": {
                            "color": "#ff9800",
                            "icon": "question-circle"
                        },
                        "error": {
                            "color": "#e74c3c",
                            "icon": "exclamation-circle"
                        }
                    },
                    "connection_types": {
                        "success": {
                            "color": "#27ae60",
                            "style": "solid"
                        },
                        "error": {
                            "color": "#e74c3c",
                            "style": "dashed"
                        },
                        "conditional": {
                            "color": "#ff9800",
                            "style": "dotted"
                        }
                    },
                    "interactive_features": {
                        "node_dragging": True,
                        "connection_creation": True,
                        "node_details_on_click": True,
                        "zoom_and_pan": True,
                        "minimap": True
                    },
                    "layout_algorithm": "dagre",
                    "auto_layout": True,
                    "standalone_component": True,
                    "container_selector": ".workflow-container",
                    "extension_only": True,
                    "preserve_existing_layout": True
                }
            },
            "integrated_input_area": {
                "name": "集成输入区域",
                "description": "在智能体卡片上方添加输入框，支持文本输入、文件上传和消息发送功能",
                "enabled": True,
                "config": {
                    "multi_line_input": True,
                    "file_upload": {
                        "enabled": True,
                        "max_file_size": 10, # MB
                        "allowed_file_types": ["*"],
                        "drag_drop_support": True
                    },
                    "send_button": True,
                    "adaptive_placeholder": True,
                    "agent_mode_awareness": True,
                    "placeholder_texts": {
                        "code_agent": "请输入代码需求或上传文件，代码智能体将帮您实现...",
                        "ppt_agent": "请输入PPT的主题和需求，或上传文件，PPT智能体将帮您制作...",
                        "web_agent": "请输入网页需求或上传设计稿，网页智能体将帮您创建...",
                        "general_agent": "请输入您的问题或需求，通用智能体将为您提供帮助..."
                    },
                    "style_isolation": {
                        "use_css_modules": True,
                        "namespace_prefix": "input-area-",
                        "scoped_styles": True
                    }
                }
            },
            "unified_work_node_workflow_view": {
                "name": "统一工作节点与工作流视图",
                "description": "将工作节点时间线和工作流程图整合在同一界面，提供连贯的任务执行视图",
                "enabled": True,
                "config": {
                    "vertical_layout": True,
                    "work_node_section": {
                        "position": "top",
                        "height_percentage": 40,
                        "collapsible": True
                    },
                    "workflow_section": {
                        "position": "bottom",
                        "height_percentage": 60,
                        "collapsible": True
                    },
                    "synchronized_selection": True,
                    "context_preservation": True,
                    "real_time_updates": True,
                    "independent_module": {
                        "standalone_component": True,
                        "isolated_state": True,
                        "style_encapsulation": True
                    }
                }
            },
            "message_history_display": {
                "name": "消息历史显示",
                "description": "在界面底部显示用户与智能体的消息历史记录，支持文本和文件附件",
                "enabled": True,
                "config": {
                    "message_types": ["text", "file", "image", "code"],
                    "message_grouping": True,
                    "timestamp_display": True,
                    "sender_identification": True,
                    "message_styling": {
                        "user_message_color": "#3498db",
                        "agent_message_color": "#f5f5f5",
                        "text_contrast": True,
                        "bubble_style": True
                    },
                    "file_attachment_preview": True,
                    "scrollable_container": True,
                    "max_displayed_messages": 50,
                    "load_more_functionality": True
                }
            }
        }
    
    def _init_prompt_features(self):
        """初始化提示词特性"""
        return {
            "context_aware_prompts": {
                "name": "上下文感知提示",
                "description": "根据测试阶段和问题类型生成针对性提示",
                "enabled": True,
                "config": {
                    "test_phase_awareness": True,
                    "problem_type_detection": True,
                    "adaptive_prompting": True
                }
            },
            "multilingual_support": {
                "name": "多语言支持",
                "description": "支持中英文等多语言提示和报告生成",
                "enabled": True,
                "config": {
                    "supported_languages": ["zh-CN", "en-US", "ja-JP"],
                    "auto_language_detection": True,
                    "translation_quality": 0.95
                }
            },
            "template_based_generation": {
                "name": "基于模板生成",
                "description": "使用预定义模板生成标准化提示和报告",
                "enabled": True,
                "config": {
                    "template_categories": ["test", "report", "analysis", "recommendation"],
                    "template_customization": True,
                    "variable_substitution": True
                }
            },
            "agent_mode_adaptive_prompts": {
                "name": "智能体模式自适应提示",
                "description": "根据选择的智能体模式自动调整输入框提示文本",
                "enabled": True,
                "config": {
                    "mode_detection": True,
                    "context_preservation": True,
                    "dynamic_placeholder_text": True,
                    "suggestion_generation": True,
                    "history_awareness": True,
                    "agent_specific_templates": {
                        "code_agent": ["代码生成", "代码优化", "代码调试", "代码解释"],
                        "ppt_agent": ["演示文稿创建", "幻灯片设计", "内容组织", "视觉效果"],
                        "web_agent": ["网页设计", "前端开发", "响应式布局", "交互功能"],
                        "general_agent": ["问题解答", "任务规划", "信息检索", "创意生成"]
                    }
                }
            }
        }
    
    def _init_thinking_features(self):
        """初始化思维特性"""
        return {
            "thought_action_recorder": {
                "name": "思考行动记录器",
                "description": "记录智能体的思考过程和行动步骤，支持回溯和分析",
                "enabled": True,
                "config": {
                    "thought_recording": True,
                    "action_recording": True,
                    "timestamp_recording": True,
                    "context_recording": True
                }
            },
            "version_rollback": {
                "name": "版本回滚能力",
                "description": "支持回滚到之前的代码版本，确保系统稳定性",
                "enabled": True,
                "config": {
                    "savepoint_creation": True,
                    "rollback_execution": True,
                    "version_comparison": True,
                    "impact_analysis": True
                }
            },
            "problem_solving_strategies": {
                "name": "问题解决策略",
                "description": "根据问题类型选择不同的解决策略，提高解决效率",
                "enabled": True,
                "config": {
                    "strategy_selection": True,
                    "strategy_adaptation": True,
                    "strategy_evaluation": True,
                    "strategy_refinement": True
                }
            },
            "workflow_optimization": {
                "name": "工作流优化",
                "description": "分析工作流执行效率，识别瓶颈并提供优化建议",
                "enabled": True,
                "config": {
                    "performance_analysis": True,
                    "bottleneck_identification": True,
                    "optimization_suggestion": True,
                    "workflow_simulation": True,
                    "execution_path_analysis": True,
                    "resource_utilization_tracking": True,
                    "parallel_execution_opportunities": True,
                    "workflow_metrics": {
                        "execution_time": True,
                        "resource_usage": True,
                        "success_rate": True,
                        "error_frequency": True
                    }
                }
            }
        }
    
    def _init_content_features(self):
        """初始化内容特性"""
        return {
            "code_generation": {
                "name": "代码生成",
                "description": "根据需求生成高质量代码，支持多种编程语言",
                "enabled": True,
                "config": {
                    "supported_languages": ["Python", "JavaScript", "TypeScript", "Java", "C++", "Go"],
                    "code_quality_check": True,
                    "best_practice_adherence": True,
                    "documentation_generation": True
                }
            },
            "report_generation": {
                "name": "报告生成",
                "description": "生成测试报告、分析报告和总结报告",
                "enabled": True,
                "config": {
                    "report_types": ["test", "analysis", "summary"],
                    "data_visualization": True,
                    "executive_summary": True,
                    "detailed_analysis": True
                }
            },
            "documentation_management": {
                "name": "文档管理",
                "description": "创建和维护项目文档，包括README、API文档和用户指南",
                "enabled": True,
                "config": {
                    "document_types": ["readme", "api", "user_guide"],
                    "auto_update": True,
                    "version_control": True,
                    "format_conversion": True
                }
            },
            "message_history_management": {
                "name": "消息历史管理",
                "description": "记录和管理用户与智能体的交互历史",
                "enabled": True,
                "config": {
                    "history_storage": True,
                    "history_retrieval": True,
                    "context_preservation": True,
                    "privacy_protection": True,
                    "message_categorization": True,
                    "search_functionality": True,
                    "export_options": ["json", "csv", "pdf"],
                    "retention_policy": {
                        "max_messages": 1000,
                        "time_period": "30d",
                        "storage_optimization": True
                    }
                }
            },
            "file_attachment_handling": {
                "name": "文件附件处理",
                "description": "管理用户上传的文件，支持多种文件类型的处理和分析",
                "enabled": True,
                "config": {
                    "supported_file_types": {
                        "images": ["jpg", "png", "gif", "webp"],
                        "documents": ["pdf", "docx", "txt", "md"],
                        "code": ["py", "js", "ts", "html", "css", "java"],
                        "data": ["csv", "json", "xml", "xlsx"]
                    },
                    "file_preview": True,
                    "content_extraction": True,
                    "virus_scanning": True,
                    "file_transformation": True,
                    "storage_management": {
                        "compression": True,
                        "deduplication": True,
                        "versioning": True,
                        "expiration": "7d"
                    }
                }
            }
        }
    
    def _init_memory_features(self):
        """初始化记忆特性"""
        return {
            "checkpoint_management": {
                "name": "检查点管理",
                "description": "创建和管理代码检查点，支持版本回滚",
                "enabled": True,
                "config": {
                    "auto_checkpoint": True,
                    "manual_checkpoint": True,
                    "checkpoint_metadata": True,
                    "checkpoint_comparison": True
                }
            },
            "historical_data_analysis": {
                "name": "历史数据分析",
                "description": "分析历史测试数据，识别趋势和模式",
                "enabled": True,
                "config": {
                    "trend_analysis": True,
                    "pattern_recognition": True,
                    "anomaly_detection": True,
                    "predictive_analysis": True
                }
            },
            "knowledge_graph_integration": {
                "name": "知识图谱集成",
                "description": "构建和维护项目知识图谱，支持智能查询和推理",
                "enabled": True,
                "config": {
                    "entity_extraction": True,
                    "relationship_mapping": True,
                    "graph_visualization": True,
                    "semantic_search": True
                }
            },
            "context_persistence": {
                "name": "上下文持久化",
                "description": "保存和恢复测试和开发上下文，确保连续性",
                "enabled": True,
                "config": {
                    "session_state_saving": True,
                    "context_restoration": True,
                    "environment_snapshot": True,
                    "dependency_tracking": True
                }
            },
            "workflow_state_persistence": {
                "name": "工作流状态持久化",
                "description": "保存工作流执行状态和历史记录，支持断点恢复和分析",
                "enabled": True,
                "config": {
                    "state_serialization": True,
                    "execution_history": True,
                    "checkpoint_creation": True,
                    "resume_from_checkpoint": True,
                    "state_visualization": True,
                    "audit_logging": True,
                    "state_comparison": True,
                    "storage_options": {
                        "database": True,
                        "file_system": True,
                        "distributed_cache": True
                    }
                }
            },
            "message_history_persistence": {
                "name": "消息历史持久化",
                "description": "持久化存储用户与智能体的交互历史，支持会话恢复和上下文理解",
                "enabled": True,
                "config": {
                    "conversation_storage": True,
                    "session_restoration": True,
                    "context_awareness": True,
                    "cross_session_memory": True,
                    "user_preference_learning": True,
                    "interaction_patterns": True,
                    "storage_optimization": {
                        "compression": True,
                        "indexing": True,
                        "sharding": True
                    },
                    "privacy_controls": {
                        "data_anonymization": True,
                        "user_deletion_rights": True,
                        "access_controls": True
                    }
                }
            }
        }
