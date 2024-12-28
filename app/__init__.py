from flask import Flask
from flask_bootstrap import Bootstrap5

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key'
    app.config['UPLOAD_FOLDER'] = 'app/fonts'
    
    # 初始化 Bootstrap
    Bootstrap5(app)
    
    # 注册路由
    from app.routes import main
    app.register_blueprint(main)
    
    return app 