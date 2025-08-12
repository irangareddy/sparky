import asyncio
import logging
import json
import sys
from pathlib import Path

# Add the src directory to the path so we can import sparky modules
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from sparky import Robot
from sparky.core.connection import Go2Connection, WebRTCConnectionMethod
from go2_webrtc_driver.constants import SPORT_CMD

# Enable logging for debugging
logging.basicConfig(level=logging.FATAL)

class MotionTester:
    def __init__(self, connection_method=WebRTCConnectionMethod.LocalAP, ip=None):
        self.conn = None
        self.connection_method = connection_method
        self.ip = ip
        self.test_results = {}
        
    async def connect(self):
        """Establish WebRTC connection"""
        try:
            if self.ip:
                self.conn = Go2WebRTCConnection(self.connection_method, ip=self.ip)
            else:
                self.conn = Go2WebRTCConnection(self.connection_method)
            
            await self.conn.connect()
            print(" WebRTC connection established")
            return True
        except Exception as e:
            print(f"FAILED Connection failed: {e}")
            return False
    
    async def get_motion_mode(self):
        """Get current motion mode"""
        try:
            response = await self.conn.datachannel.pub_sub.publish_request_new(
                RTC_TOPIC["MOTION_SWITCHER"], 
                {"api_id": 1001}
            )
            
            if response['data']['header']['status']['code'] == 0:
                data = json.loads(response['data']['data'])
                return data['name']
            return None
        except Exception as e:
            print(f"Failed to get motion mode: {e}")
            return None
    
    async def switch_motion_mode(self, mode):
        """Switch to specified motion mode"""
        try:
            print(f"Processing Switching to {mode} mode...")
            response = await self.conn.datachannel.pub_sub.publish_request_new(
                RTC_TOPIC["MOTION_SWITCHER"], 
                {
                    "api_id": 1002,
                    "parameter": {"name": mode}
                }
            )
            
            if response['data']['header']['status']['code'] == 0:
                print(f" Successfully switched to {mode} mode")
                await asyncio.sleep(5)  # Wait for mode switch
                return True
            else:
                print(f"Failed to switch to {mode} mode")
                return False
        except Exception as e:
            print(f"FAILED Error switching to {mode} mode: {e}")
            return False
    
    async def test_move_command(self, direction, x, y, z, duration=3):
        """Test move command with specific parameters"""
        try:
            print(f"Walking Testing {direction} movement: x={x}, y={y}, z={z}")
            
            response = await self.conn.datachannel.pub_sub.publish_request_new(
                RTC_TOPIC["SPORT_MOD"], 
                {
                    "api_id": SPORT_CMD["Move"],
                    "parameter": {"x": x, "y": y, "z": z}
                }
            )
            
            # Check if command was accepted
            if response['data']['header']['status']['code'] == 0:
                print(f" {direction} movement command accepted")
                await asyncio.sleep(duration)
                return True
            else:
                print(f"FAILED {direction} movement command failed")
                return False
                
        except Exception as e:
            print(f"FAILED Error in {direction} movement: {e}")
            return False
    
    async def test_sport_command(self, command_name, parameters=None):
        """Test a specific sport command"""
        try:
            print(f"Target Testing {command_name} command...")
            
            if parameters:
                response = await self.conn.datachannel.pub_sub.publish_request_new(
                    RTC_TOPIC["SPORT_MOD"], 
                    {
                        "api_id": SPORT_CMD[command_name],
                        "parameter": parameters
                    }
                )
            else:
                response = await self.conn.datachannel.pub_sub.publish_request_new(
                    RTC_TOPIC["SPORT_MOD"], 
                    {"api_id": SPORT_CMD[command_name]}
                )
            
            if response['data']['header']['status']['code'] == 0:
                print(f" {command_name} command accepted")
                await asyncio.sleep(2)
                return True
            else:
                print(f"FAILED {command_name} command failed")
                return False
                
        except Exception as e:
            print(f"FAILED Error in {command_name} command: {e}")
            return False
    
    async def run_basic_movement_tests(self):
        """Test basic movement patterns"""
        print("\n" + "="*50)
        print("BASIC MOVEMENT TESTS")
        print("="*50)
        
        # Test forward movements with different speeds
        await self.test_move_command("Forward (Slow)", 0.3, 0, 0, 3)
        await self.test_move_command("Forward (Medium)", 0.5, 0, 0, 3)
        await self.test_move_command("Forward (Fast)", 0.8, 0, 0, 3)
        
        # Test backward movements
        await self.test_move_command("Backward (Slow)", -0.3, 0, 0, 3)
        await self.test_move_command("Backward (Medium)", -0.5, 0, 0, 3)
        
        # Test lateral movements
        await self.test_move_command("Left", 0, 0.3, 0, 3)
        await self.test_move_command("Right", 0, -0.3, 0, 3)
        
        # Test rotation
        await self.test_move_command("Rotate Left", 0, 0, 0.3, 3)
        await self.test_move_command("Rotate Right", 0, 0, -0.3, 3)
        
        # Test diagonal movements
        await self.test_move_command("Forward-Left", 0.3, 0.3, 0, 3)
        await self.test_move_command("Forward-Right", 0.3, -0.3, 0, 3)
    
    async def run_sport_command_tests(self):
        """Test various sport commands"""
        print("\n" + "="*50)
        print("SPORT COMMAND TESTS")
        print("="*50)
        
        # Test basic commands
        await self.test_sport_command("Hello")
        await self.test_sport_command("Sit")
        await self.test_sport_command("StandUp")
        
        # Test advanced commands (in AI mode)
        current_mode = await self.get_motion_mode()
        if current_mode == "ai":
            await self.test_sport_command("StandOut", {"data": True})  # Handstand
            await asyncio.sleep(3)
            await self.test_sport_command("StandOut", {"data": False})  # Back to normal
            
            # Test other advanced commands
            await self.test_sport_command("Stretch")
            await self.test_sport_command("Dance1")
            await self.test_sport_command("Dance2")
    
    async def run_comprehensive_test(self):
        """Run comprehensive motion testing"""
        print(" Starting Sparky Motion Testing Suite")
        print("="*50)
        
        # Connect to robot
        if not await self.connect():
            return
        
        # Get initial motion mode
        initial_mode = await self.get_motion_mode()
        print(f"Data Initial motion mode: {initial_mode}")
        
        # Test in Normal mode
        if initial_mode != "normal":
            await self.switch_motion_mode("normal")
        
        await self.run_basic_movement_tests()
        await self.run_sport_command_tests()
        
        # Switch to AI mode for advanced commands
        await self.switch_motion_mode("ai")
        await self.run_sport_command_tests()
        
        # Return to normal mode
        await self.switch_motion_mode("normal")
        
        print("\n" + "="*50)
        print(" Motion testing completed!")
        print("="*50)

async def main():
    # You can change the connection method here
    tester = MotionTester(
        connection_method=WebRTCConnectionMethod.LocalAP
        # connection_method=WebRTCConnectionMethod.LocalSTA, ip="192.168.8.181"
    )
    
    try:
        await tester.run_comprehensive_test()
        # Keep running for a while to observe results
        await asyncio.sleep(60)
    except KeyboardInterrupt:
        print("\nSTOP Testing interrupted by user")
    except Exception as e:
        print(f"FAILED Testing failed: {e}")

if __name__ == "__main__":
    asyncio.run(main())
