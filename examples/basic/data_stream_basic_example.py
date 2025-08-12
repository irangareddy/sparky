"""
Basic Data Stream Example for Sparky Robot
Demonstrates basic usage of the data streaming system
"""

import asyncio
import logging
import sys
from pathlib import Path

# Add the src directory to the path so we can import sparky modules
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from sparky import Robot
from sparky.core.connection import Go2Connection, WebRTCConnectionMethod
from sparky.core.data_collector import DataCollector, SensorData
from sparky.core.stream_processor import StreamProcessor, MovementEvent, StreamMetrics

# Enable logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BasicDataStreamDemo:
    """Basic demonstration of data streaming capabilities"""
    
    def __init__(self):
        self.connection = None
        self.data_collector = None
        self.stream_processor = None
        self.sample_count = 0
    
    def on_new_data(self, sensor_data: SensorData):
        """Callback for new sensor data"""
        self.sample_count += 1
        
        # Print basic info every 10 samples
        if self.sample_count % 10 == 0:
            print(f"\n--- Sample #{self.sample_count} ---")
            print(f"Timestamp: {sensor_data.timestamp:.2f}")
            print(f"Is Moving: {sensor_data.is_moving}")
            print(f"Movement Magnitude: {sensor_data.movement_magnitude:.3f}")
            print(f"Stability Score: {sensor_data.stability_score:.3f}")
            print(f"Battery SOC: {sensor_data.battery_soc}%")
            print(f"Motor Temperatures: {[f'{temp:.1f}°C' for temp in sensor_data.motor_temperatures[:4]]}")
    
    def on_movement_event(self, event: MovementEvent):
        """Callback for movement events"""
        print(f"\nProcessing MOVEMENT EVENT: {event.event_type.upper()}")
        print(f"   Type: {event.movement_type}")
        print(f"   Magnitude: {event.magnitude:.3f}")
        print(f"   Confidence: {event.confidence:.2f}")
        if event.duration > 0:
            print(f"   Duration: {event.duration:.2f}s")
    
    def on_metrics_update(self, metrics: StreamMetrics):
        """Callback for metrics updates"""
        print(f"\nData METRICS UPDATE")
        print(f"   Activity Level: {metrics.activity_level}")
        print(f"   Movement %: {metrics.movement_percentage:.1f}%")
        print(f"   Health: {metrics.overall_health}")
        print(f"   Max Motor Temp: {metrics.max_motor_temperature:.1f}°C")
        print(f"   Battery Efficiency: {metrics.battery_efficiency:.1f}%")
    
    async def run_demo(self, duration_seconds: int = 60):
        """Run the basic data streaming demo"""
        try:
            print(" Starting Basic Data Stream Demo")
            print("=" * 50)
            
            # Create connection
            print("Connecting to robot...")
            self.connection = Go2Connection(WebRTCConnectionMethod.LocalAP)
            
            # Try different connection methods if LocalAP fails
            if not await self.connection.connect():
                print("LocalAP failed, trying LocalSTA...")
                self.connection = Go2Connection(WebRTCConnectionMethod.LocalSTA, ip="192.168.8.181")
                if not await self.connection.connect():
                    print("Failed to connect to robot")
                    return
            
            print(" Connected to robot!")
            
            # Initialize data streaming components
            print("Setting up data streaming...")
            self.data_collector = DataCollector(self.connection.conn, buffer_size=500)
            self.stream_processor = StreamProcessor(self.data_collector, window_size=30)
            
            # Add callbacks
            self.data_collector.add_callback(self.on_new_data)
            self.stream_processor.add_event_callback(self.on_movement_event)
            self.stream_processor.add_metrics_callback(self.on_metrics_update)
            
            # Start data collection and processing
            print("▶️  Starting data collection...")
            await self.data_collector.start_collection()
            await self.stream_processor.start_processing()
            
            print(f"Target Demo running for {duration_seconds} seconds...")
            print(" Try moving the robot to see movement detection in action!")
            print("-" * 50)
            
            # Run for specified duration
            await asyncio.sleep(duration_seconds)
            
            # Show final statistics
            await self.show_final_stats()
            
        except Exception as e:
            logger.error(f"Error in demo: {e}")
        finally:
            await self.cleanup()
    
    async def show_final_stats(self):
        """Show final statistics"""
        print("\n" + "=" * 50)
        print("Status FINAL STATISTICS")
        print("=" * 50)
        
        if self.data_collector:
            stats = self.data_collector.get_collection_stats()
            print(f"Total Samples Collected: {stats['total_samples']}")
            print(f"Sampling Rate: {stats['sampling_rate']:.2f} Hz")
            
            # Show recent data summary
            recent_data = await self.data_collector.get_data_history(50)
            if recent_data:
                moving_count = sum(1 for d in recent_data if d.is_moving)
                avg_stability = sum(d.stability_score for d in recent_data) / len(recent_data)
                print(f"Recent Activity: {(moving_count/len(recent_data)*100):.1f}% moving")
                print(f"Average Stability: {avg_stability:.3f}")
        
        if self.stream_processor:
            metrics = self.stream_processor.get_current_metrics()
            print(f"Final Activity Level: {metrics.activity_level}")
            print(f"Overall Health: {metrics.overall_health}")
    
    async def cleanup(self):
        """Clean up resources"""
        print("\nCleaning up...")
        
        if self.stream_processor:
            await self.stream_processor.stop_processing()
        
        if self.data_collector:
            await self.data_collector.stop_collection()
        
        if self.connection:
            await self.connection.disconnect()
        
        print(" Cleanup complete")

async def main():
    """Main function"""
    demo = BasicDataStreamDemo()
    
    # Run demo for 60 seconds (adjust as needed)
    await demo.run_demo(duration_seconds=60)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nWARNING  Demo interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"FAILED Demo failed: {e}")
        sys.exit(1)
