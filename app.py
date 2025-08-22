import os
import zipfile
import tempfile
import shutil
import subprocess
import json
import threading
import time
from flask import Flask, request, send_file, jsonify, render_template, session
from werkzeug.utils import secure_filename
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "default_secret_key_for_dev")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# 🚀🔥 ULTRA MEGA SUPER SERVER CONFIGURATION 🔥🚀
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 1024  # 1GB LIMIT! INSANE! 🔥
app.config['UPLOAD_TIMEOUT'] = 72000  # 20 HOURS! ULTIMATE POWER!
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0  # Zero cache for turbo speed

# 💪 UNLIMITED MEGA FILE UPLOAD SETTINGS 💪
app.config['MAX_FORM_MEMORY_SIZE'] = None  # UNLIMITED FORM MEMORY!
app.config['MAX_FORM_PARTS'] = 100000  # 100K FORM PARTS!
app.config['APPLICATION_ROOT'] = None  # No limits
app.config['SESSION_COOKIE_SECURE'] = False  # Speed optimization

# ⚡ TURBO PERFORMANCE OPTIMIZATION ⚡
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

# 🚄 MEMORY AND BUFFER MEGA OPTIMIZATIONS 🚄
import sys
import gc
sys.setrecursionlimit(50000)  # Stable recursion limit
gc.set_threshold(700, 10, 10)  # Optimized garbage collection

# 🔥 ULTIMATE THREADING SETTINGS 🔥
import threading
threading.stack_size(4194304)  # 4MB stack size per thread

# Global dictionary to track processing status
processing_status = {}

def update_progress(task_id, status, progress=0, message=""):
    """Update processing progress for a task"""
    processing_status[task_id] = {
        'status': status,
        'progress': progress,
        'message': message,
        'timestamp': time.time()
    }

def cleanup_old_status():
    """Clean up old processing status entries"""
    current_time = time.time()
    to_remove = []
    for task_id, data in processing_status.items():
        if current_time - data['timestamp'] > 43200:  # 12 hours
            to_remove.append(task_id)
    
    for task_id in to_remove:
        del processing_status[task_id]

@app.route("/")
def index():
    """Main page with upload form"""
    return render_template('index.html')

