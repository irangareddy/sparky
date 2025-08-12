import asyncio
import logging
import json
import sys
from pathlib import Path

# Add the src directory to the path so we can import sparky modules
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from sparky import Robot

# Enable logging for debugging
logging.basicConfig(level=logging.FATAL)

async def test_forward_movements():
    """Systematically test forward movement with different parameters"""
    
    try:
        # Connect to robot
        print("Connecting to Go2 robot...")
        conn = Go2WebRTCConnection(WebRTCConnectionMethod.LocalAP)
        await conn.connect()
        print(" Connected successfully!")
        
        # Ensure we're in normal mode
        print("Processing Checking motion mode...")
        response = await conn.datachannel.pub_sub.publish_request_new(
            RTC_TOPIC["MOTION_SWITCHER"], 
            {"api_id": 1001}
        )
        
        if response['data']['header']['status']['code'] == 0:
            data = json.loads(response['data']['data'])
            current_mode = data['name']
            print(f"Data Current mode: {current_mode}")
            
            if current_mode != "normal":
                print("Processing Switching to normal mode...")
                await conn.datachannel.pub_sub.publish_request_new(
                    RTC_TOPIC["MOTION_SWITCHER"], 
                    {
                        "api_id": 1002,
                        "parameter": {"name": "normal"}
                    }
                )
                await asyncio.sleep(5)
        
        # Test different forward movement speeds
        print("\n" + "="*60)
        print("FORWARD MOVEMENT TESTING")
        print("="*60)
        
        # Test 1: Very slow forward
        print("\nWalking Test 1: Very slow forward (x=0.1)")
        await conn.datachannel.pub_sub.publish_request_new(
            RTC_TOPIC["SPORT_MOD"], 
            {
                "api_id": SPORT_CMD["Move"],
                "parameter": {"x": 0.1, "y": 0, "z": 0}
            }
        )
        await asyncio.sleep(3)
        
        # Test 2: Slow forward
        print("\nWalking Test 2: Slow forward (x=0.3)")
        await conn.datachannel.pub_sub.publish_request_new(
            RTC_TOPIC["SPORT_MOD"], 
            {
                "api_id": SPORT_CMD["Move"],
                "parameter": {"x": 0.3, "y": 0, "z": 0}
            }
        )
        await asyncio.sleep(3)
        
        # Test 3: Medium forward (same as working backward)
        print("\nWalking Test 3: Medium forward (x=0.5) - same as working backward")
        await conn.datachannel.pub_sub.publish_request_new(
            RTC_TOPIC["SPORT_MOD"], 
            {
                "api_id": SPORT_CMD["Move"],
                "parameter": {"x": 0.5, "y": 0, "z": 0}
            }
        )
        await asyncio.sleep(3)
        
        # Test 4: Fast forward
        print("\nWalking Test 4: Fast forward (x=0.8)")
        await conn.datachannel.pub_sub.publish_request_new(
            RTC_TOPIC["SPORT_MOD"], 
            {
                "api_id": SPORT_CMD["Move"],
                "parameter": {"x": 0.8, "y": 0, "z": 0}
            }
        )
        await asyncio.sleep(3)
        
        # Test 5: Maximum forward
        print("\nWalking Test 5: Maximum forward (x=1.0)")
        await conn.datachannel.pub_sub.publish_request_new(
            RTC_TOPIC["SPORT_MOD"], 
            {
                "api_id": SPORT_CMD["Move"],
                "parameter": {"x": 1.0, "y": 0, "z": 0}
            }
        )
        await asyncio.sleep(3)
        
        # Test 6: Forward with slight turn
        print("\nWalking Test 6: Forward with slight right turn (x=0.5, z=-0.1)")
        await conn.datachannel.pub_sub.publish_request_new(
            RTC_TOPIC["SPORT_MOD"], 
            {
                "api_id": SPORT_CMD["Move"],
                "parameter": {"x": 0.5, "y": 0, "z": -0.1}
            }
        )
        await asyncio.sleep(3)
        
        # Test 7: Forward with slight left turn
        print("\nWalking Test 7: Forward with slight left turn (x=0.5, z=0.1)")
        await conn.datachannel.pub_sub.publish_request_new(
            RTC_TOPIC["SPORT_MOD"], 
            {
                "api_id": SPORT_CMD["Move"],
                "parameter": {"x": 0.5, "y": 0, "z": 0.1}
            }
        )
        await asyncio.sleep(3)
        
        # Stop movement
        print("\nSTOP Stopping movement...")
        await conn.datachannel.pub_sub.publish_request_new(
            RTC_TOPIC["SPORT_MOD"], 
            {
                "api_id": SPORT_CMD["StopMove"]
            }
        )
        
        print("\n" + "="*60)
        print(" Forward movement testing completed!")
        print("="*60)
        
        # Keep running for observation
        await asyncio.sleep(10)
        
    except Exception as e:
        print(f"FAILED Error: {e}")

if __name__ == "__main__":
    try:
        asyncio.run(test_forward_movements())
    except KeyboardInterrupt:
        print("\nSTOP Testing interrupted by user")
        sys.exit(0)
