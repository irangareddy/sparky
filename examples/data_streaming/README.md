# Sparky Data Streaming System

The Sparky Data Streaming System provides a comprehensive analytics framework for Go2 robots, replacing the simple motion verifier with a powerful real-time data analysis pipeline.

##  Quick Start

```python
import asyncio
from sparky.core import Go2Connection, DataCollector, StreamProcessor, AnalyticsEngine

async def quick_start():
    # Connect to robot
    connection = Go2Connection()
    await connection.connect()
    
    # Setup data streaming pipeline
    data_collector = DataCollector(connection.conn)
    stream_processor = StreamProcessor(data_collector)
    analytics_engine = AnalyticsEngine(data_collector, stream_processor)
    
    # Start the pipeline
    await data_collector.start_collection()
    await stream_processor.start_processing()
    await analytics_engine.start_analysis()
    
    # Check if robot is moving
    is_moving = await analytics_engine.is_robot_moving()
    print(f"Robot is {'moving' if is_moving else 'stationary'}")
    
    # Get movement direction
    direction = await analytics_engine.get_movement_direction()
    print(f"Movement direction: {direction.value}")
    
    # Clean up
    await analytics_engine.stop_analysis()
    await stream_processor.stop_processing()
    await data_collector.stop_collection()
    await connection.disconnect()

asyncio.run(quick_start())
```

## 🏗️ System Architecture

The data streaming system consists of three main components:

### 1. DataCollector
- **Purpose**: Collects and structures raw sensor data
- **Features**: 
  - Real-time data buffering
  - Structured data format (SensorData)
  - Multiple export formats (JSON, CSV)
  - Callback system for real-time processing

### 2. StreamProcessor
- **Purpose**: Real-time processing and event detection
- **Features**:
  - Movement event detection
  - Real-time metrics calculation
  - Configurable thresholds
  - Stream analytics

### 3. AnalyticsEngine
- **Purpose**: Advanced analytics and behavior analysis
- **Features**:
  - Movement quality assessment
  - Behavior pattern detection
  - Performance analysis
  - Movement direction classification

##  Data Structure

### SensorData
```python
@dataclass
class SensorData:
    timestamp: float
    
    # IMU Data
    imu_rpy: List[float]          # Roll, Pitch, Yaw
    imu_gyroscope: List[float]    # Angular velocity
    imu_accelerometer: List[float] # Linear acceleration
    imu_quaternion: List[float]   # Orientation quaternion
    
    # Motor Data
    motor_positions: List[float]   # Joint positions
    motor_velocities: List[float]  # Joint velocities
    motor_torques: List[float]     # Joint torques
    motor_temperatures: List[float] # Motor temperatures
    motor_lost_flags: List[bool]   # Communication status
    
    # Battery Data
    battery_soc: int              # State of charge %
    battery_current: float        # Current draw
    battery_voltage: float        # Battery voltage
    battery_temperature: float    # Battery temperature
    
    # Foot Force Data
    foot_forces: List[float]      # Forces on each foot
    
    # Additional Sensors
    temperature_ntc1: float       # NTC temperature
    power_voltage: float          # Power voltage
    
    # Derived Metrics (calculated automatically)
    movement_magnitude: float     # Overall movement intensity
    rotation_magnitude: float     # Rotation intensity
    acceleration_magnitude: float # Acceleration intensity
    is_moving: bool              # Simple movement flag
    stability_score: float       # Stability metric
```

##  Key Features

### Easy Movement Detection
```python
# Simple movement detection
is_moving = await analytics_engine.is_robot_moving()

# Movement direction
direction = await analytics_engine.get_movement_direction()
# Returns: FORWARD, BACKWARD, LEFT, RIGHT, UP, DOWN, TURN_LEFT, TURN_RIGHT, STATIONARY

# Movement quality assessment
quality = await analytics_engine.get_movement_quality()
# Returns: EXCELLENT, GOOD, FAIR, POOR
```

### Real-time Analytics
```python
# Get current metrics
metrics = stream_processor.get_current_metrics()
print(f"Activity Level: {metrics.activity_level}")  # idle, low, moderate, high
print(f"System Health: {metrics.overall_health}")   # good, warning, critical
print(f"Movement %: {metrics.movement_percentage}") # Percentage time moving
```

### Performance Analysis
```python
# Analyze recent performance (last 60 seconds)
performance = await analytics_engine.analyze_recent_performance(60.0)
print(f"Smoothness: {performance['performance_metrics']['smoothness']['average']}")
print(f"Efficiency: {performance['performance_metrics']['efficiency']['average']}")
print(f"Stability: {performance['performance_metrics']['stability']['average']}")
```

