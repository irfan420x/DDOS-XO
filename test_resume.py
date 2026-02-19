import asyncio
import logging
import os
import json
from core.controller import LunaController

# Setup logging
logging.basicConfig(level=logging.INFO)

async def test_resume_feature():
    print("\n🚀 Testing LUNA-ULTRA Resume Feature")
    print("======================================")
    
    controller = LunaController()
    
    # 1. Simulate a token limit error response
    print("\nStep 1: Simulating a Token Limit Error...")
    fake_error_response = "TOKEN_LIMIT_ERROR: The context length has been exceeded."
    
    # Manually trigger the handler to see if it saves state
    # We need to have an active execution state first
    controller.master_orchestrator.state_manager.initialize_execution(
        "Build a complex app", 
        {"steps": [{"agent": "architect", "action": "plan", "params": {}}]}
    )
    
    await controller.resume_engine.handle_token_limit_error(fake_error_response)
    
    if os.path.exists("data/agent_execution_state.json"):
        print("✅ State saved successfully in data/agent_execution_state.json")
        with open("data/agent_execution_state.json", "r") as f:
            state = json.load(f)
            print(f"   Saved Goal: {state.get('goal')}")
            print(f"   Status: {state.get('status')}")
    else:
        print("❌ Failed to save state.")
        return

    # 2. Test the 'resume' command
    print("\nStep 2: Testing 'resume' command...")
    # Note: This will try to actually call the LLM if we let it run fully, 
    # so we just check if it enters the resume logic.
    try:
        # We'll mock the resume_execution to avoid actual LLM calls in this test
        original_resume = controller.resume_engine.resume_execution
        async def mock_resume():
            return {"success": True, "message": "MOCK: Resumed successfully"}
        controller.resume_engine.resume_execution = mock_resume
        
        response = await controller.process_input("resume")
        print(f"   Controller Response: {response}")
        
        if "Resumed:" in response:
            print("✅ Resume command recognized and triggered.")
        else:
            print("❌ Resume command failed.")
    finally:
        controller.resume_engine.resume_execution = original_resume

    print("\n======================================")
    print("🎉 Resume Feature Test Completed!")

if __name__ == "__main__":
    asyncio.run(test_resume_feature())
