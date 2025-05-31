/**
 * API接口封装
 * 负责与后端不同智能体的通信
 */

// 基础API URL
const API_BASE_URL = 'http://localhost:5000/api';

// 智能体类型
export type AgentType = 'ppt_agent' | 'web_agent' | 'code_agent' | 'general_agent';

// API响应接口
interface ApiResponse<T = any> {
  status: 'success' | 'error';
  data?: T;
  message?: string;
}

/**
 * 发送请求到指定智能体
 * @param agentType 智能体类型
 * @param endpoint API端点
 * @param data 请求数据
 * @returns Promise<ApiResponse>
 */
export async function sendToAgent<T = any>(
  agentType: AgentType, 
  endpoint: string, 
  data: any
): Promise<ApiResponse<T>> {
  try {
    const response = await fetch(`${API_BASE_URL}/${agentType}/${endpoint}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    
    const result = await response.json();
    return {
      status: 'success',
      data: result,
    };
  } catch (error) {
    console.error(`Error communicating with ${agentType}:`, error);
    return {
      status: 'error',
      message: error instanceof Error ? error.message : '未知错误',
    };
  }
}

/**
 * 向PPT智能体发送请求
 * @param topic PPT主题
 * @param content PPT内容
 * @param template 模板名称
 * @returns Promise<ApiResponse>
 */
export async function generatePPT(topic: string, content: string, template?: string) {
  return sendToAgent('ppt_agent', 'generate_ppt', { topic, content, template });
}

/**
 * 向网页智能体发送请求
 * @param title 网页标题
 * @param content 网页内容
 * @param template 模板名称
 * @returns Promise<ApiResponse>
 */
export async function generateWebpage(title: string, content: string, template?: string) {
  return sendToAgent('web_agent', 'generate_webpage', { title, content, template });
}

/**
 * 向代码智能体发送请求
 * @param language 编程语言
 * @param requirement 需求描述
 * @returns Promise<ApiResponse>
 */
export async function generateCode(language: string, requirement: string) {
  return sendToAgent('code_agent', 'generate_code', { language, requirement });
}

/**
 * 向通用智能体发送请求
 * @param query 用户查询
 * @returns Promise<ApiResponse>
 */
export async function queryGeneralAgent(query: string) {
  return sendToAgent('general_agent', 'query', { query });
}

/**
 * 根据智能体类型发送通用查询
 * @param agentType 智能体类型
 * @param query 用户查询
 * @returns Promise<ApiResponse>
 */
export async function sendQuery(agentType: AgentType, query: string) {
  switch (agentType) {
    case 'ppt_agent':
      return generatePPT('自动生成', query);
    case 'web_agent':
      return generateWebpage('自动生成', query);
    case 'code_agent':
      return generateCode('auto', query);
    case 'general_agent':
      return queryGeneralAgent(query);
    default:
      return {
        status: 'error',
        message: '未知的智能体类型',
      };
  }
}
