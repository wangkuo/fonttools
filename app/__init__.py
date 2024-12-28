from flask import Flask
from flask_bootstrap import Bootstrap5
import os

def create_app():
    app = Flask(__name__)
    
    # 从环境变量获取 SECRET_KEY，如果没有则使用默认值
    app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'dev-secret-key')
    app.config['FONTS_DIR'] = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'fonts')
    
    # 初始化 Bootstrap
    Bootstrap5(app)
    
    # 注册路由
    from app.routes import main
    app.register_blueprint(main)
    
    return app 