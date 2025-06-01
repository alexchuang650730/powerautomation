/**
 * AgentCard组件单元测试
 * 使用新的CSS类选择器，覆盖所有UI状态
 */
import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import AgentCard from '../../components/AgentCard';

describe('AgentCard组件', () => {
  // 基本渲染测试
  test('正确渲染AgentCard组件', () => {
    const mockProps = {
      id: 'ppt',
      title: 'PPT模式',
      icon: 'target',
      isExpert: true,
      isSelected: false,
      onClick: jest.fn()
    };
    
    render(<AgentCard {...mockProps} />);
    
    // 使用新的CSS类选择器
    const cardElement = screen.getByTestId('agent-card-ppt');
    expect(cardElement).toHaveClass('agent-card');
    expect(cardElement).not.toHaveClass('agent-card-active');
    
    // 验证标题文本
    expect(screen.getByText('PPT模式')).toBeInTheDocument();
    
    // 验证专家标签
    const expertBadge = screen.getByText('专家');
    expect(expertBadge).toBeInTheDocument();
    expect(expertBadge).toHaveClass('expert-badge');
  });
  
  // 选中状态测试
  test('选中状态下正确应用active类', () => {
    const mockProps = {
      id: 'code',
      title: '代码模式',
      icon: 'laptop',
      isExpert: true,
      isSelected: true,
      onClick: jest.fn()
    };
    
    render(<AgentCard {...mockProps} />);
    
    // 验证选中状态的CSS类
    const cardElement = screen.getByTestId('agent-card-code');
    expect(cardElement).toHaveClass('agent-card');
    expect(cardElement).toHaveClass('agent-card-active');
  });
  
  // 点击事件测试
  test('点击时触发onClick回调', () => {
    const mockOnClick = jest.fn();
    const mockProps = {
      id: 'web',
      title: '网页模式',
      icon: 'globe',
      isExpert: false,
      isSelected: false,
      onClick: mockOnClick
    };
    
    render(<AgentCard {...mockProps} />);
    
    // 点击卡片
    const cardElement = screen.getByTestId('agent-card-web');
    fireEvent.click(cardElement);
    
    // 验证回调被调用
    expect(mockOnClick).toHaveBeenCalledTimes(1);
    expect(mockOnClick).toHaveBeenCalledWith('web');
  });
  
  // 悬停状态测试
  test('悬停状态下应用正确的样式', () => {
    const mockProps = {
      id: 'general',
      title: '通用模式',
      icon: 'sparkles',
      isExpert: true,
      isSelected: false,
      onClick: jest.fn()
    };
    
    render(<AgentCard {...mockProps} />);
    
    // 获取卡片元素
    const cardElement = screen.getByTestId('agent-card-general');
    
    // 模拟悬停
    fireEvent.mouseEnter(cardElement);
    
    // 验证悬停样式 (通过内联样式或类检查)
    // 注意：由于Jest DOM限制，可能需要检查特定属性或类名变化
    expect(cardElement).toHaveStyle('transform: translateY(-5px)');
    
    // 模拟离开悬停
    fireEvent.mouseLeave(cardElement);
    expect(cardElement).not.toHaveStyle('transform: translateY(-5px)');
  });
  
  // 图标渲染测试
  test('正确渲染不同类型的图标', () => {
    // PPT模式图标
    const pptProps = {
      id: 'ppt',
      title: 'PPT模式',
      icon: 'target',
      isExpert: true,
      isSelected: false,
      onClick: jest.fn()
    };
    
    const { rerender } = render(<AgentCard {...pptProps} />);
    expect(screen.getByTestId('icon-target')).toBeInTheDocument();
    
    // 代码模式图标
    rerender(<AgentCard {...pptProps} id="code" title="代码模式" icon="laptop" />);
    expect(screen.getByTestId('icon-laptop')).toBeInTheDocument();
    
    // 网页模式图标
    rerender(<AgentCard {...pptProps} id="web" title="网页模式" icon="globe" />);
    expect(screen.getByTestId('icon-globe')).toBeInTheDocument();
    
    // 通用模式图标
    rerender(<AgentCard {...pptProps} id="general" title="通用模式" icon="sparkles" />);
    expect(screen.getByTestId('icon-sparkles')).toBeInTheDocument();
  });
  
  // 自定义图标测试
  test('支持自定义图标URL', () => {
    const mockProps = {
      id: 'ppt',
      title: 'PPT模式',
      icon: 'custom',
      customIconUrl: '/assets/images/ppt_icon.png',
      isExpert: true,
      isSelected: false,
      onClick: jest.fn()
    };
    
    render(<AgentCard {...mockProps} />);
    
    // 验证自定义图标
    const customIcon = screen.getByAltText('PPT模式');
    expect(customIcon).toBeInTheDocument();
    expect(customIcon).toHaveAttribute('src', '/assets/images/ppt_icon.png');
    expect(customIcon).toHaveClass('agent-card-custom-icon');
  });
});
