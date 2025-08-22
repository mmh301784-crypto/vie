#!/usr/bin/env python3
"""
Ultra Stable Server Startup Script
Ensures single instance and optimal configuration
"""
import os
import sys
import signal
import subprocess
import time
import psutil

def kill_existing_servers():
    """Kill any existing gunicorn processes"""
    print("🔄 جاري إيقاف الخوادم الموجودة...")
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            if 'gunicorn' in proc.info['name'] or (proc.info['cmdline'] and any('gunicorn' in arg for arg in proc.info['cmdline'])):
                print(f"⏹️ إيقاف العملية: {proc.info['pid']}")
                proc.terminate()
                proc.wait(timeout=10)
        except (psutil.NoSuchProcess, psutil.TimeoutExpired):
            pass

def clean_temp_files():
    """Clean temporary files and directories"""
    print("🧹 تنظيف الملفات المؤقتة...")
    import shutil
    import glob
    
    # Clean /tmp
    for temp_dir in glob.glob('/tmp/tmp*'):
        try:
            if os.path.isdir(temp_dir):
                shutil.rmtree(temp_dir)
                print(f"🗑️ تم حذف: {temp_dir}")
        except:
            pass
    
    # Clean /dev/shm if needed
    for temp_file in glob.glob('/dev/shm/tmp*'):
        try:
            if os.path.isfile(temp_file):
                os.remove(temp_file)
            elif os.path.isdir(temp_file):
                shutil.rmtree(temp_file)
        except:
            pass

def start_optimized_server():
    """Start the server with optimal configuration"""
    print("🚀 بدء السيرفر الخارق...")
    
    # Set environment variables for optimization
    os.environ['PYTHONUNBUFFERED'] = '1'
    os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
    
    # Start gunicorn with our configuration
    cmd = [
        'gunicorn',
        '--config', 'gunicorn.conf.py',
        '--preload',
        'main:app'
    ]
    
    print("🔧 أمر التشغيل:", ' '.join(cmd))
    
    process = None
    try:
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        
        print("✅ تم بدء السيرفر بنجاح!")
        print("🌐 السيرفر يعمل على: http://0.0.0.0:5000")
        
        # Monitor the process
        while True:
            if process.stdout:
                output = process.stdout.readline()
                if output:
                    print(output.strip())
            if process.poll() is not None:
                break
                
    except KeyboardInterrupt:
        print("\n⏹️ إيقاف السيرفر...")
        if process:
            process.terminate()
    except Exception as e:
        print(f"❌ خطأ في بدء السيرفر: {e}")
        return False
        
    return True

def main():
    print("🚀🔥 بدء السيرفر الخارق جداً! 🔥🚀")
    
    # Step 1: Kill existing servers
    kill_existing_servers()
    time.sleep(2)
    
    # Step 2: Clean temp files
    clean_temp_files()
    
    # Step 3: Start optimized server
    success = start_optimized_server()
    
    if not success:
        print("❌ فشل في بدء السيرفر")
        sys.exit(1)

if __name__ == "__main__":
    main()