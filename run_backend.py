import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath('.'))

# 导入后端应用
from backend.main import app

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
