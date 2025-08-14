# Backend/config.py
import os

# Railway部署时使用环境变量，本地开发使用默认值
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', '6427')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_NAME', 'wildcat_guide')

# Railway会提供DATABASE_URL环境变量
DATABASE_URL = os.getenv('DATABASE_URL')

if DATABASE_URL:
    # Railway部署环境
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
else:
    # 本地开发环境
    SQLALCHEMY_DATABASE_URI = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

SQLALCHEMY_TRACK_MODIFICATIONS = False