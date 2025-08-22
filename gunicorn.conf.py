# 🚀🔥 ULTRA MEGA SUPER SERVER - SPACESHIP POWER! 🔥🚀
bind = "0.0.0.0:5000"
worker_class = "sync"
workers = 1  # Single worker for maximum stability with large files
worker_connections = 1000  # Stable connections
timeout = 72000  # 20 HOURS TIMEOUT! INSANE!
keepalive = 300  # Keep connections alive for 5 minutes
graceful_timeout = 300  # More time for graceful shutdown
max_requests = 0  # UNLIMITED requests
max_requests_jitter = 0
preload_app = True  # Lightning fast startup
reload = False
reload_engine = "auto"

# 🔥 EXTREME MEGA FILE UPLOAD SETTINGS 🔥
worker_tmp_dir = "/dev/shm"  # TURBO RAM MODE
tmp_upload_dir = "/dev/shm"  # EVERYTHING IN RAM!

# 💪 UNLIMITED POWER MEMORY OPTIMIZATION 💪
worker_rlimit_nofile = 1048576  # 1 MILLION open files!
worker_rlimit_fsize = 1073741824000  # 1TB max file size! INSANE!
worker_rlimit_core = 0  # No core dumps for speed
worker_rlimit_as = 0  # Unlimited virtual memory

# ⚡ TURBO CONNECTION OPTIMIZATION ⚡
max_worker_memory = 0  # NO MEMORY LIMITS!
max_worker_requests = 0  # NO REQUEST LIMITS!

# 🚄 MEGA BUFFER SIZES FOR MASSIVE UPLOADS 🚄
limit_request_line = 32768  # 4X BIGGER request line!
limit_request_fields = 1000  # 5X MORE request fields!
limit_request_field_size = 65536  # 4X BIGGER field sizes!

# Logging optimized for stability
accesslog = "-"
errorlog = "-"
loglevel = "info"  # Reduce logging overhead
capture_output = True
enable_stdio_inheritance = True

# Additional stability settings
worker_rlimit_data = 2147483648  # 2GB data limit per worker
worker_rlimit_stack = 16777216   # 16MB stack limit

# Process naming
proc_name = "SUPER_video_generator"

# Server mechanics
daemon = False
pidfile = None
user = None
group = None

# Performance boost
preload_app = True
worker_tmp_dir = "/dev/shm"
forwarded_allow_ips = "*"
proxy_allow_ips = "*"