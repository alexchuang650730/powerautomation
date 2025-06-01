import React from 'react';

interface SidebarProps {
  className?: string;
}

const Sidebar: React.FC<SidebarProps> = ({ className }) => {
  return (
    <div className={`w-64 bg-white border-r border-gray-200 h-screen p-4 ${className}`}>
      <div className="flex items-center mb-8">
        <div className="w-8 h-8 rounded-full bg-gradient-to-r from-blue-400 to-purple-500 mr-2"></div>
        <h1 className="text-xl font-bold">PowerAutomation</h1>
      </div>
      
      <div className="mb-6">
        <div className="relative">
          <input 
            type="text" 
            placeholder="搜索 (⌘+k)"
            className="w-full px-3 py-2 pl-9 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <svg 
            className="absolute left-3 top-2.5 text-gray-400" 
            width="16" 
            height="16" 
            viewBox="0 0 24 24" 
            fill="none" 
            stroke="currentColor" 
            strokeWidth="2" 
            strokeLinecap="round" 
            strokeLinejoin="round"
          >
            <circle cx="11" cy="11" r="8"></circle>
            <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
          </svg>
        </div>
      </div>
      
      <nav>
        <ul className="space-y-1">
          <li>
            <a href="#" className="flex items-center px-3 py-2 text-gray-800 rounded-lg bg-blue-50">
              <svg 
                className="mr-3 text-blue-500" 
                width="20" 
                height="20" 
                viewBox="0 0 24 24" 
                fill="none" 
                stroke="currentColor" 
                strokeWidth="2" 
                strokeLinecap="round" 
                strokeLinejoin="round"
              >
                <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
                <polyline points="9 22 9 12 15 12 15 22"></polyline>
              </svg>
              首页
            </a>
          </li>
          <li>
            <a href="#" className="flex items-center px-3 py-2 text-gray-600 rounded-lg hover:bg-gray-100">
              <svg 
                className="mr-3 text-gray-400" 
                width="20" 
                height="20" 
                viewBox="0 0 24 24" 
                fill="none" 
                stroke="currentColor" 
                strokeWidth="2" 
                strokeLinecap="round" 
                strokeLinejoin="round"
              >
                <path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"></path>
              </svg>
              新建项目
            </a>
          </li>
          <li>
            <a href="#" className="flex items-center px-3 py-2 text-gray-600 rounded-lg hover:bg-gray-100">
              <svg 
                className="mr-3 text-gray-400" 
                width="20" 
                height="20" 
                viewBox="0 0 24 24" 
                fill="none" 
                stroke="currentColor" 
                strokeWidth="2" 
                strokeLinecap="round" 
                strokeLinejoin="round"
              >
                <path d="M13 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z"></path>
                <polyline points="13 2 13 9 20 9"></polyline>
              </svg>
              项目
            </a>
          </li>
          <li>
            <a href="#" className="flex items-center px-3 py-2 text-gray-600 rounded-lg hover:bg-gray-100">
              <svg 
                className="mr-3 text-gray-400" 
                width="20" 
                height="20" 
                viewBox="0 0 24 24" 
                fill="none" 
                stroke="currentColor" 
                strokeWidth="2" 
                strokeLinecap="round" 
                strokeLinejoin="round"
              >
                <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path>
                <polyline points="3.27 6.96 12 12.01 20.73 6.96"></polyline>
                <line x1="12" y1="22.08" x2="12" y2="12"></line>
              </svg>
              知识库
            </a>
          </li>
        </ul>
      </nav>
    </div>
  );
};

export default Sidebar;
