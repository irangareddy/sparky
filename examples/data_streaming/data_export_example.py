"""
Data Export Example for Sparky Robot
Demonstrates data collection and export capabilities for analytics
"""

import asyncio
import logging
import json
import csv
import sys
from pathlib import Path
from datetime import datetime

# Add the src directory to the path so we can import sparky modules
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from sparky.core.connection import Go2Connection, WebRTCConnectionMethod
from sparky.core.data_collector import DataCollector

# Enable logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataExportDemo:
    """Data collection and export demonstration"""
    
    def __init__(self):
        self.connection = None
        self.data_collector = None
        self.export_dir = Path("sparky_data_exports")
    
    async def run_demo(self, duration_seconds: int = 60):
        """Run the data export demo"""
        try:
            print("Saving Starting Data Export Demo")
            print("=" * 50)
            
            # Create export directory
            self.export_dir.mkdir(exist_ok=True)
            print(f"Directory Export directory: {self.export_dir.absolute()}")
            
            # Setup connection and data collection
            await self.setup_data_collection()
            
            # Collect data
            await self.collect_data(duration_seconds)
            
            # Export data in different formats
            await self.export_all_formats()
            
            # Show export summary
            await self.show_export_summary()
            
        except Exception as e:
            logger.error(f"Error in export demo: {e}")
        finally:
            await self.cleanup()
    
    async def setup_data_collection(self):
        """Setup connection and data collector"""
        print("Connecting to robot...")
        
        # Try multiple connection methods
        for method, kwargs in [
            (WebRTCConnectionMethod.LocalAP, {}),
            (WebRTCConnectionMethod.LocalSTA, {"ip": "192.168.8.181"}),
        ]:
            self.connection = Go2Connection(method, **kwargs)
            if await self.connection.connect():
                print(f" Connected via {method}")
                break
        else:
            raise Exception("Failed to connect to robot")
        
        # Initialize data collector with larger buffer for export
        print("Setting up data collector...")
        self.data_collector = DataCollector(self.connection.conn, buffer_size=5000)
        
        # Add progress callback
        sample_count = [0]
        def progress_callback(sensor_data):
            sample_count[0] += 1
            if sample_count[0] % 50 == 0:
                print(f"Data Collected {sample_count[0]} samples...")
        
        self.data_collector.add_callback(progress_callback)
        
        # Start collection
        await self.data_collector.start_collection()
        print(" Data collection started!")
    
    async def collect_data(self, duration_seconds: int):
        """Collect data for specified duration"""
        print(f"Timer  Collecting data for {duration_seconds} seconds...")
        print(" Move the robot to capture interesting data!")
        print("-" * 50)
        
        # Show progress every 10 seconds
        for i in range(duration_seconds // 10):
            await asyncio.sleep(10)
            stats = self.data_collector.get_collection_stats()
            print(f"Timer  Progress: {(i+1)*10}s - Rate: {stats['sampling_rate']:.1f} Hz")
        
        # Wait for remaining time
        remaining = duration_seconds % 10
        if remaining > 0:
            await asyncio.sleep(remaining)
        
        print(" Data collection complete!")
    
    async def export_all_formats(self):
        """Export data in all supported formats"""
        print("\nSaving Exporting data in multiple formats...")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Export as JSON
        await self.export_json(timestamp)
        
        # Export as CSV
        await self.export_csv(timestamp)
        
        # Export summary statistics
        await self.export_summary(timestamp)
        
        # Export filtered data (movement only)
        await self.export_movement_data(timestamp)
    
    async def export_json(self, timestamp: str):
        """Export data as JSON"""
        try:
            print("Document Exporting JSON data...")
            json_data = await self.data_collector.export_data("json")
            
            json_file = self.export_dir / f"sparky_data_{timestamp}.json"
            with open(json_file, 'w') as f:
                json.dump({
                    'metadata': {
                        'export_timestamp': datetime.now().isoformat(),
                        'sample_count': len(json_data),
                        'collection_stats': self.data_collector.get_collection_stats()
                    },
                    'data': json_data
                }, f, indent=2)
            
            print(f" JSON exported: {json_file} ({len(json_data)} samples)")
            
        except Exception as e:
            print(f"FAILED JSON export failed: {e}")
    
    async def export_csv(self, timestamp: str):
        """Export data as CSV"""
        try:
            print("Data Exporting CSV data...")
            csv_data = await self.data_collector.export_data("csv")
            
            if csv_data:
                csv_file = self.export_dir / f"sparky_data_{timestamp}.csv"
                with open(csv_file, 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerows(csv_data)
                
                print(f" CSV exported: {csv_file} ({len(csv_data)-1} data rows)")
            else:
                print("WARNING  No data to export to CSV")
                
        except Exception as e:
            print(f"FAILED CSV export failed: {e}")
    
    async def export_summary(self, timestamp: str):
        """Export summary statistics"""
        try:
            print("Status Exporting summary statistics...")
            
            # Get all data for analysis
            all_data = await self.data_collector.get_data_history(10000)  # Get all data
            
            if not all_data:
                print("WARNING  No data for summary")
                return
            
            # Calculate summary statistics
            summary = {
                'collection_info': {
                    'export_timestamp': datetime.now().isoformat(),
                    'total_samples': len(all_data),
                    'collection_duration': all_data[-1].timestamp - all_data[0].timestamp,
                    'sampling_rate': self.data_collector.get_collection_stats()['sampling_rate']
                },
                'movement_analysis': {
                    'total_moving_samples': sum(1 for d in all_data if d.is_moving),
                    'movement_percentage': (sum(1 for d in all_data if d.is_moving) / len(all_data)) * 100,
                    'avg_movement_magnitude': sum(d.movement_magnitude for d in all_data) / len(all_data),
                    'max_movement_magnitude': max(d.movement_magnitude for d in all_data),
                    'avg_stability_score': sum(d.stability_score for d in all_data) / len(all_data)
                },
                'system_health': {
                    'avg_battery_soc': sum(d.battery_soc for d in all_data) / len(all_data),
                    'max_motor_temp': max(max(d.motor_temperatures) if d.motor_temperatures else 0 for d in all_data),
                    'avg_motor_temp': self._safe_avg_temp(all_data),
                    'communication_errors': sum(sum(d.motor_lost_flags) for d in all_data)
                },
                'sensor_ranges': {
                    'imu_rpy_range': self._calculate_range([d.imu_rpy for d in all_data]),
                    'gyroscope_range': self._calculate_range([d.imu_gyroscope for d in all_data]),
                    'accelerometer_range': self._calculate_range([d.imu_accelerometer for d in all_data])
                }
            }
            
            summary_file = self.export_dir / f"sparky_summary_{timestamp}.json"
            with open(summary_file, 'w') as f:
                json.dump(summary, f, indent=2)
            
            print(f" Summary exported: {summary_file}")
            
            # Print key statistics
            print(f"   Data {summary['collection_info']['total_samples']} samples over {summary['collection_info']['collection_duration']:.1f}s")
            print(f"   Walking {summary['movement_analysis']['movement_percentage']:.1f}% movement detected")
            print(f"   Avg battery: {summary['system_health']['avg_battery_soc']:.1f}%")
            
        except Exception as e:
            print(f"FAILED Summary export failed: {e}")
    
    async def export_movement_data(self, timestamp: str):
        """Export only movement data for focused analysis"""
        try:
            print("Walking Exporting movement-only data...")
            
            all_data = await self.data_collector.get_data_history(10000)
            movement_data = [d for d in all_data if d.is_moving]
            
            if not movement_data:
                print("WARNING  No movement data to export")
                return
            
            # Convert to export format
            movement_export = [d.to_dict() for d in movement_data]
            
            movement_file = self.export_dir / f"sparky_movement_{timestamp}.json"
            with open(movement_file, 'w') as f:
                json.dump({
                    'metadata': {
                        'export_timestamp': datetime.now().isoformat(),
                        'total_movement_samples': len(movement_data),
                        'movement_percentage': (len(movement_data) / len(all_data)) * 100,
                        'filter': 'movement_only'
                    },
                    'data': movement_export
                }, f, indent=2)
            
            print(f" Movement data exported: {movement_file} ({len(movement_data)} samples)")
            
        except Exception as e:
            print(f"FAILED Movement export failed: {e}")
    
    def _safe_avg_temp(self, data_list):
        """Safely calculate average temperature"""
        temps = []
        for d in data_list:
            if d.motor_temperatures:
                temps.extend(d.motor_temperatures)
        return sum(temps) / len(temps) if temps else 0.0
    
    def _calculate_range(self, vector_list):
        """Calculate range for vector data"""
        if not vector_list:
            return {"min": 0, "max": 0, "range": 0}
        
        # Flatten all vectors
        all_values = []
        for vector in vector_list:
            if isinstance(vector, list):
                all_values.extend(vector)
        
        if not all_values:
            return {"min": 0, "max": 0, "range": 0}
        
        min_val = min(all_values)
        max_val = max(all_values)
        return {"min": min_val, "max": max_val, "range": max_val - min_val}
    
    async def show_export_summary(self):
        """Show summary of exported files"""
        print("\nSummary EXPORT SUMMARY")
        print("=" * 50)
        
        exported_files = list(self.export_dir.glob("sparky_*"))
        exported_files.sort(key=lambda f: f.stat().st_mtime, reverse=True)
        
        print(f"Directory Export directory: {self.export_dir.absolute()}")
        print(f"Document Total files exported: {len(exported_files)}")
        print("\nExported files:")
        
        for file_path in exported_files:
            size_kb = file_path.stat().st_size / 1024
            print(f"   • {file_path.name} ({size_kb:.1f} KB)")
        
        print(f"\n Use these files for:")
        print(f"   • Data analysis with pandas, numpy, etc.")
        print(f"   • Machine learning model training")
        print(f"   • Movement pattern visualization")
        print(f"   • Performance benchmarking")
        print(f"   • Sharing data with other researchers")
        
        # Show sample usage
        print(f"\nPython usage example:")
        print(f"   import json")
        print(f"   with open('{exported_files[0].name}', 'r') as f:")
        print(f"       data = json.load(f)")
        print(f"   print(f'Loaded {{len(data[\"data\"])}} samples')")
    
    async def cleanup(self):
        """Clean up resources"""
        print("\nCleaning up...")
        
        if self.data_collector:
            await self.data_collector.stop_collection()
        
        if self.connection:
            await self.connection.disconnect()
        
        print(" Cleanup complete")

async def main():
    """Main function"""
    demo = DataExportDemo()
    
    # Collect data for 60 seconds (adjust as needed)
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
