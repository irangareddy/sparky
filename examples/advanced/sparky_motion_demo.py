"""
Sparky Motion Demo
Demonstrates the comprehensive motion control capabilities
"""

import asyncio
import logging
import sys
from sparky.core.connection import create_local_ap_connection
from sparky.core.motion import MotionController

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def sparky_motion_demo():
    """Demonstrate Sparky's motion control capabilities"""
    
    print(" Sparky Motion Control Demo")
    print("=" * 50)
    
    try:
        # Create connection
        print("�� Connecting to Go2 robot...")
        connection = await create_local_ap_connection()
        
        if not await connection.connect():
            print("Failed to connect to robot")
            return
        
        print(" Connected successfully!")
        
        # Create motion controller
        motion = MotionController(connection.conn)
        
        # Get initial status
        initial_mode = await motion.get_motion_mode()
        print(f"Data Initial motion mode: {initial_mode}")
        
        # Ensure we're in normal mode
        if initial_mode != "normal":
            print("Processing Switching to normal mode...")
            await motion.switch_motion_mode("normal")
        
        print("\n" + "=" * 50)
        print("BASIC MOVEMENT TESTS")
        print("=" * 50)
        
        # Test basic movements
        print("\nWalking Testing forward movement...")
        await motion.move_forward(speed=0.5, duration=3.0)
        
        print("\nWalking Testing backward movement...")
        await motion.move_backward(speed=0.5, duration=3.0)
        
        print("\nWalking Testing left movement...")
        await motion.move_left(speed=0.3, duration=2.0)
        
        print("\nWalking Testing right movement...")
        await motion.move_right(speed=0.3, duration=2.0)
        
        print("\nProcessing Testing left turn...")
        await motion.turn_left(speed=0.3, duration=2.0)
        
        print("\nProcessing Testing right turn...")
        await motion.turn_right(speed=0.3, duration=2.0)
        
        print("\n" + "=" * 50)
        print("SPORT COMMAND TESTS")
        print("=" * 50)
        
        # Test sport commands
        print("\nGoodbye Testing Hello command...")
        await motion.execute_sport_command("Hello")
        
        print("\n Testing Sit command...")
        await motion.execute_sport_command("Sit")
        await asyncio.sleep(2)
        
        print("\nLeg Testing StandUp command...")
        await motion.execute_sport_command("StandUp")
        await asyncio.sleep(2)
        
        print("\n" + "=" * 50)
        print("ADVANCED MOVEMENT TESTS")
        print("=" * 50)
        
        # Switch to AI mode for advanced commands
        print("\n Switching to AI mode for advanced commands...")
        await motion.switch_motion_mode("ai")
        
        print("\nHandstand Testing Handstand...")
        await motion.handstand(enable=True)
        await asyncio.sleep(3)
        
        print("\nLeg Returning to normal stance...")
        await motion.handstand(enable=False)
        await asyncio.sleep(2)
        
        print("\nDance Testing Dance1...")
        await motion.execute_sport_command("Dance1")
        
        print("\n" + "=" * 50)
        print("MOVEMENT PATTERNS")
        print("=" * 50)
        
        # Test movement patterns
        print("\nSquare Walking in a square pattern...")
        await motion.walk_square(side_length=0.3)
        
        print("\nProcessing Spinning 360 degrees...")
        await motion.spin_360(direction="right")
        
        print("\n" + "=" * 50)
        print("STATUS INFORMATION")
        print("=" * 50)
        
        # Show status
        status = motion.get_status()
        print(f"Current mode: {status['current_mode']}")
        print(f"Is moving: {status['is_moving']}")
        print(f"Available commands: {len(status['available_commands'])} commands")
        
        print("\n" + "=" * 50)
        print(" Sparky Motion Demo Completed!")
        print("=" * 50)
        
        # Keep running for a while
        await asyncio.sleep(10)
        
    except Exception as e:
        logger.error(f"Demo failed: {e}")
    finally:
        # Cleanup
        if 'connection' in locals():
            await connection.disconnect()

if __name__ == "__main__":
    try:
        asyncio.run(sparky_motion_demo())
    except KeyboardInterrupt:
        print("\nSTOP Demo interrupted by user")
        sys.exit(0)
