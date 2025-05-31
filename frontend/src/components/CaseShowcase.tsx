import React, { useState } from 'react';
import { Agent } from './AgentCard';

interface CaseShowcaseProps {
  cases: {
    id: number;
    title: string;
    image: string;
    thumbnail: string;
  }[];
  currentAgent?: Agent;
}

const CaseShowcase: React.FC<CaseShowcaseProps> = ({ cases, currentAgent }) => {
  const [activeCase, setActiveCase] = useState(cases[0]?.id);

  return (
    <div className="mt-6">
      <div className="grid grid-cols-3 gap-4">
        {cases.map((caseItem) => (
          <div 
            key={caseItem.id}
            className={`
              relative overflow-hidden rounded-lg border cursor-pointer transition-all
              ${activeCase === caseItem.id ? 'border-blue-500 shadow-md' : 'border-gray-200 hover:border-blue-300'}
            `}
            onClick={() => setActiveCase(caseItem.id)}
          >
            <div className="aspect-video bg-gray-100 flex items-center justify-center">
              <img 
                src={caseItem.thumbnail} 
                alt={caseItem.title}
                className="w-full h-full object-cover"
                onError={(e) => {
                  // 如果图片加载失败，显示占位符
                  e.currentTarget.src = 'https://via.placeholder.com/300x200?text=示例案例';
                }}
              />
            </div>
            <div className="p-3">
              <h3 className="text-sm font-medium text-gray-800 line-clamp-2">{caseItem.title}</h3>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default CaseShowcase;
