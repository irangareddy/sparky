# Sparky Examples

Simple, focused examples for Go2 robot control - **optimized for Vision Pro integration** and real-time applications.

##  **Start Here** - Vision Pro Ready

### **Vision Pro Integration** (`vision_pro_example.py`)
**Perfect for Vision Pro apps** - Ultra-simple API for real-time robot control.

```bash
python examples/vision_pro_example.py
```

### **Simple Robot Control** (`simple_robot_control.py`)
**Perfect for beginners** - Comprehensive demo of the high-level API.

```bash
python examples/simple_robot_control.py
```

##  **Organized Examples**

###  **Basic** (`basic/`)
**Getting started examples**
- **`data_stream_basic_example.py`** - Real-time sensor data monitoring
- **`forward_movement_test.py`** - Simple movement testing

```bash
python examples/basic/data_stream_basic_example.py
```

###  **Data Streaming** (`data_streaming/`)
**Data collection and analytics**
- **`README.md`** - Data streaming documentation
- **`data_export_example.py`** - Data collection and export
- **`data_stream_analytics_example.py`** - Advanced analytics

```bash
python examples/data_streaming/data_export_example.py
```

###  **Testing** (`testing/`)
**Robot testing and diagnostics**
- **`motion_test.py`** - Comprehensive motion testing
- **`firmware_compatibility_test.py`** - Firmware compatibility check

```bash
python examples/testing/motion_test.py
```

###  **Advanced** (`advanced/`)
**Complex demonstrations**
- **`sparky_motion_demo.py`** - Full motion capabilities demo

```bash
python examples/advanced/sparky_motion_demo.py
```

##  **Quick Integration Guide**

### For Vision Pro Apps
```python
from sparky import Robot

async def vision_pro_control():
    async with Robot() as robot:
        await robot.connect()
        await robot.hello()              # Wave
        await robot.move('forward', 0.3, 2.0)  # Move
        status = await robot.get_status()      # Monitor
```

### For Python Beginners
```python
from sparky import Robot
import asyncio

async def simple_demo():
    robot = Robot()
    await robot.connect()
    await robot.hello()
    await robot.disconnect()

asyncio.run(simple_demo())
```

##  **Setup & Running**

### Install Sparky
```bash
# From project root
pip install -e .

# Or with Poetry  
poetry install
```

### Run Examples
```bash
# Vision Pro integration
python examples/vision_pro_example.py

# Beginner demo
python examples/simple_robot_control.py

# Advanced examples
python src/sparky/examples/motion_test.py
```

## 🌐 **Connection Methods**

Examples automatically try multiple connection types:

1. **LocalAP** (default) - Robot's WiFi hotspot
2. **Router** - Shared WiFi network (requires robot IP)

##  **Why These Examples?**

- ** Real-time focused** - Optimized for responsive control
- ** Vision Pro ready** - Perfect for gesture-based apps
- ** Mobile friendly** - Simple async patterns
- ** Beginner friendly** - Clear, documented code
- ** Fast execution** - No verification overhead

## 🤝 **Need Help?**

- **New to robotics?** Start with `simple_robot_control.py`
- **Building Vision Pro apps?** Use `vision_pro_example.py`
- **Need real-time data?** Check advanced examples in `src/sparky/examples/`
- **Integration issues?** See the troubleshooting section in main README