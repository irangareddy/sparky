# Go2 Robot API Testing Guide

This document provides a systematic approach to testing all Go2 robot functionalities. Each section includes API commands, test priorities, and status tracking.

## Testing Status Legend

- ✅ **Working** - Functionality confirmed working
- ❌ **Not Working** - Functionality confirmed broken
- ⏳ **Testing** - Currently being tested
- ⭕ **Not Tested** - Not yet tested
- ❓ **Unknown** - Status unclear, needs investigation

---

## 1. 🚶 Locomotion & Movement

### Basic Movement Commands

| Command | API ID | Priority | Status | Notes |
|---------|--------|----------|--------|-------|
| Damp | 1001 | High | 🚨 | **DANGER: BLOCKED BY SAFETY** - Causes robot leg collapse! |
| BalanceStand | 1002 | High | ⭕ | Standard balanced standing |
| StopMove | 1003 | High | ⭕ | Emergency stop |
| StandUp | 1004 | High | ⭕ | Rise from lying position |
| StandDown | 1005 | Medium | ⭕ | Lower to lying position |
| RecoveryStand | 1006 | High | ⭕ | Recovery from fall |
| Move | 1008 | High | ⭕ | Basic movement control |
| Sit | 1009 | Medium | ⭕ | Sit down |
| RiseSit | 1010 | Medium | ⭕ | Rise from sitting |

### Gait Control

| Command | API ID | Priority | Status | Notes |
|---------|--------|----------|--------|-------|
| SwitchGait | 1011 | High | ⭕ | Change walking pattern |
| ContinuousGait | 1019 | Medium | ⭕ | Continuous movement |
| EconomicGait | 1035 | Medium | ⭕ | Energy-efficient movement |
| SwitchJoystick | 1027 | High | ⭕ | Toggle joystick control |

### Advanced Movements

| Command | API ID | Priority | Status | Notes |
|---------|--------|----------|--------|-------|
| FrontFlip | 1030 | Low | ✅ | Front somersault - **WORKING!** (Tested 2025-08-12) |
| BackFlip | 1044 | Low | ❌ | Back somersault - Error 3203 (MCF mode limitation) |
| LeftFlip | 1042 | Low | ❌ | Left side flip - Error 3203 (MCF mode limitation) |
| RightFlip | 1043 | Low | ❌ | Right side flip - Error 3203 (MCF mode limitation) |
| FrontJump | 1031 | Medium | ✅ | Forward jump - **WORKING!** (Tested 2025-08-12) |
| FrontPounce | 1032 | Medium | ✅ | Pouncing motion - **WORKING!** (Tested 2025-08-12) |
| Handstand | 1301 | Low | ❌ | Handstand position - Error 3203 (MCF mode limitation) |

### Fun Actions

| Command | API ID | Priority | Status | Notes |
|---------|--------|----------|--------|-------|
| Hello | 1016 | Medium | ⭕ | Greeting gesture |
| Stretch | 1017 | Medium | ⭕ | Stretching motion |
| Dance1 | 1022 | Low | ⭕ | Dance routine 1 |
| Dance2 | 1023 | Low | ⭕ | Dance routine 2 |
| WiggleHips | 1033 | Low | ⭕ | Hip wiggling motion |
| FingerHeart | 1036 | Low | ⭕ | Heart gesture |
| Wallow | 1021 | Low | ⭕ | Rolling motion |

### Specialized Gaits

| Command | API ID | Priority | Status | Notes |
|---------|--------|----------|--------|-------|
| Bound | 1304 | Medium | ⭕ | Bounding gait |
| MoonWalk | 1305 | Low | ⭕ | Moonwalk motion |
| OnesidedStep | 1303 | Medium | ⭕ | Single-side stepping |
| CrossStep | 1302 | Medium | ⭕ | Cross-stepping pattern |
| CrossWalk | 1051 | Medium | ⭕ | Cross-walking gait |
| FreeWalk | 1045 | Medium | ⭕ | Free walking mode |

