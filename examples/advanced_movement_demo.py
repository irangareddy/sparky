#!/usr/bin/env python3
"""
Advanced Movement Demo for Go2 Robot
Simple demonstration of advanced movement capabilities

This script provides a user-friendly way to test individual advanced movements
or run the complete test suite.
"""

import asyncio
import logging
import sys
from pathlib import Path

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sparky import Robot
from sparky.utils.constants import ConnectionMethod

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def demo_individual_movements():
    """Demo individual advanced movements with user interaction"""
    print("🎪 Advanced Movement Demo")
    print("=" * 40)
    print("This demo allows you to test individual advanced movements.")
    print("⚠️  Ensure robot has adequate space and soft landing area!")
    print()
    
    # Connect to robot
    robot = Robot()
    try:
        print("🔗 Connecting to robot...")
        success = await robot.connect(ConnectionMethod.LOCALAP)
        if not success:
            print("❌ Failed to connect to robot")
            return
        print("✅ Connected successfully!")
        
        # Prepare robot
        print("🧍 Preparing robot...")
        await robot.command("BalanceStand")
        await asyncio.sleep(2)
        
        # Menu-driven testing
        movements = {
            "1": ("Front Jump", robot.front_jump),
            "2": ("Front Pounce", robot.front_pounce),
            "3": ("Front Flip", robot.front_flip),
            "4": ("Back Flip", robot.back_flip),
            "5": ("Left Flip", robot.left_flip),
            "6": ("Right Flip", robot.right_flip),
            "7": ("Handstand", robot.handstand),
            "8": ("Test All Availability", None)
        }
        
        while True:
            print("\n🎯 Available Advanced Movements:")
            for key, (name, _) in movements.items():
                print(f"   {key}. {name}")
            print("   q. Quit")
            
            choice = input("\nSelect movement to test (1-8 or q): ").strip().lower()
            
            if choice == 'q':
                break
            elif choice == '8':
                print("🔍 Testing movement availability...")
                availability = await robot.test_advanced_movements()
                print("\n📊 Availability Results:")
                for cmd, available in availability.items():
                    status = "✅ Available" if available else "❌ Not Available"
                    print(f"   {cmd}: {status}")
            elif choice in movements and choice != '8':
                name, func = movements[choice]
                print(f"\n🎯 Testing {name}...")
                print("⚠️  Executing in 3 seconds - be ready!")
                await asyncio.sleep(3)
                
                try:
                    success = await func()
                    if success:
                        print(f"✅ {name} executed successfully!")
                    else:
                        print(f"❌ {name} failed or not available")
                except Exception as e:
                    print(f"❌ {name} error: {e}")
                
                # Recovery
                print("🔄 Allowing recovery time...")
                await asyncio.sleep(3)
                await robot.command("BalanceStand")
                await asyncio.sleep(2)
            else:
                print("❌ Invalid choice")
        
    except KeyboardInterrupt:
        print("\n🛑 Demo interrupted by user")
    except Exception as e:
        print(f"❌ Demo error: {e}")
    finally:
        await robot.disconnect()
        print("👋 Disconnected from robot")

async def demo_safety_sequence():
    """Demo a safe sequence of movements"""
    print("🛡️ Safe Advanced Movement Sequence")
    print("=" * 40)
    print("This demo runs a predefined safe sequence of movements.")
    print()
    
    robot = Robot()
    try:
        print("🔗 Connecting to robot...")
        success = await robot.connect(ConnectionMethod.LOCALAP)
        if not success:
            print("❌ Failed to connect to robot")
            return
        print("✅ Connected successfully!")
        
        # Safety preparation
        print("🧍 Safety preparation...")
        await robot.command("BalanceStand")
        await asyncio.sleep(3)
        
        # Test availability first
        print("🔍 Testing movement availability...")
        availability = await robot.test_advanced_movements()
        available_movements = [cmd for cmd, avail in availability.items() if avail]
        
        if not available_movements:
            print("❌ No advanced movements available in current firmware")
            return
        
        print(f"✅ Found {len(available_movements)} available movements")
        
        # Execute safe sequence (medium priority first)
        safe_sequence = [
            ("Front Jump", robot.front_jump),
            ("Front Pounce", robot.front_pounce)
        ]
        
        for name, func in safe_sequence:
            if any(name.replace(" ", "") in cmd for cmd in available_movements):
                print(f"\n🎯 Executing {name}...")
                print("⚠️  Movement starting in 3 seconds!")
                await asyncio.sleep(3)
                
                try:
                    success = await func()
                    if success:
                        print(f"✅ {name} completed!")
                    else:
                        print(f"❌ {name} failed")
                except Exception as e:
                    print(f"❌ {name} error: {e}")
                
                # Recovery between movements
                print("🔄 Recovery period...")
                await asyncio.sleep(5)
                await robot.command("BalanceStand")
                await asyncio.sleep(3)
            else:
                print(f"⏭️ Skipping {name} - not available")
        
        print("\n🎉 Safe sequence completed!")
        
    except KeyboardInterrupt:
        print("\n🛑 Demo interrupted by user")
    except Exception as e:
        print(f"❌ Demo error: {e}")
    finally:
        await robot.disconnect()
        print("👋 Disconnected from robot")

async def main():
    """Main demo selection"""
    print("🎪 Go2 Advanced Movement Demo Suite")
    print("=" * 50)
    print("Choose a demo mode:")
    print("1. Individual Movement Testing (Interactive)")
    print("2. Safe Movement Sequence (Automated)")
    print("3. Exit")
    print()
    
    choice = input("Select demo mode (1-3): ").strip()
    
    if choice == "1":
        await demo_individual_movements()
    elif choice == "2":
        await demo_safety_sequence()
    elif choice == "3":
        print("👋 Goodbye!")
    else:
        print("❌ Invalid choice")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Exiting...")
    except Exception as e:
        print(f"❌ Error: {e}")