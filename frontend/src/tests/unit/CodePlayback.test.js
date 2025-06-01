/**
 * 代码智能体代码回放组件单元测试
 * 测试代码生成过程回放、控制和交互功能
 */
import React from 'react';
import { render, screen, fireEvent, act } from '@testing-library/react';
import '@testing-library/jest-dom';
import CodePlayback from '../../components/CodePlayback';

describe('代码智能体代码回放组件', () => {
  // 模拟代码生成步骤
  const mockCodeSteps = [
    { id: '1', code: '// 初始化函数\nfunction calculateTotal() {', timestamp: 1622505600000 },
    { id: '2', code: '// 初始化函数\nfunction calculateTotal(items) {', timestamp: 1622505605000 },
    { id: '3', code: '// 初始化函数\nfunction calculateTotal(items) {\n  let total = 0;', timestamp: 1622505610000 },
    { id: '4', code: '// 初始化函数\nfunction calculateTotal(items) {\n  let total = 0;\n  \n  // 遍历所有商品', timestamp: 1622505615000 },
    { id: '5', code: '// 初始化函数\nfunction calculateTotal(items) {\n  let total = 0;\n  \n  // 遍历所有商品\n  for (const item of items) {', timestamp: 1622505620000 },
    { id: '6', code: '// 初始化函数\nfunction calculateTotal(items) {\n  let total = 0;\n  \n  // 遍历所有商品\n  for (const item of items) {\n    total += item.price * item.quantity;', timestamp: 1622505625000 },
    { id: '7', code: '// 初始化函数\nfunction calculateTotal(items) {\n  let total = 0;\n  \n  // 遍历所有商品\n  for (const item of items) {\n    total += item.price * item.quantity;\n  }\n  \n  return total;', timestamp: 1622505630000 },
    { id: '8', code: '// 初始化函数\nfunction calculateTotal(items) {\n  let total = 0;\n  \n  // 遍历所有商品\n  for (const item of items) {\n    total += item.price * item.quantity;\n  }\n  \n  return total;\n}', timestamp: 1622505635000 }
  ];

  // 基本渲染测试
  test('正确渲染代码回放组件', () => {
    render(<CodePlayback codeSteps={mockCodeSteps} />);
    
    // 验证标题存在
    expect(screen.getByText('代码回放')).toBeInTheDocument();
    
    // 验证代码编辑器存在
    expect(screen.getByTestId('code-editor')).toBeInTheDocument();
    
    // 验证控制按钮存在
    expect(screen.getByTestId('play-button')).toBeInTheDocument();
    expect(screen.getByTestId('pause-button')).toBeInTheDocument();
    expect(screen.getByTestId('step-forward-button')).toBeInTheDocument();
    expect(screen.getByTestId('step-backward-button')).toBeInTheDocument();
  });
  
  // 播放控制测试
  test('播放按钮控制回放状态', () => {
    render(<CodePlayback codeSteps={mockCodeSteps} />);
    
    // 获取控制按钮
    const playButton = screen.getByTestId('play-button');
    const pauseButton = screen.getByTestId('pause-button');
    
    // 初始状态下播放按钮应该可用，暂停按钮应该禁用
    expect(playButton).not.toBeDisabled();
    expect(pauseButton).toBeDisabled();
    
    // 点击播放按钮
    fireEvent.click(playButton);
    
    // 播放状态下播放按钮应该禁用，暂停按钮应该可用
    expect(playButton).toBeDisabled();
    expect(pauseButton).not.toBeDisabled();
    
    // 点击暂停按钮
    fireEvent.click(pauseButton);
    
    // 暂停状态下播放按钮应该可用，暂停按钮应该禁用
    expect(playButton).not.toBeDisabled();
    expect(pauseButton).toBeDisabled();
  });
  
  // 步进控制测试
  test('步进按钮控制代码显示', () => {
    render(<CodePlayback codeSteps={mockCodeSteps} initialStepIndex={2} />);
    
    // 获取步进按钮
    const stepForwardButton = screen.getByTestId('step-forward-button');
    const stepBackwardButton = screen.getByTestId('step-backward-button');
    const codeEditor = screen.getByTestId('code-editor');
    
    // 初始状态应该显示第3步的代码
    expect(codeEditor).toHaveTextContent('let total = 0;');
    
    // 点击前进按钮
    fireEvent.click(stepForwardButton);
    
    // 应该显示第4步的代码
    expect(codeEditor).toHaveTextContent('// 遍历所有商品');
    
    // 点击后退按钮
    fireEvent.click(stepBackwardButton);
    
    // 应该回到第3步的代码
    expect(codeEditor).toHaveTextContent('let total = 0;');
    
    // 连续点击后退按钮到第一步
    fireEvent.click(stepBackwardButton);
    fireEvent.click(stepBackwardButton);
    
    // 应该显示第1步的代码
    expect(codeEditor).toHaveTextContent('function calculateTotal() {');
    
    // 此时后退按钮应该禁用
    expect(stepBackwardButton).toBeDisabled();
  });
  
  // 播放速度控制测试
  test('可以调整播放速度', () => {
    render(<CodePlayback codeSteps={mockCodeSteps} />);
    
    // 获取速度控制滑块
    const speedSlider = screen.getByTestId('speed-slider');
    
    // 初始速度应该是1x
    expect(speedSlider).toHaveValue('1');
    
    // 调整速度到2x
    fireEvent.change(speedSlider, { target: { value: '2' } });
    
    // 验证速度已更新
    expect(speedSlider).toHaveValue('2');
    expect(screen.getByText('2x')).toBeInTheDocument();
  });
  
  // 自动播放测试
  test('自动播放功能正常工作', async () => {
    jest.useFakeTimers();
    
    render(<CodePlayback codeSteps={mockCodeSteps} playbackSpeed={1} />);
    
    // 获取播放按钮和代码编辑器
    const playButton = screen.getByTestId('play-button');
    const codeEditor = screen.getByTestId('code-editor');
    
    // 点击播放按钮开始自动播放
    fireEvent.click(playButton);
    
    // 初始应该显示第1步的代码
    expect(codeEditor).toHaveTextContent('function calculateTotal() {');
    
    // 前进到第2步
    act(() => {
      jest.advanceTimersByTime(1000);
    });
    expect(codeEditor).toHaveTextContent('function calculateTotal(items) {');
    
    // 前进到第3步
    act(() => {
      jest.advanceTimersByTime(1000);
    });
    expect(codeEditor).toHaveTextContent('let total = 0;');
    
    jest.useRealTimers();
  });
  
  // 进度条测试
  test('进度条正确显示当前位置', () => {
    render(<CodePlayback codeSteps={mockCodeSteps} initialStepIndex={4} />);
    
    // 获取进度条
    const progressBar = screen.getByTestId('playback-progress');
    
    // 当前在第5步（索引4），总共8步，进度应该是5/8
    expect(progressBar).toHaveValue('5');
    expect(progressBar).toHaveAttribute('max', '8');
    
    // 拖动进度条到第7步
    fireEvent.change(progressBar, { target: { value: '7' } });
    
    // 验证代码已更新到第7步
    const codeEditor = screen.getByTestId('code-editor');
    expect(codeEditor).toHaveTextContent('return total;');
  });
  
  // 空步骤测试
  test('处理空代码步骤列表', () => {
    render(<CodePlayback codeSteps={[]} />);
    
    // 验证提示信息
    expect(screen.getByText('暂无代码生成记录')).toBeInTheDocument();
    
    // 所有控制按钮应该禁用
    expect(screen.getByTestId('play-button')).toBeDisabled();
    expect(screen.getByTestId('pause-button')).toBeDisabled();
    expect(screen.getByTestId('step-forward-button')).toBeDisabled();
    expect(screen.getByTestId('step-backward-button')).toBeDisabled();
  });
  
  // 时间戳显示测试
  test('正确显示代码生成时间戳', () => {
    render(<CodePlayback codeSteps={mockCodeSteps} initialStepIndex={2} />);
    
    // 获取时间戳显示
    const timestamp = screen.getByTestId('timestamp');
    
    // 验证时间戳格式正确（第3步的时间戳是1622505610000，对应的时间是2021-06-01 10:00:10）
    expect(timestamp).toHaveTextContent('10:00:10');
  });
});
