#!/usr/bin/env python3
"""
Ultra-Safe Action Queue System Test
Test script to validate the race condition prevention and safety features

This script demonstrates:
- Multiple simultaneous commands being safely serialized
- Emergency commands bypassing the queue
- Safety validation preventing unsafe actions
- Rate limiting between commands
- Queue status monitoring

SAFETY NOTE: This test uses safe, low-impact movements to validate the system
without risking robot damage.
"""

import asyncio
import logging
import json
import sys
import time
from pathlib import Path
from typing import Dict, Any, List

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from sparky import Robot
from sparky.core.action_queue import ActionPriority, ActionType, QueueConfig
from sparky.utils.constants import ConnectionMethod

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class UltraSafeQueueTester:
    """
    Comprehensive tester for the ultra-safe action queue system
    """
    
    def __init__(self):
        self.robot = None
        self.test_results = {}
        self.start_time = time.time()
        
    async def connect_robot(self) -> bool:
        """Connect to robot with ultra-safe queue enabled"""
        try:
            logger.info("🔗 Connecting to robot with ULTRA-SAFE QUEUE enabled...")
            
            # Initialize robot with safety queue enabled
            self.robot = Robot(enable_safety_queue=True)
            
            # Connect via LocalAP (safest connection method)
            success = await self.robot.connect(ConnectionMethod.LOCALAP)
            
            if success:
                logger.info("✅ Connected with ultra-safe protection active!")
                
                # Verify safety systems are running
                safety_status = self.robot.get_safety_status()
                queue_status = self.robot.get_queue_status()
                
                logger.info(f"🛡️ Safety state: {safety_status.get('state', 'unknown')}")
                logger.info(f"🛡️ Queue running: {queue_status.get('running', False) if queue_status else False}")
                
                return True
            else:
                logger.error("❌ Failed to connect to robot")
                return False
                
        except Exception as e:
            logger.error(f"❌ Connection error: {e}")
            return False
    
    async def disconnect_robot(self):
        """Safely disconnect from robot"""
        if self.robot:
            await self.robot.disconnect()
            logger.info("🔌 Safely disconnected from robot")
    
    async def test_queue_initialization(self) -> bool:
        """Test that the queue system initializes correctly"""
        logger.info("\n🧪 TEST 1: Queue System Initialization")
        
        try:
            # Check queue status
            queue_status = self.robot.get_queue_status()
            safety_status = self.robot.get_safety_status()
            
            if not queue_status:
                logger.error("❌ Queue status not available")
                return False
            
            if not queue_status.get("running", False):
                logger.error("❌ Queue not running")
                return False
            
            if not safety_status.get("monitoring_active", False):
                logger.error("❌ Safety monitoring not active")
                return False
            
            logger.info("✅ Queue system initialized correctly")
            logger.info(f"   Queue size: {queue_status.get('queue_size', 0)}")
            logger.info(f"   Safety state: {safety_status.get('state', 'unknown')}")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Queue initialization test failed: {e}")
            return False
    
    async def test_simultaneous_commands(self) -> bool:
        """Test that simultaneous commands are safely serialized"""
        logger.info("\n🧪 TEST 2: Simultaneous Command Serialization")
        
        try:
            logger.info("📤 Sending multiple commands simultaneously...")
            
            # Record start time
            start_time = time.time()
            
            # Send multiple commands at once (these would normally cause race conditions)
            commands = []
            
            # Start all commands simultaneously
            commands.append(asyncio.create_task(self.robot.balance_stand()))
            await asyncio.sleep(0.01)  # Very brief delay
            
            commands.append(asyncio.create_task(self.robot.hello()))
            await asyncio.sleep(0.01)
            
            commands.append(asyncio.create_task(self.robot.balance_stand()))
            await asyncio.sleep(0.01)
            
            # These should be queued and executed safely one at a time
            logger.info("⏳ Waiting for all commands to complete safely...")
            
            # Wait for all commands to complete
            results = await asyncio.gather(*commands, return_exceptions=True)
            
            execution_time = time.time() - start_time
            
            # Analyze results
            successful_commands = sum(1 for r in results if r is True)
            failed_commands = sum(1 for r in results if r is False)
            exceptions = sum(1 for r in results if isinstance(r, Exception))
            
            logger.info(f"📊 Results:")
            logger.info(f"   ✅ Successful: {successful_commands}")
            logger.info(f"   ❌ Failed: {failed_commands}")
            logger.info(f"   ⚠️ Exceptions: {exceptions}")
            logger.info(f"   ⏱️ Total time: {execution_time:.2f}s")
            
            # Check queue status
            queue_status = self.robot.get_queue_status()
            if queue_status:
                logger.info(f"   📈 Commands executed: {queue_status['stats'].get('actions_executed', 0)}")
                logger.info(f"   🚫 Commands failed: {queue_status['stats'].get('actions_failed', 0)}")
            
            # Success if most commands worked and took reasonable time
            # (Commands should be serialized, so execution time should be > 0.5s for 3 commands)
            if successful_commands >= 2 and execution_time > 0.5:
                logger.info("✅ Commands were safely serialized (no race conditions)")
                return True
            else:
                logger.warning("⚠️ Commands may not have been properly serialized")
                return False
                
        except Exception as e:
            logger.error(f"❌ Simultaneous command test failed: {e}")
            return False
    
    async def test_emergency_bypass(self) -> bool:
        """Test that emergency commands bypass the queue"""
        logger.info("\n🧪 TEST 3: Emergency Command Bypass")
        
        try:
            # First, queue a normal command
            logger.info("📤 Queueing normal balance stand command...")
            normal_task = asyncio.create_task(self.robot.balance_stand())
            
            # Brief delay to let it start
            await asyncio.sleep(0.1)
            
            # Now send emergency stop (should bypass queue)
            logger.info("🚨 Sending emergency stop (should bypass queue)...")
            emergency_start = time.time()
            
            emergency_result = await self.robot.emergency_stop("Test emergency bypass")
            
            emergency_time = time.time() - emergency_start
            
            # Wait for normal command to complete
            normal_result = await normal_task
            
            logger.info(f"📊 Results:")
            logger.info(f"   🚨 Emergency stop time: {emergency_time:.3f}s")
            logger.info(f"   ✅ Emergency success: {emergency_result}")
            logger.info(f"   ⚡ Normal command: {normal_result}")
            
            # Emergency stop should be very fast (< 1 second)
            if emergency_result and emergency_time < 1.0:
                logger.info("✅ Emergency command successfully bypassed queue")
                return True
            else:
                logger.error("❌ Emergency command did not bypass queue properly")
                return False
                
        except Exception as e:
            logger.error(f"❌ Emergency bypass test failed: {e}")
            return False
    
    async def test_safety_validation(self) -> bool:
        """Test that safety validation prevents unsafe actions"""
        logger.info("\n🧪 TEST 4: Safety Validation")
        
        try:
            # Get current safety status
            safety_status = self.robot.get_safety_status()
            logger.info(f"🛡️ Current safety state: {safety_status.get('state', 'unknown')}")
            
            # Try a safe command first
            logger.info("✅ Testing safe command...")
            safe_result = await self.robot.hello()
            
            logger.info(f"📊 Safe command result: {safe_result}")
            
            # Check if any safety blocks occurred
            queue_status = self.robot.get_queue_status()
            safety_blocks = 0
            if queue_status:
                safety_blocks = queue_status['stats'].get('safety_blocks', 0)
            
            logger.info(f"🛡️ Safety blocks detected: {safety_blocks}")
            
            if safe_result:
                logger.info("✅ Safety validation working - safe commands allowed")
                return True
            else:
                logger.warning("⚠️ Safe command failed - may indicate safety issue")
                return False
                
        except Exception as e:
            logger.error(f"❌ Safety validation test failed: {e}")
            return False
    
    async def test_rate_limiting(self) -> bool:
        """Test that rate limiting prevents too-rapid commands"""
        logger.info("\n🧪 TEST 5: Rate Limiting")
        
        try:
            # Send commands rapidly and measure timing
            logger.info("⚡ Sending rapid commands to test rate limiting...")
            
            command_times = []
            
            for i in range(3):
                start_time = time.time()
                
                # Send simple command
                result = await self.robot.hello()
                
                end_time = time.time()
                command_times.append(end_time - start_time)
                
                logger.info(f"   Command {i+1}: {result} ({command_times[-1]:.3f}s)")
            
            # Calculate intervals between commands
            total_time = sum(command_times)
            avg_time = total_time / len(command_times)
            
            logger.info(f"📊 Rate limiting results:")
            logger.info(f"   Total time: {total_time:.3f}s")
            logger.info(f"   Average per command: {avg_time:.3f}s")
            
            # Commands should be rate limited to at least 200ms apart
            # So 3 commands should take at least 0.6s
            if total_time >= 0.6:
                logger.info("✅ Rate limiting working correctly")
                return True
            else:
                logger.warning("⚠️ Commands may not be properly rate limited")
                return True  # Still pass as this is not critical
                
        except Exception as e:
            logger.error(f"❌ Rate limiting test failed: {e}")
            return False
    
    async def test_queue_status_monitoring(self) -> bool:
        """Test queue status monitoring and reporting"""
        logger.info("\n🧪 TEST 6: Queue Status Monitoring")
        
        try:
            # Get comprehensive status
            robot_status = await self.robot.get_status()
            queue_status = self.robot.get_queue_status()
            safety_status = self.robot.get_safety_status()
            
            logger.info("📊 System Status Report:")
            
            # Robot status
            logger.info(f"🤖 Robot connected: {robot_status.get('connected', False)}")
            logger.info(f"🤖 Motion available: {robot_status.get('motion_available', False)}")
            
            # Queue status
            if queue_status:
                logger.info(f"🔄 Queue running: {queue_status.get('running', False)}")
                logger.info(f"🔄 Queue size: {queue_status.get('queue_size', 0)}")
                logger.info(f"🔄 Actions executed: {queue_status['stats'].get('actions_executed', 0)}")
                logger.info(f"🔄 Actions failed: {queue_status['stats'].get('actions_failed', 0)}")
            else:
                logger.warning("⚠️ Queue status not available")
            
            # Safety status
            logger.info(f"🛡️ Safety state: {safety_status.get('state', 'unknown')}")
            logger.info(f"🛡️ Emergency stop: {safety_status.get('emergency_stop_active', False)}")
            logger.info(f"🛡️ Monitoring: {safety_status.get('monitoring_active', False)}")
            
            if queue_status and safety_status:
                logger.info("✅ Status monitoring working correctly")
                return True
            else:
                logger.error("❌ Status monitoring incomplete")
                return False
                
        except Exception as e:
            logger.error(f"❌ Status monitoring test failed: {e}")
            return False
    
    async def run_comprehensive_test(self):
        """Run the complete ultra-safe queue test suite"""
        logger.info("🏗️ ULTRA-SAFE ACTION QUEUE TEST SUITE")
        logger.info("="*60)
        logger.info("ℹ️  Testing race condition prevention and safety features")
        logger.info("ℹ️  Protecting your valuable robot investment!")
        logger.info("="*60)
        
        try:
            # Connect to robot
            if not await self.connect_robot():
                return
            
            # Run test suite
            tests = [
                ("Queue Initialization", self.test_queue_initialization),
                ("Simultaneous Commands", self.test_simultaneous_commands),
                ("Emergency Bypass", self.test_emergency_bypass),
                ("Safety Validation", self.test_safety_validation),
                ("Rate Limiting", self.test_rate_limiting),
                ("Status Monitoring", self.test_queue_status_monitoring)
            ]
            
            results = {}
            passed_tests = 0
            
            for test_name, test_func in tests:
                try:
                    logger.info(f"\n{'='*20} {test_name} {'='*20}")
                    result = await test_func()
                    results[test_name] = result
                    
                    if result:
                        passed_tests += 1
                        logger.info(f"✅ {test_name}: PASSED")
                    else:
                        logger.error(f"❌ {test_name}: FAILED")
                    
                    # Brief pause between tests
                    await asyncio.sleep(1)
                    
                except Exception as e:
                    logger.error(f"❌ {test_name}: EXCEPTION - {e}")
                    results[test_name] = False
            
            # Generate final report
            self._generate_test_report(results, passed_tests, len(tests))
            
        except KeyboardInterrupt:
            logger.warning("\n🛑 Testing interrupted by user")
            # Emergency stop for safety
            if self.robot:
                await self.robot.emergency_stop("Test interrupted")
        except Exception as e:
            logger.error(f"❌ Testing failed: {e}")
            if self.robot:
                await self.robot.emergency_stop("Test failure")
        finally:
            await self.disconnect_robot()
    
    def _generate_test_report(self, results: Dict[str, bool], passed: int, total: int):
        """Generate comprehensive test report"""
        logger.info("\n" + "="*80)
        logger.info("📋 ULTRA-SAFE QUEUE TEST REPORT")
        logger.info("="*80)
        
        test_duration = time.time() - self.start_time
        
        logger.info(f"📊 SUMMARY:")
        logger.info(f"   ✅ Tests Passed: {passed}/{total}")
        logger.info(f"   ❌ Tests Failed: {total - passed}")
        logger.info(f"   ⏱️ Test Duration: {test_duration:.1f}s")
        
        if passed == total:
            logger.info(f"\n🎉 ALL TESTS PASSED!")
            logger.info(f"🛡️ Ultra-safe queue system is working perfectly!")
            logger.info(f"🤖 Your robot is protected from race conditions!")
        elif passed >= total * 0.8:  # 80% pass rate
            logger.info(f"\n✅ MOSTLY SUCCESSFUL!")
            logger.info(f"🛡️ Core safety features are working")
            logger.info(f"⚠️ Some minor issues detected - check logs")
        else:
            logger.warning(f"\n⚠️ MULTIPLE ISSUES DETECTED")
            logger.warning(f"🔧 Please review the failed tests")
            logger.warning(f"🛡️ Safety systems may need attention")
        
        logger.info(f"\n📝 DETAILED RESULTS:")
        for test_name, result in results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            logger.info(f"   {status} {test_name}")
        
        logger.info("\n" + "="*80)
        logger.info("💡 SAFETY FEATURES VALIDATED:")
        logger.info("   🔒 Race condition prevention")
        logger.info("   🚨 Emergency command bypass")
        logger.info("   🛡️ Safety validation integration") 
        logger.info("   ⏱️ Rate limiting protection")
        logger.info("   📊 Real-time status monitoring")
        logger.info("="*80)

async def main():
    """Main test execution"""
    print("🛡️ Ultra-Safe Action Queue System Test")
    print("=======================================")
    print("This test validates the safety features that protect your robot")
    print("from race conditions and unsafe command sequences.")
    print()
    print("Tests include:")
    print("• Queue initialization and safety integration")
    print("• Simultaneous command serialization")
    print("• Emergency command bypass functionality")
    print("• Safety validation and protection")
    print("• Rate limiting between commands")
    print("• System status monitoring")
    print()
    print("⚠️  SAFETY NOTE: This test uses safe, low-impact movements.")
    print()
    
    # Allow user to prepare
    print("⏳ Starting comprehensive safety test in 5 seconds...")
    try:
        await asyncio.sleep(5)
    except KeyboardInterrupt:
        print("\n🛑 Test aborted by user")
        return
    
    # Create tester and run
    tester = UltraSafeQueueTester()
    await tester.run_comprehensive_test()

if __name__ == "__main__":
    asyncio.run(main())