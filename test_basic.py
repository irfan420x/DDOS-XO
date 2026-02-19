#!/usr/bin/env python3
"""
LUNA-ULTRA Basic Test Script
Tests core functionality without requiring API keys or GUI
"""

import sys
import os
import asyncio
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def test_imports():
    """Test if all core modules can be imported"""
    print("\n" + "="*60)
    print("TEST 1: Module Import Test")
    print("="*60)
    
    modules_to_test = [
        ('app.bootstrap', 'LunaBootstrap'),
        ('core.controller', 'LunaController'),
        ('core.orchestrator', 'Orchestrator'),
        ('core.state_manager', 'StateManager'),
        ('core.cognitive_mode', 'CognitiveMode'),
        ('memory.memory_manager', 'MemoryManager'),
        ('security.permission_engine', 'PermissionEngine'),
        ('llm.router', 'LLMRouter'),
    ]
    
    passed = 0
    failed = 0
    
    for module_path, class_name in modules_to_test:
        try:
            module = __import__(module_path, fromlist=[class_name])
            cls = getattr(module, class_name)
            print(f"✅ {module_path}.{class_name} - OK")
            passed += 1
        except Exception as e:
            print(f"❌ {module_path}.{class_name} - FAILED: {str(e)}")
            failed += 1
    
    print(f"\nResult: {passed} passed, {failed} failed")
    return failed == 0

def test_config_loading():
    """Test if configuration files can be loaded"""
    print("\n" + "="*60)
    print("TEST 2: Configuration Loading Test")
    print("="*60)
    
    config_files = [
        'config/core.yaml',
        'config/llm.yaml',
        'config/security.yaml',
        'config/automation.yaml',
        'config/features.yaml',
        'config/system_prompt.txt'
    ]
    
    passed = 0
    failed = 0
    
    for config_file in config_files:
        if os.path.exists(config_file):
            try:
                if config_file.endswith('.yaml'):
                    import yaml
                    with open(config_file, 'r') as f:
                        data = yaml.safe_load(f)
                    print(f"✅ {config_file} - OK (loaded {len(data) if data else 0} keys)")
                else:
                    with open(config_file, 'r') as f:
                        content = f.read()
                    print(f"✅ {config_file} - OK ({len(content)} chars)")
                passed += 1
            except Exception as e:
                print(f"❌ {config_file} - FAILED: {str(e)}")
                failed += 1
        else:
            print(f"⚠️  {config_file} - NOT FOUND")
            failed += 1
    
    print(f"\nResult: {passed} passed, {failed} failed")
    return failed == 0

def test_directory_structure():
    """Test if all required directories exist"""
    print("\n" + "="*60)
    print("TEST 3: Directory Structure Test")
    print("="*60)
    
    required_dirs = [
        'app', 'core', 'agents', 'llm', 'automation',
        'security', 'memory', 'config', 'logs'
    ]
    
    passed = 0
    failed = 0
    
    for directory in required_dirs:
        if os.path.exists(directory) and os.path.isdir(directory):
            file_count = len([f for f in os.listdir(directory) if f.endswith('.py')])
            print(f"✅ {directory}/ - OK ({file_count} Python files)")
            passed += 1
        else:
            print(f"❌ {directory}/ - NOT FOUND")
            failed += 1
    
    print(f"\nResult: {passed} passed, {failed} failed")
    return failed == 0

async def test_basic_functionality():
    """Test basic controller initialization"""
    print("\n" + "="*60)
    print("TEST 4: Basic Functionality Test")
    print("="*60)
    
    try:
        # Create logs directory if not exists
        if not os.path.exists("logs"):
            os.makedirs("logs")
        
        print("Attempting to initialize LunaController...")
        from core.controller import LunaController
        
        # This will fail without API keys, but we can check if it initializes
        controller = LunaController("config")
        print("✅ LunaController initialized successfully")
        
        # Test basic methods
        status = controller.get_status()
        print(f"✅ Controller status: {status}")
        
        return True
    except Exception as e:
        print(f"❌ Basic functionality test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_agent_loading():
    """Test if agents can be loaded"""
    print("\n" + "="*60)
    print("TEST 5: Agent Loading Test")
    print("="*60)
    
    agent_files = [
        'agents/code_agent.py',
        'agents/automation_agent.py',
        'agents/system_agent.py',
        'agents/architect_agent.py',
        'agents/dynamic_agent.py',
        'agents/screen_agent.py',
    ]
    
    passed = 0
    failed = 0
    
    for agent_file in agent_files:
        if os.path.exists(agent_file):
            try:
                # Try to compile the file
                import py_compile
                py_compile.compile(agent_file, doraise=True)
                print(f"✅ {agent_file} - Syntax OK")
                passed += 1
            except Exception as e:
                print(f"❌ {agent_file} - FAILED: {str(e)}")
                failed += 1
        else:
            print(f"⚠️  {agent_file} - NOT FOUND")
            failed += 1
    
    print(f"\nResult: {passed} passed, {failed} failed")
    return failed == 0

def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("🌙 LUNA-ULTRA Basic Test Suite")
    print("="*60)
    
    results = []
    
    # Run tests
    results.append(("Module Import", test_imports()))
    results.append(("Configuration Loading", test_config_loading()))
    results.append(("Directory Structure", test_directory_structure()))
    results.append(("Agent Loading", test_agent_loading()))
    
    # Run async test
    try:
        result = asyncio.run(test_basic_functionality())
        results.append(("Basic Functionality", result))
    except Exception as e:
        print(f"Failed to run async test: {e}")
        results.append(("Basic Functionality", False))
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name}: {status}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! LUNA-ULTRA is ready to use.")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
