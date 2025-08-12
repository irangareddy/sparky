# Go2 Firmware Update Notes

##  Important Changes in Recent Firmware Update

### What Changed

The Go2 robot firmware has been updated, and this has significantly impacted the available motion control capabilities.

### Motion Mode Changes

#### Before (Legacy Firmware):
- **normal**: Basic motion mode with standard movements
- **ai**: Advanced mode with access to flips, handstands, and complex movements
- **mcf**: Manual Control Firmware mode

#### After (Current Firmware):
- **mcf**: Only available mode (Manual Control Firmware)
- ~~normal~~: **REMOVED** - No longer available
- ~~ai~~: **REMOVED** - No longer available

### Impact on Commands

####  Commands That Still Work:
- All basic movement commands (Move, StopMove)
- Core sport commands:
  - Hello
  - Sit
  - StandUp
  - Dance1, Dance2
  - Stretch
  - BalanceStand
  - RecoveryStand
  - Euler
  - SwitchGait
  - BodyHeight
  - FootRaiseHeight
  - SpeedLevel

####  Commands That May Not Work:
- Advanced commands that previously required "ai" mode:
  - Handstand (StandOut)
  - BackFlip, FrontFlip, LeftFlip, RightFlip
  - FrontJump, FrontPounce
  - Some other advanced stunt commands

### Error Codes

When trying to use unavailable features, you may encounter these error codes:

- **7004**: Motion mode switching restriction (normal/ai not available)
- **7002**: AI mode not available in current firmware
- **3203**: Command not available in current motion mode

### Sparky Package Updates

The Sparky package has been updated to:

1. **Document these changes** in all relevant files
2. **Provide clear warnings** when trying to use unavailable features
3. **Include firmware compatibility information** in the API
4. **Focus on working features** while documenting limitations

### Testing Your Robot

To test what works with your current firmware:

```bash
# Run the firmware compatibility test
poetry run python src/sparky/examples/firmware_compatibility_test.py
```

### Recommendations

1. **Start with basic movements** - These work reliably
2. **Test sport commands individually** - Some may work, others may not
3. **Don't try to switch motion modes** - Only "mcf" is available
4. **Check error codes** - Use the documented error codes for troubleshooting
5. **Focus on core functionality** - Basic movements and common sport commands

### Future Updates

If Go2 releases new firmware that restores these features, the Sparky package can be updated accordingly. The current implementation is designed to be forward-compatible while clearly documenting current limitations.

### Getting Help

If you encounter issues:

1. Run the firmware compatibility test
2. Check the error codes against this documentation
3. Test basic movements first
4. Open an issue on GitHub with specific error codes and commands that failed
