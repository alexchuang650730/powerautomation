/**
 * TaskPlayback组件单元测试
 * 使用新的CSS类选择器，覆盖所有UI状态
 */
import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import TaskPlayback from '../../components/TaskPlayback';

describe('TaskPlayback组件', () => {
  // 基本渲染测试
  test('正确渲染TaskPlayback组件', () => {
    const mockPlaybackData = {
      title: 'AgentCard.test.js',
      content: '/**\n * AgentCard组件单元测试\n * 使用新的CSS类选择器，覆盖所有UI状态\n */\nimport React from \'react\';\nimport { render, screen, fireEvent } from \'@testing-library/react\';\n',
      language: 'javascript',
      timestamp: '2025-06-01T12:30:45Z'
    };
    
    render(<TaskPlayback playbackData={mockPlaybackData} />);
    
    // 验证标题存在
    expect(screen.getByText('AgentCard.test.js')).toBeInTheDocument();
    
    // 验证代码内容
    expect(screen.getByText(/AgentCard组件单元测试/)).toBeInTheDocument();
    
    // 验证时间戳
    const formattedDate = new Date(mockPlaybackData.timestamp).toLocaleString();
    expect(screen.getByText(formattedDate)).toBeInTheDocument();
  });
  
  // 代码高亮测试
  test('正确应用代码高亮', () => {
    const mockPlaybackData = {
      title: 'example.js',
      content: 'function test() {\n  console.log("Hello");\n  return true;\n}',
      language: 'javascript',
      timestamp: '2025-06-01T12:30:45Z'
    };
    
    render(<TaskPlayback playbackData={mockPlaybackData} />);
    
    // 验证代码容器存在
    const codeContainer = screen.getByTestId('code-container');
    expect(codeContainer).toBeInTheDocument();
    
    // 验证语法高亮应用
    expect(codeContainer).toHaveClass('language-javascript');
    
    // 验证关键字高亮
    const keywords = screen.getAllByTestId('keyword');
    expect(keywords.length).toBeGreaterThan(0);
    expect(keywords[0]).toHaveClass('token-keyword');
  });
  
  // 控制按钮测试
  test('播放控制按钮功能正常', () => {
    const mockPlaybackData = {
      title: 'example.js',
      content: 'console.log("Test");',
      language: 'javascript',
      timestamp: '2025-06-01T12:30:45Z'
    };
    
    const mockOnPrevious = jest.fn();
    const mockOnNext = jest.fn();
    const mockOnPlay = jest.fn();
    
    render(
      <TaskPlayback 
        playbackData={mockPlaybackData}
        onPrevious={mockOnPrevious}
        onNext={mockOnNext}
        onPlay={mockOnPlay}
      />
    );
    
    // 获取控制按钮
    const previousButton = screen.getByTestId('previous-button');
    const playButton = screen.getByTestId('play-button');
    const nextButton = screen.getByTestId('next-button');
    
    // 点击按钮
    fireEvent.click(previousButton);
    fireEvent.click(playButton);
    fireEvent.click(nextButton);
    
    // 验证回调被调用
    expect(mockOnPrevious).toHaveBeenCalledTimes(1);
    expect(mockOnPlay).toHaveBeenCalledTimes(1);
    expect(mockOnNext).toHaveBeenCalledTimes(1);
  });
  
  // 实时模式测试
  test('实时模式下的组件表现', () => {
    const mockPlaybackData = {
      title: 'example.js',
      content: 'console.log("Test");',
      language: 'javascript',
      timestamp: '2025-06-01T12:30:45Z',
      isLive: true
    };
    
    render(<TaskPlayback playbackData={mockPlaybackData} />);
    
    // 验证实时标志存在
    const liveIndicator = screen.getByText('实时');
    expect(liveIndicator).toBeInTheDocument();
    expect(liveIndicator).toHaveClass('live-indicator');
    
    // 验证实时模式下的特殊样式
    const playbackContainer = screen.getByTestId('playback-container');
    expect(playbackContainer).toHaveClass('live-mode');
  });
  
  // 空数据测试
  test('处理空数据', () => {
    render(<TaskPlayback playbackData={null} />);
    
    // 验证空状态提示
    expect(screen.getByText('暂无回放数据')).toBeInTheDocument();
  });
  
  // 不同语言测试
  test('支持不同编程语言的高亮', () => {
    const pythonData = {
      title: 'example.py',
      content: 'def test():\n    print("Hello")\n    return True',
      language: 'python',
      timestamp: '2025-06-01T12:30:45Z'
    };
    
    const { rerender } = render(<TaskPlayback playbackData={pythonData} />);
    
    // 验证Python高亮
    let codeContainer = screen.getByTestId('code-container');
    expect(codeContainer).toHaveClass('language-python');
    
    // 重新渲染为HTML
    const htmlData = {
      title: 'example.html',
      content: '<div class="test">Hello</div>',
      language: 'html',
      timestamp: '2025-06-01T12:30:45Z'
    };
    
    rerender(<TaskPlayback playbackData={htmlData} />);
    
    // 验证HTML高亮
    codeContainer = screen.getByTestId('code-container');
    expect(codeContainer).toHaveClass('language-html');
  });
});
