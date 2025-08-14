# Backend/run.py
import os
from Backend import create_app, db
from flask_cors import CORS 

app = create_app()
CORS(app) 

if __name__ == '__main__':
    # Railway会设置PORT环境变量
    port = int(os.environ.get('PORT', 5001))
    # Railway部署时debug=False，本地开发debug=True
    debug = os.environ.get('NODE_ENV') != 'production'
    
    app.run(debug=debug, host='0.0.0.0', port=port)