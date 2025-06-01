"""
通用智能体六大特性定义文档
更新日期：2025-06-01
版本：1.1

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
            "structure_based_extension"
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
            "n8n_style_workflow_visualization"
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
            "context_persistence"
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
            "technical_term_recognition": {
                "name": "技术术语识别",
                "description": "准确识别并解释测试和开发领域的专业术语",
                "enabled": True,
                "config": {
                    "term_database_size": 5000,
                    "context_based_disambiguation": True,
                    "explanation_generation": True
                }
            }
        }
    
    def _init_thinking_features(self):
        """初始化思维特性"""
        return {
            "test_strategy_planning": {
                "name": "测试策略规划",
                "description": "自动分析代码结构，制定最优测试策略",
                "enabled": True,
                "config": {
                    "code_structure_analysis": True,
                    "test_coverage_optimization": True,
                    "risk_based_prioritization": True
                }
            },
            "root_cause_analysis": {
                "name": "问题根因分析",
                "description": "通过调用Manus能力，深入分析测试失败原因",
                "enabled": True,
                "config": {
                    "log_analysis_depth": "deep",
                    "pattern_recognition": True,
                    "historical_comparison": True,
                    "mcp_integration": {
                        "use_coordinator": True,
                        "use_brain": True,
                        "use_planner": True
                    }
                }
            },
            "fix_solution_generation": {
                "name": "修复方案生成",
                "description": "基于历史数据和最佳实践，提供针对性修复建议",
                "enabled": True,
                "config": {
                    "solution_database_size": 10000,
                    "context_relevance_threshold": 0.8,
                    "code_generation_enabled": True
                }
            },
            "priority_sorting": {
                "name": "优先级排序",
                "description": "智能评估问题严重性，合理安排修复顺序",
                "enabled": True,
                "config": {
                    "severity_levels": ["critical", "high", "medium", "low"],
                    "business_impact_assessment": True,
                    "effort_estimation": True
                }
            },
            "version_rollback_capability": {
                "name": "版本回滚能力",
                "description": "智能确认版本回滚需求，执行回滚操作并验证回滚结果",
                "enabled": True,
                "config": {
                    "rollback_history_tracking": True,
                    "rollback_success_rate_analysis": True,
                    "pre_post_rollback_comparison": True,
                    "auto_rollback_threshold": 5,
                    "rollback_verification_steps": [
                        "代码完整性检查",
                        "功能测试验证",
                        "性能影响评估",
                        "依赖兼容性确认"
                    ]
                }
            },
            "agent_manufacturing": {
                "name": "自动化制造智能体",
                "description": "根据需求自动生成、训练和部署专用智能体，实现智能体的自我复制和进化",
                "enabled": True,
                "config": {
                    "agent_blueprint_generation": True,
                    "component_assembly": True,
                    "knowledge_transfer": True,
                    "capability_inheritance": True,
                    "self_optimization": True,
                    "manufacturing_stages": [
                        "需求分析",
                        "能力规划",
                        "知识库构建",
                        "模型训练",
                        "行为验证",
                        "部署集成"
                    ],
                    "quality_assurance": {
                        "behavior_testing": True,
                        "knowledge_validation": True,
                        "performance_benchmarking": True,
                        "safety_checks": True
                    },
                    "feedback_loop": True
                }
            }
        }
    
    def _init_content_features(self):
        """初始化内容特性"""
        return {
            "test_report_generation": {
                "name": "测试报告生成",
                "description": "自动生成结构化、可视化的测试报告",
                "enabled": True,
                "config": {
                    "report_formats": ["html", "pdf", "markdown"],
                    "visualization_types": ["charts", "tables", "heatmaps"],
                    "auto_summary": True
                }
            },
            "code_explanation": {
                "name": "代码解释",
                "description": "提供清晰、易懂的代码注释和解释",
                "enabled": True,
                "config": {
                    "language_support": ["python", "javascript", "java", "c++"],
                    "explanation_detail_level": "medium",
                    "include_examples": True
                }
            },
            "documentation_generation": {
                "name": "文档生成",
                "description": "自动生成API文档、用户手册和开发指南",
                "enabled": True,
                "config": {
                    "api_doc_generation": True,
                    "user_manual_generation": True,
                    "developer_guide_generation": True,
                    "multilingual_support": True
                }
            }
        }
    
    def _init_memory_features(self):
        """初始化记忆特性"""
        return {
            "historical_data_analysis": {
                "name": "历史数据分析",
                "description": "分析历史测试数据，识别趋势和模式",
                "enabled": True,
                "config": {
                    "data_retention_period": 365,
                    "trend_analysis": True,
                    "pattern_recognition": True
                }
            },
            "knowledge_graph_integration": {
                "name": "知识图谱集成",
                "description": "构建测试和开发知识图谱，支持智能查询和推理",
                "enabled": True,
                "config": {
                    "entity_types": ["test", "bug", "fix", "component"],
                    "relation_types": ["causes", "fixes", "depends_on", "affects"],
                    "inference_enabled": True
                }
            },
            "context_persistence": {
                "name": "上下文持久化",
                "description": "保持测试和开发上下文，支持长期任务和多轮对话",
                "enabled": True,
                "config": {
                    "session_timeout": 3600,
                    "context_size_limit": 10000,
                    "priority_based_retention": True
                }
            },
            "checkpoint_management": {
                "name": "检查点管理",
                "description": "创建和管理代码检查点，支持版本回滚和比较",
                "enabled": True,
                "config": {
                    "auto_checkpoint": True,
                    "checkpoint_interval": 3600,
                    "max_checkpoints": 50,
                    "diff_visualization": True,
                    "checkpoint_tagging": True,
                    "checkpoint_search": True,
                    "checkpoint_comparison": True,
                    "checkpoint_restoration": True
                }
            }
        }
