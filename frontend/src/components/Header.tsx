import React from 'react';

interface HeaderProps {
  className?: string;
}

const Header: React.FC<HeaderProps> = ({ className }) => {
  return (
    <header className={`flex items-center justify-between p-4 border-b border-gray-200 ${className}`}>
      <div className="flex-1"></div>
      
      <div className="flex items-center space-x-4">
        <button className="flex items-center px-3 py-1.5 text-sm text-gray-600 border border-gray-300 rounded-full hover:bg-gray-100">
          <svg 
            className="mr-1.5 text-gray-500" 
            width="16" 
            height="16" 
            viewBox="0 0 24 24" 
            fill="none" 
            stroke="currentColor" 
            strokeWidth="2" 
            strokeLinecap="round" 
            strokeLinejoin="round"
          >
            <path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"></path>
            <circle cx="12" cy="7" r="4"></circle>
          </svg>
          登录/注册
        </button>
        
        <div className="relative">
          <button className="flex items-center justify-center w-8 h-8 bg-blue-100 text-blue-600 rounded-full">
            <svg 
              width="18" 
              height="18" 
              viewBox="0 0 24 24" 
              fill="none" 
              stroke="currentColor" 
              strokeWidth="2" 
              strokeLinecap="round" 
              strokeLinejoin="round"
            >
              <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
              <circle cx="12" cy="7" r="4"></circle>
            </svg>
          </button>
        </div>
      </div>
    </header>
  );
};

export default Header;
