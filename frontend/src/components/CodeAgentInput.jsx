import React, { useState, useEffect } from 'react';
import { decomposeRequest, storeContextMemory, sendToMCPPlanner, recordWithThoughtActionRecorder } from '../utils/agent-decomposer';

/**
 * 代码智能体输入组件
 * 负责处理用户输入，进行需求拆解，并路由到合适的智能体
 * 同时将思考过程传递给MCP Planner和ThoughtActionRecorder
 */
const CodeAgentInput = ({ onSubmit, onAgentChange }) => {
  const [input, setInput] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [decompositionResult, setDecompositionResult] = useState(null);
  const [mcpResponse, setMcpResponse] = useState(null);
  const [recorderResponse, setRecorderResponse] = useState(null);

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
    setRecorderResponse(null);
    
    try {
      // 进行需求拆解
      const result = decomposeRequest(input, 'code_agent');
      setDecompositionResult(result);
      
      // 发送思考过程到MCP Planner
      if (result.thinkingProcess) {
        const plannerResponse = await sendToMCPPlanner(result.thinkingProcess);
        setMcpResponse(plannerResponse);
      }
      
      // 如果是通用请求，存储六大特性并使用ThoughtActionRecorder记录
      if (result.isGeneralRequest && result.generalFeatures) {
        const recorderResponse = await recordWithThoughtActionRecorder(result.generalFeatures);
        setRecorderResponse(recorderResponse);
        
        // 存储上下文记忆，包含六大特性
        await storeContextMemory(input, result, result.generalFeatures);
      } else {
        // 存储上下文记忆，不包含六大特性
        await storeContextMemory(input, result);
      }
      
      // 通知父组件需要切换智能体
      if (result.targetAgent !== 'code_agent' && onAgentChange) {
        onAgentChange(result.targetAgent);
      }
      
      // 提交处理后的请求
      if (onSubmit) {
        onSubmit(result.processedQuery, result.targetAgent);
      }
    } catch (error) {
      console.error('需求拆解或处理失败:', error);
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="code-agent-input">
      <form onSubmit={handleSubmit} className="input-form">
        <textarea
          value={input}
          onChange={handleInputChange}
          placeholder="请输入您的代码需求，代码智能体会自动分析并路由到最合适的智能体处理..."
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
          <p>正在分析需求并路由到最合适的智能体...</p>
        </div>
      )}
      
      {decompositionResult && (
        <div className="decomposition-result">
          <div className="result-header">
            需求分析结果:
          </div>
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
      
      {mcpResponse && (
        <div className="mcp-response">
          <div className="response-header">
            MCP Planner响应:
          </div>
          <pre className="response-content">
            {JSON.stringify(mcpResponse, null, 2)}
          </pre>
        </div>
      )}
      
      {recorderResponse && (
        <div className="recorder-response">
          <div className="response-header">
            ThoughtActionRecorder响应:
          </div>
          <pre className="response-content">
            {JSON.stringify(recorderResponse, null, 2)}
          </pre>
        </div>
      )}
    </div>
  );
};

export default CodeAgentInput;
