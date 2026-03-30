# InMoov Robot Research & Analysis for 3D Visualization Integration

## 📋 What is InMoov?

**InMoov** is an **open-source, life-size 3D printed humanoid robot** created by French designer **Gael Langevin** in 2012.

### Key Characteristics:
- **First fully 3D-printed, open-source humanoid robot**
- **Fully replicable** - Anyone with a 3D printer can build one
- **Modular design** - Build parts independently (hand, arm, torso, head, etc.)
- **3D Printer Requirements**: Minimum 12×12×12 cm (about 5"×5"×5") build area
- **Materials**: ABS or PLA plastic via FDM 3D printing
- **Control**: Arduino + MyRobotLab software
- **Global Community**: Thousands of builders worldwide

---

## 🦾 Robot Structure & Joints

### Hand & Forearm
```
HAND (5 fingers + thumb)
├─ Thumb (1 servo controlled)
├─ Index (1 servo controlled)
├─ Middle/Majeure (1 servo controlled)
├─ Ring/RingFinger (1 servo controlled)
└─ Pinky/Auriculaire (1 servo controlled)

FOREARM
├─ Wrist Rotation (1 servo, motorized)
├─ Wrist Flex (tendons via hand servos)
└─ Servo Bed (houses 6 servos for finger actuation)
```

### Arm Structure
```
ARM (Left & Right)
├─ Shoulder (2-3 DOF)
├─ Bicep (elbow rotation)
├─ Forearm
├─ Wrist
└─ Hand

Total Joints per Arm:
- Hand: 5 fingers + thumb = 5 servos
- Wrist: 1 servo (rotation)
- Elbow: 1 servo (flex)
- Shoulder: 2-3 servos (pan, lift)
= ~8-9 servos per arm
```

### Full Robot Structure
```
HEAD
├─ Neck Pan (1 servo)
├─ Neck Tilt/Lift (1 servo)
├─ Eyes (2 servos for gaze)
├─ Jaw (optional, 1 servo)
└─ Head Rotation (1 servo)

TORSO
├─ Left Arm (8-9 servos)
├─ Right Arm (8-9 servos)
├─ Head (5-6 servos)
├─ Chest/Spine (optional)
└─ Waist (optional)

Total: ~20-30 servos for full humanoid
```

---

## 🔧 Technical Specifications

### Servo Motors
**Recommended Models:**
- **HK15298B** (12kg torque, 90° limited - most common)
- **MG996R** (13kg torque, 180° full range)
- **HS805BB** (14kg torque, high quality)
- **Not Recommended**: SG90 (too weak - only 1.8kg torque)

**Why High Torque?**
- Tendons run 8cm+ from servo to fingers
- Friction loss through wrist rotation
- Multiple joints in series reduce effective force
- Rule: Minimum 12kg torque for hand/arm

### Control Electronics
```
PER ARM HAND:
├─ Arduino Uno (for single hand)
└─ 6-7 servo connections

PER FULL ARM + HEAD:
├─ Arduino Mega (more pins)
└─ Nervo Board (servo driver shield)

FULL ROBOT:
├─ 2× Arduino Mega (left + right body sides)
├─ 2× Nervo Boards
├─ Power Supply: 6V-12V at 20-30A
└─ Software: MyRobotLab (Python-based)
```

### Actuation Method
**Tendon-Driven System:**
- Braided fishing line (200lb test) acts as tendons
- Servo rotation pulls tendons to flex fingers
- Springs provide tension relief during wrist rotation
- Similar to biological muscle-tendon system

---

## 📐 Key Dimensions

### Hand
- **Palm Width**: ~8 cm
- **Finger Length**: ~10 cm each
- **Total Hand Volume**: 15×10×8 cm
- **Weight**: ~750g (with servos)

### Arm Assembly
- **Forearm Length**: ~15 cm
- **Bicep Length**: ~20 cm
- **Total Arm Length**: ~40-50 cm
- **Total Weight**: 2-3 kg per arm

### Full Robot (Life-Size)
- **Height**: 170 cm (~5'7")
- **Arm Span**: 150+ cm
- **Total Weight**: 15-20 kg with all components
- **Comparison**: Roughly torso-like, not full legs

---

## 🎯 What You Need to Change for Your AXEL → InMoov Visualization

### Major Changes Required:

#### 1. **Joint Configuration**
**AXEL (Your Current Model):**
- 7 main joints (head_pan, head_tilt, shoulder_pan, shoulder_lift, elbow, wrist_1, hand)

**InMoov (Required):**
- **Head**: 2 joints (pan, tilt) ✓ Same as AXEL
- **Right Shoulder**: 2 joints (pan, lift)
- **Right Elbow**: 1 joint (flex)
- **Right Wrist**: 1 joint (rotation)
- **Right Hand**: 5 fingers independently controlled
- **Left Arm**: Same as right (10 more joints)
- **Total**: 20-25 joints for full system

#### 2. **Hand Visualization**
**Add Individual Finger Control:**
```python
# Current AXEL visualization has simple gripper
# InMoov needs individual finger joints:

fingers = {
    'thumb': {
        'base': (x1, y1, z1),
        'middle': (x2, y2, z2),
        'tip': (x3, y3, z3),
        'servo_angle': angle  # 0=open, 180=closed
    },
    'index': {...},
    'middle': {...},
    'ring': {...},
    'pinky': {...}
}
```

#### 3. **New Arm Segments**
```
Current AXEL:
├─ Torso (fixed)
├─ Head
└─ Right Arm (single segment)

InMoov Needed:
├─ Torso
├─ Head
├─ Right Shoulder
├─ Right Bicep
├─ Right Forearm
├─ Right Wrist
├─ Right Hand (with 5 fingers)
└─ Left Side (duplicate)
```

#### 4. **Kinematics Model Update**
**Current AXEL Code:**
```python
# Forward kinematics uses simplified 7-joint model
def compute_forward_kinematics(self):
    # Base → Torso → Head, Shoulder → Elbow → Wrist
```

**InMoov Changes:**
```python
# Much more complex kinematic chain
def compute_forward_kinematics(self):
    # Base → Torso
    #   ├─ Head: pan(neck) → tilt(neck) → head_position
    #   ├─ Left Arm (same chain below)
    #   └─ Right Arm:
    #       ├─ Shoulder: pan + lift → shoulder_pos
    #       ├─ Bicep: elbow angle → elbow_pos
    #       ├─ Forearm: length_segment
    #       ├─ Wrist: rotation_angle → wrist_pos
    #       └─ Hand:
    #           ├─ Thumb: 2 DOF + open/close
    #           ├─ Index: base_pos + bend angles
    #           ├─ Middle: base_pos + bend angles
    #           ├─ Ring: base_pos + bend angles
    #           └─ Pinky: base_pos + bend angles
```

#### 5. **Configuration File Updates**
```yaml
# Current robot_config.yaml structure for AXEL:
joints:
  head_pan: {min: -1.57, max: 1.57}
  head_tilt: {min: -0.79, max: 0.79}
  shoulder_pan: {min: -3.14, max: 3.14}
  # ... 7 joints total

# InMoov structure:
joints:
  head_pan: {min: -1.57, max: 1.57}
  head_tilt: {min: -0.79, max: 0.79}
  right_shoulder_pan: {min: -1.57, max: 1.57}
  right_shoulder_lift: {min: -1.57, max: 1.57}
  right_elbow: {min: 0, max: 3.14}
  right_wrist: {min: -1.57, max: 1.57}
  right_thumb: {min: 0, max: 3.14}
  right_index: {min: 0, max: 3.14}
  right_middle: {min: 0, max: 3.14}
  right_ring: {min: 0, max: 3.14}
  right_pinky: {min: 0, max: 3.14}
  # ... same for left arm
  # = 16 joints minimum
```

#### 6. **UI Control Panel Changes**
**Current (7 sliders):**
```
Control Panel
├─ Head Pan: ___________
├─ Head Tilt: __________
├─ Shoulder Pan: _______
├─ Shoulder Lift: ______
├─ Elbow: ______________
├─ Wrist: ______________
└─ Hand: _______________
```

**InMoov (16+ sliders):**
```
Control Panel (Left & Right Tabs)
LEFT ARM TAB:
├─ Shoulder Pan: ___
├─ Shoulder Lift: __
├─ Elbow: _________
├─ Wrist: _________
└─ Hand:
    ├─ Thumb: _____
    ├─ Index: _____
    ├─ Middle: ____
    ├─ Ring: ______
    └─ Pinky: _____

RIGHT ARM TAB:
[Same as left]

HEAD TAB:
├─ Pan: ___________
└─ Tilt: __________
```

---

## 🎨 3D Visualization Changes Needed

### 1. **Link Representation**
**Current AXEL visualization:**
```python
# 7 joint spheres (red) + links (blue lines)
# Simple tree structure

links = {
    'base': (0, 0, 0),
    'torso': (0, 0.5, 0),
    'head': (0, 1, 0),
    'shoulder_r': (0.2, 0.8, 0),
    'elbow_r': (0.2, 0.5, 0),
    'wrist_r': (0.2, 0.1, 0),
    'hand_r': (0.2, 0, 0)
}
```

**InMoov visualization:**
```python
# 20+ joints + separate finger rendering

# Arm chain (right side, left similar):
links = {
    'base': (0, 0, 0),
    'torso': (0, 0.5, 0),
    'head': (0, 1.0, 0),
    
    # Right arm chain
    'shoulder_r': (0.15, 0.8, 0),
    'bicep_r': (0.15, 0.6, 0),
    'elbow_r': (0.15, 0.4, 0),
    'forearm_r': (0.15, 0.2, 0),
    'wrist_r': (0.15, 0.0, 0),
    
    # Right hand fingers (complex)
    'hand_r': (0.15, -0.05, 0),
    'thumb_base': (0.12, -0.08, 0),
    'thumb_mid': (0.10, -0.12, 0),
    'thumb_tip': (0.08, -0.15, 0),
    
    'index_base': (0.15, -0.08, 0.02),
    'index_mid': (0.15, -0.12, 0.02),
    'index_tip': (0.15, -0.16, 0.02),
    # ... similar for middle, ring, pinky
}
```

### 2. **Color Coding**
**Suggest:**
- **Green**: Base/torso (fixed segments)
- **Blue**: Arm links (shoulder, bicep, forearm)
- **Red**: Joints (servo positions)
- **Yellow**: Fingers (for visibility)
- **Gray**: Ground plane

### 3. **Multiple Views**
**Add rendering options:**
- Front view (frontal plane - arms spread left/right)
- Side view (sagittal plane - arms forward/back)
- Top view (arms overhead)
- 3D isometric (current)

### 4. **Joint Constraints Visualization**
**Show limits with colored zones:**
```python
# Elbow: 0-180°
# If elbow_angle > 150°: highlight in yellow (near limit)
# If elbow_angle > 170°: highlight in red (dangerous)
```

---

## 📊 Configuration File Structure Example

```yaml
robot_name: InMoov
type: humanoid
total_joints: 16

# Head section
head:
  pan:
    joint_name: head_pan
    servo: HS805BB
    min_angle: -90.0
    max_angle: 90.0
    default: 0.0
  tilt:
    joint_name: head_tilt
    servo: HS805BB
    min_angle: -30.0
    max_angle: 30.0
    default: 0.0

# Right arm section
right_arm:
  shoulder:
    pan:
      joint_name: right_shoulder_pan
      servo: MG996R
      min_angle: -90.0
      max_angle: 90.0
    lift:
      joint_name: right_shoulder_lift
      servo: MG996R
      min_angle: -45.0
      max_angle: 135.0
      
  elbow:
    joint_name: right_elbow
    servo: HK15298B
    min_angle: 0.0
    max_angle: 180.0
    
  wrist:
    joint_name: right_wrist
    servo: HK15298B
    min_angle: -90.0
    max_angle: 90.0
    
  hand:
    thumb:
      joint_name: right_thumb
      servo: HK15298B
      min_angle: 0.0
      max_angle: 180.0
    index:
      joint_name: right_index
      servo: HK15298B
      min_angle: 0.0
      max_angle: 180.0
    # ... middle, ring, pinky

# Left arm (mirror of right)
left_arm: {...}

# Link dimensions for kinematics
dimensions:
  shoulder_to_elbow: 20  # cm
  elbow_to_wrist: 15     # cm
  wrist_to_hand: 8       # cm
  hand_length: 10        # cm
  finger_length: 10      # cm
```

---

## 🔄 Implementation Roadmap

### Phase 1: Core Structure (1-2 days)
- [ ] Update robot_config.yaml with 16+ joints
- [ ] Add left arm support (mirror right arm)
- [ ] Expand StateManager to track all joints

### Phase 2: Visualization (2-3 days)
- [ ] Redesign RobotVisualizer3D with full arm chains
- [ ] Add finger joint visualization
- [ ] Implement multiple viewing angles
- [ ] Add joint limit indicators

### Phase 3: Control Panel (1-2 days)
- [ ] Create tabbed interface (Head, Right Arm, Left Arm)
- [ ] Add 5 finger sliders per hand
- [ ] Update save/load position system

### Phase 4: Testing (1 day)
- [ ] Full kinematics validation
- [ ] Visualization accuracy tests
- [ ] UI responsiveness checks

---

## 💡 Key Takeaways for Integration

**Complexity Increase:**
- AXEL: 7 joints → InMoov: 16-20 joints
- AXEL: 1 simple arm → InMoov: 2 complex arms + 5 finger per hand
- AXEL: Simple kinematics → InMoov: Complex tendon-driven hand model

**Benefits of InMoov for Your Project:**
- ✅ Well-documented open-source design
- ✅ Proven 3D-printable components
- ✅ Active community with solutions
- ✅ Modular design (can build incrementally)
- ✅ Realistic humanoid proportions

**Visualization Advantages:**
- Show individual finger movements
- Demonstrate tendon-driven mechanism
- Educational value for students
- Professional appearance for presentations

---

## 🌐 Resources

- **Official Website**: https://inmoov.fr/
- **STL Files**: https://inmoov.fr/inmoov-stl-parts-viewer/
- **Hardware Map**: http://inmoov.fr/default-hardware-map/
- **MyRobotLab**: http://myrobotlab.org/
- **Community Forum**: https://inmoov.fr/community-v2/
- **Thingiverse Derivatives**: http://www.thingiverse.com/Gael_Langevin/collections/inmoov-parts-and-derivatives

---

## ✅ Recommendation

**For your software project:**

I recommend **starting with AXEL** as it is, then **optionally adding InMoov support** as a second "robot configuration" option. This way:

1. Your AXEL control software remains simple and working
2. Users can switch between AXEL and InMoov in a dropdown
3. Different visualization modes for each robot type
4. Future extensibility for other humanoid robots

**File Structure:**
```
axel_robot_software/
├── config/
│   ├── robot_config.yaml          # Default AXEL
│   ├── inmoov_config.yaml        # NEW: InMoov config
│   └── other_robots_config/       # Extensible
├── axel_core/
│   ├── robot_models/
│   │   ├── axel_kinematics.py
│   │   └── inmoov_kinematics.py  # NEW
└── ...
```

This is a **professional, scalable approach** used in industry robot software!

