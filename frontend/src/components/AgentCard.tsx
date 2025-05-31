import React from 'react';
import { cn } from '../lib/utils';

export interface Agent {
  id: string;
  name: string;
  icon: string;
  description: string;
  isExpert: boolean;
}

interface AgentCardProps {
  agent: Agent;
  isActive: boolean;
  onClick?: (id: string) => void;
}

const AgentCard: React.FC<AgentCardProps> = ({ agent, isActive, onClick }) => {
  const { id, name, icon, isExpert } = agent;
  
  return (
    <div 
      className={cn(
        "flex flex-col items-center justify-center p-4 rounded-lg cursor-pointer transition-all",
        "border border-gray-200 hover:border-blue-400 hover:shadow-md",
        "bg-white hover:bg-blue-50",
        isActive ? "border-blue-500 shadow-md bg-blue-50" : ""
      )}
      onClick={() => onClick && onClick(id)}
    >
      {isExpert && (
        <div className="absolute top-2 right-2 bg-blue-600 text-white text-xs px-2 py-1 rounded-full">
          专家
        </div>
      )}
      <div className="text-3xl mb-2">{icon}</div>
      <div className="font-medium text-gray-800">{name}</div>
    </div>
  );
};

export default AgentCard;
