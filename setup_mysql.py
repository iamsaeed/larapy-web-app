#!/usr/bin/env python3
"""
MySQL Database Setup Script for Larapy MyApp

This script helps set up the MySQL database for the Larapy application.
Run this before starting the application.
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def create_mysql_database():
    """Create MySQL database if it doesn't exist"""
    try:
        import pymysql
        
        # Database connection parameters
        host = os.getenv('DB_HOST', '127.0.0.1')
        port = int(os.getenv('DB_PORT', '3306'))
        username = os.getenv('DB_USERNAME', 'root')
        password = os.getenv('DB_PASSWORD', '')
        database = os.getenv('DB_DATABASE', 'larapy_myapp')
        
        print(f"🔧 Setting up MySQL database: {database}")
        print(f"📍 Host: {host}:{port}")
        print(f"👤 User: {username}")
        
        # Connect to MySQL server (without specifying database)
        connection = pymysql.connect(
            host=host,
            port=port,
            user=username,
            password=password,
            charset='utf8mb4'
        )
        
        with connection.cursor() as cursor:
            # Create database if it doesn't exist
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{database}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            print(f"✅ Database '{database}' created or already exists")
            
            # Show databases
            cursor.execute("SHOW DATABASES")
            databases = cursor.fetchall()
            print("\n📋 Available databases:")
            for db in databases:
                marker = "🎯" if db[0] == database else "  "
                print(f"{marker} {db[0]}")
        
        connection.close()
        
        # Test connection to the specific database
        test_connection = pymysql.connect(
            host=host,
            port=port,
            user=username,
            password=password,
            database=database,
            charset='utf8mb4'
        )
        test_connection.close()
        
        print(f"\n✅ Successfully connected to database '{database}'")
        print("\n🚀 Ready to run migrations!")
        print("   Run: ./larapy migrate:install")
        print("   Then: ./larapy migrate")
        
        return True
        
    except ImportError:
        print("❌ PyMySQL not installed")
        print("📦 Install with: pip install PyMySQL cryptography")
        return False
        
    except Exception as e:
        print(f"❌ Database setup failed: {e}")
        print("\n🔍 Troubleshooting:")
        print("   - Check MySQL server is running")
        print("   - Verify credentials in .env file")
        print("   - Ensure user has CREATE DATABASE privileges")
        return False

def show_config():
    """Show current database configuration"""
    print("\n📄 Current Configuration (.env):")
    print(f"   DB_CONNECTION: {os.getenv('DB_CONNECTION')}")
    print(f"   DB_HOST: {os.getenv('DB_HOST')}")
    print(f"   DB_PORT: {os.getenv('DB_PORT')}")
    print(f"   DB_DATABASE: {os.getenv('DB_DATABASE')}")
    print(f"   DB_USERNAME: {os.getenv('DB_USERNAME')}")
    print(f"   DB_PASSWORD: {'*' * len(os.getenv('DB_PASSWORD', ''))}")

def main():
    """Main setup function"""
    print("🔰 Larapy MySQL Database Setup")
    print("=" * 40)
    
    show_config()
    
    if create_mysql_database():
        print("\n🎉 Database setup completed successfully!")
    else:
        print("\n💥 Database setup failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()