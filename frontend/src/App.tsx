import { useState } from 'react';
import AgentCard, { Agent } from './components/AgentCard';
import InputSection from './components/InputSection';
import './App.css';

// 智能体数据
const agents: Agent[] = [
  {
    id: 'ppt',
    name: 'PPT模式',
    icon: '🎯',
    description: '专业制作精美PPT，支持多种模板和风格',
    isExpert: true
  },
  {
    id: 'code',
    name: '代码模式',
    icon: '💻',
    description: '编写高质量代码，支持多种编程语言',
    isExpert: true
  },
  {
    id: 'web',
    name: '网页模式',
    icon: '🌐',
    description: '快速构建响应式网页，支持多种前端框架',
    isExpert: true
  },
  {
    id: 'general',
    name: '通用模式',
    icon: '✨',
    description: '处理各类通用任务，回答问题和提供建议',
    isExpert: true
  }
];

function App() {
  const [selectedAgent, setSelectedAgent] = useState<string>('ppt');
  
  // 处理智能体选择
  const handleAgentSelect = (id: string) => {
    setSelectedAgent(id);
  };
  
  // 处理消息发送
  const handleSendMessage = (text: string, file: File | null, agentType: string) => {
    console.log('Message sent:', { text, file, agentType });
    
    // 模拟将数据发送到后端对应的agents目录
    const formData = new FormData();
    formData.append('text', text);
    if (file) {
      formData.append('file', file);
    }
    formData.append('agentType', agentType);
    
    // 根据不同的智能体类型，将数据发送到不同的处理端点
    let endpoint = '';
    switch (agentType) {
      case 'ppt':
        endpoint = '/api/agents/ppt';
        break;
      case 'code':
        endpoint = '/api/agents/code';
        break;
      case 'web':
        endpoint = '/api/agents/web';
        break;
      case 'general':
        endpoint = '/api/agents/general';
        break;
      default:
        endpoint = '/api/agents/general';
    }
    
    // 这里是模拟发送请求，实际项目中应该使用fetch或axios发送真实请求
    console.log(`Sending data to ${endpoint}`, formData);
  };

  return (
    <div className="min-h-screen bg-gray-50 px-4 py-8">
      <div className="max-w-6xl mx-auto">
        <h1 className="platform-title">企业级多智能体协作平台 PowerAutomation</h1>
        
        <InputSection 
          selectedAgent={selectedAgent}
          onSendMessage={handleSendMessage}
        />
        
        <div className="agent-grid-container">
          {agents.map(agent => (
            <AgentCard 
              key={agent.id}
              agent={agent}
              isActive={selectedAgent === agent.id}
              onClick={handleAgentSelect}
            />
          ))}
        </div>
      </div>
    </div>
  );
}

export default App;
