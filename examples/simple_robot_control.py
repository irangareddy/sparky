"""
Simple Robot Control Example
Demonstrates the new high-level Sparky API for easy robot control
"""

import asyncio
import logging

# Import the high-level API
from sparky import Robot, ConnectionMethod

# Enable logging to see what's happening
logging.basicConfig(level=logging.INFO)

async def simple_control_demo():
    """Demonstrate simple robot control using the high-level API"""
    
    print("Simple Robot Control Demo")
    print("=" * 40)
    
    # Create robot instance
    robot = Robot()
    
    try:
        # Connect to robot (defaults to LocalAP)
        print("Connecting to robot...")
        connected = await robot.connect()
        
        if not connected:
            print("Failed to connect to robot")
            return
        
        print(" Connected successfully!")
        
        # Check robot status
        status = await robot.get_status()
        print(f"Robot Status: {status['motion']['current_mode']}")
        
        # Basic movements
        print("\nTesting basic movements...")
        
        # Move forward
        print("Moving forward...")
        await robot.move("forward", speed=0.3, duration=2.0)
        
        # Turn left
        print("Turning left...")
        await robot.move("turn-left", speed=0.3, duration=1.0)
        
        # Move backward
        print("Moving backward...")
        await robot.move("backward", speed=0.3, duration=2.0)
        
        # Simple commands
        print("\nTesting simple commands...")
        
        # Say hello
        print("Saying hello...")
        await robot.hello()
        
        # Sit down
        print("Sitting down...")
        await robot.sit()
        
        # Stand up
        print("Standing up...")
        await robot.stand_up()
        
        # Dance
        print("Dancing...")
        await robot.dance(1)
        
        print("\n Demo completed successfully!")
        
    except Exception as e:
        print(f"Error during demo: {e}")
        
    finally:
        # Always disconnect when done
        print("\nCleaning up...")
        await robot.disconnect()
        print("Goodbye!")

async def advanced_control_demo():
    """Demonstrate advanced features with data streaming"""
    
    print("\nAdvanced Control Demo")
    print("=" * 40)
    
    # Using context manager for automatic cleanup
    async with Robot() as robot:
        # Connect with explicit method
        await robot.connect(ConnectionMethod.LOCAL_AP)
        
        # Start data streaming for analytics
        print("Starting data streaming...")
        await robot.start_data_stream()
        
        print("Performing monitored movements...")
        
        # Move and check if actually moving
        await robot.move("forward", speed=0.4, duration=3.0)
        
        is_moving = await robot.is_moving()
        print(f"Robot moving status: {is_moving}")
        
        # Perform complex pattern
        print("Walking in square pattern...")
        await robot.walk_square(0.4)
        
        # Export collected data
        print("Exporting movement data...")
        data = await robot.export_data("json")
        print(f"Exported {len(data)} data points")
        
        # Get final status
        final_status = await robot.get_status()
        print(f"Final status: {final_status['data_collection']}")

async def connection_methods_demo():
    """Demonstrate different connection methods"""
    
    print("\nConnection Methods Demo")
    print("=" * 40)
    
    robot = Robot()
    
    # Try LocalAP first
    print("Trying LocalAP connection...")
    if await robot.connect(ConnectionMethod.LOCAL_AP):
        print(" LocalAP connection successful")
        await robot.hello()
        await robot.disconnect()
    else:
        print("LocalAP connection failed")
        
        # Try LocalSTA as fallback
        print("Trying LocalSTA connection...")
        if await robot.connect(ConnectionMethod.LOCAL_STA, ip="192.168.8.181"):
            print(" LocalSTA connection successful")
            await robot.hello()
            await robot.disconnect()
        else:
            print("LocalSTA connection failed")

async def main():
    """Run all demos"""
    
    print("Sparky High-Level API Demo")
    print("=" * 50)
    print("This demo shows how easy it is to control robots with the new API!")
    print()
    
    # Run basic demo
    await simple_control_demo()
    
    # Ask user if they want to see advanced features
    try:
        response = input("\nRun advanced demo? (y/n): ")
        if response.lower() == 'y':
            await advanced_control_demo()
        
        response = input("\nTest connection methods? (y/n): ")
        if response.lower() == 'y':
            await connection_methods_demo()
            
    except KeyboardInterrupt:
        print("\nDemo interrupted by user")
    
    print("\nAll demos completed!")
    print("\nKey Benefits of the High-Level API:")
    print("   • Simple, intuitive methods")
    print("   • Automatic resource management")
    print("   • Built-in error handling")
    print("   • Context manager support")
    print("   • Optional advanced features")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nDemo interrupted. Goodbye!")
    except Exception as e:
        print(f"Demo failed: {e}")
