"""
High-Level Robot API
Simplified interface for common robot operations
"""

import asyncio
import logging
from typing import Dict, Any, Optional, Union

from .interfaces import RobotInterface
from .utils.constants import ConnectionMethod
from .core.connection import Go2Connection, WebRTCConnectionMethod
from .core.motion import MotionController
from .core.data_collector import DataCollector
from .core.stream_processor import StreamProcessor
from .core.analytics_engine import AnalyticsEngine

logger = logging.getLogger(__name__)

class Robot(RobotInterface):
    """
    High-level robot interface that simplifies common operations
    
    This class provides a simplified API for basic robot operations,
    hiding the complexity of the underlying components while still
    allowing access to advanced features when needed.
    """
    
    def __init__(self):
        self.connection: Optional[Go2Connection] = None
        self.motion: Optional[MotionController] = None
        self.data_collector: Optional[DataCollector] = None
        self.stream_processor: Optional[StreamProcessor] = None
        self.analytics_engine: Optional[AnalyticsEngine] = None
        self._data_streaming_active = False
        
    async def connect(self, 
                     method: ConnectionMethod = ConnectionMethod.LOCALAP,
                     ip: Optional[str] = None,
                     serial_number: Optional[str] = None,
                     username: Optional[str] = None,
                     password: Optional[str] = None) -> bool:
        """
        Connect to robot using simplified parameters
        
        Args:
            method: Connection method to use
            ip: Robot IP address (for LocalSTA)
            serial_number: Robot serial number (for LocalSTA/Remote)
            username: Username (for Remote)
            password: Password (for Remote)
            
        Returns:
            True if connection successful, False otherwise
        """
        try:
            # Map interface enum to internal enum
            method_map = {
                ConnectionMethod.LOCALAP: WebRTCConnectionMethod.LocalAP,
                ConnectionMethod.ROUTER: WebRTCConnectionMethod.LocalSTA
            }
            
            webrtc_method = method_map[method]
            
            # Create connection based on method
            self.connection = Go2Connection(
                connection_method=webrtc_method,
                ip=ip,
                serial_number=serial_number,
                username=username,
                password=password
            )
            
            # Attempt connection
            success = await self.connection.connect()
            
            if success:
                # Initialize motion controller
                self.motion = MotionController(self.connection.conn)
                logger.info(f"Successfully connected to robot via {method.value}")
                return True
            else:
                logger.error(f"Failed to connect to robot via {method.value}")
                return False
                
        except Exception as e:
            logger.error(f"Error connecting to robot: {e}")
            return False
    
    async def disconnect(self) -> bool:
        """Disconnect from robot and cleanup resources"""
        try:
            # Stop data streaming if active
            if self._data_streaming_active:
                await self.stop_data_stream()
            
            # Disconnect from robot
            if self.connection:
                success = await self.connection.disconnect()
                self.connection = None
                self.motion = None
                logger.info("Disconnected from robot")
                return success
            
            return True
            
        except Exception as e:
            logger.error(f"Error disconnecting from robot: {e}")
            return False
    
    async def move(self, 
                  direction: str, 
                  speed: float = 0.5, 
                  duration: float = 2.0,
                  verify: bool = True) -> bool:
        """
        Move robot in specified direction
        
        Args:
            direction: Movement direction (forward, backward, left, right, turn-left, turn-right)
            speed: Movement speed (0.1 to 1.0)
            duration: Movement duration in seconds
            verify: Whether to verify movement actually occurred
            
        Returns:
            True if movement successful, False otherwise
        """
        if not self.motion:
            logger.error("Not connected to robot")
            return False
        
        try:
            direction = direction.lower().replace("_", "-")
            
            if direction == "forward":
                return await self.motion.move_forward(speed, duration, verify=verify)
            elif direction == "backward":
                return await self.motion.move_backward(speed, duration, verify=verify)
            elif direction == "left":
                return await self.motion.move_left(speed, duration, verify=verify)
            elif direction == "right":
                return await self.motion.move_right(speed, duration, verify=verify)
            elif direction in ["turn-left", "turnleft"]:
                return await self.motion.turn_left(speed, duration, verify=verify)
            elif direction in ["turn-right", "turnright"]:
                return await self.motion.turn_right(speed, duration, verify=verify)
            elif direction == "stop":
                return await self.motion.stop()
            else:
                logger.error(f"Unknown movement direction: {direction}")
                return False
                
        except Exception as e:
            logger.error(f"Error moving robot {direction}: {e}")
            return False
    
    async def command(self, command: str, verify: bool = True) -> bool:
        """
        Execute a sport command
        
        Args:
            command: Sport command to execute (hello, sit, standup, etc.)
            verify: Whether to verify command execution
            
        Returns:
            True if command successful, False otherwise
        """
        if not self.motion:
            logger.error("Not connected to robot")
            return False
        
        try:
            return await self.motion.execute_sport_command(command.title(), verify=verify)
        except Exception as e:
            logger.error(f"Error executing command {command}: {e}")
            return False
    
    async def is_moving(self) -> bool:
        """
        Check if robot is currently moving
        
        Returns:
            True if robot is moving, False otherwise
        """
        if self.analytics_engine:
            try:
                return await self.analytics_engine.is_robot_moving()
            except Exception as e:
                logger.error(f"Error checking movement via analytics: {e}")
        
        # Fallback to motion controller status
        if self.motion:
            try:
                status = self.motion.get_status()
                return status.get("is_moving", False)
            except Exception as e:
                logger.error(f"Error checking movement status: {e}")
        
        return False
    
    async def get_status(self) -> Dict[str, Any]:
        """
        Get comprehensive robot status
        
        Returns:
            Dictionary containing robot status information
        """
        status = {
            "connected": self.connection is not None and self.connection.is_connected,
            "data_streaming": self._data_streaming_active,
            "motion_available": self.motion is not None,
            "analytics_available": self.analytics_engine is not None
        }
        
        if self.connection:
            status["connection"] = self.connection.get_connection_info()
        
        if self.motion:
            status["motion"] = self.motion.get_status()
        
        if self.data_collector:
            status["data_collection"] = self.data_collector.get_collection_stats()
        
        if self.stream_processor:
            status["metrics"] = self.stream_processor.get_current_metrics()
        
        return status
    
    async def start_data_stream(self, buffer_size: int = 1000, analytics: bool = True) -> None:
        """
        Start data streaming and analytics
        
        Args:
            buffer_size: Size of data buffer
            analytics: Whether to enable analytics engine
        """
        if not self.connection or not self.connection.is_connected:
            raise RuntimeError("Not connected to robot")
        
        try:
            # Initialize data collection components
            self.data_collector = DataCollector(self.connection.conn, buffer_size)
            self.stream_processor = StreamProcessor(self.data_collector)
            
            if analytics:
                self.analytics_engine = AnalyticsEngine(self.data_collector)
            
            # Start data streaming
            await self.data_collector.start_collection()
            await self.stream_processor.start_processing()
            
            if self.analytics_engine:
                await self.analytics_engine.start_streaming()
            
            self._data_streaming_active = True
            logger.info("Data streaming started")
            
        except Exception as e:
            logger.error(f"Error starting data stream: {e}")
            raise
    
    async def stop_data_stream(self) -> None:
        """Stop data streaming and analytics"""
        try:
            if self.analytics_engine:
                await self.analytics_engine.stop_streaming()
                self.analytics_engine = None
            
            if self.stream_processor:
                await self.stream_processor.stop_processing()
                self.stream_processor = None
            
            if self.data_collector:
                await self.data_collector.stop_collection()
                self.data_collector = None
            
            self._data_streaming_active = False
            logger.info("Data streaming stopped")
            
        except Exception as e:
            logger.error(f"Error stopping data stream: {e}")
    
    async def export_data(self, format_type: str = "json") -> Any:
        """
        Export collected data
        
        Args:
            format_type: Export format ("json" or "csv")
            
        Returns:
            Exported data in specified format
        """
        if not self.data_collector:
            raise RuntimeError("Data collection not active")
        
        try:
            return await self.data_collector.export_data(format_type)
        except Exception as e:
            logger.error(f"Error exporting data: {e}")
            raise
    
    # Convenience methods for common operations
    
    async def hello(self) -> bool:
        """Make robot wave hello"""
        return await self.command("hello")
    
    async def sit(self) -> bool:
        """Make robot sit down"""
        return await self.command("sit")
    
    async def stand_up(self) -> bool:
        """Make robot stand up"""
        return await self.command("standup")
    
    async def dance(self, dance_number: int = 1) -> bool:
        """Make robot dance"""
        return await self.command(f"dance{dance_number}")
    
    async def walk_square(self, side_length: float = 0.5) -> bool:
        """Make robot walk in a square pattern"""
        if not self.motion:
            return False
        try:
            return await self.motion.walk_square(side_length)
        except Exception as e:
            logger.error(f"Error walking square: {e}")
            return False
    
    async def spin_360(self, direction: str = "right") -> bool:
        """Make robot spin 360 degrees"""
        if not self.motion:
            return False
        try:
            return await self.motion.spin_360(direction)
        except Exception as e:
            logger.error(f"Error spinning 360: {e}")
            return False
    
    # Context manager support
    async def __aenter__(self):
        """Async context manager entry"""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.disconnect()

# Convenience functions for quick usage
async def connect_robot(method: ConnectionMethod = ConnectionMethod.LOCALAP, **kwargs) -> Robot:
    """
    Quick function to connect to a robot
    
    Args:
        method: Connection method to use
        **kwargs: Additional connection parameters
        
    Returns:
        Connected Robot instance
    """
    robot = Robot()
    success = await robot.connect(method, **kwargs)
    if not success:
        raise RuntimeError("Failed to connect to robot")
    return robot
