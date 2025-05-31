import { useState } from 'react';
import Header from './components/Header';
import Sidebar from './components/Sidebar';
import SearchBar from './components/SearchBar';
import AgentCard, { Agent } from './components/AgentCard';
import CaseShowcase from './components/CaseShowcase';
import { AgentType, sendQuery } from './lib/api';

// 智能体数据
const agents: Agent[] = [
  {
    id: 'ppt_agent',
    name: 'PPT智能体',
    icon: '📊',
    description: '专业制作精美PPT，支持多种模板和风格',
    isExpert: true
  },
  {
    id: 'web_agent',
    name: '网页智能体',
    icon: '🌐',
    description: '快速构建响应式网页，支持多种前端框架',
    isExpert: true
  },
  {
    id: 'code_agent',
    name: '代码智能体',
    icon: '💻',
    description: '编写高质量代码，支持多种编程语言',
    isExpert: true
  },
  {
    id: 'general_agent',
    name: '通用智能体',
    icon: '🤖',
    description: '处理各类通用任务，回答问题和提供建议',
    isExpert: true
  }
];

// 案例数据
const showcaseCases = [
  {
    id: 1,
    title: '企业年度报告PPT',
    image: 'https://via.placeholder.com/800x450?text=企业年度报告PPT',
    thumbnail: 'https://via.placeholder.com/300x200?text=企业年度报告PPT'
  },
  {
    id: 2,
    title: '响应式电商网站',
    image: 'https://via.placeholder.com/800x450?text=响应式电商网站',
    thumbnail: 'https://via.placeholder.com/300x200?text=响应式电商网站'
  },
  {
    id: 3,
    title: '数据分析可视化',
    image: 'https://via.placeholder.com/800x450?text=数据分析可视化',
    thumbnail: 'https://via.placeholder.com/300x200?text=数据分析可视化'
  }
];

function App() {
  const [selectedAgent, setSelectedAgent] = useState<Agent | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [response, setResponse] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  // 处理智能体选择
  const handleAgentSelect = (id: string) => {
    const agent = agents.find(a => a.id === id) || null;
    setSelectedAgent(agent);
    // 清除之前的响应和错误
    setResponse(null);
    setError(null);
  };

  // 处理搜索提交
  const handleSearch = async (query: string) => {
    if (!selectedAgent) {
      setError('请先选择一个智能体');
      return;
    }

    try {
      setIsLoading(true);
      setError(null);
      setResponse(null);
      
      // 发送请求到对应的智能体
      const result = await sendQuery(selectedAgent.id as AgentType, query);
      
      if (result.status === 'success') {
        setResponse(JSON.stringify(result.data, null, 2));
      } else {
        setError(result.message || '请求失败');
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : '未知错误');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex h-screen bg-gray-50">
      {/* 左侧边栏 */}
      <Sidebar className="hidden md:block" />
      
      {/* 主内容区 */}
      <div className="flex-1 flex flex-col overflow-hidden">
        <Header className="bg-white" />
        
        <main className="flex-1 overflow-y-auto p-6">
          <div className="max-w-6xl mx-auto">
            <h1 className="text-3xl font-bold text-gray-800 mb-6">PowerAutomation 自动化平台</h1>
            
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
              {agents.map(agent => (
                <AgentCard 
                  key={agent.id}
                  agent={agent}
                  isActive={selectedAgent?.id === agent.id}
                  onClick={handleAgentSelect}
                />
              ))}
            </div>
            
            <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
              <h2 className="text-xl font-semibold text-gray-800 mb-4">
                {selectedAgent ? `与${selectedAgent.name}对话` : '请选择一个智能体开始对话'}
              </h2>
              
              <SearchBar 
                placeholder={selectedAgent 
                  ? `向${selectedAgent.name}提问...` 
                  : "请先选择一个智能体..."
                }
                onSearch={handleSearch}
              />
              
              {selectedAgent && (
                <div className="mt-4 text-sm text-gray-600">
                  <p>{selectedAgent.description}</p>
                </div>
              )}
              
              {/* 加载状态 */}
              {isLoading && (
                <div className="mt-4 p-4 bg-blue-50 rounded-lg">
                  <div className="flex items-center justify-center">
                    <svg className="animate-spin h-5 w-5 text-blue-500 mr-2" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    <span>正在处理您的请求...</span>
                  </div>
                </div>
              )}
              
              {/* 错误信息 */}
              {error && (
                <div className="mt-4 p-4 bg-red-50 text-red-700 rounded-lg">
                  <p className="font-medium">错误：{error}</p>
                </div>
              )}
              
              {/* 响应结果 */}
              {response && (
                <div className="mt-4 p-4 bg-green-50 rounded-lg">
                  <h3 className="font-medium text-green-800 mb-2">响应结果：</h3>
                  <pre className="bg-white p-3 rounded border border-green-200 overflow-x-auto text-sm">
                    {response}
                  </pre>
                </div>
              )}
            </div>
            
            <div className="mt-8">
              <h2 className="text-xl font-semibold text-gray-800 mb-4">精选案例</h2>
              <CaseShowcase cases={showcaseCases} currentAgent={selectedAgent || undefined} />
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}

export default App;
