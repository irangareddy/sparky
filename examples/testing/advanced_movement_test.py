#!/usr/bin/env python3
"""
Advanced Movement Testing for Go2 Robot
Tests advanced acrobatic and specialized movements systematically

This script tests the 7 advanced movement commands from the testing guide:
- FrontFlip (1030)
- BackFlip (1044) 
- LeftFlip (1042)
- RightFlip (1043)
- FrontJump (1031)
- FrontPounce (1032)
- Handstand (1301)

WARNING: These movements may not be available in current Go2 firmware.
Previous versions required "ai" mode which has been removed in recent updates.
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

class AdvancedMovementTester:
    """
    Comprehensive tester for advanced Go2 robot movements
    """
    
    # Advanced movement commands from the testing guide
    ADVANCED_MOVEMENTS = {
        "FrontFlip": {"id": 1030, "priority": "Low", "description": "Front somersault"},
        "BackFlip": {"id": 1044, "priority": "Low", "description": "Back somersault"}, 
        "LeftFlip": {"id": 1042, "priority": "Low", "description": "Left side flip"},
        "RightFlip": {"id": 1043, "priority": "Low", "description": "Right side flip"},
        "FrontJump": {"id": 1031, "priority": "Medium", "description": "Forward jump"},
        "FrontPounce": {"id": 1032, "priority": "Medium", "description": "Pouncing motion"},
        "Handstand": {"id": 1301, "priority": "Low", "description": "Handstand position"}
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
    
    async def pre_flight_safety_check(self) -> bool:
        """Comprehensive pre-flight safety check"""
        logger.info("🛡️ Performing pre-flight safety check...")
        
        try:
            # Check motion mode
            mode = await self.get_motion_mode()
            logger.info(f"📊 Motion mode: {mode}")
            
            if mode != "mcf":
                logger.warning(f"⚠️ Unexpected motion mode: {mode}. Expected 'mcf'")
            
            # Test basic commands first
            logger.info("🔍 Testing basic command availability...")
            basic_test = await self.robot.command("BalanceStand")
            if not basic_test:
                logger.error("❌ Basic BalanceStand command failed - aborting tests")
                return False
            
            logger.info("✅ Basic commands working")
            
            # Test command availability without execution
            logger.info("🔍 Testing advanced command availability...")
            availability = await self.robot.test_advanced_movements()
            available_count = sum(availability.values())
            logger.info(f"📊 Advanced movements available: {available_count}/{len(availability)}")
            
            if available_count == 0:
                logger.warning("⚠️ No advanced movements available - continuing with tests anyway")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Pre-flight check failed: {e}")
            return False

    async def safe_preparation_sequence(self) -> bool:
        """Prepare robot safely for advanced movements"""
        try:
            logger.info("🔧 Preparing robot for advanced movements...")
            
            # Pre-flight safety check
            if not await self.pre_flight_safety_check():
                return False
            
            # Ensure robot is standing and balanced
            logger.info("🧍 Ensuring robot is in balanced stand...")
            await self.robot.command("BalanceStand")
            await asyncio.sleep(2)
            
            # Test stop command
            logger.info("🛑 Testing emergency stop...")
            await self.robot.command("StopMove")
            await asyncio.sleep(1)
            
            # Return to balanced stand
            await self.robot.command("BalanceStand")
            await asyncio.sleep(2)
            
            # Brief recovery period
            logger.info("⏰ Allowing system to stabilize...")
            await asyncio.sleep(3)
            
            logger.info("✅ Robot preparation complete")
            return True
            
        except Exception as e:
            logger.error(f"❌ Preparation sequence failed: {e}")
            return False
    
    async def test_advanced_movement(self, command_name: str, max_attempts: int = 1) -> Dict[str, Any]:
        """
        Test a single advanced movement command
        
        Args:
            command_name: Name of the movement command
            max_attempts: Maximum number of test attempts
            
        Returns:
            Dictionary with test results
        """
        command_info = self.ADVANCED_MOVEMENTS[command_name]
        command_id = command_info["id"]
        
        result = {
            "command": command_name,
            "api_id": command_id,
            "priority": command_info["priority"],
            "description": command_info["description"],
            "status": "⭕",
            "attempts": 0,
            "error_codes": [],
            "notes": [],
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        logger.info(f"\n🎯 Testing {command_name} (ID: {command_id}) - {command_info['description']}")
        logger.info(f"   Priority: {command_info['priority']}")
        
        for attempt in range(max_attempts):
            result["attempts"] += 1
            
            try:
                logger.info(f"   Attempt {attempt + 1}/{max_attempts}")
                
                # Send the sport command
                response = await self.conn.datachannel.pub_sub.publish_request_new(
                    RTC_TOPIC["SPORT_MOD"], 
                    {"api_id": command_id}
                )
                
                status_code = response['data']['header']['status']['code']
                
                if status_code == 0:
                    result["status"] = "✅"
                    result["notes"].append("Command accepted by robot")
                    logger.info(f"   ✅ {command_name} command accepted!")
                    
                    # Wait for command execution
                    logger.info("   ⏳ Waiting for movement execution...")
                    await asyncio.sleep(5)
                    
                    # Allow robot to recover
                    logger.info("   🔄 Allowing recovery time...")
                    await asyncio.sleep(3)
                    
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
        
        # Safety check - ensure robot is stable after test
        try:
            await asyncio.sleep(1)
            await self.robot.command("BalanceStand")
            await asyncio.sleep(2)
        except:
            pass
        
        return result
    
    def _interpret_error_code(self, code: int) -> str:
        """Interpret common error codes"""
        error_codes = {
            3203: "Command not available in current motion mode (MCF mode limitation)",
            7002: "AI mode not available in current firmware",
            7004: "Motion mode switching restriction",
            3001: "Robot not in correct state for this command",
            3002: "Invalid command parameters",
            3004: "Command execution timeout"
        }
        return error_codes.get(code, "Unknown error")
    
    async def run_medium_priority_tests(self) -> Dict[str, Any]:
        """Test medium priority movements first (safer)"""
        logger.info("\n" + "="*60)
        logger.info("🚀 TESTING MEDIUM PRIORITY ADVANCED MOVEMENTS")
        logger.info("="*60)
        
        medium_priority = ["FrontJump", "FrontPounce"]
        results = {}
        
        for command in medium_priority:
            result = await self.test_advanced_movement(command)
            results[command] = result
            self.test_results[command] = result
            
            # Brief pause between tests
            await asyncio.sleep(2)
        
        return results
    
    async def run_low_priority_tests(self) -> Dict[str, Any]:
        """Test low priority movements (more complex/risky)"""
        logger.info("\n" + "="*60)
        logger.info("🤸 TESTING LOW PRIORITY ADVANCED MOVEMENTS")
        logger.info("="*60)
        
        low_priority = ["FrontFlip", "BackFlip", "LeftFlip", "RightFlip", "Handstand"]
        results = {}
        
        for command in low_priority:
            result = await self.test_advanced_movement(command)
            results[command] = result
            self.test_results[command] = result
            
            # Longer pause between complex movements
            await asyncio.sleep(3)
        
        return results
    
    async def run_comprehensive_test(self):
        """Run complete advanced movement test suite"""
        logger.info("🎪 STARTING ADVANCED MOVEMENT TEST SUITE")
        logger.info("="*60)
        logger.info("⚠️  WARNING: Testing advanced acrobatic movements!")
        logger.info("⚠️  Ensure robot has adequate space and soft landing area!")
        logger.info("="*60)
        
        try:
            # Connect to robot
            if not await self.connect():
                return
            
            # Safety preparation
            if not await self.safe_preparation_sequence():
                logger.error("❌ Safety preparation failed - aborting tests")
                return
            
            # Test medium priority movements first
            medium_results = await self.run_medium_priority_tests()
            
            # Ask user before proceeding to more complex movements
            logger.info("\n" + "="*60)
            logger.info("⚠️  READY TO TEST COMPLEX ACROBATIC MOVEMENTS")
            logger.info("   These include flips and handstand which may cause falls!")
            logger.info("   Ensure safe environment before proceeding.")
            logger.info("="*60)
            
            # For automated testing, proceed automatically after delay
            logger.info("⏳ Proceeding with complex movements in 5 seconds...")
            logger.info("   Press Ctrl+C to abort if needed")
            await asyncio.sleep(5)
            
            # Test low priority movements
            low_results = await self.run_low_priority_tests()
            
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
            
            # Generate results section
            results_section = "\n### 🔄 **LATEST TEST RESULTS** (Auto-updated)\n\n"
            results_section += f"**Test Date**: {time.strftime('%Y-%m-%d %H:%M:%S')}\n"
            results_section += f"**Test Script**: advanced_movement_test.py\n"
            results_section += f"**Total Commands Tested**: {len(self.test_results)}\n\n"
            
            # Summary table
            results_section += "| Command | Status | API ID | Notes |\n"
            results_section += "|---------|--------|--------| ----- |\n"
            
            for command, result in self.test_results.items():
                status_emoji = result["status"]
                notes = "; ".join(result["notes"][:2])  # First 2 notes
                results_section += f"| {command} | {status_emoji} | {result['api_id']} | {notes} |\n"
            
            results_section += f"\n**Working Commands**: {len([r for r in self.test_results.values() if r['status'] == '✅'])}/7\n"
            results_section += f"**Firmware Limited**: {len([r for r in self.test_results.values() if 'Firmware limitation' in str(r['notes'])])}/7\n\n"
            
            # Look for existing auto-updated section and replace, or add new
            if "### 🔄 **LATEST TEST RESULTS**" in content:
                # Replace existing section
                start_marker = "### 🔄 **LATEST TEST RESULTS**"
                end_marker = "\n### "  # Next section
                
                start_idx = content.find(start_marker)
                end_idx = content.find(end_marker, start_idx + len(start_marker))
                
                if end_idx == -1:  # Last section
                    end_idx = content.find("\n---", start_idx + len(start_marker))
                    if end_idx == -1:
                        end_idx = len(content)
                
                new_content = content[:start_idx] + results_section + content[end_idx:]
            else:
                # Add new section before the final separator
                insertion_point = content.rfind("\n---\n")
                if insertion_point != -1:
                    new_content = content[:insertion_point] + "\n" + results_section + content[insertion_point:]
                else:
                    new_content = content + "\n" + results_section
            
            # Write updated guide
            with open(guide_path, 'w') as f:
                f.write(new_content)
                
            logger.info(f"✅ Test results exported to {guide_path}")
            
        except Exception as e:
            logger.error(f"❌ Failed to export results to guide: {e}")

    def _generate_test_report(self):
        """Generate comprehensive test report"""
        logger.info("\n" + "="*80)
        logger.info("📋 ADVANCED MOVEMENT TEST REPORT")
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
        logger.info(f"   ✅ Working: {len(working_commands)} commands")
        logger.info(f"   ❌ Failed: {len(failed_commands)} commands") 
        logger.info(f"   🚫 Firmware Limited: {len(firmware_limited)} commands")
        
        if working_commands:
            logger.info(f"\n✅ WORKING COMMANDS:")
            for cmd in working_commands:
                logger.info(f"   • {cmd}: {self.ADVANCED_MOVEMENTS[cmd]['description']}")
        
        if firmware_limited:
            logger.info(f"\n🚫 FIRMWARE LIMITED COMMANDS:")
            for cmd in firmware_limited:
                logger.info(f"   • {cmd}: {self.ADVANCED_MOVEMENTS[cmd]['description']}")
                logger.info(f"     Reason: Requires AI mode (not available in current firmware)")
        
        if failed_commands:
            logger.info(f"\n❌ FAILED COMMANDS:")
            for cmd in failed_commands:
                result = self.test_results[cmd]
                logger.info(f"   • {cmd}: {self.ADVANCED_MOVEMENTS[cmd]['description']}")
                if result["error_codes"]:
                    logger.info(f"     Error codes: {result['error_codes']}")
        
        logger.info(f"\n📝 DETAILED RESULTS:")
        for command, result in self.test_results.items():
            logger.info(f"\n   {command} (API ID: {result['api_id']})")
            logger.info(f"   Status: {result['status']} | Priority: {result['priority']}")
            logger.info(f"   Attempts: {result['attempts']} | Time: {result['timestamp']}")
            if result['notes']:
                logger.info(f"   Notes: {'; '.join(result['notes'])}")
        
        logger.info("\n" + "="*80)
        logger.info("💡 RECOMMENDATIONS:")
        logger.info("   1. Update the testing guide with these results")
        logger.info("   2. Focus on working commands for demonstrations")
        logger.info("   3. Check for firmware updates that might restore AI mode")
        logger.info("   4. Consider MCF mode limitations in motion planning")
        logger.info("="*80)
        
        # Export results to testing guide
        logger.info("\n📄 Exporting results to testing guide...")
        self._export_results_to_guide()

async def main():
    """Main test execution"""
    print("🎪 Go2 Advanced Movement Tester")
    print("================================")
    print("This script will test all advanced movement commands")
    print("including flips, jumps, and handstands.")
    print()
    print("⚠️  SAFETY WARNING:")
    print("   • Ensure robot has adequate space (3m x 3m minimum)")
    print("   • Use soft surface or mats for landing")
    print("   • Be ready to catch robot if needed")
    print("   • Have emergency stop ready (Ctrl+C)")
    print()
    
    # Allow user to prepare
    print("⏳ Starting test in 10 seconds...")
    print("   Press Ctrl+C to abort if needed")
    try:
        await asyncio.sleep(10)
    except KeyboardInterrupt:
        print("\n🛑 Test aborted by user")
        return
    
    # Create tester and run
    tester = AdvancedMovementTester(
        connection_method=WebRTCConnectionMethod.LocalAP
        # For router connection, use:
        # connection_method=WebRTCConnectionMethod.LocalSTA, 
        # ip="192.168.8.181"
    )
    
    await tester.run_comprehensive_test()

if __name__ == "__main__":
    asyncio.run(main())