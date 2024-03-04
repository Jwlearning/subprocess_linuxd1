# -*- coding: utf-8 -*-
import subprocess
import os
import locale
import logging

# 设置日志
logging.basicConfig(filename='system_info.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_command(command, timeout=10):
    """执行系统命令并返回输出，跳过权限不足的命令，并设置超时"""
    try:
        default_encoding = locale.getdefaultlocale()[1] or 'utf-8'
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        stdout, stderr = process.communicate(timeout=timeout)

        if process.returncode == 0:
            return stdout.strip()
        else:
            error_msg = stderr.strip().lower()
            if "permission denied" in error_msg:
                logging.warning(f"Permission denied for command: {command}. Skipping...")
                return "Permission denied, skipping..."
            else:
                logging.error(f"Command failed: {command}\nError: {error_msg}")
                return f"Error: {error_msg}"
    except subprocess.TimeoutExpired:
        logging.warning(f"Command timeout: {command}")
        return "Command timeout, skipping..."
    except Exception as e:
        logging.error(f"Exception during command execution: {command}\n{str(e)}")
        return "Command execution failed"

def collect_system_info():
    print("用户列表：")
    print(run_command("cat /etc/passwd | cut -d: -f1"))

    print("\n当前登录的用户：")
    print(run_command("who"))

    print("\nCPU和内存使用情况：")
    print(run_command("top -b -n 1 | head -n 5"))

    print("\n磁盘使用和IO统计：")
    print(run_command("df -h"))
    print(run_command("iostat"))

    print("\n网络状态：")
    print(run_command("netstat -tuln"))

    print("\n已安装软件包列表（Debian/Ubuntu）：")
    print(run_command("dpkg --get-selections | grep -v deinstall"))

    print("\n系统服务：")
    print(run_command("systemctl list-unit-files --type=service | grep enabled"))

    print("\n历史命令：")
    history_file = os.environ.get('HISTFILE', os.path.expanduser('~/.bash_history'))
    print(run_command(f"tail -n 20 {history_file}", timeout=5))

    print("\n系统变量：")
    print(run_command("printenv"))

if __name__ == "__main__":
    try:
        collect_system_info()
    except KeyboardInterrupt:
        print("Script interrupted by user.")
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        print(f"An unexpected error occurred: {str(e)}")
