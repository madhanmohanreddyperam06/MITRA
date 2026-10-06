"""Unit tests for configuration management"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'backend'))

from app.core.config import settings

def test_settings_initialization():
    """Test that settings can be initialized"""
    assert settings is not None
    assert settings.APP_NAME is not None
    print("[PASS] Settings initialization test passed")

def test_default_values():
    """Test that default values are set correctly"""
    assert settings.APP_ENV == "development"
    assert settings.DEBUG == True
    assert settings.API_HOST == "127.0.0.1"
    assert settings.API_PORT == 8000
    assert settings.SPACY_MODEL == "en_core_web_sm"
    assert settings.CONFIDENCE_THRESHOLD == 0.5
    print("[PASS] Default values test passed")

def test_database_url():
    """Test database URL configuration"""
    assert settings.DATABASE_URL is not None
    assert "mysql" in settings.DATABASE_URL.lower()
    print("[PASS] Database URL test passed")

if __name__ == "__main__":
    try:
        test_settings_initialization()
        test_default_values()
        test_database_url()
        print("\n[PASS] All configuration tests passed")
    except Exception as e:
        print(f"\n[FAIL] Test failed: {e}")
        sys.exit(1)
