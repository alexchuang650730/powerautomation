# PowerAutomation 前端使用指南

## 项目概述

PowerAutomation 前端是一个基于 React + TypeScript + Tailwind CSS 的现代化 Web 应用，提供了类似 Skywork.ai 的两栏布局界面，展示四个专业智能体（PPT智能体、网页智能体、代码智能体、通用智能体），并支持与后端智能体服务的无缝通信。

## 目录结构

```
frontend/
├── public/                 # 静态资源
├── src/                    # 源代码
│   ├── assets/             # 图片、图标等资源
│   ├── components/         # 可复用组件
│   │   ├── AgentCard.tsx   # 智能体卡片组件
│   │   ├── CaseShowcase.tsx # 案例展示组件
│   │   ├── Header.tsx      # 页面头部组件
│   │   ├── SearchBar.tsx   # 搜索输入组件
│   │   ├── Sidebar.tsx     # 侧边栏组件
│   │   └── ui/             # UI基础组件
│   ├── hooks/              # 自定义React Hooks
│   ├── lib/                # 工具库
│   │   ├── api.ts          # API接口封装
│   │   └── utils.ts        # 通用工具函数
│   ├── App.tsx             # 应用主组件
│   ├── main.tsx            # 应用入口
│   └── index.css           # 全局样式
├── package.json            # 项目依赖
└── tsconfig.json           # TypeScript配置
```

## 安装与启动

### 环境要求

- Node.js 18.0.0 或更高版本
- npm 9.0.0 或更高版本（或使用 pnpm/yarn）

### 安装依赖

```bash
cd frontend
npm install
```

### 启动开发服务器

```bash
npm run dev
```

应用将在 http://localhost:5173 启动。

### 构建生产版本

```bash
npm run build
```

构建后的文件将位于 `dist` 目录中。

## 智能体交互流程

1. **选择智能体**：用户首先需要点击选择一个智能体（PPT、网页、代码或通用）
2. **输入需求**：在输入框中输入具体需求或问题
3. **提交请求**：点击发送按钮，前端会将请求路由到对应的后端智能体服务
4. **处理响应**：前端接收后端响应并展示结果

## 与后端通信

前端通过 `src/lib/api.ts` 中的接口与后端通信，主要函数包括：

- `sendToAgent(agentType, endpoint, data)`: 向指定智能体发送请求
- `sendQuery(agentType, query)`: 根据智能体类型发送通用查询

每个智能体对应的后端路由如下：

- PPT智能体: `/api/ppt_agent/*`
- 网页智能体: `/api/web_agent/*`
- 代码智能体: `/api/code_agent/*`
- 通用智能体: `/api/general_agent/*`

## 自定义与扩展

### 添加新智能体

1. 在 `App.tsx` 中的 `agents` 数组添加新智能体定义
2. 在 `src/lib/api.ts` 中添加对应的 API 调用函数
3. 确保后端有对应的路由和服务实现

### 修改界面样式

项目使用 Tailwind CSS 进行样式管理，可以通过修改组件中的类名来调整样式。主题配置位于 `tailwind.config.js` 文件中。

## 常见问题

### 跨域请求问题

如果遇到跨域请求问题，请确保后端服务已正确配置 CORS 头信息。在开发环境中，可以在 `vite.config.ts` 中配置代理：

```typescript
export default defineConfig({
  // ...其他配置
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:5000',
        changeOrigin: true,
      },
    },
  },
});
```

### 后端连接失败

如果无法连接到后端服务，请检查：

1. 后端服务是否正在运行
2. API 基础 URL 是否正确（在 `src/lib/api.ts` 中配置）
3. 网络连接是否正常

## 无限上下文记忆功能

PowerAutomation 前端支持无限上下文记忆功能，使 MCP Planner 和 MCP Brainstorm 能够找到合适的工具生产优质内容。此功能通过以下方式实现：

1. 保存用户与智能体的完整对话历史
2. 在发送新请求时附带上下文信息
3. 智能体能够基于历史对话提供连贯的回复

要启用此功能，请确保在与智能体交互时保持同一会话，系统会自动处理上下文记忆。
