/**
 * TaskProgress组件单元测试
 * 使用新的CSS类选择器，覆盖所有UI状态
 */
import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import TaskProgress from '../../components/TaskProgress';

describe('TaskProgress组件', () => {
  // 基本渲染测试
  test('正确渲染TaskProgress组件', () => {
    const mockTasks = [
      { id: '1', title: '更新通用智能体六大特性', completed: true, icon: 'clock' },
      { id: '2', title: '重新运行TestAndIssueCollector脚本', completed: false, icon: 'clock' },
      { id: '3', title: '分析测试日志并提取问题信息', completed: false, icon: 'clock' }
    ];
    
    render(<TaskProgress tasks={mockTasks} currentTaskIndex={1} totalTasks={3} />);
    
    // 验证标题存在
    expect(screen.getByText('任务进度')).toBeInTheDocument();
    
    // 验证进度计数
    expect(screen.getByText('1 / 3')).toBeInTheDocument();
    
    // 验证任务项目
    expect(screen.getByText('更新通用智能体六大特性')).toBeInTheDocument();
    expect(screen.getByText('重新运行TestAndIssueCollector脚本')).toBeInTheDocument();
    expect(screen.getByText('分析测试日志并提取问题信息')).toBeInTheDocument();
  });
  
  // 完成状态测试
  test('正确显示任务完成状态', () => {
    const mockTasks = [
      { id: '1', title: '更新通用智能体六大特性', completed: true, icon: 'clock' },
      { id: '2', title: '重新运行TestAndIssueCollector脚本', completed: false, icon: 'clock' }
    ];
    
    render(<TaskProgress tasks={mockTasks} currentTaskIndex={1} totalTasks={2} />);
    
    // 获取任务项目
    const taskItems = screen.getAllByRole('listitem');
    
    // 验证完成状态的CSS类
    expect(taskItems[0]).toHaveClass('completed');
    expect(taskItems[1]).not.toHaveClass('completed');
  });
  
  // 当前任务测试
  test('正确高亮当前任务', () => {
    const mockTasks = [
      { id: '1', title: '更新通用智能体六大特性', completed: true, icon: 'clock' },
      { id: '2', title: '重新运行TestAndIssueCollector脚本', completed: false, icon: 'clock' },
      { id: '3', title: '分析测试日志并提取问题信息', completed: false, icon: 'clock' }
    ];
    
    render(<TaskProgress tasks={mockTasks} currentTaskIndex={2} totalTasks={3} />);
    
    // 获取任务项目
    const taskItems = screen.getAllByRole('listitem');
    
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
    const taskList = screen.getByRole('list');
    expect(taskList.children.length).toBe(0);
  });
  
  // 图标渲染测试
  test('正确渲染不同类型的图标', () => {
    const mockTasks = [
      { id: '1', title: '任务1', completed: false, icon: 'clock' },
      { id: '2', title: '任务2', completed: false, icon: 'check' },
      { id: '3', title: '任务3', completed: false, icon: 'warning' }
    ];
    
    render(<TaskProgress tasks={mockTasks} currentTaskIndex={1} totalTasks={3} />);
    
    // 获取图标元素
    const icons = screen.getAllByTestId('task-icon');
    
    // 验证图标类名
    expect(icons[0]).toHaveClass('clock');
    expect(icons[1]).toHaveClass('check');
    expect(icons[2]).toHaveClass('warning');
  });
});
