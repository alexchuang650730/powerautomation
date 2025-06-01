/**
 * ThoughtActionRecorder组件单元测试
 * 使用新的CSS类选择器，覆盖所有UI状态
 */
import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import ThoughtActionRecorder from '../../components/ThoughtActionRecorder';

describe('ThoughtActionRecorder组件', () => {
  // 基本渲染测试
  test('正确渲染ThoughtActionRecorder组件', () => {
    const mockThoughts = [
      { id: '1', type: 'thinking', content: '分析测试日志中的错误模式', timestamp: '12:30:45' },
      { id: '2', type: 'action', content: '执行代码静态分析', timestamp: '12:31:20' },
      { id: '3', type: 'thinking', content: '识别到可能的内存泄漏问题', timestamp: '12:32:05' }
    ];
    
    render(<ThoughtActionRecorder thoughts={mockThoughts} />);
    
    // 验证标题存在
    expect(screen.getByText('思考与行动记录')).toBeInTheDocument();
    
    // 验证思考和行动内容
    expect(screen.getByText('分析测试日志中的错误模式')).toBeInTheDocument();
    expect(screen.getByText('执行代码静态分析')).toBeInTheDocument();
    expect(screen.getByText('识别到可能的内存泄漏问题')).toBeInTheDocument();
    
    // 验证时间戳
    expect(screen.getByText('12:30:45')).toBeInTheDocument();
    expect(screen.getByText('12:31:20')).toBeInTheDocument();
    expect(screen.getByText('12:32:05')).toBeInTheDocument();
  });
  
  // 不同类型项目测试
  test('正确区分思考和行动项目', () => {
    const mockThoughts = [
      { id: '1', type: 'thinking', content: '分析问题', timestamp: '12:30:45' },
      { id: '2', type: 'action', content: '执行修复', timestamp: '12:31:20' }
    ];
    
    render(<ThoughtActionRecorder thoughts={mockThoughts} />);
    
    // 获取思考和行动项目
    const thinkingItem = screen.getByText('分析问题').closest('.thought-item');
    const actionItem = screen.getByText('执行修复').closest('.thought-item');
    
    // 验证CSS类
    expect(thinkingItem).toHaveClass('thinking');
    expect(actionItem).toHaveClass('action');
  });
  
  // 空记录测试
  test('处理空记录列表', () => {
    render(<ThoughtActionRecorder thoughts={[]} />);
    
    // 验证标题存在
    expect(screen.getByText('思考与行动记录')).toBeInTheDocument();
    
    // 验证空状态提示
    expect(screen.getByText('暂无思考与行动记录')).toBeInTheDocument();
  });
  
  // 长内容测试
  test('正确处理长内容', () => {
    const longContent = '这是一段非常长的内容，用于测试组件如何处理长文本。这段文本应该会被正确地显示，可能会自动换行或者使用省略号，取决于组件的实现方式。无论如何，组件应该能够优雅地处理这种情况，而不是出现布局错乱或者文本溢出等问题。';
    
    const mockThoughts = [
      { id: '1', type: 'thinking', content: longContent, timestamp: '12:30:45' }
    ];
    
    render(<ThoughtActionRecorder thoughts={mockThoughts} />);
    
    // 验证长内容被正确渲染
    expect(screen.getByText(longContent)).toBeInTheDocument();
    
    // 验证容器样式（这里假设有最大高度和溢出滚动）
    const contentContainer = screen.getByText(longContent).closest('.thought-content');
    expect(contentContainer).toHaveStyle('max-height: 100px');
    expect(contentContainer).toHaveStyle('overflow-y: auto');
  });
  
  // 高亮最新项目测试
  test('高亮显示最新项目', () => {
    const mockThoughts = [
      { id: '1', type: 'thinking', content: '第一条思考', timestamp: '12:30:45' },
      { id: '2', type: 'action', content: '第一个行动', timestamp: '12:31:20' },
      { id: '3', type: 'thinking', content: '最新的思考', timestamp: '12:32:05', isLatest: true }
    ];
    
    render(<ThoughtActionRecorder thoughts={mockThoughts} />);
    
    // 获取最新项目
    const latestItem = screen.getByText('最新的思考').closest('.thought-item');
    
    // 验证高亮CSS类
    expect(latestItem).toHaveClass('latest');
    
    // 验证非最新项目没有高亮
    const normalItem = screen.getByText('第一条思考').closest('.thought-item');
    expect(normalItem).not.toHaveClass('latest');
  });
});
