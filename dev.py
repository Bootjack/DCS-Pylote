#!/usr/bin/env python3
"""
Development setup script for DCS Pylote.

Usage:
    ipython dev.py
"""

import sys
import os
from pathlib import Path

# Add src to Python path
project_root = Path(__file__).parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

print("🚀 DCS Pylote Development Environment")
print("=" * 40)

def reload_modules(module_mapping=None, update_globals=True):
    """
    Reload specified modules and optionally update globals.
    
    Args:
        module_mapping: Dict of {'module.name': ['Class1', 'function2', ...]} 
                       If None, uses default DCS Pylote modules.
        update_globals: If True, updates the calling frame's globals directly.
    
    Usage in IPython:
        reload_modules()  # Reload defaults and update globals
        reload_modules({'my.module': ['MyClass']})  # Custom modules
        
    Customize the default mapping by editing the function.
    """
    import importlib
    import inspect
    
    # Default module mapping for DCS Pylote
    if module_mapping is None:
        module_mapping = {
            'dcs_pylote.vendor.dcs_client': ['DCSClient', 'DCSLaunchMode'],
            'dcs_pylote.main': ['main'],
            'dcs_pylote.utils.logger': ['setup_logging'],
        }
    
    print("🔄 Reloading modules...")
    
    fresh_imports = {}
    
    for module_name, items_to_import in module_mapping.items():
        try:
            # Reload or import the module
            if module_name in sys.modules:
                module = importlib.reload(sys.modules[module_name])
                print(f"  ✓ Reloaded: {module_name}")
            else:
                module = importlib.import_module(module_name)
                print(f"  ✓ Imported: {module_name}")
            
            # Extract specified items
            for item_name in items_to_import:
                if hasattr(module, item_name):
                    fresh_imports[item_name] = getattr(module, item_name)
                    print(f"    ✓ {item_name}")
                else:
                    print(f"    ✗ {item_name} not found in {module_name}")
                    
        except Exception as e:
            print(f"  ✗ Failed to reload {module_name}: {e}")
    
    print("🎯 Reload complete!")
    
    # Update globals in the calling frame if requested
    if update_globals:
        # Get the caller's frame (IPython session)
        caller_frame = inspect.currentframe().f_back
        caller_globals = caller_frame.f_globals
        
        for name, obj in fresh_imports.items():
            caller_globals[name] = obj
        
        print(f"📚 Updated {len(fresh_imports)} items in globals:")
        for name in fresh_imports:
            print(f"  {name}")
    else:
        print("📚 Available (not added to globals):")
        for name in fresh_imports:
            print(f"  {name}")
        return fresh_imports

# Convenient alias
reload = reload_modules

# Core imports
try:
    from dcs_pylote.vendor.dcs_client import DCSClient, DCSLaunchMode
    print("✓ DCSClient, DCSLaunchMode")
except ImportError as e:
    print(f"✗ DCSClient: {e}")

try:
    from dcs_pylote.main import main
    print("✓ main")
except ImportError as e:
    print(f"✗ main: {e}")

try:
    from dcs_pylote.utils.logger import setup_logging
    print("✓ setup_logging")
except ImportError as e:
    print(f"✗ setup_logging: {e}")

# Standard library imports
import time
import logging
import importlib

print("✓ Standard library modules")
print("✓ Reload utility")

print("\n📚 Ready to use:")
print("  DCSClient, DCSLaunchMode, main, setup_logging")
print("  time, logging, Path, os, sys, importlib")
print("\n🔄 Reload utility:")
print("  reload()  # Reload all modules and update globals automatically")

print("=" * 40)
