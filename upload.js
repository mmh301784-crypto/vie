/**
 * Video Generation App - Upload and Progress Tracking
 * Handles file upload, progress monitoring, and video display
 */

class VideoGenerator {
    constructor() {
        this.currentTaskId = null;
        this.progressInterval = null;
        this.uploadXhr = null;
        
        this.initializeElements();
        this.bindEvents();
    }
    
    initializeElements() {
        // Form elements
        this.uploadForm = document.getElementById('upload-form');
        this.fileInput = document.getElementById('file-input');
        this.uploadBtn = document.getElementById('upload-btn');
        
        // Progress elements
        this.uploadProgress = document.getElementById('upload-progress');
        this.uploadProgressBar = document.getElementById('upload-progress-bar');
        this.uploadSize = document.getElementById('upload-size');
        this.processingProgress = document.getElementById('processing-progress');
        this.processingProgressBar = document.getElementById('processing-progress-bar');
        this.processingMessage = document.getElementById('processing-message');
        
        // Result elements
        this.resultSection = document.getElementById('result-section');
        this.resultVideo = document.getElementById('result-video');
        this.downloadBtn = document.getElementById('download-btn');
        this.newUploadBtn = document.getElementById('new-upload-btn');
        
        // Error elements
        this.errorSection = document.getElementById('error-section');
        this.errorMessage = document.getElementById('error-message');
        
        // Sections
        this.uploadSection = document.getElementById('upload-section');
    }
    
    bindEvents() {
        this.uploadForm.addEventListener('submit', (e) => this.handleUpload(e));
        this.downloadBtn.addEventListener('click', () => this.downloadVideo());
        this.newUploadBtn.addEventListener('click', () => this.resetForm());
        
        // File input change event for validation
        this.fileInput.addEventListener('change', (e) => this.validateFile(e));
    }
    
    validateFile(event) {
        const file = event.target.files[0];
        if (!file) return;
        
        // Check file size (1GB limit) 🚀🔥
        const maxSize = 1024 * 1024 * 1024; // 1GB in bytes! MEGA POWER!
        if (file.size > maxSize) {
            this.showError('❌ حجم الملف كبير جداً. الحد الأقصى 1 جيجابايت! 🚀');
            this.fileInput.value = '';
            return;
        }
        
        // Check file type
        if (!file.name.toLowerCase().endsWith('.zip')) {
            this.showError('❌ يجب اختيار ملف مضغوط بصيغة ZIP.');
            this.fileInput.value = '';
            return;
        }
        
        this.hideError();
    }
    
    async handleUpload(event) {
        event.preventDefault();
        
        const file = this.fileInput.files[0];
        if (!file) {
            this.showError('❌ يرجى اختيار ملف للرفع.');
            return;
        }
        
        this.hideError();
        this.disableForm();
        this.showUploadProgress();
        
        const formData = new FormData();
        formData.append('file', file);
        
        // Create XMLHttpRequest for upload progress tracking
        this.uploadXhr = new XMLHttpRequest();
        
        // Upload progress handler
        this.uploadXhr.upload.addEventListener('progress', (e) => {
            if (e.lengthComputable) {
                const percentComplete = (e.loaded / e.total) * 100;
                const uploadedMB = (e.loaded / (1024 * 1024)).toFixed(1);
                const totalMB = (e.total / (1024 * 1024)).toFixed(1);
                
                this.updateUploadProgress(percentComplete, uploadedMB, totalMB);
            }
        });
        
        // Response handler
        this.uploadXhr.addEventListener('load', () => {
            if (this.uploadXhr.status === 200) {
                try {
                    const response = JSON.parse(this.uploadXhr.responseText);
                    if (response.success) {
                        this.currentTaskId = response.task_id;
                        this.hideUploadProgress();
                        this.showProcessingProgress();
                        this.startProgressMonitoring();
                    } else {
                        this.showError(response.error || 'حدث خطأ غير متوقع');
                        this.enableForm();
                    }
                } catch (e) {
                    this.showError('❌ خطأ في معالجة الاستجابة من الخادم');
                    this.enableForm();
                }
            } else {
                try {
                    const response = JSON.parse(this.uploadXhr.responseText);
                    this.showError(response.error || `❌ خطأ في الخادم: ${this.uploadXhr.status}`);
                } catch (e) {
                    this.showError(`❌ خطأ في الخادم: ${this.uploadXhr.status}`);
                }
                this.enableForm();
            }
            this.hideUploadProgress();
        });
        
        // Error handler
        this.uploadXhr.addEventListener('error', () => {
            this.showError('❌ حدث خطأ في الاتصال بالخادم');
            this.enableForm();
            this.hideUploadProgress();
        });
        
        // Timeout handler (20 hours) 🚀🔥💪
        this.uploadXhr.timeout = 72000000; // 20 HOURS! MEGA POWER!
        this.uploadXhr.addEventListener('timeout', () => {
            this.showError('❌ انتهت مهلة الرفع والمعالجة (20 ساعة!)');
            this.enableForm();
            this.hideUploadProgress();
        });
        
        // Send the request
        this.uploadXhr.open('POST', '/upload');
        this.uploadXhr.send(formData);
    }
    
