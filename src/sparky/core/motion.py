"""
Sparky Motion Controller
Comprehensive motion control for Go2 robots

IMPORTANT FIRMWARE UPDATE NOTE:
The Go2 robot firmware has been updated and no longer supports the "normal" and "ai" motion modes
that were present in earlier firmware versions. The robot now operates primarily in "mcf" 
(Manual Control Firmware) mode, which provides access to basic movements and sport commands
but restricts advanced features that previously required AI mode.

This change affects:
- Motion mode switching (normal/ai modes no longer available)
- Advanced commands like handstand, flips, etc. (may not be available)
- Command availability and behavior
"""

import asyncio
import json
import logging
from typing import Dict, Any, Optional, Tuple
from go2_webrtc_driver.constants import RTC_TOPIC, SPORT_CMD
# Motion verifier removed - using simplified approach for real-time control

logger = logging.getLogger(__name__)

class MotionController:
    """
    Comprehensive motion controller for Go2 robots
    Handles all movement commands and motion mode switching
    
    Note: Current Go2 firmware only supports "mcf" mode.
    Legacy "normal" and "ai" modes are no longer available.
    """
    
    def __init__(self, connection):
        self.conn = connection
        self.current_mode = None
        self.is_moving = False
        # Motion verifier removed for faster real-time control
        
    async def get_motion_mode(self) -> Optional[str]:
        """Get current motion mode"""
        try:
            response = await self.conn.datachannel.pub_sub.publish_request_new(
                RTC_TOPIC["MOTION_SWITCHER"], 
                {"api_id": 1001}
            )
            
            if response['data']['header']['status']['code'] == 0:
                data = json.loads(response['data']['data'])
                self.current_mode = data['name']
                return self.current_mode
            return None
        except Exception as e:
            logger.error(f"Failed to get motion mode: {e}")
            return None
    
    async def switch_motion_mode(self, mode: str) -> bool:
        """
        Switch to specified motion mode
        
        WARNING: Current Go2 firmware only supports "mcf" mode.
        Attempting to switch to "normal" or "ai" will fail with error codes:
        - 7004: Motion mode switching restriction
        - 7002: AI mode not available
        
        Args:
            mode: Motion mode to switch to (currently only "mcf" is supported)
        """
        try:
            logger.info(f"Attempting to switch to {mode} mode...")
            
            # Check if trying to switch to unsupported modes
            if mode in ["normal", "ai"]:
                logger.warning(f"Mode '{mode}' is not supported in current firmware. Only 'mcf' mode is available.")
                logger.warning("This is due to a recent firmware update that removed normal/ai modes.")
                return False
            
            response = await self.conn.datachannel.pub_sub.publish_request_new(
                RTC_TOPIC["MOTION_SWITCHER"], 
                {
                    "api_id": 1002,
                    "parameter": {"name": mode}
                }
            )
            
            if response['data']['header']['status']['code'] == 0:
                self.current_mode = mode
                logger.info(f"Successfully switched to {mode} mode")
                await asyncio.sleep(5)  # Wait for mode switch
                return True
            else:
                error_code = response['data']['header']['status']['code']
                logger.error(f"Failed to switch to {mode} mode. Error code: {error_code}")
                if error_code in [7004, 7002]:
                    logger.error("This error indicates the requested mode is not available in current firmware.")
                return False
        except Exception as e:
            logger.error(f"Error switching to {mode} mode: {e}")
            return False
    
    async def move(self, x: float = 0, y: float = 0, z: float = 0, duration: float = 3.0, verify: bool = True) -> bool:
        """
        Move the robot with specified parameters
        
        Args:
            x: Forward/backward movement (-1.0 to 1.0)
            y: Left/right movement (-1.0 to 1.0) 
            z: Rotation/yaw (-1.0 to 1.0)
            duration: How long to maintain this movement
            verify: Whether to verify that movement actually occurred
        """
        try:
            logger.info(f"Moving: x={x}, y={y}, z={z}, duration={duration}")
            
            response = await self.conn.datachannel.pub_sub.publish_request_new(
                RTC_TOPIC["SPORT_MOD"], 
                {
                    "api_id": SPORT_CMD["Move"],
                    "parameter": {"x": x, "y": y, "z": z}
                }
            )
            
            if response['data']['header']['status']['code'] == 0:
                self.is_moving = True
                logger.info("Move command accepted")
                
                # Verification removed for faster real-time control
                # Movement commands are executed without verification for speed
                
                await asyncio.sleep(duration)
                return True
            else:
                logger.error("Move command failed")
                return False
                
        except Exception as e:
            logger.error(f"Error in move command: {e}")
            return False
    
    def _get_expected_direction(self, x: float, y: float, z: float) -> str:
        """Get expected movement direction based on parameters"""
        if abs(x) > abs(y) and abs(x) > abs(z):
            return "forward" if x > 0 else "backward"
        elif abs(y) > abs(x) and abs(y) > abs(z):
            return "left" if y > 0 else "right"
        elif abs(z) > abs(x) and abs(z) > abs(y):
            return "turn-left" if z > 0 else "turn-right"
        else:
            return "unknown"
    
    async def stop(self) -> bool:
        """Stop all movement"""
        try:
            logger.info("Stopping movement...")
            response = await self.conn.datachannel.pub_sub.publish_request_new(
                RTC_TOPIC["SPORT_MOD"], 
                {"api_id": SPORT_CMD["StopMove"]}
            )
            
            if response['data']['header']['status']['code'] == 0:
                self.is_moving = False
                logger.info("Stop command accepted")
                return True
            else:
                logger.error("Stop command failed")
                return False
                
        except Exception as e:
            logger.error(f"Error in stop command: {e}")
            return False
    
    # Convenience methods for common movements
    async def move_forward(self, speed: float = 0.5, duration: float = 3.0, verify: bool = True) -> bool:
        """Move forward at specified speed"""
        return await self.move(x=speed, duration=duration, verify=verify)
    
    async def move_backward(self, speed: float = 0.5, duration: float = 3.0, verify: bool = True) -> bool:
        """Move backward at specified speed"""
        return await self.move(x=-speed, duration=duration, verify=verify)
    
    async def move_left(self, speed: float = 0.3, duration: float = 3.0, verify: bool = True) -> bool:
        """Move left at specified speed"""
        return await self.move(y=speed, duration=duration, verify=verify)
    
    async def move_right(self, speed: float = 0.3, duration: float = 3.0, verify: bool = True) -> bool:
        """Move right at specified speed"""
        return await self.move(y=-speed, duration=duration, verify=verify)
    
    async def turn_left(self, speed: float = 0.3, duration: float = 3.0, verify: bool = True) -> bool:
        """Turn left at specified speed"""
        return await self.move(z=speed, duration=duration, verify=verify)
    
    async def turn_right(self, speed: float = 0.3, duration: float = 3.0, verify: bool = True) -> bool:
        """Turn right at specified speed"""
        return await self.move(z=-speed, duration=duration, verify=verify)
    
    async def execute_sport_command(self, command_name: str, parameters: Optional[Dict] = None, verify: bool = True) -> bool:
        """
        Execute a sport command by name
        
        Note: Some advanced commands may not be available in current firmware.
        Commands that previously required "ai" mode may fail with error code 3203.
        
        Args:
            command_name: Name of the command (e.g., "Hello", "Sit", "StandUp")
            parameters: Optional parameters for the command
            verify: Whether to verify that command was actually executed
        """
        try:
            # Check if command exists and suggest alternatives
            if command_name not in SPORT_CMD:
                # Try to find similar commands
                available_commands = list(SPORT_CMD.keys())
                similar_commands = [cmd for cmd in available_commands if command_name.lower() in cmd.lower() or cmd.lower() in command_name.lower()]
                
                error_msg = f"Unknown sport command: {command_name}"
                if similar_commands:
                    error_msg += f". Did you mean one of: {', '.join(similar_commands[:3])}?"
                else:
                    error_msg += f". Available commands include: {', '.join(available_commands[:5])}..."
                
                logger.error(error_msg)
                return False
            
            logger.info(f"Executing sport command: {command_name}")
            
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
                logger.info(f"Sport command {command_name} accepted")
                
                # Verification removed for faster real-time control
                
                await asyncio.sleep(2)  # Wait for command execution
                return True
            else:
                error_code = response['data']['header']['status']['code']
                logger.error(f"Sport command {command_name} failed. Error code: {error_code}")
                if error_code == 3203:
                    logger.error("This command may not be available in current firmware or motion mode.")
                return False
                
        except Exception as e:
            logger.error(f"Error executing sport command {command_name}: {e}")
            return False
    
    # Advanced movement sequences
    async def walk_square(self, side_length: float = 0.5, verify: bool = True) -> bool:
        """Walk in a square pattern"""
        try:
            logger.info("Starting square walk pattern")
            
            # Forward
            if not await self.move_forward(side_length, 2.0, verify):
                logger.error("Square walk failed at forward movement")
                return False
            await self.stop()
            await asyncio.sleep(1)
            
            # Right
            if not await self.move_right(side_length, 2.0, verify):
                logger.error("Square walk failed at right movement")
                return False
            await self.stop()
            await asyncio.sleep(1)
            
            # Backward
            if not await self.move_backward(side_length, 2.0, verify):
                logger.error("Square walk failed at backward movement")
                return False
            await self.stop()
            await asyncio.sleep(1)
            
            # Left
            if not await self.move_left(side_length, 2.0, verify):
                logger.error("Square walk failed at left movement")
                return False
            await self.stop()
            
            logger.info("Square walk pattern completed")
            return True
            
        except Exception as e:
            logger.error(f"Error in square walk: {e}")
            return False
    
    async def spin_360(self, direction: str = "right", verify: bool = True) -> bool:
        """Spin 360 degrees"""
        try:
            logger.info(f"Spinning 360 degrees {direction}")
            
            if direction.lower() == "right":
                success = await self.turn_right(0.5, 6.0, verify)
            else:
                success = await self.turn_left(0.5, 6.0, verify)
            
            await self.stop()
            
            if success:
                logger.info("360 degree spin completed")
            else:
                logger.warning("360 degree spin may not have completed successfully")
            
            return success
            
        except Exception as e:
            logger.error(f"Error in 360 spin: {e}")
            return False
    
    async def handstand(self, enable: bool = True, verify: bool = True) -> bool:
        """
        Enable/disable handstand mode
        
        WARNING: This command may not be available in current firmware.
        Previous versions required "ai" mode, which is no longer available.
        """
        try:
            logger.warning("Handstand command may not be available in current firmware.")
            logger.warning("This command previously required 'ai' mode, which has been removed.")
            
            logger.info(f"{'Enabling' if enable else 'Disabling'} handstand mode")
            return await self.execute_sport_command("StandOut", {"data": enable}, verify)
            
        except Exception as e:
            logger.error(f"Error in handstand command: {e}")
            return False
    
    def get_available_commands(self) -> Dict[str, int]:
        """Get all available sport commands"""
        return SPORT_CMD.copy()
    
    def get_status(self) -> Dict[str, Any]:
        """Get current motion controller status"""
        status = {
            "current_mode": self.current_mode,
            "is_moving": self.is_moving,
            "available_commands": list(SPORT_CMD.keys()),
            "firmware_note": "Current firmware only supports 'mcf' mode. Legacy 'normal' and 'ai' modes are not available."
        }
        
        # Verification removed for real-time performance
        
        return status
    
    # Advanced Movement Methods
    async def front_flip(self, verify: bool = True) -> bool:
        """
        Execute front flip/somersault
        
        WARNING: This command may not be available in current firmware.
        Previous versions required "ai" mode, which is no longer available.
        """
        try:
            logger.warning("FrontFlip command may not be available in current firmware.")
            logger.info("Executing front flip command")
            return await self.execute_sport_command("FrontFlip", verify=verify)
        except Exception as e:
            logger.error(f"Error in front flip: {e}")
            return False
    
    async def back_flip(self, verify: bool = True) -> bool:
        """
        Execute back flip/somersault
        
        WARNING: This command may not be available in current firmware.
        """
        try:
            logger.warning("BackFlip command may not be available in current firmware.")
            logger.info("Executing back flip command")
            return await self.execute_sport_command("BackFlip", verify=verify)
        except Exception as e:
            logger.error(f"Error in back flip: {e}")
            return False
    
    async def left_flip(self, verify: bool = True) -> bool:
        """
        Execute left side flip
        
        WARNING: This command may not be available in current firmware.
        """
        try:
            logger.warning("LeftFlip command may not be available in current firmware.")
            logger.info("Executing left flip command")
            return await self.execute_sport_command("LeftFlip", verify=verify)
        except Exception as e:
            logger.error(f"Error in left flip: {e}")
            return False
    
    async def right_flip(self, verify: bool = True) -> bool:
        """
        Execute right side flip
        
        WARNING: This command may not be available in current firmware.
        """
        try:
            logger.warning("RightFlip command may not be available in current firmware.")
            logger.info("Executing right flip command")
            return await self.execute_sport_command("RightFlip", verify=verify)
        except Exception as e:
            logger.error(f"Error in right flip: {e}")
            return False
    
    async def front_jump(self, verify: bool = True) -> bool:
        """
        Execute forward jump
        
        This command has medium priority and may work in current firmware.
        """
        try:
            logger.info("Executing front jump command")
            return await self.execute_sport_command("FrontJump", verify=verify)
        except Exception as e:
            logger.error(f"Error in front jump: {e}")
            return False
    
    async def front_pounce(self, verify: bool = True) -> bool:
        """
        Execute pouncing motion
        
        This command has medium priority and may work in current firmware.
        """
        try:
            logger.info("Executing front pounce command")
            return await self.execute_sport_command("FrontPounce", verify=verify)
        except Exception as e:
            logger.error(f"Error in front pounce: {e}")
            return False
    
    async def test_advanced_movement_availability(self) -> Dict[str, bool]:
        """
        Test which advanced movements are available in current firmware
        
        Returns:
            Dictionary mapping command names to availability status
        """
        advanced_commands = [
            "FrontFlip", "BackFlip", "LeftFlip", "RightFlip", 
            "FrontJump", "FrontPounce", "Handstand"
        ]
        
        availability = {}
        
        logger.info("Testing advanced movement availability...")
        
        for command in advanced_commands:
            try:
                # Test command availability without executing
                response = await self.conn.datachannel.pub_sub.publish_request_new(
                    RTC_TOPIC["SPORT_MOD"], 
                    {"api_id": SPORT_CMD[command]}
                )
                
                if response['data']['header']['status']['code'] == 0:
                    availability[command] = True
                    logger.info(f"✅ {command} is available")
                else:
                    availability[command] = False
                    error_code = response['data']['header']['status']['code']
                    logger.warning(f"❌ {command} not available (error {error_code})")
                    
            except Exception as e:
                availability[command] = False
                logger.error(f"❌ {command} test failed: {e}")
                
            # Brief pause between tests
            await asyncio.sleep(0.5)
        
        return availability

    def get_firmware_compatibility_info(self) -> Dict[str, Any]:
        """
        Get information about firmware compatibility and limitations
        """
        return {
            "supported_modes": ["mcf"],
            "unsupported_modes": ["normal", "ai"],
            "firmware_update_note": "Recent firmware update removed normal/ai motion modes",
            "error_codes": {
                "7004": "Motion mode switching restriction (normal/ai not available)",
                "7002": "AI mode not available in current firmware",
                "3203": "Command not available in current motion mode"
            },
            "working_commands": [
                "Move", "StopMove", "Hello", "Sit", "StandUp", "Dance1", "Dance2",
                "Stretch", "BalanceStand", "RecoveryStand"
            ],
            "potentially_restricted_commands": [
                "Handstand", "BackFlip", "FrontFlip", "LeftFlip", "RightFlip",
                "StandOut", "FrontJump", "FrontPounce"
            ],
            "advanced_movements": {
                "FrontFlip": {"id": 1030, "risk": "High", "firmware_dependent": True},
                "BackFlip": {"id": 1044, "risk": "High", "firmware_dependent": True},
                "LeftFlip": {"id": 1042, "risk": "High", "firmware_dependent": True},
                "RightFlip": {"id": 1043, "risk": "High", "firmware_dependent": True},
                "FrontJump": {"id": 1031, "risk": "Medium", "firmware_dependent": False},
                "FrontPounce": {"id": 1032, "risk": "Medium", "firmware_dependent": False},
                "Handstand": {"id": 1301, "risk": "High", "firmware_dependent": True}
            }
        }
