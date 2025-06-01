/**
 * 兼容性测试 - 验证不同调用路径下的功能一致性
 * 测试直接调用和通过MCP协调器间接调用的兼容性和稳定性
 */
import pytest
import os
import sys
import json
import logging
from unittest.mock import patch, MagicMock

# 添加项目根目录到Python路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# 导入需要测试的模块
from mcptool.adapters.mcp_adapter import MCPAdapter
from agents.features.general_agent_features import GeneralAgentFeatures
from agents.features.code_agent_features import CodeAgentFeatures

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("compatibility_test.log")
    ]
)
logger = logging.getLogger("CompatibilityTest")

class TestMCPAdapterCompatibility:
    """测试MCP适配器在不同调用路径下的兼容性和稳定性"""
    
    @pytest.fixture
    def mcp_adapter(self):
        """创建MCP适配器实例"""
        return MCPAdapter()
    
    @pytest.fixture
    def mock_coordinator(self):
        """模拟MCP协调器"""
        mock = MagicMock()
        mock.execute_tool.return_value = {"status": "success", "result": "mock_result"}
        mock.run_e2e_test.return_value = {"status": "success", "result": "mock_test_result"}
        return mock
    
    def test_direct_tool_execution(self, mcp_adapter):
        """测试直接执行工具的路径"""
        # 禁用MCP组件
        with patch.object(mcp_adapter, 'is_mcp_available', return_value=False):
            # 执行工具
            result = mcp_adapter.execute_tool("test_and_issue_collector", "run_test", test_name="sample_test")
            
            # 验证结果
            assert "status" in result, "结果中应包含状态字段"
            logger.info(f"直接执行工具结果: {result}")
    
    def test_indirect_tool_execution(self, mcp_adapter, mock_coordinator):
        """测试通过MCP协调器间接执行工具的路径"""
        # 启用MCP组件并注入模拟协调器
        with patch.object(mcp_adapter, 'is_mcp_available', return_value=True), \
             patch.object(mcp_adapter, 'coordinator', mock_coordinator):
            # 执行工具
            result = mcp_adapter.execute_tool("test_and_issue_collector", "run_test", test_name="sample_test")
            
            # 验证结果
            assert result == {"status": "success", "result": "mock_result"}, "间接执行工具结果不符合预期"
            # 验证协调器被正确调用
            mock_coordinator.execute_tool.assert_called_once_with(
                "test_and_issue_collector", "run_test", test_name="sample_test"
            )
            logger.info(f"间接执行工具结果: {result}")
    
    def test_graceful_degradation(self, mcp_adapter, mock_coordinator):
        """测试当MCP协调器调用失败时的优雅降级"""
        # 启用MCP组件并注入模拟协调器，但使其抛出异常
        mock_coordinator.execute_tool.side_effect = Exception("模拟协调器错误")
        
        with patch.object(mcp_adapter, 'is_mcp_available', return_value=True), \
             patch.object(mcp_adapter, 'coordinator', mock_coordinator), \
             patch.object(mcp_adapter, '_direct_execute_tool', return_value={"status": "success", "result": "fallback_result"}):
            # 执行工具
            result = mcp_adapter.execute_tool("test_and_issue_collector", "run_test", test_name="sample_test")
            
            # 验证结果
            assert result == {"status": "success", "result": "fallback_result"}, "降级执行结果不符合预期"
            # 验证协调器被调用且直接执行被调用
            mock_coordinator.execute_tool.assert_called_once()
            mcp_adapter._direct_execute_tool.assert_called_once()
            logger.info(f"降级执行工具结果: {result}")
    
    def test_run_test_compatibility(self, mcp_adapter, mock_coordinator):
        """测试运行测试功能在不同路径下的兼容性"""
        # 测试直接路径
        with patch.object(mcp_adapter, 'is_mcp_available', return_value=False), \
             patch.object(mcp_adapter, '_direct_run_test', return_value={"status": "success", "result": "direct_test_result"}):
            direct_result = mcp_adapter.run_test("unit:sample_test")
            assert direct_result == {"status": "success", "result": "direct_test_result"}, "直接运行测试结果不符合预期"
        
        # 测试间接路径
        with patch.object(mcp_adapter, 'is_mcp_available', return_value=True), \
             patch.object(mcp_adapter, 'coordinator', mock_coordinator):
            indirect_result = mcp_adapter.run_test("unit:sample_test")
            assert indirect_result == {"status": "success", "result": "mock_test_result"}, "间接运行测试结果不符合预期"
            mock_coordinator.run_e2e_test.assert_called_once()
    
    def test_analyze_problem_compatibility(self, mcp_adapter, mock_coordinator):
        """测试问题分析功能在不同路径下的兼容性"""
        problem = "测试失败：无法连接数据库"
        context = {"test_name": "database_connection_test"}
        
        # 测试直接路径
        with patch.object(mcp_adapter, 'is_mcp_available', return_value=False), \
             patch.object(mcp_adapter, '_direct_analyze_problem', return_value={"status": "success", "result": "direct_analysis"}):
            direct_result = mcp_adapter.analyze_problem(problem, context)
            assert direct_result == {"status": "success", "result": "direct_analysis"}, "直接分析问题结果不符合预期"
        
        # 测试间接路径
        mock_coordinator.execute_tool.return_value = {"status": "success", "result": "indirect_analysis"}
        with patch.object(mcp_adapter, 'is_mcp_available', return_value=True), \
             patch.object(mcp_adapter, 'coordinator', mock_coordinator):
            indirect_result = mcp_adapter.analyze_problem(problem, context)
            assert indirect_result == {"status": "success", "result": "indirect_analysis"}, "间接分析问题结果不符合预期"
            mock_coordinator.execute_tool.assert_called_once()


