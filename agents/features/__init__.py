"""
智能体六大特性包

提供四个智能体（PPT、网页、代码、通用）的六大特性定义和管理
"""

from .agent_features import (
    AgentFeatures,
    PPTAgentFeatures,
    WebAgentFeatures,
    CodeAgentFeatures,
    GeneralAgentFeatures,
    create_agent_features,
    get_agent_features,
    update_agent_features
)

__all__ = [
    'AgentFeatures',
    'PPTAgentFeatures',
    'WebAgentFeatures',
    'CodeAgentFeatures',
    'GeneralAgentFeatures',
    'create_agent_features',
    'get_agent_features',
    'update_agent_features'
]
