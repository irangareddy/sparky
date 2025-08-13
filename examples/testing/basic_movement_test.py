#!/usr/bin/env python3
"""
Basic Movement Testing for Go2 Robot
Tests fundamental movement commands that form the foundation of robot operation

This script tests the 9 basic movement commands from the testing guide:
- Damp (1001) - 🚨 DANGER: BLOCKED BY SAFETY (causes robot leg collapse)
- BalanceStand (1002) - Standard balanced standing  
- StopMove (1003) - Emergency stop
- StandUp (1004) - Rise from lying position
- StandDown (1005) - Lower to lying position
- RecoveryStand (1006) - Recovery from fall
- Move (1008) - Basic movement control
- Sit (1009) - Sit down
- RiseSit (1010) - Rise from sitting

These are fundamental MCF mode commands and should work in current firmware.
"""

import asyncio
import logging
import json
import sys
import time
from pathlib import Path
from typing import Dict, Any, Optional

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from sparky import Robot
from sparky.core.connection import Go2Connection, WebRTCConnectionMethod
from go2_webrtc_driver.constants import SPORT_CMD, RTC_TOPIC

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class BasicMovementTester:
    """
    Comprehensive tester for basic Go2 robot movements
    """
    
    # Basic movement commands from the testing guide
    BASIC_MOVEMENTS = {
        # High Priority Commands
        "Damp": {"id": 1001, "priority": "High", "description": "🚨 DANGER: BLOCKED BY SAFETY - Causes robot leg collapse!", "category": "stance"},
        "BalanceStand": {"id": 1002, "priority": "High", "description": "Standard balanced standing", "category": "stance"},
        "StopMove": {"id": 1003, "priority": "High", "description": "Emergency stop", "category": "safety"},
        "StandUp": {"id": 1004, "priority": "High", "description": "Rise from lying position", "category": "transition"},
        "RecoveryStand": {"id": 1006, "priority": "High", "description": "Recovery from fall", "category": "safety"},
        "Move": {"id": 1008, "priority": "High", "description": "Basic movement control", "category": "locomotion"},
        
        # Medium Priority Commands  
        "StandDown": {"id": 1005, "priority": "Medium", "description": "Lower to lying position", "category": "transition"},
        "Sit": {"id": 1009, "priority": "Medium", "description": "Sit down", "category": "transition"},
        "RiseSit": {"id": 1010, "priority": "Medium", "description": "Rise from sitting", "category": "transition"}
    }
    
    def __init__(self, connection_method=WebRTCConnectionMethod.LocalAP, ip=None):
        self.connection_method = connection_method
        self.ip = ip
        self.conn = None
        self.robot = None
        self.test_results = {}
        self.motion_mode = None
        
    async def connect(self) -> bool:
        """Establish connection to robot"""
        try:
            self.robot = Robot()
            
            if self.connection_method == WebRTCConnectionMethod.LocalAP:
                success = await self.robot.connect()
            else:
                success = await self.robot.connect(method=self.connection_method, ip=self.ip)
            
            if success:
                self.conn = self.robot.connection.conn
                logger.info("✅ Successfully connected to Go2 robot")
                return True
            else:
                logger.error("❌ Failed to connect to robot")
                return False
                
        except Exception as e:
            logger.error(f"❌ Connection error: {e}")
            return False
    
    async def disconnect(self):
        """Safely disconnect from robot"""
        if self.robot:
            await self.robot.disconnect()
            logger.info("🔌 Disconnected from robot")
    
    async def emergency_stop(self):
        """Emergency stop - immediately halt all movement"""
        try:
            if self.robot and self.robot.motion:
                await self.robot.motion.stop()
                logger.warning("🛑 EMERGENCY STOP EXECUTED")
        except Exception as e:
            logger.error(f"❌ Emergency stop failed: {e}")
    
    async def get_motion_mode(self) -> Optional[str]:
        """Get current motion mode"""
        try:
            response = await self.conn.datachannel.pub_sub.publish_request_new(
                RTC_TOPIC["MOTION_SWITCHER"], 
                {"api_id": 1001}
            )
            
            if response['data']['header']['status']['code'] == 0:
                data = json.loads(response['data']['data'])
                self.motion_mode = data['name']
                return self.motion_mode
            return None
        except Exception as e:
            logger.error(f"Failed to get motion mode: {e}")
            return None
    
    async def safe_preparation_sequence(self) -> bool:
        """Prepare robot safely for basic movement testing"""
        try:
            logger.info("🔧 Preparing robot for basic movement testing...")
            
            # Get current motion mode
            mode = await self.get_motion_mode()
            logger.info(f"📊 Current motion mode: {mode}")
            
            # Test basic connectivity with a simple command
            logger.info("🔍 Testing basic command connectivity...")
            try:
                # Try a simple balance stand command
                response = await self.conn.datachannel.pub_sub.publish_request_new(
                    RTC_TOPIC["SPORT_MOD"], 
                    {"api_id": SPORT_CMD["BalanceStand"]}
                )
                
                if response['data']['header']['status']['code'] == 0:
                    logger.info("✅ Basic command connectivity working")
                    await asyncio.sleep(2)
                else:
                    logger.warning(f"⚠️ Basic command returned code: {response['data']['header']['status']['code']}")
            except Exception as e:
                logger.error(f"❌ Basic command test failed: {e}")
                return False
            
            # Brief stabilization period
            logger.info("⏰ Allowing system to stabilize...")
            await asyncio.sleep(3)
            
            logger.info("✅ Robot preparation complete")
            return True
            
        except Exception as e:
            logger.error(f"❌ Preparation sequence failed: {e}")
            return False
    
    async def test_basic_movement(self, command_name: str, parameters: Optional[Dict] = None, max_attempts: int = 1) -> Dict[str, Any]:
        """
        Test a single basic movement command
        
        Args:
            command_name: Name of the movement command
            parameters: Optional parameters for the command
            max_attempts: Maximum number of test attempts
            
        Returns:
            Dictionary with test results
        """
        command_info = self.BASIC_MOVEMENTS[command_name]
        command_id = command_info["id"]
        
        result = {
            "command": command_name,
            "api_id": command_id,
            "priority": command_info["priority"],
            "description": command_info["description"],
            "category": command_info["category"],
            "status": "⭕",
            "attempts": 0,
            "error_codes": [],
            "notes": [],
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        logger.info(f"\n🎯 Testing {command_name} (ID: {command_id}) - {command_info['description']}")
        logger.info(f"   Priority: {command_info['priority']} | Category: {command_info['category']}")
        
        # Special handling for dangerous Damp command
        if command_name == "Damp":
            logger.critical("🚨 DAMP COMMAND DETECTED - This command is BLOCKED by safety system!")
            logger.critical("💡 Damp causes robot leg collapse and expensive damage")
            result["status"] = "🚫"
            result["notes"].append("Command blocked by ultra-safe protection system")
            result["notes"].append("Damp reduces leg stiffness causing immediate collapse")
            result["notes"].append("Use BalanceStand or RecoveryStand for safe stabilization")
            return result
        
        for attempt in range(max_attempts):
            result["attempts"] += 1
            
            try:
                logger.info(f"   Attempt {attempt + 1}/{max_attempts}")
                
                # Prepare command payload
                if parameters:
                    payload = {
                        "api_id": command_id,
                        "parameter": parameters
                    }
                else:
                    payload = {"api_id": command_id}
                
                # Send the sport command
                response = await self.conn.datachannel.pub_sub.publish_request_new(
                    RTC_TOPIC["SPORT_MOD"], 
                    payload
                )
                
                status_code = response['data']['header']['status']['code']
                
                if status_code == 0:
                    result["status"] = "✅"
                    result["notes"].append("Command accepted by robot")
                    logger.info(f"   ✅ {command_name} command accepted!")
                    
                    # Wait for command execution
                    execution_time = self._get_execution_time(command_name)
                    logger.info(f"   ⏳ Waiting for execution ({execution_time}s)...")
                    await asyncio.sleep(execution_time)
                    
                    # Brief recovery period for transition commands
                    if command_info["category"] in ["transition", "safety"]:
                        logger.info("   🔄 Allowing transition recovery...")
                        await asyncio.sleep(2)
                    
                    break
                    
                else:
                    result["error_codes"].append(status_code)
                    error_msg = self._interpret_error_code(status_code)
                    result["notes"].append(f"Error {status_code}: {error_msg}")
                    logger.warning(f"   ❌ {command_name} failed with error {status_code}: {error_msg}")
                    
                    if status_code in [3203, 7002, 7004]:
                        # These are firmware/mode related errors - no point retrying
                        result["status"] = "❌"
                        result["notes"].append("Firmware limitation - command not available")
                        break
                    
            except Exception as e:
                error_msg = str(e)
                result["notes"].append(f"Exception: {error_msg}")
                logger.error(f"   ❌ Exception during {command_name}: {error_msg}")
        
        # Final status determination
        if result["status"] == "⭕":
            result["status"] = "❌"
            result["notes"].append("Command failed after all attempts")
        
        # Small pause between tests
        await asyncio.sleep(1)
        
        return result
    
    def _get_execution_time(self, command_name: str) -> int:
        """Get appropriate execution time for different command types"""
        command_info = self.BASIC_MOVEMENTS[command_name]
        category = command_info["category"]
        
        execution_times = {
            "stance": 2,      # Quick stance changes
            "safety": 1,      # Emergency stops should be immediate
            "transition": 4,  # Sit/stand transitions take longer
            "locomotion": 3   # Movement commands
        }
        
        return execution_times.get(category, 2)
    
    def _interpret_error_code(self, code: int) -> str:
        """Interpret common error codes"""
        error_codes = {
            3203: "Command not available in current motion mode (MCF mode limitation)",
            7002: "AI mode not available in current firmware", 
            7004: "Motion mode switching restriction",
            3001: "Robot not in correct state for this command",
            3002: "Invalid command parameters",
            3004: "Command execution timeout",
            3005: "Command rejected - robot busy"
        }
        return error_codes.get(code, "Unknown error")
    
    async def run_high_priority_tests(self) -> Dict[str, Any]:
        """Test high priority basic movements first (safer)"""
        logger.info("\n" + "="*60)
        logger.info("🔴 TESTING HIGH PRIORITY BASIC MOVEMENTS")
        logger.info("="*60)
        
        high_priority = [cmd for cmd, info in self.BASIC_MOVEMENTS.items() if info["priority"] == "High"]
        results = {}
        
        # Test in logical order: stance -> safety -> transitions -> locomotion
        # NOTE: Damp removed from test order - blocked by safety system
        test_order = ["BalanceStand", "StopMove", "RecoveryStand", "StandUp", "Move"]
        
        for command in test_order:
            if command in high_priority:
                # Special handling for Move command
                if command == "Move":
                    result = await self.test_basic_movement(command, {"x": 0.2, "y": 0, "z": 0})
                else:
                    result = await self.test_basic_movement(command)
                
                results[command] = result
                self.test_results[command] = result
                
                # Brief pause between tests
                await asyncio.sleep(1)
        
        return results
    
    async def run_medium_priority_tests(self) -> Dict[str, Any]:
        """Test medium priority basic movements"""
        logger.info("\n" + "="*60)
        logger.info("🟡 TESTING MEDIUM PRIORITY BASIC MOVEMENTS")
        logger.info("="*60)
        
        medium_priority = [cmd for cmd, info in self.BASIC_MOVEMENTS.items() if info["priority"] == "Medium"]
        results = {}
        
        # Test transitions in logical order
        test_order = ["Sit", "RiseSit", "StandDown"]
        
        for command in test_order:
            if command in medium_priority:
                result = await self.test_basic_movement(command)
                results[command] = result
                self.test_results[command] = result
                
                # Longer pause between transition commands
                await asyncio.sleep(2)
        
        return results
    
    async def run_comprehensive_test(self):
        """Run complete basic movement test suite"""
        logger.info("🏗️ STARTING BASIC MOVEMENT TEST SUITE")
        logger.info("="*60)
        logger.info("ℹ️  Testing fundamental commands for Go2 robot operation")
        logger.info("ℹ️  These commands should work in MCF mode")
        logger.info("="*60)
        
        try:
            # Connect to robot
            if not await self.connect():
                return
            
            # Safety preparation
            if not await self.safe_preparation_sequence():
                logger.error("❌ Safety preparation failed - aborting tests")
                return
            
            # Test high priority movements first
            high_results = await self.run_high_priority_tests()
            
            # Test medium priority movements
            medium_results = await self.run_medium_priority_tests()
            
            # Generate summary report
            self._generate_test_report()
            
        except KeyboardInterrupt:
            logger.warning("\n🛑 Testing interrupted by user")
            await self.emergency_stop()
        except Exception as e:
            logger.error(f"❌ Testing failed: {e}")
            await self.emergency_stop()
        finally:
            await self.disconnect()
    
    def _export_results_to_guide(self):
        """Export test results to the testing guide document"""
        try:
            guide_path = Path(__file__).parent.parent.parent / "docs" / "go2_api_testing_guide.md"
            
            if not guide_path.exists():
                logger.warning(f"Testing guide not found at {guide_path}")
                return
            
            # Read current guide
            with open(guide_path, 'r') as f:
                content = f.read()
            
            # Update basic movement commands table
            for command, result in self.test_results.items():
                command_info = self.BASIC_MOVEMENTS[command]
                api_id = command_info["id"]
                priority = command_info["priority"]
                status = result["status"]
                description = command_info["description"]
                
                # Create updated notes
                if status == "✅":
                    notes = f"{description} - **WORKING!** (Tested {result['timestamp'][:10]})"
                else:
                    error_notes = "; ".join(result["notes"][:2])
                    notes = f"{description} - {error_notes}"
                
                # Find and replace the line in the basic movements table
                old_pattern = f"| {command} | {api_id} | {priority} | ⭕ | {description} |"
                new_pattern = f"| {command} | {api_id} | {priority} | {status} | {notes} |"
                
                content = content.replace(old_pattern, new_pattern)
            
            # Write updated guide
            with open(guide_path, 'w') as f:
                f.write(content)
                
            logger.info(f"✅ Test results exported to {guide_path}")
            
        except Exception as e:
            logger.error(f"❌ Failed to export results to guide: {e}")
    
    def _generate_test_report(self):
        """Generate comprehensive test report"""
        logger.info("\n" + "="*80)
        logger.info("📋 BASIC MOVEMENT TEST REPORT")
        logger.info("="*80)
        
        working_commands = []
        failed_commands = []
        firmware_limited = []
        
        for command, result in self.test_results.items():
            if result["status"] == "✅":
                working_commands.append(command)
            elif any("Firmware limitation" in note for note in result["notes"]):
                firmware_limited.append(command)
            else:
                failed_commands.append(command)
        
        logger.info(f"📊 SUMMARY:")
        logger.info(f"   ✅ Working: {len(working_commands)}/{len(self.test_results)} commands")
        logger.info(f"   ❌ Failed: {len(failed_commands)} commands") 
        logger.info(f"   🚫 Firmware Limited: {len(firmware_limited)} commands")
        
        if working_commands:
            logger.info(f"\n✅ WORKING COMMANDS:")
            for cmd in working_commands:
                info = self.BASIC_MOVEMENTS[cmd]
                logger.info(f"   • {cmd} ({info['priority']}): {info['description']}")
        
        if firmware_limited:
            logger.info(f"\n🚫 FIRMWARE LIMITED COMMANDS:")
            for cmd in firmware_limited:
                info = self.BASIC_MOVEMENTS[cmd]
                logger.info(f"   • {cmd} ({info['priority']}): {info['description']}")
        
        if failed_commands:
            logger.info(f"\n❌ FAILED COMMANDS:")
            for cmd in failed_commands:
                result = self.test_results[cmd]
                info = self.BASIC_MOVEMENTS[cmd]
                logger.info(f"   • {cmd} ({info['priority']}): {info['description']}")
                if result["error_codes"]:
                    logger.info(f"     Error codes: {result['error_codes']}")
        
        logger.info(f"\n📝 DETAILED RESULTS BY CATEGORY:")
        categories = {}
        for command, result in self.test_results.items():
            category = result["category"]
            if category not in categories:
                categories[category] = []
            categories[category].append((command, result))
        
        for category, commands in categories.items():
            logger.info(f"\n   {category.upper()}:")
            for command, result in commands:
                logger.info(f"   {result['status']} {command} (ID: {result['api_id']}) - {result['description']}")
        
        logger.info("\n" + "="*80)
        logger.info("💡 RECOMMENDATIONS:")
        logger.info("   1. Use working commands as foundation for robot applications")
        logger.info("   2. Focus development on confirmed working functionality")
        logger.info("   3. Basic movements are essential - investigate any failures")
        logger.info("   4. Update application logic based on test results")
        logger.info("="*80)
        
        # Export results to testing guide
        logger.info("\n📄 Exporting results to testing guide...")
        self._export_results_to_guide()

async def main():
    """Main test execution"""
    print("🏗️ Go2 Basic Movement Tester")
    print("===============================")
    print("This script will test all 9 fundamental movement commands")
    print("that form the foundation of robot operation.")
    print()
    print("Commands to test:")
    print("• High Priority: BalanceStand, StopMove, StandUp, RecoveryStand, Move")
    print("• 🚨 BLOCKED: Damp (causes dangerous robot leg collapse)")
    print("• Medium Priority: StandDown, Sit, RiseSit")
    print()
    print("These are basic MCF mode commands and should work reliably.")
    print()
    
    # Allow user to prepare
    print("⏳ Starting test in 5 seconds...")
    try:
        await asyncio.sleep(5)
    except KeyboardInterrupt:
        print("\n🛑 Test aborted by user")
        return
    
    # Create tester and run
    tester = BasicMovementTester(
        connection_method=WebRTCConnectionMethod.LocalAP
        # For router connection, use:
        # connection_method=WebRTCConnectionMethod.LocalSTA, 
        # ip="192.168.8.181"
    )
    
    await tester.run_comprehensive_test()

if __name__ == "__main__":
    asyncio.run(main())