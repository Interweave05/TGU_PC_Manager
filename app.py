from flask import Flask, render_template, jsonify
from modules.AutoStart.routes import autostart_bp
from modules.DiskManager.routes import disk_bp

import config
import psutil
import shutil


app = Flask(__name__)
app.register_blueprint(autostart_bp)
app.register_blueprint(disk_bp)
app.config.from_object(config.ProductionConfig)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/sysinfo')
def sysinfo():
    cpu = psutil.cpu_percent(interval=0.5)
    mem = psutil.virtual_memory()
    disk = shutil.disk_usage("/")

    try:
        temps = psutil.sensors_temperatures()
        if "coretemp" in temps:
            temp = temps["coretemp"][0].current  # Intel CPU 通常使用 coretemp
        elif "cpu-thermal" in temps:
            temp = temps["cpu-thermal"][0].current  # 树莓派等平台
        else:
            temp = None
    except Exception:
        temp = None

    return jsonify({
        "cpu": round(cpu, 1),
        "cpu_temp": round(temp, 1) if temp else None,
        "memory": {
            "used": round(mem.used / 1024 / 1024, 1),
            "total": round(mem.total / 1024 / 1024, 1)
        },
        "disk": {
            "used": round(disk.used / 1024 / 1024 / 1024, 1),
            "total": round(disk.total / 1024 / 1024 / 1024, 1)
        }
    })

def print_tgu():
    print(r"""
  _______ _____ _    _ 
 |__   __/ ____| |  | |
    | | | |  __| |  | |
    | | | | |_ | |  | |
    | | | |__| | |__| |
    |_|  \_____|\____/ 

""")

if __name__ == '__main__':
    print_tgu()
    app.run(host = app.config['HOST'], port = app.config['PORT'], debug = app.config['DEBUG'])
