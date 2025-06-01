/**
 * 代码智能体任务进度组件单元测试
 * 测试任务进度展示、状态变化和交互功能
 */
import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import TaskProgress from '../../components/TaskProgress';

describe('代码智能体任务进度组件', () => {
  // 基本渲染测试
  test('正确渲染任务进度组件', () => {
    const mockTasks = [
      { id: '1', title: '分析代码结构', completed: true, icon: 'code-structure' },
      { id: '2', title: '生成测试用例', completed: false, icon: 'test' },
      { id: '3', title: '优化性能瓶颈', completed: false, icon: 'performance' }
    ];
    
    render(<TaskProgress tasks={mockTasks} currentTaskIndex={1} totalTasks={3} />);
    
    // 验证标题存在
    expect(screen.getByText('任务进度')).toBeInTheDocument();
    
    // 验证进度计数
    expect(screen.getByText('1 / 3')).toBeInTheDocument();
    
    // 验证任务项目
    expect(screen.getByText('分析代码结构')).toBeInTheDocument();
    expect(screen.getByText('生成测试用例')).toBeInTheDocument();
    expect(screen.getByText('优化性能瓶颈')).toBeInTheDocument();
  });
  
  // 完成状态测试
  test('正确显示任务完成状态', () => {
    const mockTasks = [
      { id: '1', title: '分析代码结构', completed: true, icon: 'code-structure' },
      { id: '2', title: '生成测试用例', completed: false, icon: 'test' }
    ];
    
    render(<TaskProgress tasks={mockTasks} currentTaskIndex={1} totalTasks={2} />);
    
    // 获取任务项目
    const taskItems = screen.getAllByTestId('task-item');
    
    // 验证完成状态的CSS类
    expect(taskItems[0]).toHaveClass('completed');
    expect(taskItems[1]).not.toHaveClass('completed');
  });
  
  // 当前任务测试
  test('正确高亮当前任务', () => {
    const mockTasks = [
      { id: '1', title: '分析代码结构', completed: true, icon: 'code-structure' },
      { id: '2', title: '生成测试用例', completed: false, icon: 'test' },
      { id: '3', title: '优化性能瓶颈', completed: false, icon: 'performance' }
    ];
    
    render(<TaskProgress tasks={mockTasks} currentTaskIndex={2} totalTasks={3} />);
    
    // 获取任务项目
    const taskItems = screen.getAllByTestId('task-item');
    
    // 验证当前任务的CSS类
    expect(taskItems[0]).not.toHaveClass('current');
    expect(taskItems[1]).toHaveClass('current');
    expect(taskItems[2]).not.toHaveClass('current');
  });
  
  // 空任务列表测试
  test('处理空任务列表', () => {
    render(<TaskProgress tasks={[]} currentTaskIndex={0} totalTasks={0} />);
    
    // 验证标题存在
    expect(screen.getByText('任务进度')).toBeInTheDocument();
    
    // 验证进度计数
    expect(screen.getByText('0 / 0')).toBeInTheDocument();
    
    // 验证没有任务项目
    const taskList = screen.getByTestId('task-list');
    expect(taskList.children.length).toBe(0);
  });
  
  // 图标渲染测试
  test('正确渲染不同类型的图标', () => {
    const mockTasks = [
      { id: '1', title: '任务1', completed: false, icon: 'code-structure' },
      { id: '2', title: '任务2', completed: false, icon: 'test' },
      { id: '3', title: '任务3', completed: false, icon: 'performance' }
    ];
    
    render(<TaskProgress tasks={mockTasks} currentTaskIndex={1} totalTasks={3} />);
    
    // 获取图标元素
    const icons = screen.getAllByTestId('task-icon');
    
    // 验证图标类名
    expect(icons[0]).toHaveClass('code-structure');
    expect(icons[1]).toHaveClass('test');
    expect(icons[2]).toHaveClass('performance');
  });
  
  // 任务点击交互测试
  test('点击任务项触发回调', () => {
    const mockTasks = [
      { id: '1', title: '分析代码结构', completed: true, icon: 'code-structure' },
      { id: '2', title: '生成测试用例', completed: false, icon: 'test' }
    ];
    
    const mockOnTaskClick = jest.fn();
    
    render(
      <TaskProgress 
        tasks={mockTasks} 
        currentTaskIndex={1} 
        totalTasks={2} 
        onTaskClick={mockOnTaskClick} 
      />
    );
    
    // 点击第一个任务
    const taskItems = screen.getAllByTestId('task-item');
    fireEvent.click(taskItems[0]);
    
    // 验证回调被调用，且参数正确
    expect(mockOnTaskClick).toHaveBeenCalledWith('1');
  });
  
  // 进度条测试
  test('正确显示进度条', () => {
    const mockTasks = [
      { id: '1', title: '任务1', completed: true, icon: 'code-structure' },
      { id: '2', title: '任务2', completed: true, icon: 'test' },
      { id: '3', title: '任务3', completed: false, icon: 'performance' },
      { id: '4', title: '任务4', completed: false, icon: 'deploy' }
    ];
    
    render(<TaskProgress tasks={mockTasks} currentTaskIndex={3} totalTasks={4} />);
    
    // 获取进度条元素
    const progressBar = screen.getByTestId('progress-bar');
    
    // 验证进度条宽度（应为50%，因为2/4任务已完成）
    expect(progressBar).toHaveStyle('width: 50%');
  });
  
  // 任务详情展开/折叠测试
  test('点击任务可以展开/折叠详情', () => {
    const mockTasks = [
      { 
        id: '1', 
        title: '分析代码结构', 
        completed: true, 
        icon: 'code-structure',
        details: '分析代码的结构、依赖关系和性能瓶颈'
      }
    ];
    
    render(<TaskProgress tasks={mockTasks} currentTaskIndex={1} totalTasks={1} />);
    
    // 初始状态下详情应该是隐藏的
    expect(screen.queryByText('分析代码的结构、依赖关系和性能瓶颈')).not.toBeInTheDocument();
    
    // 点击任务项展开详情
    const taskItem = screen.getByTestId('task-item');
    fireEvent.click(taskItem);
    
    // 验证详情已显示
    expect(screen.getByText('分析代码的结构、依赖关系和性能瓶颈')).toBeInTheDocument();
    
    // 再次点击折叠详情
    fireEvent.click(taskItem);
    
    // 验证详情已隐藏
    expect(screen.queryByText('分析代码的结构、依赖关系和性能瓶颈')).not.toBeInTheDocument();
  });
});
