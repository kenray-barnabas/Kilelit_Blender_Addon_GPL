Kilelit Blender Add-on. 

Kilel means Picture in my native tongue, Pohnapeian. Pronounced "gil-el". The "it" is added English. Ki for short.

Ki is a rendering tool that helps automate the rendering workflow while also offering some strong features for ease of work. 
The add-on also includes all the rendering features available in one area for easy access. In the thought of helping artist speed up their workflow. 

The first panel of this add-on is where alot of the automation is happening, and also Ki's biggest solutions. 
From Render History, History navigation, render complete sound notification, and rendering selected only.
The rest of the add-on are focused to place things in one area, which comes in handy when working in the viewport alone. 

To install the Ki, simply go to the preferences in Blender, add-ons, and install from disk the zip file.

I hope you guys find this tool useful! Happy Blendering!


# Kilelit Add-on — Beginner Friendly Guide

## What is Kilelit?
Kilelit is a Blender add-on designed to **speed up rendering workflows**, **simplify common render tasks**, and **centralize useful render controls** into clean, accessible panels.  
It is especially useful for **artists, beginners, and technical artists** who want faster iteration without digging through Blender’s deep render menus.

---

## Where to Find Kilelit
**Properties Panel → Render Tab**

You will see several collapsible Kilelit panels:
- Render
- Render Settings
- Render Passes
- Material Override
- Render Visibility
- Render Output
- Kilelit Info

---

## Render Panel

### Purpose
Quick access to rendering actions and common toggles.

### Key Features
- **Render Engine Selector** (EEVEE / Cycles)
- **Render Button** – start renders instantly
- **Render History**
  - Save renders automatically
  - Open render history folder
- **Render Modes**
  - Still
  - Animation
  - Transparent
  - Selected Only
- **Viewport Render**
- **Fast GI Approximation Toggle**



---

## Render Settings

### Purpose
Control quality vs performance without hunting through Blender menus.

### Sections Explained
**Sampling**
- Render samples
- Viewport samples
- Noise threshold
- Denoising (Optix / OpenImageDenoise)

**Performance**
- Threads (auto/manual)
- Memory handling
- Tiling & acceleration
- Persistent data

**Lighting & Light Paths**
- Fast GI Approximation
- AO distance & factor

👉 *Beginner Tip:*  
Start with lower samples and enable denoising for fast previews.


---

## Render Passes

### Purpose
Enable passes for compositing and post-production.

### Pass Categories
**Data**
- Depth
- Normal
- UV
- Object Index

**Light**
- Diffuse
- Glossy
- Transmission
- Volume
- Emission
- Shadow
- AO

**Cryptomatte**
- Object
- Material
- Asset
- Adjustable accuracy levels

Remember: enabling more passes increases render time and file size.


---

## Material Override

### Purpose
Quickly override all materials in the scene.

### Common Uses
- Clay renders
- Lighting tests
- Lookdev

### Features
- Toggle override on/off
- Create Clay Render Material
- Custom material assignment
- Sample override control



---

## Render Visibility

### Purpose
Fine control over how selected objects appear in renders.

### Controls
- Show / Hide in Render
- Shadow Catcher
- Holdout

**Visibility Toggles**
- Camera
- Diffuse
- Glossy
- Transmission
- Volume Scatter
- Shadow

**Culling**
- Camera Cull
- Distance Cull



---

## Render Output

### Purpose
Centralized output and color management.

### Key Controls
- Resolution presets
- Output path
- Image format (PNG, JPG, EXR)
- Color mode (RGB / RGBA)
- Bit depth
- Compression

**Color Management**
- View Transform
- Exposure
- Gamma
- Curves



---

## Kilelit Info

### Displays
- Add-on name
- Author
- Version

### Quick Links
- KB Space Portals
- 3D Portfolio


---

## Who Is Kilelit For?
- Beginners learning Blender rendering
- Artists wanting faster workflows
- Lookdev & lighting artists
- Technical artists building pipelines

---

## Beginner Workflow Example
1. Choose render engine in **Render**
2. Adjust quality in **Render Settings**
3. Enable passes in **Render Passes**
4. Use **Material Override** for lighting tests
5. Set resolution & output in **Render Output**
6. Render!

---

## Notes
- Kilelit does **not replace Blender settings**
- It provides **faster access and automation**
- All changes remain fully compatible with Blender

---

Kenray Barnabas — Kilelit Add-on
