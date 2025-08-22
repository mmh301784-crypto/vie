# Video Generator App

## Overview

This is a Flask-based web application that creates videos from audio files and images. Users upload a ZIP file containing an audio file (MP3/WAV) and PNG images, and the application processes these to generate a video output. The app features real-time progress tracking, file validation, and a responsive Arabic/RTL interface using Bootstrap with dark theme.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Template Engine**: Jinja2 templates with Flask's built-in templating
- **UI Framework**: Bootstrap with Replit's dark theme for consistent styling
- **Internationalization**: Arabic/RTL interface with proper text direction support
- **Client-Side Logic**: Vanilla JavaScript for upload handling, progress tracking, and user interactions
- **Responsive Design**: Mobile-first approach using Bootstrap's responsive grid system

### Backend Architecture
- **Web Framework**: Flask with threaded request handling for concurrent uploads
- **File Processing**: Temporary directory management using Python's tempfile module
- **Upload Handling**: Werkzeug's secure filename utilities and file validation
- **Progress Tracking**: In-memory dictionary-based status tracking with automatic cleanup
- **Session Management**: Flask sessions with configurable secret key
- **Proxy Support**: ProxyFix middleware for proper header handling in deployment

### File Processing Pipeline
- **Upload Validation**: File type checking, size limits (250MB), and ZIP format validation
- **Extraction Logic**: Automatic audio file detection (MP3/WAV) and PNG image sorting
- **Video Generation**: Subprocess-based video creation (likely using FFmpeg or similar)
- **Temporary Storage**: Secure temporary directory creation and cleanup

### Security Features
- **File Upload Security**: Secure filename handling and file type validation
- **Size Limitations**: 250MB upload limit with 10-hour processing timeout
- **Session Security**: Configurable session secret with environment variable support
- **Input Sanitization**: Werkzeug's secure filename utilities for file handling

## External Dependencies

### Frontend Libraries
- **Bootstrap CSS**: Replit's dark theme variant for consistent UI styling
- **Font Awesome**: Icon library for enhanced visual elements
- **Web Fonts**: Cairo and Amiri fonts for proper Arabic text rendering

### Python Packages
- **Flask**: Core web framework with templating and request handling
- **Werkzeug**: Utilities for secure file handling and WSGI middleware
- **Standard Library**: zipfile, tempfile, shutil, subprocess, threading for core functionality

### System Dependencies
- **Video Processing Tools**: External command-line tools (likely FFmpeg) for video generation
- **File System**: Temporary directory support for file processing workflows

### Configuration
- **Environment Variables**: SESSION_SECRET for secure session management
- **Runtime Settings**: Configurable upload limits, timeouts, and processing parameters