### Configuration Commands

| Command | API ID | Priority | Status | Notes |
|---------|--------|----------|--------|-------|
| BodyHeight | 1013 | High | ⭕ | Adjust body height |
| FootRaiseHeight | 1014 | Medium | ⭕ | Adjust foot lift height |
| SpeedLevel | 1015 | High | ⭕ | Set movement speed |
| GetBodyHeight | 1024 | Medium | ⭕ | Read current body height |
| GetFootRaiseHeight | 1025 | Medium | ⭕ | Read foot raise height |
| GetSpeedLevel | 1026 | Medium | ⭕ | Read current speed level |
| GetState | 1034 | High | ⭕ | Get current movement state |

---

## 2. 🔊 Audio System

### Audio Player Commands

| Function | API ID | Priority | Status | Notes |
|----------|--------|----------|--------|-------|
| Get Audio List | 1001 | High | ⭕ | List available audio files |
| Select & Play | 1002 | High | ⭕ | Start playing selected file |
| Pause | 1003 | High | ⭕ | Pause current playback |
| Resume | 1004 | High | ⭕ | Resume paused playback |
| Previous Track | 1005 | Medium | ⭕ | Play previous audio file |
| Next Track | 1006 | Medium | ⭕ | Play next audio file |
| Set Play Mode | 1007 | Medium | ⭕ | Configure playback mode |
| Get Play Mode | 1010 | Medium | ⭕ | Read current play mode |
| Rename File | 1008 | Low | ⭕ | Rename audio file |
| Delete File | 1009 | Low | ⭕ | Delete audio file |

### Audio Upload

| Function | API ID | Priority | Status | Notes |
|----------|--------|----------|--------|-------|
| Upload Audio | 2001 | Medium | ⭕ | Upload new audio file |

### Internal Corpus

| Function | API ID | Priority | Status | Notes |
|----------|--------|----------|--------|-------|
| Start Obstacle Avoidance Audio | 3001 | Medium | ⭕ | Audio feedback for obstacles |
| Exit Obstacle Avoidance Audio | 3002 | Medium | ⭕ | Stop obstacle audio |
| Start Companion Mode Audio | 3003 | Medium | ⭕ | Companion mode sounds |
| Exit Companion Mode Audio | 3004 | Medium | ⭕ | Stop companion sounds |

### Megaphone System

| Function | API ID | Priority | Status | Notes |
|----------|--------|----------|--------|-------|
| Enter Megaphone | 4001 | Medium | ⭕ | Enable megaphone mode |
| Exit Megaphone | 4002 | Medium | ⭕ | Disable megaphone |
| Upload Megaphone Audio | 4003 | Low | ⭕ | Upload megaphone content |

### Long Corpus Playback

| Function | API ID | Priority | Status | Notes |
|----------|--------|----------|--------|-------|
| Select Long Corpus | 5001 | Low | ⭕ | Play extended audio |
| Playback Complete | 5002 | Low | ⭕ | Long playback finished |
| Stop Long Playback | 5003 | Low | ⭕ | Stop extended audio |

---

## 3. 📹 Vision & Video

### Video Streaming

| Topic | Priority | Status | Notes |
|-------|----------|--------|-------|
| rt/api/videohub/request | High | ⭕ | Front camera control |
| Video Data Channel | High | ⭕ | Real-time video stream |

### Video Hub API Tests

| Test | Priority | Status | Notes |
|------|----------|--------|-------|
| Start video stream | High | ⭕ | Begin camera capture |
| Stop video stream | High | ⭕ | End camera capture |
| Change resolution | Medium | ⭕ | Adjust video quality |
| Frame rate control | Medium | ⭕ | FPS configuration |

---

## 4. 🗺️ LIDAR & Mapping

### LIDAR Data Streams

