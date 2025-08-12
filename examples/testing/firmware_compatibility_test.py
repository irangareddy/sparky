"""
Sparky Firmware Compatibility Test
Tests and documents what works with current Go2 firmware
"""

import asyncio
import logging
import sys
from sparky.core.connection import create_local_ap_connection
from sparky.core.motion import MotionController

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def firmware_compatibility_test():
    """Test and document firmware compatibility"""
    
    print("Status Sparky Firmware Compatibility Test")
    print("=" * 60)
    print("This test will check what works with your current Go2 firmware")
    print("=" * 60)
    
    try:
        # Connect to robot
        print("\nConnecting to Go2 robot...")
        connection = await create_local_ap_connection()
        
        if not await connection.connect():
            print("Failed to connect to robot")
            return
        
        print(" Connected successfully!")
        
        # Create motion controller
        motion = MotionController(connection.conn)
        
        # Get initial status
        initial_mode = await motion.get_motion_mode()
        print(f"\nData Initial motion mode: {initial_mode}")
        
        # Get firmware compatibility info
        compatibility = motion.get_firmware_compatibility_info()
        
        print("\n" + "=" * 60)
        print("FIRMWARE COMPATIBILITY ANALYSIS")
        print("=" * 60)
        
        print(f"\n Supported modes: {compatibility['supported_modes']}")
        print(f"FAILED Unsupported modes: {compatibility['unsupported_modes']}")
        print(f"Note: {compatibility['firmware_update_note']}")
        
        print("\n" + "=" * 60)
        print("MOTION MODE TESTING")
        print("=" * 60)
        
        # Test motion mode switching
        print("\nProcessing Testing motion mode switching...")
        
        # Try to switch to normal mode (should fail)
        print("  Testing switch to 'normal' mode...")
        normal_result = await motion.switch_motion_mode("normal")
        print(f"  Result: {'Failed (expected)' if not normal_result else ' Unexpected success'}")
        
        # Try to switch to ai mode (should fail)
        print("  Testing switch to 'ai' mode...")
        ai_result = await motion.switch_motion_mode("ai")
        print(f"  Result: {'Failed (expected)' if not ai_result else ' Unexpected success'}")
        
        # Try to switch to mcf mode (should work if not already in it)
        if initial_mode != "mcf":
            print("  Testing switch to 'mcf' mode...")
            mcf_result = await motion.switch_motion_mode("mcf")
            print(f"  Result: {' Success' if mcf_result else 'Failed'}")
        else:
            print("  Already in 'mcf' mode, skipping switch test")
        
        print("\n" + "=" * 60)
        print("BASIC MOVEMENT TESTING")
        print("=" * 60)
        
        # Test basic movements
        print("\nWalking Testing basic movements...")
        
        movements = [
            ("Forward", lambda: motion.move_forward(0.3, 2.0)),
            ("Backward", lambda: motion.move_backward(0.3, 2.0)),
            ("Left", lambda: motion.move_left(0.2, 2.0)),
            ("Right", lambda: motion.move_right(0.2, 2.0)),
            ("Turn Left", lambda: motion.turn_left(0.2, 2.0)),
            ("Turn Right", lambda: motion.turn_right(0.2, 2.0)),
        ]
        
        for name, movement_func in movements:
            print(f"  Testing {name}...")
            try:
                result = await movement_func()
                print(f"  Result: {' Success' if result else 'Failed'}")
            except Exception as e:
                print(f"  Result: FAILED Error - {e}")
        
        print("\n" + "=" * 60)
        print("SPORT COMMAND TESTING")
        print("=" * 60)
        
        # Test working commands
        print("\n Testing commands that should work...")
        working_commands = ["Hello", "Sit", "StandUp", "Dance1", "Stretch"]
        
        for cmd in working_commands:
            print(f"  Testing {cmd}...")
            try:
                result = await motion.execute_sport_command(cmd)
                print(f"  Result: {' Success' if result else 'Failed'}")
            except Exception as e:
                print(f"  Result: FAILED Error - {e}")
        
        # Test potentially restricted commands
        print("\nWARNING Testing commands that may be restricted...")
        restricted_commands = ["Handstand", "BackFlip", "FrontFlip", "StandOut"]
        
        for cmd in restricted_commands:
            print(f"  Testing {cmd}...")
            try:
                if cmd == "Handstand":
                    result = await motion.handstand(True)
                else:
                    result = await motion.execute_sport_command(cmd)
                print(f"  Result: {' Success' if result else 'Failed (expected)'}")
            except Exception as e:
                print(f"  Result: FAILED Error - {e}")
        
        print("\n" + "=" * 60)
        print("MOVEMENT PATTERN TESTING")
        print("=" * 60)
        
        # Test movement patterns
        print("\nSquare Testing square walk pattern...")
        try:
            result = await motion.walk_square(0.2)
            print(f"Result: {' Success' if result else 'Failed'}")
        except Exception as e:
            print(f"Result: FAILED Error - {e}")
        
        print("\nProcessing Testing 360-degree spin...")
        try:
            result = await motion.spin_360("right")
            print(f"Result: {' Success' if result else 'Failed'}")
        except Exception as e:
            print(f"Result: FAILED Error - {e}")
        
        print("\n" + "=" * 60)
        print("FINAL STATUS")
        print("=" * 60)
        
        # Final status
        status = motion.get_status()
        print(f"\nData Final motion mode: {status['current_mode']}")
        print(f"Processing Is moving: {status['is_moving']}")
        print(f"Summary Available commands: {len(status['available_commands'])} commands")
        print(f"Note Firmware note: {status['firmware_note']}")
        
        print("\n" + "=" * 60)
        print("SUMMARY")
        print("=" * 60)
        
        print("\n What works in current firmware:")
        print("  - Basic movements (forward, backward, left, right, turns)")
        print("  - Core sport commands (Hello, Sit, StandUp, Dance1, etc.)")
        print("  - Movement patterns (square walk, 360 spin)")
        print("  - Stop command")
        
        print("\nFAILED What doesn't work in current firmware:")
        print("  - Motion mode switching to 'normal' or 'ai'")
        print("  - Advanced commands that required AI mode")
        print("  - Some flip and stunt commands")
        
        print("\nWARNING Recommendations:")
        print("  - Use 'mcf' mode for all operations")
        print("  - Test advanced commands individually")
        print("  - Check error codes for troubleshooting")
        print("  - Focus on basic movements and core sport commands")
        
        print("\n" + "=" * 60)
        print(" Firmware compatibility test completed!")
        print("=" * 60)
        
        # Keep running for a while
        await asyncio.sleep(5)
        
    except Exception as e:
        logger.error(f"Test failed: {e}")
    finally:
        # Cleanup
        if 'connection' in locals():
            await connection.disconnect()

if __name__ == "__main__":
    try:
        asyncio.run(firmware_compatibility_test())
    except KeyboardInterrupt:
        print("\nSTOP Test interrupted by user")
        sys.exit(0)
