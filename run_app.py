#!/usr/bin/env python3
"""
NiFi NL Builder - Startup Script

This script runs the Streamlit application with proper configuration.
"""

import subprocess
import sys
import os
from pathlib import Path

def main():
    """Run the Streamlit app"""
    print("🚀 Starting NiFi NL Builder...")
    
    # Get the directory where this script is located
    script_dir = Path(__file__).parent
    app_path = script_dir / "streamlit_app" / "app.py"
    
    # Check if the app file exists
    if not app_path.exists():
        print(f"❌ Error: App file not found at {app_path}")
        sys.exit(1)
    
    print(f"📁 App location: {app_path}")
    print("🌐 Starting Streamlit server...")
    print("📖 Open your browser to: http://localhost:8501")
    print("⏹️  Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        # Run the Streamlit app
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", str(app_path),
            "--server.port", "8501",
            "--server.address", "localhost",
            "--browser.gatherUsageStats", "false"
        ])
    except KeyboardInterrupt:
        print("\n👋 Shutting down NiFi NL Builder...")
    except Exception as e:
        print(f"❌ Error running the app: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 