| Topic | Priority | Status | Notes |
|-------|----------|--------|-------|
| rt/utlidar/switch | High | ⭕ | LIDAR on/off control |
| rt/utlidar/voxel_map | High | ⭕ | 3D voxel map data |
| rt/utlidar/voxel_map_compressed | Medium | ⭕ | Compressed voxel data |
| rt/utlidar/lidar_state | High | ⭕ | LIDAR system status |
| rt/utlidar/robot_pose | High | ⭕ | Robot position in map |

### SLAM & Mapping

| Topic | Priority | Status | Notes |
|-------|----------|--------|-------|
| rt/mapping/grid_map | High | ⭕ | 2D occupancy grid |
| rt/uslam/client_command | High | ⭕ | SLAM control commands |
| rt/uslam/frontend/cloud_world_ds | Medium | ⭕ | Downsampled point cloud |
| rt/uslam/frontend/odom | High | ⭕ | SLAM odometry |
| rt/uslam/cloud_map | Medium | ⭕ | Complete map data |
| rt/uslam/server_log | Low | ⭕ | SLAM system logs |

### Localization

| Topic | Priority | Status | Notes |
|-------|----------|--------|-------|
| rt/uslam/localization/odom | High | ⭕ | Localization odometry |
| rt/uslam/localization/cloud_world | Medium | ⭕ | Localization point cloud |

### Navigation

| Topic | Priority | Status | Notes |
|-------|----------|--------|-------|
| rt/uslam/navigation/global_path | High | ⭕ | Path planning output |

### SLAM Qt Interface

| Topic | Priority | Status | Notes |
|-------|----------|--------|-------|
| rt/qt_command | Medium | ⭕ | Qt interface commands |
| rt/qt_add_node | Low | ⭕ | Add graph node |
| rt/qt_add_edge | Low | ⭕ | Add graph edge |
| rt/qt_notice | Low | ⭕ | Qt notifications |
| rt/pctoimage_local | Low | ⭕ | Point cloud to image |

### LIO-SAM Integration

| Topic | Priority | Status | Notes |
|-------|----------|--------|-------|
| rt/lio_sam_ros2/mapping/odometry | Medium | ⭕ | LIO-SAM odometry |

---

## 5. 📊 Sensor Data & State

### Robot State

| Topic | Priority | Status | Notes |
|-------|----------|--------|-------|
| rt/lf/lowstate | High | ⭕ | Low-level robot state |
| rt/multiplestate | High | ⭕ | Multiple state data |
| rt/sportmodestate | High | ⭕ | Sport mode status |
| rt/lf/sportmodestate | High | ⭕ | Low-frequency sport state |
| rt/servicestate | Medium | ⭕ | System service status |

### Positioning & UWB

| Topic | Priority | Status | Notes |
|-------|----------|--------|-------|
| rt/api/uwbswitch/request | Medium | ⭕ | UWB system control |
| rt/uwbstate | Medium | ⭕ | UWB positioning data |

### Environmental Sensors

| Topic | Priority | Status | Notes |
|-------|----------|--------|-------|
| rt/gas_sensor | Medium | ⭕ | Gas sensor readings |
| rt/api/gas_sensor/request | Medium | ⭕ | Gas sensor control |

### System Diagnostics

| Topic | Priority | Status | Notes |
|-------|----------|--------|-------|
| rt/selftest | High | ⭕ | System self-test results |

---

## 6. 🎮 Control & Programming

### Low-Level Control

| Topic | Priority | Status | Notes |
|-------|----------|--------|-------|
| rt/lowcmd | High | ⭕ | Direct motor commands |
| rt/wirelesscontroller | High | ⭕ | Remote controller input |

### Sport Mode Control

| Topic | Priority | Status | Notes |
|-------|----------|--------|-------|
| rt/api/sport/request | High | ⭕ | Sport mode commands |

### Arm Control (if equipped)

| Topic | Priority | Status | Notes |
|-------|----------|--------|-------|
| rt/arm_Command | Medium | ⭕ | Arm movement commands |
| rt/arm_Feedback | Medium | ⭕ | Arm position feedback |

### Programming Interface

| Topic | Priority | Status | Notes |
|-------|----------|--------|-------|
| rt/programming_actuator/command | Low | ⭕ | Custom actuator control |