### Data Export for Analytics
```python
# Export all data as JSON
json_data = await data_collector.export_data("json")

# Export as CSV for Excel/pandas
csv_data = await data_collector.export_data("csv")

# Get recent data for analysis
recent_data = await data_collector.get_data_history(100)  # Last 100 samples
timeframe_data = await data_collector.get_data_in_timeframe(30.0)  # Last 30 seconds
```

##  Analytics Examples

### Movement Pattern Analysis
```python
# Analyze movement patterns
pattern_analysis = await stream_processor.analyze_movement_pattern(30.0)
print(f"Movement variance: {pattern_analysis['movement_stats']['variance']}")
print(f"Activity summary: {pattern_analysis['activity_summary']}")
```

### Behavior Detection
```python
# Get detected behavior patterns
behaviors = analytics_engine.get_behavior_patterns(5)
for behavior in behaviors:
    print(f"Pattern: {behavior.pattern_type}")
    print(f"Confidence: {behavior.confidence}")
    print(f"Duration: {behavior.end_time - behavior.start_time:.2f}s")
```

### Health Monitoring
```python
# Monitor system health
metrics = stream_processor.get_current_metrics()
if metrics.overall_health == "critical":
    print(" Critical system health detected!")
    print(f"Max temperature: {metrics.max_motor_temperature}°C")
    print(f"Communication health: {metrics.communication_health}%")
```

##  Configuration

### Thresholds
```python
# Adjust movement detection sensitivity
stream_processor.set_movement_threshold(0.1)  # Higher = less sensitive

# Set temperature warnings
stream_processor.set_temperature_thresholds(warning=60.0, critical=80.0)
```

### Buffer Sizes
```python
# Larger buffer for more data history
data_collector = DataCollector(connection.conn, buffer_size=5000)

# Larger processing window for smoother analytics
stream_processor = StreamProcessor(data_collector, window_size=100)
```

##  Example Scripts

1. **`data_stream_basic_example.py`** - Basic data streaming demo
2. **`data_stream_analytics_example.py`** - Advanced analytics demo
3. **`data_export_example.py`** - Data collection and export demo

Run examples:
```bash
cd src/sparky/examples
python data_stream_basic_example.py
python data_stream_analytics_example.py
python data_export_example.py
```

## 🆚 Comparison with Motion Verifier

| Feature | Old Motion Verifier | New Data Streaming System |
|---------|-------------------|---------------------------|
| Movement Detection | Basic threshold-based | Multi-factor analysis with confidence |
| Data Storage | None | Configurable buffering + export |
| Analytics | Simple pass/fail | Comprehensive performance metrics |
| Real-time Processing | Limited | Full streaming pipeline |
| Export Capability | None | JSON, CSV, filtered exports |
| Health Monitoring | None | System health + diagnostics |
| Behavior Analysis | None | Pattern detection + classification |
| Quality Assessment | None | Movement quality scoring |

## 🎛️ API Reference

### DataCollector
- `start_collection()` - Start data collection
- `stop_collection()` - Stop data collection
- `get_latest_data()` - Get most recent sensor data
- `get_data_history(count)` - Get recent data history
- `export_data(format)` - Export data in JSON/CSV format
- `add_callback(func)` - Add real-time data callback

### StreamProcessor
- `start_processing()` - Start stream processing
- `stop_processing()` - Stop processing
- `get_current_metrics()` - Get current metrics
- `add_event_callback(func)` - Add movement event callback
- `analyze_movement_pattern(duration)` - Analyze movement patterns

### AnalyticsEngine
- `start_analysis()` - Start analytics
- `is_robot_moving()` - Check if robot is moving
- `get_movement_direction()` - Get movement direction
- `get_movement_quality()` - Get movement quality score
- `analyze_recent_performance(duration)` - Performance analysis
- `get_behavior_patterns()` - Get detected behaviors

##  Getting Started

1. **Install dependencies** (if not already installed):
   ```bash
   pip install go2-webrtc-driver
   ```

2. **Run basic example**:
   ```bash
   python data_stream_basic_example.py
   ```

3. **Try advanced analytics**:
   ```bash
   python data_stream_analytics_example.py
   ```

4. **Export data for analysis**:
   ```bash
   python data_export_example.py
   ```

##  Use Cases

- **Research**: Export data for machine learning and research
- **Performance Monitoring**: Track robot performance over time
- **Debugging**: Detailed diagnostics for troubleshooting
- **Optimization**: Identify areas for movement improvement
- **Health Monitoring**: Proactive maintenance and health checks
- **Behavior Analysis**: Understand robot movement patterns

The new data streaming system provides a foundation for advanced robotics analytics while maintaining simplicity for basic movement detection needs.
