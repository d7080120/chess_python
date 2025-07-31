"""
conftest.py - הגדרות גלובליות לבדיקות
"""
import sys
import pathlib

# הוסף את src לpath כדי שהimports יעבדו
project_root = pathlib.Path(__file__).parent
sys.path.insert(0, str(project_root / "src"))
sys.path.insert(0, str(project_root))