### System Commands

| Topic | Priority | Status | Notes |
|-------|----------|--------|-------|
| rt/api/bashrunner/request | Low | ⭕ | Execute bash commands |
| rt/api/motion_switcher/request | Medium | ⭕ | Motion mode switching |

---

## 7. 🤖 AI & Voice

### Voice User Interface

| Topic | Priority | Status | Notes |
|-------|----------|--------|-------|
| rt/api/vui/request | High | ⭕ | Voice commands |

#### VUI LED Colors

| Color | Value | Priority | Status | Notes |
|-------|-------|----------|--------|-------|
| White | 'white' | Medium | ⭕ | Default color |
| Red | 'red' | Medium | ⭕ | Alert/error state |
| Yellow | 'yellow' | Medium | ⭕ | Warning state |
| Blue | 'blue' | Medium | ⭕ | Info state |
| Green | 'green' | Medium | ⭕ | Success state |
| Cyan | 'cyan' | Low | ⭕ | Custom state |
| Purple | 'purple' | Low | ⭕ | Custom state |

### AI Features

| Topic | Priority | Status | Notes |
|-------|----------|--------|-------|
| rt/gptflowfeedback | Medium | ⭕ | AI interaction feedback |
| rt/api/assistant_recorder/request | Medium | ⭕ | Voice recording for AI |

### Obstacle Avoidance

| Topic | Priority | Status | Notes |
|-------|----------|--------|-------|
| rt/api/obstacles_avoid/request | High | ⭕ | AI obstacle avoidance |

---

## 8. ⚠️ Error Handling & Diagnostics

### Communication Errors (100 series)

| Error Code | Description | Priority | Status | Notes |
|------------|-------------|----------|--------|-------|
| 100_1 | DDS message timeout | High | ⭕ | Communication issue |
| 100_2 | Distribution switch abnormal | High | ⭕ | Power distribution |
| 100_10 | Battery communication error | High | ⭕ | Battery system |
| 100_20 | Abnormal mote control communication | Medium | ⭕ | Control module |
| 100_40 | MCU communication error | High | ⭕ | Main controller |
| 100_80 | Motor communication error | High | ⭕ | Motor system |

### Fan System Errors (200 series)

| Error Code | Description | Priority | Status | Notes |
|------------|-------------|----------|--------|-------|
| 200_1 | Rear left fan jammed | Medium | ⭕ | Cooling system |
| 200_2 | Rear right fan jammed | Medium | ⭕ | Cooling system |
| 200_4 | Front fan jammed | Medium | ⭕ | Cooling system |

### Motor Errors (300 series)

| Error Code | Description | Priority | Status | Notes |
|------------|-------------|----------|--------|-------|
| 300_1 | Overcurrent | High | ⭕ | Electrical protection |
| 300_2 | Overvoltage | High | ⭕ | Electrical protection |
| 300_4 | Driver overheating | High | ⭕ | Thermal protection |
| 300_8 | Generatrix undervoltage | High | ⭕ | Power supply |
| 300_10 | Winding overheating | High | ⭕ | Motor temperature |
| 300_20 | Encoder abnormal | High | ⭕ | Position feedback |
| 300_100 | Motor communication interruption | High | ⭕ | Communication |

### Sensor Errors (400 series)

| Error Code | Description | Priority | Status | Notes |
|------------|-------------|----------|--------|-------|
| 400_1 | Motor rotate speed abnormal | High | ⭕ | Speed control |
| 400_2 | PointCloud data abnormal | Medium | ⭕ | LIDAR data |
| 400_4 | Serial port data abnormal | Medium | ⭕ | Communication |
| 400_10 | Abnormal dirt index | Low | ⭕ | Environmental |

### UWB Errors (500 series)

| Error Code | Description | Priority | Status | Notes |
|------------|-------------|----------|--------|-------|
| 500_1 | UWB serial port open abnormal | Medium | ⭕ | UWB communication |
| 500_2 | Robot dog information retrieval abnormal | Medium | ⭕ | Data access |

