# PowerAutomation 本地环境启动指南

## 后端启动指南

### 安装依赖
```bash
# 在项目根目录下执行
pip install -r requirements.txt
```

### 启动后端服务
```bash
# 在项目根目录下执行
python run_backend.py
```

> **注意**: 不要直接运行 `backend/main.py`，这可能会导致导入错误。请始终使用项目根目录下的 `run_backend.py` 启动后端服务。

### 验证后端服务
后端服务启动后，可以通过访问以下URL验证服务是否正常运行：
```
http://localhost:5000/api/health
```

## 前端启动指南

### 安装依赖
```bash
# 进入前端目录
cd frontend

# 使用Node.js v16或v18版本(推荐)
# 如果使用nvm管理Node.js版本
nvm install 16
nvm use 16

# 安装依赖
npm install
# 安装Vite兼容性所需依赖
npm install crypto-js @vitejs/plugin-react --save-dev
```

如果遇到npm安装错误，可以尝试以下解决方案：
1. 清除npm缓存: `npm cache clean --force`
2. 删除node_modules目录和package-lock.json: `rm -rf node_modules package-lock.json`
3. 使用兼容的Node.js版本(推荐v16.x或v18.x)
4. 使用yarn替代npm: `yarn install`

### 启动前端服务
```bash
# 在frontend目录下执行
npm run dev
```

前端服务启动后，可以通过浏览器访问:
```
http://localhost:5173
```

## 常见问题解决

### 后端导入错误
如果遇到导入错误，请确保使用`run_backend.py`启动后端服务，该脚本会自动处理Python模块导入路径问题。

### 前端依赖安装错误
前端使用了较新版本的依赖，可能与某些Node.js版本不兼容。建议使用Node.js v16.x或v18.x版本，这些版本与大多数依赖兼容性较好。

### Vite兼容性问题
如果遇到`crypto.getRandomValues is not a function`错误，项目已添加vite.config.js配置文件解决此问题。确保安装了crypto-js和@vitejs/plugin-react依赖。

### 样式文件缺失
如果遇到样式文件导入错误，项目已添加所有必要的CSS文件。如果仍有缺失，请检查对应组件的导入路径是否正确。

### 跨域问题
后端已配置CORS支持，允许前端访问API。如果仍然遇到跨域问题，请确保前端和后端的URL配置正确。
