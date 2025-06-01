/**
 * MCPAdapter组件单元测试
 * 测试通过MCP框架进行间接调用的适配器
 */
import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import MCPAdapter from '../../components/MCPAdapter';

// 模拟MCP模块
jest.mock('../../services/mcpcoordinator', () => ({
  callTool: jest.fn().mockResolvedValue({ success: true, data: { result: 'test result' } }),
  registerCallback: jest.fn(),
  unregisterCallback: jest.fn()
}));

jest.mock('../../services/mcpbrain', () => ({
  analyze: jest.fn().mockResolvedValue({ analysis: 'test analysis', confidence: 0.95 }),
  getRecommendation: jest.fn().mockResolvedValue(['recommendation1', 'recommendation2'])
}));

jest.mock('../../services/mcpplanner', () => ({
  createPlan: jest.fn().mockResolvedValue({ steps: ['step1', 'step2'], estimatedTime: '2min' }),
  updatePlan: jest.fn().mockResolvedValue({ status: 'updated' })
}));

import { callTool } from '../../services/mcpcoordinator';
import { analyze, getRecommendation } from '../../services/mcpbrain';
import { createPlan, updatePlan } from '../../services/mcpplanner';

describe('MCPAdapter组件', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });
  
  // 基本渲染测试
  test('正确渲染MCPAdapter组件', () => {
    render(<MCPAdapter />);
    
    // 验证组件已渲染
    expect(screen.getByTestId('mcp-adapter')).toBeInTheDocument();
  });
  
  // 工具调用测试
  test('通过mcpcoordinator调用工具', async () => {
    const mockOnResult = jest.fn();
    render(<MCPAdapter onResult={mockOnResult} />);
    
    // 获取调用按钮并点击
    const callButton = screen.getByTestId('call-tool-button');
    fireEvent.click(callButton);
    
    // 验证mcpcoordinator.callTool被调用
    expect(callTool).toHaveBeenCalledTimes(1);
    
    // 等待异步调用完成
    await waitFor(() => {
      expect(mockOnResult).toHaveBeenCalledWith({ success: true, data: { result: 'test result' } });
    });
  });
  
  // 分析测试
  test('通过mcpbrain进行分析', async () => {
    const mockOnAnalysis = jest.fn();
    render(<MCPAdapter onAnalysis={mockOnAnalysis} />);
    
    // 获取分析按钮并点击
    const analyzeButton = screen.getByTestId('analyze-button');
    fireEvent.click(analyzeButton);
    
    // 验证mcpbrain.analyze被调用
    expect(analyze).toHaveBeenCalledTimes(1);
    
    // 等待异步调用完成
    await waitFor(() => {
      expect(mockOnAnalysis).toHaveBeenCalledWith({ analysis: 'test analysis', confidence: 0.95 });
    });
  });
  
  // 推荐测试
  test('通过mcpbrain获取推荐', async () => {
    const mockOnRecommendation = jest.fn();
    render(<MCPAdapter onRecommendation={mockOnRecommendation} />);
    
    // 获取推荐按钮并点击
    const recommendButton = screen.getByTestId('recommend-button');
    fireEvent.click(recommendButton);
    
    // 验证mcpbrain.getRecommendation被调用
    expect(getRecommendation).toHaveBeenCalledTimes(1);
    
    // 等待异步调用完成
    await waitFor(() => {
      expect(mockOnRecommendation).toHaveBeenCalledWith(['recommendation1', 'recommendation2']);
    });
  });
  
  // 计划创建测试
  test('通过mcpplanner创建计划', async () => {
    const mockOnPlan = jest.fn();
    render(<MCPAdapter onPlan={mockOnPlan} />);
    
    // 获取计划按钮并点击
    const planButton = screen.getByTestId('create-plan-button');
    fireEvent.click(planButton);
    
    // 验证mcpplanner.createPlan被调用
    expect(createPlan).toHaveBeenCalledTimes(1);
    
    // 等待异步调用完成
    await waitFor(() => {
      expect(mockOnPlan).toHaveBeenCalledWith({ steps: ['step1', 'step2'], estimatedTime: '2min' });
    });
  });
  
  // 计划更新测试
  test('通过mcpplanner更新计划', async () => {
    const mockOnPlanUpdate = jest.fn();
    render(<MCPAdapter onPlanUpdate={mockOnPlanUpdate} />);
    
    // 获取更新按钮并点击
    const updateButton = screen.getByTestId('update-plan-button');
    fireEvent.click(updateButton);
    
    // 验证mcpplanner.updatePlan被调用
    expect(updatePlan).toHaveBeenCalledTimes(1);
    
    // 等待异步调用完成
    await waitFor(() => {
      expect(mockOnPlanUpdate).toHaveBeenCalledWith({ status: 'updated' });
    });
  });
  
  // 错误处理测试
  test('处理调用错误', async () => {
    // 模拟调用失败
    callTool.mockRejectedValueOnce(new Error('调用失败'));
    
    const mockOnError = jest.fn();
    render(<MCPAdapter onError={mockOnError} />);
    
    // 获取调用按钮并点击
    const callButton = screen.getByTestId('call-tool-button');
    fireEvent.click(callButton);
    
    // 等待异步调用完成
    await waitFor(() => {
      expect(mockOnError).toHaveBeenCalledWith(expect.any(Error));
    });
    
    // 验证错误状态显示
    expect(screen.getByText('调用失败')).toBeInTheDocument();
  });
  
  // 禁用状态测试
  test('禁用状态下的组件表现', () => {
    render(<MCPAdapter disabled={true} />);
    
    // 验证所有按钮被禁用
    const buttons = screen.getAllByRole('button');
    buttons.forEach(button => {
      expect(button).toBeDisabled();
    });
  });
});
