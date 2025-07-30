"""
migrate_legacy_tests.py - המרת טסטים ישנים ל pytest format
"""
import pathlib
import shutil


def migrate_test_files():
    """העבר קבצי טסט ישנים לתיקיית pytest_tests"""
    
    old_tests_dir = pathlib.Path(__file__).parent / "It1_interfaces"
    new_tests_dir = pathlib.Path(__file__).parent / "pytest_tests"
    
    # רשימת קבצי טסט שכדאי להעביר
    test_files_to_migrate = [
        "test_observer_score.py",
        "test_score_display.py", 
        "test_move_fixes.py",
        "test_integration_pytest.py",
        "test_refactored_pytest.py",
    ]
    
    print("🔄 מעביר קבצי טסט ל-pytest format...")
    
    for test_file in test_files_to_migrate:
        old_path = old_tests_dir / test_file
        if old_path.exists():
            new_path = new_tests_dir / f"legacy_{test_file}"
            
            try:
                shutil.copy2(old_path, new_path)
                print(f"✅ הועבר: {test_file} -> legacy_{test_file}")
                
                # עדכן imports בקובץ החדש
                update_imports_in_file(new_path)
                
            except Exception as e:
                print(f"❌ שגיאה בהעברת {test_file}: {e}")
    
    print("\n📋 קבצי טסט חדשים:")
    for test_file in new_tests_dir.glob("test_*.py"):
        print(f"   - {test_file.name}")


def update_imports_in_file(file_path):
    """עדכן imports בקובץ טסט"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # עדכון imports נפוצים
        imports_to_update = {
            'from unittest.mock import Mock': 'import pytest\nfrom unittest.mock import Mock',
            'import sys\nimport pathlib': 'import pytest\nimport sys\nimport pathlib',
        }
        
        for old_import, new_import in imports_to_update.items():
            if old_import in content and 'import pytest' not in content:
                content = content.replace(old_import, new_import)
        
        # הוסף fixtures אם נדרש
        if 'ScoreManager(' in content and '@pytest.fixture' not in content:
            content = """import pytest
from unittest.mock import Mock

@pytest.fixture
def mock_game():
    return Mock()

@pytest.fixture  
def score_manager(mock_game):
    from ScoreManager import ScoreManager
    return ScoreManager(mock_game)

""" + content
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
    except Exception as e:
        print(f"⚠️ לא ניתן לעדכן imports ב-{file_path.name}: {e}")


def create_test_runner():
    """צור קובץ להרצת כל הטסטים"""
    runner_content = '''"""
run_all_tests.py - הרצת כל הטסטים
"""
import subprocess
import sys
import pathlib

def run_pytest():
    """הרץ את כל הטסטים עם pytest"""
    print("🧪 מריץ את כל הטסטים עם pytest...")
    print("=" * 60)
    
    # הרץ pytest
    result = subprocess.run([
        sys.executable, "-m", "pytest", 
        "pytest_tests/",
        "-v",
        "--tb=short"
    ], cwd=pathlib.Path(__file__).parent)
    
    if result.returncode == 0:
        print("\\n🎉 כל הטסטים עברו בהצלחה!")
    else:
        print("\\n❌ יש טסטים שנכשלו")
    
    return result.returncode

if __name__ == "__main__":
    exit_code = run_pytest()
    sys.exit(exit_code)
'''
    
    runner_path = pathlib.Path(__file__).parent / "run_all_tests.py"
    with open(runner_path, 'w', encoding='utf-8') as f:
        f.write(runner_content)
    
    print(f"✅ נוצר: {runner_path.name}")


if __name__ == "__main__":
    migrate_test_files()
    create_test_runner()
    
    print("\n" + "=" * 60)
    print("🎉 המעבר ל-pytest הושלם!")
    print("\n📖 איך להריץ טסטים:")
    print("   pytest                    # כל הטסטים")
    print("   pytest test_score_manager.py    # טסט ספציפי")
    print("   pytest -v                 # עם פלט מפורט")
    print("   pytest -s                 # עם print statements")
    print("   python run_all_tests.py   # הרצה דרך סקריפט")
    print("\n🗂️ מבנה הטסטים החדש:")
    print("   pytest_tests/")
    print("   ├── conftest.py           # הגדרות משותפות")
    print("   ├── test_score_manager.py # טסטים ל-ScoreManager") 
    print("   ├── test_observer_system.py # טסטים ל-Observer")
    print("   └── test_integration.py   # טסטי אינטגרציה")
