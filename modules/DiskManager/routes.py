import os
import shutil
import psutil
from flask import jsonify
from flask import Blueprint, render_template, redirect, url_for, flash, request

disk_bp = Blueprint('diskmanager', __name__, url_prefix='/diskmanager')

EXCLUDED_DIRS = ['/proc', '/dev', '/mnt', '/lost+found', '/cdrom']

def get_directory_usage(path):
    """返回指定目录的占用字节数，排除特殊目录"""
    # 排除 /proc 和 /dev 以及它们的子目录
    for exclude in EXCLUDED_DIRS:
        if os.path.abspath(path) == exclude or os.path.abspath(path).startswith(exclude + os.sep):
            return 0

    total = 0
    for dirpath, dirnames, filenames in os.walk(path, topdown=True, onerror=lambda e: None):
        for f in filenames:
            try:
                fp = os.path.join(dirpath, f)
                total += os.path.getsize(fp)
            except Exception:
                pass
    return total



@disk_bp.route('/')
def disk_overview():
    # 总体磁盘使用情况
    usage = psutil.disk_usage('/')
    total = round(usage.total / (1024 ** 3), 2)  # GB
    used = round(usage.used / (1024 ** 3), 2)
    free = round(usage.free / (1024 ** 3), 2)
    percent_used = usage.percent

    # 获取根目录下一级文件夹的使用情况
    root_path = '/'
    folders = [f for f in os.listdir(root_path) if os.path.isdir(os.path.join(root_path, f))]
    folder_usage = []
    total_used = 0

    for folder in folders:
        path = os.path.join(root_path, folder)
        try:
            size = get_directory_usage(path)
            folder_usage.append({'name': folder, 'size': size})
            total_used += size
        except Exception:
            folder_usage.append({'name': folder, 'size': 0})

    # 排序并计算百分比
    folder_usage.sort(key=lambda x: x['size'], reverse=True)
    for f in folder_usage:
        f['percent'] = (f['size'] / total_used) * 100 if total_used > 0 else 0

    return render_template('diskmanager.html',
                           total=total,
                           used=used,
                           free=free,
                           percent_used=percent_used,
                           folder_usage=folder_usage)

@disk_bp.route('/clean_tmp', methods=['POST'])
def clean_tmp():
    tmp_path = '/tmp'
    try:
        for filename in os.listdir(tmp_path):
            file_path = os.path.join(tmp_path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception:
                continue
        flash("✅ /tmp 清理完成", "success")
    except Exception as e:
        flash(f"⚠️ 清理失败: {e}", "danger")

    return redirect(url_for('diskmanager.disk_overview'))
