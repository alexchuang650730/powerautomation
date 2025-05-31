#!/usr/bin/env python
"""
PowerAutomation 数据库初始化脚本

此脚本用于初始化PowerAutomation系统所需的SQLite数据库，
创建必要的表结构并插入基础数据。
"""

import os
import sys
import sqlite3
import logging
from datetime import datetime
from pathlib import Path

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('init_db')

# 获取项目根目录
PROJECT_ROOT = Path(__file__).parent.parent.absolute()
DB_DIR = PROJECT_ROOT / "data"
DB_PATH = DB_DIR / "powerautomation.db"

# 创建数据目录
def create_data_directory():
    """创建数据目录"""
    if not DB_DIR.exists():
        logger.info(f"创建数据目录: {DB_DIR}")
        DB_DIR.mkdir(parents=True, exist_ok=True)

# 数据库表定义
TABLES = {
    "users": """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        email TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        last_login TIMESTAMP
    )
    """,
    
    "tasks": """
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        description TEXT,
        status TEXT NOT NULL DEFAULT 'pending',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        completed_at TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    """,
    
    "agents": """
    CREATE TABLE IF NOT EXISTS agents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        type TEXT NOT NULL,
        description TEXT,
        config_json TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """,
    
    "agent_executions": """
    CREATE TABLE IF NOT EXISTS agent_executions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        agent_id INTEGER NOT NULL,
        task_id INTEGER NOT NULL,
        status TEXT NOT NULL DEFAULT 'pending',
        result_json TEXT,
        started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        completed_at TIMESTAMP,
        FOREIGN KEY (agent_id) REFERENCES agents (id),
        FOREIGN KEY (task_id) REFERENCES tasks (id)
    )
    """
}

# 初始数据
INITIAL_DATA = {
    "agents": [
        (
            "general_agent", 
            "general", 
            "通用智能体，可处理各种常见任务", 
            '{"model": "gpt-4", "temperature": 0.7}'
        ),
        (
            "ppt_agent", 
            "ppt", 
            "PPT智能体，专门用于创建和编辑演示文稿", 
            '{"model": "gpt-4", "temperature": 0.5}'
        ),
        (
            "web_agent", 
            "web", 
            "Web智能体，专门用于网页浏览和信息提取", 
            '{"model": "gpt-4", "temperature": 0.3}'
        ),
        (
            "code_agent", 
            "code", 
            "代码智能体，专门用于代码生成和分析", 
            '{"model": "gpt-4", "temperature": 0.2}'
        )
    ]
}

def init_database():
    """初始化数据库"""
    create_data_directory()
    
    # 检查数据库文件是否已存在
    db_exists = DB_PATH.exists()
    
    # 连接数据库（如果不存在则创建）
    logger.info(f"连接数据库: {DB_PATH}")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 创建表
    for table_name, create_table_sql in TABLES.items():
        logger.info(f"创建表: {table_name}")
        cursor.execute(create_table_sql)
    
    # 如果是新数据库，插入初始数据
    if not db_exists:
        logger.info("插入初始数据")
        
        # 插入智能体数据
        cursor.executemany(
            "INSERT INTO agents (name, type, description, config_json) VALUES (?, ?, ?, ?)",
            INITIAL_DATA["agents"]
        )
        
        # 创建测试用户
        cursor.execute(
            "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
            ("admin", "admin@example.com", "pbkdf2:sha256:150000$HASHED_PASSWORD")
        )
    
    # 提交事务
    conn.commit()
    
    # 验证数据
    logger.info("验证数据库初始化")
    cursor.execute("SELECT COUNT(*) FROM agents")
    agent_count = cursor.fetchone()[0]
    logger.info(f"智能体数量: {agent_count}")
    
    cursor.execute("SELECT COUNT(*) FROM users")
    user_count = cursor.fetchone()[0]
    logger.info(f"用户数量: {user_count}")
    
    # 关闭连接
    conn.close()
    
    logger.info("数据库初始化完成")
    return True

if __name__ == "__main__":
    try:
        logger.info("开始初始化数据库")
        success = init_database()
        if success:
            logger.info("数据库初始化成功")
            print("数据库初始化成功！")
            sys.exit(0)
        else:
            logger.error("数据库初始化失败")
            print("数据库初始化失败，请查看日志获取详细信息。")
            sys.exit(1)
    except Exception as e:
        logger.exception("数据库初始化过程中发生错误")
        print(f"错误: {str(e)}")
        sys.exit(1)
