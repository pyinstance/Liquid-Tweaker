import subprocess
import os
import shutil

def disable_xbox_services():
    subprocess.run(["sc", "stop", "XblGameSave"], shell=True)
    subprocess.run(["sc", "config", "XblGameSave", "start= disabled"], shell=True)

def disable_search():
    subprocess.run(["sc", "stop", "WSearch"], shell=True)
    subprocess.run(["sc", "config", "WSearch", "start= disabled"], shell=True)

def disable_sysmain():
    subprocess.run(["sc", "stop", "SysMain"], shell=True)
    subprocess.run(["sc", "config", "SysMain", "start= disabled"], shell=True)

def delete_prefetch():
    prefetch_path = r"C:\Windows\Prefetch"
    for file in os.listdir(prefetch_path):
        try:
            file_path = os.path.join(prefetch_path, file)
            os.remove(file_path)
        except Exception:
            pass

def disable_nagle():
    # Registry tweak - disabling Nagle's Algorithm
    import winreg
    try:
        key = r"SYSTEM\CurrentControlSet\Services\Tcpip\Parameters\Interfaces"
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key) as parent:
            for i in range(100):
                try:
                    subkey_name = winreg.EnumKey(parent, i)
                    with winreg.OpenKey(parent, subkey_name, 0, winreg.KEY_SET_VALUE) as subkey:
                        winreg.SetValueEx(subkey, "TcpAckFrequency", 0, winreg.REG_DWORD, 1)
                        winreg.SetValueEx(subkey, "TCPNoDelay", 0, winreg.REG_DWORD, 1)
                except OSError:
                    break
    except Exception:
        pass

def flush_dns():
    subprocess.run(["ipconfig", "/flushdns"], shell=True)

def disable_startup_delay():
    subprocess.run(['reg', 'add', r'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Serialize', 
                    '/v', 'StartupDelayInMSec', '/t', 'REG_DWORD', '/d', '0', '/f'], shell=True)

def disable_hibernation():
    subprocess.run(["powercfg", "-h", "off"], shell=True)

def clear_pagefile_on_shutdown():
    subprocess.run(['reg', 'add', r'HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management',
                    '/v', 'ClearPageFileAtShutdown', '/t', 'REG_DWORD', '/d', '1', '/f'], shell=True)

def enable_fast_startup():
    subprocess.run(['powercfg', '/hibernate', 'on'], shell=True)
    subprocess.run(['reg', 'add', r'HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\Power',
                    '/v', 'HiberbootEnabled', '/t', 'REG_DWORD', '/d', '1', '/f'], shell=True)

def disable_game_dvr():
    subprocess.run(['reg', 'add', r'HKCU\Software\Microsoft\Windows\CurrentVersion\GameDVR',
                    '/v', 'AppCaptureEnabled', '/t', 'REG_DWORD', '/d', '0', '/f'], shell=True)

def set_gpu_priority():
    subprocess.run(['reg', 'add', r'HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Games',
                    '/v', 'GPU Priority', '/t', 'REG_DWORD', '/d', '8', '/f'], shell=True)

def disable_update_bandwidth():
    subprocess.run(['reg', 'add', r'HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\DeliveryOptimization\Config',
                    '/v', 'DODownloadMode', '/t', 'REG_DWORD', '/d', '0', '/f'], shell=True)

def optimize_tcp():
    subprocess.run(['netsh', 'int', 'tcp', 'set', 'global', 'autotuninglevel=highlyrestricted'], shell=True)

def disable_ui_animations():
    subprocess.run(['reg', 'add', r'HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\VisualEffects',
                    '/v', 'VisualFXSetting', '/t', 'REG_DWORD', '/d', '2', '/f'], shell=True)

def disable_telemetry():
    subprocess.run(['reg', 'add', r'HKLM\SOFTWARE\Policies\Microsoft\Windows\DataCollection',
                    '/v', 'AllowTelemetry', '/t', 'REG_DWORD', '/d', '0', '/f'], shell=True)

def disable_tips():
    subprocess.run(['reg', 'add', r'HKCU\Software\Microsoft\Windows\CurrentVersion\ContentDeliveryManager',
                    '/v', 'SubscribedContent-310093Enabled', '/t', 'REG_DWORD', '/d', '0', '/f'], shell=True)
