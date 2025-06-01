import React from 'react';
import '../styles/TaskProgress.css';

interface Task {
  id: string;
  title: string;
  completed: boolean;
  icon: string;
}

interface TaskProgressProps {
  tasks: Task[];
  currentTaskIndex: number;
  totalTasks: number;
}

const TaskProgress: React.FC<TaskProgressProps> = ({ tasks, currentTaskIndex, totalTasks }) => {
  return (
    <div className="task-progress-container">
      <div className="task-progress-header">
        <h2>任务进度</h2>
        <span className="task-progress-count">{currentTaskIndex} / {totalTasks}</span>
      </div>
      
      <div className="task-list">
        {tasks.map((task, index) => (
          <div 
            key={task.id} 
            className={`task-item ${task.completed ? 'completed' : ''} ${index === currentTaskIndex - 1 ? 'current' : ''}`}
          >
            <div className="task-icon">
              <i className={task.icon}></i>
            </div>
            <div className="task-title">{task.title}</div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default TaskProgress;
