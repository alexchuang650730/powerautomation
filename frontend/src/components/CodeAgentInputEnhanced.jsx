/**
 * 代码智能体输入组件增强版
 * 负责处理用户输入，进行需求拆解，并路由到合适的智能体
 * 同时支持多智能体六特性完善、MCP Planner集成和RL Factory学习
 */
import React, { useState, useEffect } from 'react';
import { decomposeRequest, storeContextMemory } from '../utils/agent-decomposer';
import { mcpPlannerProcess } from '../utils/mcp-planner-enhancer';
import { processMultiAgentEnhancement } from '../utils/multi-agent-enhancer';

const CodeAgentInputEnhanced = ({ onSubmit, onAgentChange }) => {
  const [input, setInput] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [decompositionResult, setDecompositionResult] = useState(null);
  const [mcpResponse, setMcpResponse] = useState(null);
  const [enhancementResult, setEnhancementResult] = useState(null);
  const [processingStep, setProcessingStep] = useState('');

  // 处理输入变化
  const handleInputChange = (e) => {
    setInput(e.target.value);
  };

  // 处理表单提交
  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!input.trim()) return;
    
    setIsProcessing(true);
    setDecompositionResult(null);
    setMcpResponse(null);
    setEnhancementResult(null);
    
    try {
      // 步骤1: 需求拆解
      setProcessingStep('需求拆解');
      const result = decomposeRequest(input, 'code_agent');
      setDecompositionResult(result);
      
      // 步骤2: 处理六特性增强
      setProcessingStep('六特性增强');
      const enhancementResult = await processMultiAgentEnhancement(input);
      setEnhancementResult(enhancementResult);
      
      // 步骤3: MCP Planner处理
      setProcessingStep('MCP Planner处理');
      const thinkingProcess = result.thinkingProcess;
      const mcpResult = await mcpPlannerProcess(input, thinkingProcess);
      setMcpResponse(mcpResult);
      
      // 步骤4: 存储上下文记忆
      setProcessingStep('存储上下文记忆');
      if (result.isGeneralRequest && result.generalFeatures) {
        // 存储上下文记忆，包含六大特性
        await storeContextMemory(input, result, result.generalFeatures);
      } else {
        // 存储上下文记忆，不包含六大特性
        await storeContextMemory(input, result);
      }
      
      // 步骤5: 通知父组件需要切换智能体
      setProcessingStep('智能体路由');
      if (result.targetAgent !== 'code_agent' && onAgentChange) {
        onAgentChange(result.targetAgent);
      }
      
      // 步骤6: 提交处理后的请求
      setProcessingStep('提交请求');
      if (onSubmit) {
        onSubmit(result.processedQuery, result.targetAgent);
      }
      
      setProcessingStep('完成');
    } catch (error) {
      console.error('处理失败:', error);
      setProcessingStep(`错误: ${error.message}`);
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="code-agent-input-enhanced">
      <form onSubmit={handleSubmit} className="input-form">
        <textarea
          value={input}
          onChange={handleInputChange}
          placeholder="请输入您的需求，代码智能体会自动分析并完善四个智能体的六大特性..."
          className="input-textarea"
          rows={4}
        />
        
        <div className="input-actions">
          <button 
            type="submit" 
            className="submit-button"
            disabled={isProcessing || !input.trim()}
          >
            {isProcessing ? '处理中...' : '提交'}
          </button>
        </div>
      </form>
      
      {isProcessing && (
        <div className="processing-indicator">
          <div className="spinner"></div>
          <p>正在{processingStep}...</p>
        </div>
      )}
      
      {decompositionResult && (
        <div className="result-section">
          <h3 className="section-title">需求拆解结果</h3>
          <div className="result-content">
            <p><strong>目标智能体:</strong> {decompositionResult.targetAgent}</p>
            <p><strong>是否通用请求:</strong> {decompositionResult.isGeneralRequest ? '是' : '否'}</p>
            <p><strong>思考过程:</strong></p>
            <pre className="thinking-process">{decompositionResult.thinkingProcess}</pre>
            
            {decompositionResult.isGeneralRequest && decompositionResult.generalFeatures && (
              <div className="general-features">
                <p><strong>通用智能体六大特性:</strong></p>
                <ul>
                  <li><strong>特性1:</strong> {decompositionResult.generalFeatures.feature1}</li>
                  <li><strong>特性2:</strong> {decompositionResult.generalFeatures.feature2}</li>
                  <li><strong>特性3:</strong> {decompositionResult.generalFeatures.feature3}</li>
                  <li><strong>特性4:</strong> {decompositionResult.generalFeatures.feature4}</li>
                  <li><strong>特性5:</strong> {decompositionResult.generalFeatures.feature5}</li>
                  <li><strong>特性6:</strong> {decompositionResult.generalFeatures.feature6}</li>
                </ul>
              </div>
            )}
          </div>
        </div>
      )}
      
      {enhancementResult && (
        <div className="result-section">
          <h3 className="section-title">六特性增强结果</h3>
          <div className="result-content">
            <p><strong>分析结果:</strong></p>
            <ul>
              <li><strong>目标智能体:</strong> {enhancementResult.analysisResult?.targetAgents?.join(', ')}</li>
              <li><strong>目标特性:</strong> {enhancementResult.analysisResult?.targetFeatures?.join(', ')}</li>
              <li><strong>增强类型:</strong> {enhancementResult.analysisResult?.enhancementType}</li>
              <li><strong>置信度:</strong> {enhancementResult.analysisResult?.confidence}</li>
            </ul>
            
            {Object.keys(enhancementResult.enhancementResults || {}).map(agentType => (
              <div key={agentType} className="agent-enhancement">
                <p><strong>{agentType}增强结果:</strong></p>
                <ul>
                  {Object.keys(enhancementResult.enhancementResults[agentType]?.features || {}).map(featureType => (
                    <li key={featureType}>
                      <strong>{featureType}:</strong> {enhancementResult.enhancementResults[agentType]?.features[featureType]}
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </div>
      )}
      
      {mcpResponse && (
        <div className="result-section">
          <h3 className="section-title">MCP Planner处理结果</h3>
          <div className="result-content">
            <p><strong>处理状态:</strong> {mcpResponse.success ? '成功' : '失败'}</p>
            <p><strong>处理步骤:</strong></p>
            <ul>
              {mcpResponse.steps?.map(step => (
                <li key={step.id}>
                  <strong>{step.name}:</strong> {step.state}
                </li>
              ))}
            </ul>
            
            {mcpResponse.outputs?.code && (
              <div className="code-output">
                <p><strong>代码输出:</strong></p>
                <pre className="code-preview">{mcpResponse.outputs.code.code}</pre>
              </div>
            )}
            
            {mcpResponse.outputs?.github && (
              <div className="github-output">
                <p><strong>GitHub推送结果:</strong> {mcpResponse.outputs.github.success ? '成功' : '失败'}</p>
                {mcpResponse.outputs.github.url && (
                  <p><strong>提交URL:</strong> <a href={mcpResponse.outputs.github.url} target="_blank" rel="noopener noreferrer">{mcpResponse.outputs.github.url}</a></p>
                )}
              </div>
            )}
            
            {mcpResponse.outputs?.learning && (
              <div className="learning-output">
                <p><strong>RL Factory学习结果:</strong> {mcpResponse.outputs.learning.success ? '成功' : '失败'}</p>
                <p><strong>学习质量:</strong> {mcpResponse.outputs.learning.quality}</p>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default CodeAgentInputEnhanced;
