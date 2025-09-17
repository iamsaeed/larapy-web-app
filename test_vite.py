#!/usr/bin/env python3

import sys
import os
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

from larapy.foundation.application import Application
from larapy.view.engine import ViewEngine

# Create a test app
app = Application(str(Path(__file__).parent))

# Setup view engine
view_engine = ViewEngine()
view_engine.init_app(app.flask_app, str(Path(__file__).parent))

# Test the vite function
with app.flask_app.app_context():
    vite_func = app.flask_app.jinja_env.globals.get('vite')
    if vite_func:
        result = vite_func(['resources/css/app.css', 'resources/js/app.js'])
        print("Vite function output:")
        print(result)

        # Check if manifest exists
        manifest_path = Path.cwd() / 'public' / 'build' / '.vite' / 'manifest.json'
        print(f"\nManifest path: {manifest_path}")
        print(f"Manifest exists: {manifest_path.exists()}")

        if manifest_path.exists():
            import json
            with open(manifest_path) as f:
                manifest = json.load(f)
            print(f"Manifest content: {manifest}")
    else:
        print("Vite function not found!")