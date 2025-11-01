#run.py

import app
from waitress import serve
from app.communication import QueueProcessorThread
import sys

# 建立 Flask 應用程式實例
application = app.create_app()

# 這是唯一的進入點
if __name__ == '__main__':
    # 確保 app_context
    with application.app_context():
        print("============================================================")
        print("正在啟動 CKW 4S CMP...")

        # 1. 啟動 TCP 伺服器
        print(
            f"準備啟動 TCP 伺服器於 {application.config['TCP_SERVER_HOST']}:{application.config['TCP_SERVER_PORT']}...")
        app.tcp_server.start()

        # 2. 啟動所有 Serial 裝置
        print("準備啟動所有已啟用的 Serial 裝置...")
        app.connection_manager.start_all_serial_devices()

        # 3. 啟動佇列處理器
        print("準備啟動佇列處理器...")
        queue_processor = QueueProcessorThread(app=application)
        queue_processor.start()

        print("---所有背景服務已成功啟動---")

    # 4. 啟動 Waitress 網頁伺服器
    # Nginx 將會代理到這個 5000 埠
    print(f"準備啟動 Waitress 網頁伺服器於 http://127.0.0.1:5000 ...")
    print("============================================================")

    # 刷新 stdout，確保日誌立即寫入 (替代 -u)
    sys.stdout.flush()

    # 啟動 Waitress 伺服器來服務 Flask app
    # 這是_blocking_調用，它會保持 run.py 腳本持續運行
    serve(application, host='127.0.0.1', port=5000)