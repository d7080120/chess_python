try:
    import PlayerNameDialog
    print("✅ PlayerNameDialog imports successfully")
except Exception as e:
    print(f"❌ Import error: {e}")
    
try:
    from PlayerNameDialog import PlayerNameDialog
    print("✅ PlayerNameDialog class imports successfully")
except Exception as e:
    print(f"❌ Class import error: {e}")