class TestFeatureStructureCompatibility:
    """测试特性结构调整后的兼容性和稳定性"""
    
    def test_general_agent_features_structure(self):
        """测试通用智能体特性结构"""
        features = GeneralAgentFeatures()
        
        # 验证UI布局特性已恢复到上一个版本
        ui_features = features.ui_layout_features
        
        # 验证存在的特性
        assert "agent_card_layout" in ui_features, "通用智能体应包含agent_card_layout特性"
        assert "platform_title_style" in ui_features, "通用智能体应包含platform_title_style特性"
        assert "responsive_design" in ui_features, "通用智能体应包含responsive_design特性"
        assert "theme_customization" in ui_features, "通用智能体应包含theme_customization特性"
        
        # 验证已移除的特性
        assert "two_column_layout" not in ui_features, "通用智能体不应包含two_column_layout特性"
        assert "realtime_status_feedback" not in ui_features, "通用智能体不应包含realtime_status_feedback特性"
        
        # 验证特性配置
        assert ui_features["agent_card_layout"]["config"]["card_spacing"] == 16, "agent_card_layout配置不正确"
        assert ui_features["responsive_design"]["config"]["desktop_breakpoint"] == 1200, "responsive_design配置不正确"
        
        logger.info("通用智能体特性结构验证通过")
    
    def test_code_agent_features_structure(self):
        """测试代码智能体特性结构"""
        features = CodeAgentFeatures()
        
        # 验证UI布局特性包含从通用智能体迁移的功能
        ui_features = features.ui_layout_features
        
        # 验证存在的特性
        assert "two_column_layout" in ui_features, "代码智能体应包含two_column_layout特性"
        assert "task_progress_display" in ui_features, "代码智能体应包含task_progress_display特性"
        assert "code_playback" in ui_features, "代码智能体应包含code_playback特性"
        assert "code_editor_integration" in ui_features, "代码智能体应包含code_editor_integration特性"
        
        # 验证特性配置
        assert ui_features["two_column_layout"]["config"]["left_column_width_percentage"] == 40, "two_column_layout配置不正确"
        assert ui_features["task_progress_display"]["config"]["progress_bar"] == True, "task_progress_display配置不正确"
        
        logger.info("代码智能体特性结构验证通过")
    
    def test_feature_serialization_compatibility(self):
        """测试特性序列化和反序列化的兼容性"""
        # 通用智能体特性
        general_features = GeneralAgentFeatures()
        general_dict = general_features.to_dict()
        general_json = general_features.to_json()
        
        # 验证序列化结果
        assert "ui_layout_features" in general_dict, "序列化结果应包含ui_layout_features"
        assert "agent_card_layout" in general_dict["ui_layout_features"], "序列化结果应包含agent_card_layout"
        
        # 代码智能体特性
        code_features = CodeAgentFeatures()
        code_dict = code_features.to_dict()
        code_json = code_features.to_json()
        
        # 验证序列化结果
        assert "ui_layout_features" in code_dict, "序列化结果应包含ui_layout_features"
        assert "two_column_layout" in code_dict["ui_layout_features"], "序列化结果应包含two_column_layout"
        
        logger.info("特性序列化兼容性验证通过")
    
    def test_feature_update_compatibility(self):
        """测试特性更新的兼容性"""
        # 通用智能体特性更新
        general_features = GeneralAgentFeatures()
        general_features.update_feature("ui_layout_features", "agent_card_layout", {
            "config": {
                "card_spacing": 20,
                "card_border_radius": 10
            }
        })
        
        # 验证更新结果
        assert general_features.ui_layout_features["agent_card_layout"]["config"]["card_spacing"] == 20, "特性更新失败"
        assert general_features.ui_layout_features["agent_card_layout"]["config"]["card_border_radius"] == 10, "特性更新失败"
        
        # 代码智能体特性更新
        code_features = CodeAgentFeatures()
        code_features.update_feature("ui_layout_features", "two_column_layout", {
            "config": {
                "left_column_width_percentage": 35,
                "right_column_width_percentage": 65
            }
        })
        
        # 验证更新结果
        assert code_features.ui_layout_features["two_column_layout"]["config"]["left_column_width_percentage"] == 35, "特性更新失败"
        assert code_features.ui_layout_features["two_column_layout"]["config"]["right_column_width_percentage"] == 65, "特性更新失败"
        
        logger.info("特性更新兼容性验证通过")


if __name__ == "__main__":
    # 运行测试
    pytest.main(["-v", __file__])
