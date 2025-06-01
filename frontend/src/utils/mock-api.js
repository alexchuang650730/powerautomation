/**
 * 模拟MCP Planner和ThoughtActionRecorder的API响应
 * 用于前端测试和验证
 */

// 模拟API响应延迟
const simulateDelay = (ms) => new Promise(resolve => setTimeout(resolve, ms));

/**
 * 模拟MCP Planner API
 * @param {Request} req - 请求对象
 * @param {Response} res - 响应对象
 */
export const mockMCPPlannerAPI = async (req, res) => {
  try {
    const { thinkingProcess } = req.body;
    
    if (!thinkingProcess) {
      return res.status(400).json({
        success: false,
        error: '缺少思考过程参数'
      });
    }
    
    // 模拟处理延迟
    await simulateDelay(1000);
    
    // 生成模拟响应
    const response = {
      success: true,
      planId: `plan-${Date.now()}`,
      steps: [
        {
          id: 1,
          action: '分析用户输入',
          status: 'completed'
        },
        {
          id: 2,
          action: '确定最适合的智能体',
          status: 'completed'
        },
        {
          id: 3,
          action: '准备执行计划',
          status: 'pending'
        }
      ],
      thinkingSummary: `已处理思考过程，长度为${thinkingProcess.length}字符`,
      timestamp: new Date().toISOString()
    };
    
    return res.status(200).json(response);
  } catch (error) {
    console.error('MCP Planner模拟API错误:', error);
    return res.status(500).json({
      success: false,
      error: error.message || '服务器内部错误'
    });
  }
};

/**
 * 模拟ThoughtActionRecorder API
 * @param {Request} req - 请求对象
 * @param {Response} res - 响应对象
 */
export const mockThoughtActionRecorderAPI = async (req, res) => {
  try {
    const { features } = req.body;
    
    if (!features) {
      return res.status(400).json({
        success: false,
        error: '缺少特性参数'
      });
    }
    
    // 模拟处理延迟
    await simulateDelay(800);
    
    // 验证六大特性是否完整
    const requiredFeatures = ['feature1', 'feature2', 'feature3', 'feature4', 'feature5', 'feature6'];
    const missingFeatures = requiredFeatures.filter(f => !features[f]);
    
    if (missingFeatures.length > 0) {
      return res.status(400).json({
        success: false,
        error: `缺少必要的特性: ${missingFeatures.join(', ')}`
      });
    }
    
    // 生成模拟响应
    const response = {
      success: true,
      recordId: `record-${Date.now()}`,
      featuresStored: Object.keys(features),
      analysisResults: {
        feature1Quality: 'high',
        feature2Quality: 'medium',
        feature3Quality: 'high',
        feature4Quality: 'high',
        feature5Quality: 'medium',
        feature6Quality: 'high',
        overallQuality: 'high'
      },
      timestamp: new Date().toISOString()
    };
    
    return res.status(200).json(response);
  } catch (error) {
    console.error('ThoughtActionRecorder模拟API错误:', error);
    return res.status(500).json({
      success: false,
      error: error.message || '服务器内部错误'
    });
  }
};

export default {
  mockMCPPlannerAPI,
  mockThoughtActionRecorderAPI
};
