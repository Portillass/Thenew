#!/usr/bin/env python3
"""
PDF Tool Startup Script
A simple script to check dependencies and start the PDF tool application.
"""

import sys
import subprocess
import os

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 7):
        print("❌ Error: Python 3.7 or higher is required.")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = [
        'flask', 'PyPDF2', 'gtts', 'werkzeug'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} is installed")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package} is missing")
    
    if missing_packages:
        print(f"\n📦 Installing missing packages: {', '.join(missing_packages)}")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
            print("✅ All dependencies installed successfully!")
        except subprocess.CalledProcessError:
            print("❌ Failed to install dependencies. Please run: pip install -r requirements.txt")
            return False
    
    return True

def create_directories():
    """Create necessary directories if they don't exist"""
    directories = ['uploads', 'audio', 'templates']
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"📁 Created directory: {directory}")
        else:
            print(f"✅ Directory exists: {directory}")

def main():
    """Main startup function"""
    print("🚀 Starting PDF Tool...")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Check and install dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Create necessary directories
    create_directories()
    
    print("\n" + "=" * 50)
    print("🎉 All checks passed! Starting the application...")
    print("🌐 The application will be available at: http://localhost:5000")
    print("📖 Press Ctrl+C to stop the server")
    print("=" * 50)
    
    # Import and run the Flask app
    try:
        from app import app
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main() 