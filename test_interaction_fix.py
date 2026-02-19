#!/usr/bin/env python3
"""
Test script to reproduce and verify the 'Task completed: Success' issue
This script demonstrates the problem and can be used to test the fix
"""

import asyncio
import sys
import os

# Add the DDOS-XO directory to path
sys.path.insert(0, '/home/ubuntu/DDOS-XO')

async def test_interaction():
    """Test the interaction to reproduce the issue"""
    
    print("\n" + "="*60)
    print("🌙 LUNA-ULTRA Interaction Test")
    print("Testing the 'Task completed: Success' issue")
    print("="*60)
    
    try:
        from core.controller import LunaController
        
        # Initialize controller
        print("\n[INFO] Initializing LunaController...")
        controller = LunaController("config")
        print("[SUCCESS] Controller initialized\n")
        
        # Test 1: Simple Greeting
        print("="*60)
        print("Test 1: Simple Greeting")
        print("="*60)
        user_input = "Hello, how are you?"
        print(f"User: {user_input}")
        response = await controller.process_input(user_input)
        print(f"LUNA: {response}")
        print(f"Expected: A friendly greeting response")
        print()
        
        # Test 2: Identity Check (Bengali)
        print("="*60)
        print("Test 2: Identity Check (Bengali)")
        print("="*60)
        user_input = "তোমার নাম কি এবং তোমাকে কে বানিয়েছে?"
        print(f"User: {user_input}")
        response = await controller.process_input(user_input)
        print(f"LUNA: {response}")
        print(f"Expected: Introduction in Bengali")
        print()
        
        # Test 3: API & Logic Check (THE PROBLEMATIC ONE)
        print("="*60)
        print("Test 3: API & Logic Check (PROBLEMATIC)")
        print("="*60)
        user_input = "What is the square root of 144 multiplied by 5?"
        print(f"User: {user_input}")
        response = await controller.process_input(user_input)
        print(f"LUNA: {response}")
        print(f"Expected: '60' or 'The answer is 60'")
        print(f"Actual Problem: 'Task completed: Success' (no actual answer)")
        
        # Check if the response contains the actual answer
        if "60" in response:
            print("\n✅ TEST PASSED: Response contains the correct answer!")
        elif "Task completed" in response and "60" not in response:
            print("\n❌ TEST FAILED: Got 'Task completed' without actual answer")
            print("   This is the bug we're trying to fix!")
        else:
            print("\n⚠️  TEST UNCLEAR: Response doesn't match expected patterns")
        
        print("\n" + "="*60)
        print("Test Completed!")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

async def main():
    """Main function"""
    # Ensure logs directory exists
    if not os.path.exists("/home/ubuntu/DDOS-XO/logs"):
        os.makedirs("/home/ubuntu/DDOS-XO/logs")
    
    # Change to DDOS-XO directory
    os.chdir("/home/ubuntu/DDOS-XO")
    
    success = await test_interaction()
    return 0 if success else 1

if __name__ == "__main__":
    try:
        sys.exit(asyncio.run(main()))
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nUnhandled exception: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