### Protection Systems (600 series)

| Error Code | Description | Priority | Status | Notes |
|------------|-------------|----------|--------|-------|
| 600_4 | Overheating software protection | High | ⭕ | Thermal safety |
| 600_8 | Low battery software protection | High | ⭕ | Power management |

### Wheel Motor Errors

| Error Code | Description | Priority | Status | Notes |
|------------|-------------|----------|--------|-------|
| wheel_300_40 | Calibration Data Abnormality | Medium | ⭕ | Wheel calibration |
| wheel_300_80 | Abnormal Reset | Medium | ⭕ | Wheel system reset |
| wheel_300_100 | Motor Communication Interruption | High | ⭕ | Wheel communication |

---

## 9. 📡 Data Channel Types

### WebRTC Communication

| Type | Purpose | Priority | Status | Notes |
|------|---------|----------|--------|-------|
| validation | Connection validation | High | ⭕ | Initial handshake |
| subscribe | Topic subscription | High | ⭕ | Data stream setup |
| unsubscribe | Topic unsubscription | High | ⭕ | Stop data streams |
| msg | General messages | High | ⭕ | Data communication |
| req | Requests | High | ⭕ | Command sending |
| res | Responses | High | ⭕ | Command acknowledgment |
| vid | Video data | Medium | ⭕ | Video streaming |
| aud | Audio data | Medium | ⭕ | Audio streaming |
| err | Error messages | High | ⭕ | Error handling |
| heartbeat | Connection keepalive | High | ⭕ | Connection monitoring |

### WebRTC Connection Methods

| Method | Description | Priority | Status | Notes |
|--------|-------------|----------|--------|-------|
| LocalAP (1) | Local Access Point | High | ⭕ | Direct WiFi connection |
| LocalSTA (2) | Local Station | High | ⭕ | WiFi network connection |
| Remote (3) | Remote connection | Medium | ⭕ | Internet connection |

---

## Testing Strategy

### Phase 1: Basic Functionality (High Priority)

1. Test basic movement commands (Stand, Move, Stop)
2. Verify state monitoring (LOW_STATE, MULTIPLE_STATE)
3. Test audio playback controls
4. Check video streaming capability
5. Validate LIDAR data streams

### Phase 2: Advanced Features (Medium Priority)

1. Test advanced movement patterns
2. Verify SLAM and mapping functionality
3. Test obstacle avoidance
4. Check UWB positioning
5. Validate voice interface

### Phase 3: Specialized Features (Low Priority)

1. Test acrobatic movements
2. Verify custom programming interfaces
3. Test specialized gaits
4. Check advanced audio features

### Testing Notes

- Update status after each test
- Record any error codes encountered
- Note performance issues or limitations
- Document workarounds for non-functional features
- Keep track of firmware version compatibility

---

## Quick Test Commands

```python
# Basic movement test
robot.sport_cmd(SPORT_CMD["BalanceStand"])
robot.sport_cmd(SPORT_CMD["Move"])
robot.sport_cmd(SPORT_CMD["StopMove"])

# Audio test
robot.audio_cmd(AUDIO_API["GET_AUDIO_LIST"])
robot.audio_cmd(AUDIO_API["SELECT_START_PLAY"])

# State monitoring
robot.subscribe("rt/lf/lowstate")
robot.subscribe("rt/multiplestate")

# Video stream test
robot.subscribe("rt/api/videohub/request")

# Basic movements test (using Sparky Robot class)
from sparky import Robot

async def test_basic_movements():
    robot = Robot()
    await robot.connect()
    
    # Test availability first
    availability = await robot.test_basic_movements()
    print("Available basic movements:", availability)
    
    # Test individual basic movements (safe commands)
    # await robot.damp()            # 🚨 DANGER: BLOCKED - Causes robot leg collapse!
    await robot.balance_stand()     # High priority - standard standing
    await robot.sit()               # Medium priority - sit down
    await robot.rise_sit()          # Medium priority - rise from sitting
    await robot.move_basic(0.2)     # High priority - gentle forward movement
    await robot.command("StopMove") # High priority - emergency stop
    
    await robot.disconnect()

# Advanced movements test (using Sparky Robot class)
async def test_advanced_movements():
    robot = Robot()
    await robot.connect()
    
    # Test availability first
    availability = await robot.test_advanced_movements()
    print("Available advanced movements:", availability)
    
    # Test individual movements (ensure safe environment!)
    await robot.front_jump()      # Medium priority
    await robot.front_pounce()    # Medium priority
    await robot.front_flip()      # Low priority - may not work
    await robot.back_flip()       # Low priority - may not work
    await robot.handstand()       # Low priority - may not work
    
    await robot.disconnect()
```

