#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
PowerAutomation MCP 系统架构图生成脚本
使用Python和Graphviz生成高质量架构图
"""

import os
import graphviz as gv

# 创建有向图
g = gv.Digraph('PowerAutomation_MCP', filename='architecture.png', format='png')
g.attr(rankdir='TB', size='10,7', dpi='300')
g.attr('node', shape='box', style='filled', fontname='SimHei', fontsize='14')
g.attr('edge', fontname='SimHei', fontsize='12')

# 设置图表标题
g.attr(label='PowerAutomation MCP 系统架构图', labelloc='t', fontsize='20', fontname='SimHei')

# 定义节点颜色
central_color = '#a8d1ff'  # 中央协调器 - 浅蓝色
planner_color = '#a8d1ff'  # 规划器 - 浅蓝色
brainstorm_color = '#b5e6b5'  # 头脑风暴器 - 浅绿色
recorder_color = '#ffb3a8'  # 记录器 - 浅红色
release_color = '#ffd9a8'  # Release管理器 - 浅橙色
test_color = '#ffc1a8'  # 测试收集器 - 浅橙红色
solver_color = '#e6b5e6'  # 问题解决器 - 浅紫色
external_color = '#e6e6e6'  # 外部系统 - 浅灰色

# 添加节点
g.node('central', 'MCP中央协调器\n(MCPCentralCoordinator)', fillcolor=central_color)
g.node('planner', 'MCP规划器\n(MCPPlanner)', fillcolor=planner_color)
g.node('brainstorm', 'MCP头脑风暴器\n(MCPBrainstorm)', fillcolor=brainstorm_color)
g.node('recorder', '思考与操作记录器\n(ThoughtActionRecorder)', fillcolor=recorder_color)
g.node('release', 'Release管理器\n(ReleaseManager)', fillcolor=release_color)
g.node('test', '测试与问题收集器\n(TestAndIssueCollector)', fillcolor=test_color)
g.node('solver', '问题解决驱动器\n(AgentProblemSolver)', fillcolor=solver_color)
g.node('mcp_so', 'mcp.so模块', fillcolor=external_color)
g.node('github', 'GitHub', fillcolor=external_color)

# 添加边
g.edge('mcp_so', 'planner', label='集成')
g.edge('central', 'github', label='同步')
g.edge('central', 'planner', label='协调', dir='both')
g.edge('central', 'brainstorm', label='协调', dir='both')
g.edge('planner', 'brainstorm', label='能力提升', dir='both', color='green')
g.edge('planner', 'recorder', label='调用', color='green')
g.edge('planner', 'release', label='调用', color='green')
g.edge('planner', 'test', label='调用', color='green')
g.edge('planner', 'solver', label='调用', color='green')

# 添加子图分组
with g.subgraph(name='cluster_legend') as c:
    c.attr(label='图例', fontname='SimHei', style='filled', color='lightgrey', fillcolor='white')
    c.node('legend_central', '中央组件', shape='box', style='filled', fillcolor=central_color)
    c.node('legend_brainstorm', '头脑风暴器', shape='box', style='filled', fillcolor=brainstorm_color)
    c.node('legend_tools', '开发工具模块', shape='box', style='filled', fillcolor=release_color)
    c.node('legend_external', '外部系统', shape='box', style='filled', fillcolor=external_color)
    c.attr('node', style='invis')
    c.attr('edge', style='invis')
    c.edge('legend_central', 'legend_brainstorm')
    c.edge('legend_brainstorm', 'legend_tools')
    c.edge('legend_tools', 'legend_external')

# 设置节点位置
g.attr('graph', nodesep='0.5', ranksep='0.8')

# 保存图片
output_path = os.path.join(os.path.dirname(__file__), 'architecture.png')
g.render(cleanup=True)
print(f"架构图已生成: {output_path}")
