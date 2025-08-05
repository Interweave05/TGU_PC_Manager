from flask import Blueprint, request, render_template, redirect, url_for
import subprocess
import tempfile
from pathlib import Path

autostart_bp = Blueprint('autostart', __name__, url_prefix='/autostart')

SYSTEMD_SYSTEM_DIR = Path("/etc/systemd/system")

def get_service_status(name):
    try:
        result = subprocess.run(
            ["systemctl", "is-active", name],
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
        workdir = request.form.get('workdir', '').strip()
        env_text = request.form.get('environment', '').strip()

        if not name or not exec_path:
            message = "名称和命令不能为空"
        else:
            service_file_path = SYSTEMD_SYSTEM_DIR / f"{name}.service"

            with tempfile.NamedTemporaryFile("w", delete=False) as tmpfile:
                tmpfile.write(f"""[Unit]
Description=Autostart service for {name}
After=network.target

[Service]
""")
                # 写入用户自定义的 Environment 变量，每行一条
                if env_text:
                    for line in env_text.splitlines():
                        line = line.strip()
                        if line:
                            tmpfile.write(f"Environment={line}\n")

                tmpfile.write(f"ExecStart={exec_path}\nRestart=on-failure\n")

                if workdir:
                    tmpfile.write(f"WorkingDirectory={workdir}\n")

                tmpfile.write("""[Install]
WantedBy=multi-user.target
""")
                tmpfile_path = tmpfile.name

            subprocess.run(["sudo", "cp", tmpfile_path, str(service_file_path)])
            subprocess.run(["sudo", "chmod", "644", str(service_file_path)])

            subprocess.run(["sudo", "systemctl", "daemon-reload"])
            subprocess.run(["sudo", "systemctl", "enable", f"{name}.service"])
            subprocess.run(["sudo", "systemctl", "start", f"{name}.service"])
            message = f"✅ 已创建并启动 {name}.service"

    services = []
    if SYSTEMD_SYSTEM_DIR.exists():
        for file in SYSTEMD_SYSTEM_DIR.glob("*.service"):
            svc_name = file.name
            status = get_service_status(svc_name)
            services.append({"name": svc_name, "status": status})

    return render_template("autostart.html", files=services, message=message)

@autostart_bp.route('/enable/<name>')
def enable_service(name):
    subprocess.run(["sudo", "systemctl", "enable", name])
    subprocess.run(["sudo", "systemctl", "start", name])
    return redirect(url_for('autostart.manage_autostart'))

@autostart_bp.route('/stop/<name>')
def stop_service(name):
    subprocess.run(["sudo", "systemctl", "stop", name])
    return redirect(url_for('autostart.manage_autostart'))

@autostart_bp.route('/disable/<name>')
def disable_service(name):
    subprocess.run(["sudo", "systemctl", "disable", name])
    return redirect(url_for('autostart.manage_autostart'))

@autostart_bp.route('/delete/<name>')
def delete_service(name):
    service_path = SYSTEMD_SYSTEM_DIR / name
    if service_path.exists():
        subprocess.run(["sudo", "systemctl", "stop", name])
        subprocess.run(["sudo", "systemctl", "disable", name])
        subprocess.run(["sudo", "rm", str(service_path)])
        subprocess.run(["sudo", "systemctl", "daemon-reload"])
    return redirect(url_for('autostart.manage_autostart'))
