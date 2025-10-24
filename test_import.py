#!/usr/bin/env python3
"""
Test script to verify imports work correctly
"""

print("Testing imports...")

try:
    import os
    print("✅ os imported")
except ImportError as e:
    print(f"❌ os import failed: {e}")

try:
    import pandas as pd
    print("✅ pandas imported")
except ImportError as e:
    print(f"❌ pandas import failed: {e}")

try:
    from flask import Flask
    print("✅ Flask imported")
except ImportError as e:
    print(f"❌ Flask import failed: {e}")

try:
    from sarvamai import SarvamAI
    print("✅ SarvamAI imported")
except ImportError as e:
    print(f"❌ SarvamAI import failed: {e}")

try:
    import wave
    print("✅ wave imported")
except ImportError as e:
    print(f"❌ wave import failed: {e}")

try:
    import numpy as np
    print("✅ numpy imported")
except ImportError as e:
    print(f"❌ numpy import failed: {e}")

print("Import test completed!")
