#!/usr/bin/env python3
"""
Vision Pro Integration Example
Simple, fast robot control perfect for Vision Pro apps
"""

import asyncio
from sparky import Robot, ConnectionMethod

async def vision_pro_control_demo():
    """
    Demonstrates the simplified API perfect for Vision Pro integration
    """
    print("Vision Pro Robot Control Demo")
    print("=" * 40)
    
    # Create robot instance - super simple!
    robot = Robot()
    
    try:
        # Connect to robot (default: local AP mode)
        print("Connecting to robot...")
        connected = await robot.connect()
        
        if not connected:
            print("Failed to connect to robot")
            return
        
        print(" Connected successfully!")
        
        # Get status
        status = await robot.get_status()
        print(f"Robot status: {status['connected']}")
        
        # Basic movements for Vision Pro gestures
        print("\nDemonstrating basic movements...")
        
        # Wave hello
        print("Waving hello...")
        await robot.hello()
        await asyncio.sleep(2)
        
        # Simple movements
        print("Moving forward...")
        await robot.move('forward', speed=0.3, duration=2.0)
        
        print("Turning left...")
        await robot.move('turn-left', speed=0.3, duration=2.0)
        
        # Check if moving
        is_moving = await robot.is_moving()
        print(f"🏃 Robot is moving: {is_moving}")
        
        # Sit down
        print("Sitting down...")
        await robot.sit()
        await asyncio.sleep(2)
        
        # Stand up
        print("Standing up...")
        await robot.stand_up()
        
        print("\n Demo completed successfully!")
        
    except Exception as e:
        print(f"Error during demo: {e}")
    
    finally:
        # Always disconnect
        print("Disconnecting...")
        await robot.disconnect()
        print("Goodbye!")

async def vision_pro_with_data_streaming():
    """
    Example with data streaming for real-time monitoring
    """
    print("\nVision Pro with Data Streaming")
    print("=" * 40)
    
    # Context manager ensures clean disconnect
    async with Robot() as robot:
        await robot.connect()
        
        # Start lightweight data streaming
        print("Starting data stream...")
        await robot.start_data_stream(analytics=True)
        
        # Perform some movements while monitoring
        await robot.hello()
        
        # Check real-time status
        status = await robot.get_status()
        print(f"Data streaming active: {status['data_streaming']}")
        
        # Movement with real-time feedback
        await robot.move('forward', 0.3, 1.0)
        is_moving = await robot.is_moving()
        print(f"🏃 Movement detected: {is_moving}")
        
        # Stop data stream
        await robot.stop_data_stream()
        print("Data streaming stopped")

if __name__ == "__main__":
    print("Starting Vision Pro Robot Control Examples")
    
    # Run basic demo
    asyncio.run(vision_pro_control_demo())
    
    # Run data streaming demo
    asyncio.run(vision_pro_with_data_streaming())
    
    print("\n All demos completed!")
    print("\nIntegration Tips for Vision Pro:")
    print("  • Use Robot() class for simple control")
    print("  • All methods are async/await compatible")
    print("  • Real-time status checking available")
    print("  • Lightweight data streaming for monitoring")
    print("  • Context manager support for clean resource management")