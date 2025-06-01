/**
 * InputSection组件单元测试
 * 使用新的CSS类选择器，覆盖所有UI状态和交互
 */
import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import InputSection from '../../components/InputSection';

describe('InputSection组件', () => {
  // 基本渲染测试
  test('正确渲染InputSection组件', () => {
    const mockProps = {
      selectedAgent: 'ppt',
      onSendMessage: jest.fn(),
      onFileUpload: jest.fn(),
      onSceneChange: jest.fn(),
      onNetworkToggle: jest.fn(),
      isOnline: true
    };
    
    render(<InputSection {...mockProps} />);
    
    // 使用新的CSS类选择器
    const inputSection = screen.getByTestId('input-section');
    expect(inputSection).toHaveClass('input-section');
    
    // 验证输入框存在
    const inputField = screen.getByPlaceholderText(/请输入您的需求/i);
    expect(inputField).toBeInTheDocument();
    
    // 验证发送按钮存在
    const sendButton = screen.getByTestId('send-button');
    expect(sendButton).toBeInTheDocument();
    
    // 验证文件上传按钮存在
    const fileUploadButton = screen.getByTestId('file-upload-button');
    expect(fileUploadButton).toBeInTheDocument();
    
    // 验证场景选择下拉菜单存在
    const sceneSelector = screen.getByTestId('scene-selector');
    expect(sceneSelector).toBeInTheDocument();
    expect(sceneSelector).toHaveTextContent('通用场景');
    
    // 验证联网开关存在
    const networkToggle = screen.getByTestId('network-toggle');
    expect(networkToggle).toBeInTheDocument();
    expect(networkToggle).toHaveClass('network-toggle-online');
  });
  
  // 输入文本测试
  test('输入文本并发送消息', () => {
    const mockSendMessage = jest.fn();
    const mockProps = {
      selectedAgent: 'code',
      onSendMessage: mockSendMessage,
      onFileUpload: jest.fn(),
      onSceneChange: jest.fn(),
      onNetworkToggle: jest.fn(),
      isOnline: true
    };
    
    render(<InputSection {...mockProps} />);
    
    // 获取输入框并输入文本
    const inputField = screen.getByPlaceholderText(/请输入您的需求/i);
    fireEvent.change(inputField, { target: { value: '测试消息内容' } });
    
    // 验证输入内容
    expect(inputField.value).toBe('测试消息内容');
    
    // 点击发送按钮
    const sendButton = screen.getByTestId('send-button');
    fireEvent.click(sendButton);
    
    // 验证发送回调被调用
    expect(mockSendMessage).toHaveBeenCalledTimes(1);
    expect(mockSendMessage).toHaveBeenCalledWith('测试消息内容', 'code');
    
    // 验证输入框被清空
    expect(inputField.value).toBe('');
  });
  
  // 文件上传测试
  test('上传文件功能', () => {
    const mockFileUpload = jest.fn();
    const mockProps = {
      selectedAgent: 'web',
      onSendMessage: jest.fn(),
      onFileUpload: mockFileUpload,
      onSceneChange: jest.fn(),
      onNetworkToggle: jest.fn(),
      isOnline: true
    };
    
    render(<InputSection {...mockProps} />);
    
    // 获取文件上传输入
    const fileInput = screen.getByTestId('file-input');
    
    // 模拟文件上传
    const file = new File(['测试文件内容'], 'test.txt', { type: 'text/plain' });
    fireEvent.change(fileInput, { target: { files: [file] } });
    
    // 验证上传回调被调用
    expect(mockFileUpload).toHaveBeenCalledTimes(1);
    expect(mockFileUpload).toHaveBeenCalledWith(file, 'web');
  });
  
  // 场景选择测试
  test('场景选择功能', () => {
    const mockSceneChange = jest.fn();
    const mockProps = {
      selectedAgent: 'general',
      onSendMessage: jest.fn(),
      onFileUpload: jest.fn(),
      onSceneChange: mockSceneChange,
      onNetworkToggle: jest.fn(),
      isOnline: true
    };
    
    render(<InputSection {...mockProps} />);
    
    // 点击场景选择器
    const sceneSelector = screen.getByTestId('scene-selector');
    fireEvent.click(sceneSelector);
    
    // 选择工作汇报场景
    const workReportOption = screen.getByText('工作汇报');
    fireEvent.click(workReportOption);
    
    // 验证场景变更回调被调用
    expect(mockSceneChange).toHaveBeenCalledTimes(1);
    expect(mockSceneChange).toHaveBeenCalledWith('work_report', 'general');
    
    // 验证选择器显示更新
    expect(sceneSelector).toHaveTextContent('工作汇报');
  });
  
  // 联网开关测试
  test('联网开关功能', () => {
    const mockNetworkToggle = jest.fn();
    const mockProps = {
      selectedAgent: 'ppt',
      onSendMessage: jest.fn(),
      onFileUpload: jest.fn(),
      onSceneChange: jest.fn(),
      onNetworkToggle: mockNetworkToggle,
      isOnline: true
    };
    
    const { rerender } = render(<InputSection {...mockProps} />);
    
    // 获取联网开关
    const networkToggle = screen.getByTestId('network-toggle');
    expect(networkToggle).toHaveClass('network-toggle-online');
    
    // 点击开关
    fireEvent.click(networkToggle);
    
    // 验证回调被调用
    expect(mockNetworkToggle).toHaveBeenCalledTimes(1);
    expect(mockNetworkToggle).toHaveBeenCalledWith(false, 'ppt');
    
    // 重新渲染为离线状态
    rerender(<InputSection {...mockProps} isOnline={false} />);
    
    // 验证样式变化
    expect(networkToggle).toHaveClass('network-toggle-offline');
    expect(networkToggle).not.toHaveClass('network-toggle-online');
  });
  
  // 不同智能体的提示文本测试
  test('根据选中的智能体显示不同的提示文本', () => {
    const mockProps = {
      selectedAgent: 'ppt',
      onSendMessage: jest.fn(),
      onFileUpload: jest.fn(),
      onSceneChange: jest.fn(),
      onNetworkToggle: jest.fn(),
      isOnline: true
    };
    
    const { rerender } = render(<InputSection {...mockProps} />);
    
    // PPT模式提示文本
    let inputField = screen.getByPlaceholderText(/请输入您的PPT需求/i);
    expect(inputField).toBeInTheDocument();
    
    // 代码模式提示文本
    rerender(<InputSection {...mockProps} selectedAgent="code" />);
    inputField = screen.getByPlaceholderText(/请输入您的代码需求/i);
    expect(inputField).toBeInTheDocument();
    
    // 网页模式提示文本
    rerender(<InputSection {...mockProps} selectedAgent="web" />);
    inputField = screen.getByPlaceholderText(/请输入您的网页需求/i);
    expect(inputField).toBeInTheDocument();
    
    // 通用模式提示文本
    rerender(<InputSection {...mockProps} selectedAgent="general" />);
    inputField = screen.getByPlaceholderText(/请输入您的需求/i);
    expect(inputField).toBeInTheDocument();
  });
  
  // 禁用状态测试
  test('禁用状态下的组件表现', () => {
    const mockProps = {
      selectedAgent: 'ppt',
      onSendMessage: jest.fn(),
      onFileUpload: jest.fn(),
      onSceneChange: jest.fn(),
      onNetworkToggle: jest.fn(),
      isOnline: true,
      disabled: true
    };
    
    render(<InputSection {...mockProps} />);
    
    // 验证输入框被禁用
    const inputField = screen.getByPlaceholderText(/请输入您的PPT需求/i);
    expect(inputField).toBeDisabled();
    
    // 验证发送按钮被禁用
    const sendButton = screen.getByTestId('send-button');
    expect(sendButton).toBeDisabled();
    expect(sendButton).toHaveClass('send-button-disabled');
    
    // 验证文件上传按钮被禁用
    const fileUploadButton = screen.getByTestId('file-upload-button');
    expect(fileUploadButton).toBeDisabled();
    expect(fileUploadButton).toHaveClass('file-upload-button-disabled');
  });
});
