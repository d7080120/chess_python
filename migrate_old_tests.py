"""
migrate_old_tests.py - מעביר טסטים ישנים לתיקיית old_tests
"""
import pathlib
import shutil

def migrate_old_tests():
    """העבר טסטים ישנים לתיקייה נפרדת"""
    
    project_root = pathlib.Path(__file__).parent
    it1_interfaces = project_root / "It1_interfaces"
    old_tests_dir = project_root / "old_tests"
    
    # צור תיקיית old_tests
    old_tests_dir.mkdir(exist_ok=True)
    
    # רשימת קבצי טסט ישנים
    old_test_files = [
        "test_observer_score.py",
        "test_real_capture_fixed.py", 
        "test_move_fixes.py",
        "test_score_display.py",
        "test_integration_pytest.py",
        "test_refactored_pytest.py",
        "test_refactored.py",
        "test_capture_simple.py",
        "test_capture.py",
        "test_jump_in_place.py",
        "test_jump.py",
        "test_keys.py",
        "test_pawn_promotion.py",
        "test_player_names.py",
        "test_real_promotion.py",
        "test_wasd.py",
        "simple_capture_test.py",
        "demo_with_names.py",
        "enhanced_game_summary.py",
        "enhanced_player_features.py",
        "fixes_summary.py",
        "observer_migration_summary.py"
    ]
    
    moved_files = []
    not_found_files = []
    
    for test_file in old_test_files:
        source_path = it1_interfaces / test_file
        if source_path.exists():
            dest_path = old_tests_dir / test_file
            try:
                shutil.move(str(source_path), str(dest_path))
                moved_files.append(test_file)
                print(f"✅ הועבר: {test_file}")
            except Exception as e:
                print(f"❌ שגיאה בהעברת {test_file}: {e}")
        else:
            not_found_files.append(test_file)
    
    # צור README בתיקיית old_tests
    readme_content = """# Old Tests Directory

This directory contains old test files that were migrated from It1_interfaces.

## Migrated Files:
"""
    for file in moved_files:
        readme_content += f"- {file}\n"
    
    if not_found_files:
        readme_content += "\n## Files Not Found (may have been already moved or deleted):\n"
        for file in not_found_files:
            readme_content += f"- {file}\n"
    
    readme_content += """
## New Test Structure:
- Modern tests are now in `tests_new/` directory
- Uses pytest framework
- Organized by functionality
- Proper fixtures and test isolation

## Running Old Tests:
These old tests may need path adjustments to run correctly from this location.
For new development, use the tests in `tests_new/` directory.
"""
    
    readme_path = old_tests_dir / "README.md"
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print(f"\n📊 סיכום ההעברה:")
    print(f"✅ הועברו: {len(moved_files)} קבצים")
    print(f"❌ לא נמצאו: {len(not_found_files)} קבצים")
    print(f"📝 נוצר: README.md בתיקיית old_tests")
    print(f"\n🎯 הטסטים החדשים נמצאים ב-tests_new/")
    print(f"🚀 הרץ עם: pytest tests_new/")

if __name__ == "__main__":
    migrate_old_tests()