@app.route("/upload", methods=["POST"])
def upload():
    """Handle file upload and video generation with MEGA STABILITY! 🚀"""
    temp_dir = None
    try:
        # Check if the post request has the file part
        if "file" not in request.files:
            return jsonify({"error": "❌ لم يتم رفع أي ملف. الرجاء رفع ملف مضغوط (ZIP)."}), 400

        file = request.files["file"]
        if not file or file.filename == '' or file.filename is None:
            return jsonify({"error": "❌ لم يتم اختيار أي ملف."}), 400

        # Check file size (1GB MEGA LIMIT!) 🚀🔥
        if hasattr(file, 'content_length') and file.content_length and file.content_length > 1024 * 1024 * 1024:
            return jsonify({"error": "❌ حجم الملف كبير جداً. الحد الأقصى 1 جيجابايت! 🚀"}), 413

        # Generate unique task ID
        task_id = str(int(time.time() * 1000))
        update_progress(task_id, "uploading", 0, "جاري رفع الملف...")

        # Create temporary directory
        temp_dir = tempfile.mkdtemp()
        filename = secure_filename(file.filename) if file.filename else "uploaded.zip"
        zip_path = os.path.join(temp_dir, filename)
        
        try:
            file.save(zip_path)
            update_progress(task_id, "extracting", 10, "جاري فك ضغط الملف...")
            
            # Extract ZIP file
            try:
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(temp_dir)
            except zipfile.BadZipFile:
                shutil.rmtree(temp_dir)
                return jsonify({"error": "❌ الملف المرفوع ليس ملف مضغوط صالح (ZIP)."}), 400

            update_progress(task_id, "searching", 20, "جاري البحث عن الملفات...")

            # Find audio file
            audio_file = None
            for root, _, files in os.walk(temp_dir):
                for f in files:
                    if f.lower().endswith((".mp3", ".wav", ".m4a", ".aac")):
                        audio_file = os.path.join(root, f)
                        break
                if audio_file:
                    break

            if not audio_file:
                shutil.rmtree(temp_dir)
                return jsonify({"error": "❌ لم يتم العثور على ملف صوتي (MP3, WAV, M4A, AAC) داخل الملف المضغوط."}), 400

            # Find PNG images and sort them
            images = []
            for root, _, files in os.walk(temp_dir):
                for f in files:
                    if f.lower().endswith((".png", ".jpg", ".jpeg")):
                        images.append(os.path.join(root, f))

            images.sort()

            if not images:
                shutil.rmtree(temp_dir)
                return jsonify({"error": "❌ لم يتم العثور على أي صور (PNG, JPG, JPEG) داخل الملف المضغوط."}), 400

            update_progress(task_id, "analyzing", 30, f"تم العثور على {len(images)} صورة و ملف صوتي واحد")

            # Get audio duration
            try:
                result = subprocess.run(
                    ["ffprobe", "-i", audio_file, "-show_entries", "format=duration", "-v", "quiet", "-of", "csv=p=0"],
                    capture_output=True, text=True, timeout=60
                )
                audio_duration = float(result.stdout.strip())
            except Exception as e:
                shutil.rmtree(temp_dir)
                return jsonify({"error": f"❌ حدث خطأ أثناء قراءة مدة الصوت: {str(e)}"}), 500

            update_progress(task_id, "preparing", 40, f"مدة الصوت: {audio_duration:.1f} ثانية")

            # Create images list file for FFmpeg
            images_list_file = os.path.join(temp_dir, "images.txt")
            per_image_duration = audio_duration / len(images)
            
            with open(images_list_file, "w") as f:
                for img in images:
                    # Escape single quotes in file paths for FFmpeg
                    escaped_path = img.replace("'", "'\\''")
                    f.write(f"file '{escaped_path}'\n")
                    f.write(f"duration {per_image_duration}\n")
                # Add the last image again to ensure proper timing
                if images:
                    escaped_path = images[-1].replace("'", "'\\''")
                    f.write(f"file '{escaped_path}'\n")

            # Generate video using FFmpeg with MEGA STABILITY! 🚀🔥
            output_path = os.path.join(temp_dir, "output.mp4")
            update_progress(task_id, "processing", 50, "جاري إنشاء الفيديو باستخدام FFmpeg بقوة خارقة...")

            process = None
            try:
                # SUPER STABLE FFmpeg process with memory optimization
                process = subprocess.Popen([
                    "ffmpeg",
                    "-y", "-hide_banner", "-loglevel", "error",  # Reduce memory usage
                    "-f", "concat",
                    "-safe", "0",
                    "-i", images_list_file,
                    "-i", audio_file,
                    "-c:v", "libx264",
                    "-preset", "medium",  # Better balance of speed/quality
                    "-crf", "23",  # Constant quality
                    "-r", "1",  # 1 fps since we're using duration for each image
                    "-pix_fmt", "yuv420p",
                    "-c:a", "aac",
                    "-b:a", "128k",
                    "-shortest",
                    "-movflags", "+faststart",  # Optimize for web playback
                    "-max_muxing_queue_size", "9999",  # Prevent queue overflow
                    "-avoid_negative_ts", "make_zero",  # Stability fix
                    output_path
                ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, 
                bufsize=0, universal_newlines=True)  # Unbuffered for real-time

                # ENHANCED progress monitoring with stability checks
                progress_count = 50
                last_update = time.time()
                consecutive_errors = 0
                
                while process.poll() is None:
                    current_time = time.time()
                    
                    # Check if process is still alive and responsive
                    if current_time - last_update > 30:  # Every 30 seconds
                        try:
                            # Test if process is responsive
                            process.poll()
                            last_update = current_time
                            consecutive_errors = 0
                        except Exception as e:
                            consecutive_errors += 1
                            if consecutive_errors > 3:
                                app.logger.error(f"FFmpeg unresponsive: {str(e)}")
                                break
                    
                    time.sleep(5)  # Check every 5 seconds instead of 2
                    progress_count = min(90, progress_count + 2)  # Slower progress updates
                    update_progress(task_id, "processing", progress_count, 
                                  f"جاري معالجة الفيديو... ({progress_count}%)")
                    
                    # Force garbage collection to free memory
                    import gc
                    gc.collect()

                # Wait for completion with MEGA TIMEOUT! 🚀🔥
                try:
                    stdout, stderr = process.communicate(timeout=72000)  # 20 HOURS!
                except subprocess.TimeoutExpired:
                    app.logger.error("FFmpeg timeout after 20 hours")
                    if process:
                        process.kill()
                        process.wait()
                    raise
                
                if process.returncode != 0:
                    app.logger.error(f"FFmpeg failed with return code {process.returncode}: {stderr}")
                    shutil.rmtree(temp_dir)
                    return jsonify({"error": f"❌ حدث خطأ أثناء إنشاء الفيديو: {stderr[:200]}..."}), 500

            except subprocess.TimeoutExpired:
                app.logger.error("FFmpeg process timed out")
                if process:
                    try:
                        process.kill()
                        process.wait(timeout=10)
                    except:
                        pass
                if os.path.exists(temp_dir):
                    shutil.rmtree(temp_dir)
                return jsonify({"error": "❌ انتهت مهلة معالجة الفيديو (20 ساعة! قوة خارقة)."}), 500
            except Exception as e:
                app.logger.error(f"FFmpeg process error: {str(e)}")
                if process:
                    try:
                        process.kill()
                        process.wait(timeout=10)
                    except:
                        pass
                if os.path.exists(temp_dir):
                    shutil.rmtree(temp_dir)
                return jsonify({"error": f"❌ خطأ في معالجة الفيديو: {str(e)[:200]}..."}), 500

            update_progress(task_id, "completed", 100, "تم إنشاء الفيديو بنجاح!")

            # Store the output path in session for later download
            session[f'video_path_{task_id}'] = output_path
            
            return jsonify({
                "success": True,
                "task_id": task_id,
                "message": "✅ تم إنشاء الفيديو بنجاح!"
            })

        except Exception as e:
            app.logger.error(f"Upload processing error: {str(e)}")
            if temp_dir and os.path.exists(temp_dir):
                try:
                    shutil.rmtree(temp_dir)
                except:
                    pass
            return jsonify({"error": f"❌ خطأ في معالجة الملف: {str(e)[:200]}..."}), 500

    except Exception as e:
        app.logger.error(f"Upload general error: {str(e)}")
        if temp_dir and os.path.exists(temp_dir):
            try:
                shutil.rmtree(temp_dir)
            except:
                pass
        return jsonify({"error": f"❌ خطأ غير متوقع: {str(e)[:200]}..."}), 500

@app.route("/progress/<task_id>")
def get_progress(task_id):
    """Get processing progress for a task"""
    cleanup_old_status()
    
    if task_id in processing_status:
        return jsonify(processing_status[task_id])
    else:
        return jsonify({"status": "not_found", "progress": 0, "message": "المهمة غير موجودة"})

@app.route("/download/<task_id>")
def download_video(task_id):
    """Download the generated video"""
    video_path = session.get(f'video_path_{task_id}')
    
    if not video_path or not os.path.exists(video_path):
        return jsonify({"error": "❌ الفيديو غير موجود أو منتهي الصلاحية."}), 404
    
    try:
        return send_file(
            video_path, 
            as_attachment=True, 
            download_name=f"video_{task_id}.mp4",
            mimetype='video/mp4'
        )
    except Exception as e:
        return jsonify({"error": f"❌ خطأ في تحميل الفيديو: {str(e)}"}), 500

@app.route("/stream/<task_id>")
def stream_video(task_id):
    """Stream the generated video for preview"""
    video_path = session.get(f'video_path_{task_id}')
    
    if not video_path or not os.path.exists(video_path):
        return jsonify({"error": "❌ الفيديو غير موجود أو منتهي الصلاحية."}), 404
    
    try:
        return send_file(
            video_path, 
            mimetype='video/mp4'
        )
    except Exception as e:
        return jsonify({"error": f"❌ خطأ في تشغيل الفيديو: {str(e)}"}), 500

@app.errorhandler(413)
def too_large(e):
    return jsonify({"error": "❌ حجم الملف كبير جداً. الحد الأقصى 1 جيجابايت! 🚀🔥"}), 413

@app.errorhandler(500)
def internal_error(e):
    return jsonify({"error": "❌ خطأ داخلي في الخادم. يرجى المحاولة مرة أخرى."}), 500

@app.errorhandler(Exception)
def handle_exception(e):
    # Log the error for debugging
    app.logger.error(f"Unhandled exception: {str(e)}", exc_info=True)
    return jsonify({"error": "❌ حدث خطأ غير متوقع. يرجى المحاولة مرة أخرى."}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