    updateUploadProgress(percentage, uploadedMB, totalMB) {
        this.uploadProgressBar.style.width = `${percentage}%`;
        this.uploadProgressBar.textContent = `${percentage.toFixed(1)}%`;
        this.uploadSize.textContent = `${uploadedMB} MB / ${totalMB} MB`;
    }
    
    startProgressMonitoring() {
        if (!this.currentTaskId) return;
        
        this.progressInterval = setInterval(async () => {
            try {
                const response = await fetch(`/progress/${this.currentTaskId}`);
                const data = await response.json();
                
                if (data.status === 'completed') {
                    this.hideProcessingProgress();
                    this.showVideoResult();
                    this.enableForm();
                    clearInterval(this.progressInterval);
                } else if (data.status === 'error') {
                    this.showError(data.message || 'حدث خطأ في المعالجة');
                    this.hideProcessingProgress();
                    this.enableForm();
                    clearInterval(this.progressInterval);
                } else {
                    this.updateProcessingProgress(data.progress || 0, data.message || 'جاري المعالجة...');
                }
            } catch (error) {
                console.error('Error fetching progress:', error);
                // Continue monitoring, don't break on temporary network issues
            }
        }, 2000); // Check every 2 seconds
    }
    
    updateProcessingProgress(percentage, message) {
        this.processingProgressBar.style.width = `${percentage}%`;
        this.processingProgressBar.textContent = `${percentage}%`;
        this.processingMessage.textContent = message;
    }
    
    showVideoResult() {
        this.resultVideo.src = `/stream/${this.currentTaskId}`;
        this.resultSection.classList.remove('d-none');
        this.resultSection.classList.add('fade-in');
        
        // Scroll to video
        this.resultSection.scrollIntoView({ behavior: 'smooth' });
    }
    
    downloadVideo() {
        if (!this.currentTaskId) return;
        
        const link = document.createElement('a');
        link.href = `/download/${this.currentTaskId}`;
        link.download = `video_${this.currentTaskId}.mp4`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }
    
    resetForm() {
        // Clear current task
        this.currentTaskId = null;
        
        // Clear intervals
        if (this.progressInterval) {
            clearInterval(this.progressInterval);
            this.progressInterval = null;
        }
        
        // Abort any ongoing upload
        if (this.uploadXhr) {
            this.uploadXhr.abort();
            this.uploadXhr = null;
        }
        
        // Reset form
        this.uploadForm.reset();
        
        // Hide all sections except upload
        this.hideUploadProgress();
        this.hideProcessingProgress();
        this.hideError();
        this.resultSection.classList.add('d-none');
        
        // Enable form
        this.enableForm();
        
        // Scroll to top
        this.uploadSection.scrollIntoView({ behavior: 'smooth' });
    }
    
    showUploadProgress() {
        this.uploadProgress.classList.remove('d-none');
    }
    
    hideUploadProgress() {
        this.uploadProgress.classList.add('d-none');
    }
    
    showProcessingProgress() {
        this.processingProgress.classList.remove('d-none');
    }
    
    hideProcessingProgress() {
        this.processingProgress.classList.add('d-none');
    }
    
    showError(message) {
        this.errorMessage.textContent = message;
        this.errorSection.classList.remove('d-none');
        this.errorSection.scrollIntoView({ behavior: 'smooth' });
    }
    
    hideError() {
        this.errorSection.classList.add('d-none');
    }
    
    disableForm() {
        this.uploadBtn.disabled = true;
        this.fileInput.disabled = true;
        this.uploadBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> جاري الرفع...';
    }
    
    enableForm() {
        this.uploadBtn.disabled = false;
        this.fileInput.disabled = false;
        this.uploadBtn.innerHTML = '<i class="fas fa-upload"></i> رفع وإنشاء الفيديو';
    }
}

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new VideoGenerator();
});

// Handle page visibility changes to pause/resume monitoring
document.addEventListener('visibilitychange', () => {
    // This helps prevent unnecessary requests when tab is not active
    if (window.videoGenerator && window.videoGenerator.progressInterval) {
        if (document.hidden) {
            // Page is hidden, could implement pause logic here
            console.log('Page hidden - progress monitoring continues');
        } else {
            // Page is visible
            console.log('Page visible - progress monitoring active');
        }
    }
});
