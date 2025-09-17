#!/usr/bin/env python3
"""
Simple Larapy Package Updater
Simple script to update the package without external dependencies
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path

class LarapyUpdater:
    """Simple package updater"""
    
    def __init__(self):
        self.website_dir = Path(__file__).parent
        self.package_dir = self.website_dir.parent / "package-larapy"
    
    def update_package(self, verbose=True):
        """Update the package installation"""
        if verbose:
            print("🔄 Updating Larapy package...")
        
        try:
            # Change to website directory
            os.chdir(self.website_dir)
            
            # Uninstall current package
            if verbose:
                print("📦 Uninstalling current package...")
            
            result = subprocess.run([
                sys.executable, "-m", "pip", "uninstall", "larapy", "-y"
            ], capture_output=True, text=True)
            
            # Install package in editable mode
            if verbose:
                print("📦 Installing updated package...")
            
            result = subprocess.run([
                sys.executable, "-m", "pip", "install", "-e", str(self.package_dir)
            ], capture_output=True, text=True)
            
            if result.returncode != 0:
                print(f"❌ Installation failed: {result.stderr}")
                return False
            
            # Test import
            if verbose:
                print("✅ Testing import...")
            
            test_result = subprocess.run([
                sys.executable, "-c", 
                "import larapy; from larapy.core.application import Application; print('✅ Import successful')"
            ], capture_output=True, text=True)
            
            if test_result.returncode == 0:
                if verbose:
                    print("🎉 Package updated successfully!")
                return True
            else:
                print(f"❌ Import test failed: {test_result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Error updating package: {e}")
            return False
    
    def check_package_exists(self):
        """Check if package directory exists"""
        return self.package_dir.exists()
    
    def get_package_info(self):
        """Get package information"""
        try:
            result = subprocess.run([
                sys.executable, "-c", 
                "import larapy; print(getattr(larapy, '__version__', 'development'))"
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                return result.stdout.strip()
            else:
                return "Not installed"
        except:
            return "Error getting version"

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Update Larapy package")
    parser.add_argument("--quiet", "-q", action="store_true",
                       help="Quiet mode - minimal output")
    parser.add_argument("--check", "-c", action="store_true",
                       help="Check current package status")
    
    args = parser.parse_args()
    
    updater = LarapyUpdater()
    
    if not updater.check_package_exists():
        print(f"❌ Package directory not found: {updater.package_dir}")
        sys.exit(1)
    
    if args.check:
        print(f"📦 Package directory: {updater.package_dir}")
        print(f"📋 Current version: {updater.get_package_info()}")
        return
    
    if not args.quiet:
        print("🔄 Larapy Package Updater")
        print("-" * 30)
    
    success = updater.update_package(verbose=not args.quiet)
    
    if success:
        if not args.quiet:
            print(f"📋 Updated version: {updater.get_package_info()}")
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