## Movement Testing Scripts

The following test scripts are available in the `/examples/` directory:

### Basic Movement Testing
1. **`testing/basic_movement_test.py`** - Comprehensive automated testing of all 9 basic movements
2. **`basic_movement_demo.py`** - Interactive demo for testing individual basic movements

### Advanced Movement Testing  
3. **`testing/advanced_movement_test.py`** - Comprehensive automated testing of all advanced movements
4. **`advanced_movement_demo.py`** - Interactive demo for testing individual advanced movements

### General Testing
5. **`testing/motion_test.py`** - General motion testing framework

### Running Movement Tests

```bash
# Basic Movement Testing
python examples/testing/basic_movement_test.py        # Test all 9 basic commands
python examples/basic_movement_demo.py               # Interactive basic movement demo

# Advanced Movement Testing  
python examples/testing/advanced_movement_test.py    # Test all 7 advanced commands
python examples/advanced_movement_demo.py            # Interactive advanced movement demo

# General Testing
python examples/testing/motion_test.py               # General motion testing framework
```

### Safety Guidelines for Advanced Movement Testing

⚠️ **IMPORTANT SAFETY REQUIREMENTS:**

1. **Space Requirements**: Minimum 3m x 3m clear area
2. **Surface**: Use soft mats or grass for landing
3. **Supervision**: Always have a spotter ready
4. **Emergency Stop**: Keep Ctrl+C ready to abort
5. **Recovery**: Allow 5+ seconds between complex movements
6. **Environment**: Test in controlled, safe environment only

### Expected Results by Firmware

Based on current Go2 firmware limitations:

- **Working (Medium Priority)**: FrontJump, FrontPounce
- **Likely Restricted (Low Priority)**: FrontFlip, BackFlip, LeftFlip, RightFlip, Handstand
- **Reason**: Current firmware only supports MCF mode; AI mode (required for complex acrobatics) has been removed

### ✅ **ACTUAL TEST RESULTS** (Updated 2025-08-12)

**Test Configuration:**
- Robot: Go2 
- Firmware Mode: MCF (Manual Control Firmware)
- Connection: Local AP
- Test Script: `advanced_movement_test.py`

**Results Summary:**
- ✅ **Working Commands (3/7)**: FrontJump, FrontPounce, **FrontFlip**
- ❌ **Firmware Limited (4/7)**: BackFlip, LeftFlip, RightFlip, Handstand
- **Error Code**: 3203 - "Command not available in current motion mode"

**Key Findings:**
1. **FrontFlip surprisingly works!** Despite being a "flip" command, it doesn't trigger error 3203
2. **Medium priority commands work as expected** (FrontJump, FrontPounce)
3. **Other flip commands are restricted** - only BackFlip, LeftFlip, RightFlip fail
4. **Handstand is completely blocked** - confirms AI mode dependency

**Recommendations:**
- Focus demos on FrontJump, FrontPounce, and FrontFlip
- Use FrontFlip cautiously - ensure safe landing area
- Consider FrontFlip as your "showcase" acrobatic move
- BackFlip/side flips require firmware update or AI mode restoration

---

*Last updated: [Date]*
*Sparky version: [Version]*
*Go2 firmware: [Version]*
