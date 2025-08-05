from flask import Blueprint, request, render_template, redirect, url_for
import subprocess
from pathlib import Path

autostart_bp = Blueprint('autostart', __name__, url_prefix='/autostart')

SYSTEMD_USER_DIR = Path.home() / ".config" / "systemd" / "user"

def get_service_status(name):
    try:
        result = subprocess.run(
            ["systemctl", "--user", "is-active", name],
            capture_output=True, text=True, check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return "unknown"

@autostart_bp.route('/', methods=['GET', 'POST'])
def manage_autostart():
    message = ""
    if request.method == 'POST':
        name = request.form['name'].strip()
        exec_path = request.form['command'].strip()

        if not name or not exec_path:
            message = "名称和命令不能为空"
        else:
            SYSTEMD_USER_DIR.mkdir(parents=True, exist_ok=True)
            service_file = SYSTEMD_USER_DIR / f"{name}.service"

            with open(service_file, 'w') as f:
                f.write(f"""[Unit]
Description=Autostart service for {name}
After=network.target

[Service]
ExecStart={exec_path}
Restart=on-failure

[Install]
WantedBy=default.target
""")

            subprocess.run(["systemctl", "--user", "daemon-reload"])
            subprocess.run(["systemctl", "--user", "enable", f"{name}.service"])
            subprocess.run(["systemctl", "--user", "start", f"{name}.service"])
            message = f"✅ 已创建并启动 {name}.service"

    services = []
    if SYSTEMD_USER_DIR.exists():
        for file in SYSTEMD_USER_DIR.glob("*.service"):
            svc_name = file.name
            status = get_service_status(svc_name)
            services.append({"name": svc_name, "status": status})

    return render_template("autostart.html", files=services, message=message)


@autostart_bp.route('/enable/<name>')
def enable_service(name):
    subprocess.run(["systemctl", "--user", "enable", name])
    subprocess.run(["systemctl", "--user", "start", name])
    return redirect(url_for('autostart.manage_autostart'))

@autostart_bp.route('/stop/<name>')
def stop_service(name):
    subprocess.run(["systemctl", "--user", "stop", name])
    return redirect(url_for('autostart.manage_autostart'))

@autostart_bp.route('/disable/<name>')
def disable_service(name):
    subprocess.run(["systemctl", "--user", "disable", name])
    return redirect(url_for('autostart.manage_autostart'))

@autostart_bp.route('/delete/<name>')
def delete_service(name):
    service_path = SYSTEMD_USER_DIR / name
    if service_path.exists():
        subprocess.run(["systemctl", "--user", "stop", name])
        subprocess.run(["systemctl", "--user", "disable", name])
        service_path.unlink()
        subprocess.run(["systemctl", "--user", "daemon-reload"])
    return redirect(url_for('autostart.manage_autostart'))
