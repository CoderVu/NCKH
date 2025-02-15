# Time Cost Optimization Application

## Overview
The Time Cost Optimization Application is designed to help users optimize project tasks by minimizing time and cost while adhering to specified deadlines. The application utilizes the critical path method to analyze task dependencies and generate visualizations such as Gantt charts.

## Project Structure
```
time-cost-optimization-app
├── src
│   ├── main.py               # Entry point for the application
│   ├── time_cost_optimization.py  # Core logic for optimization
│   └── ui
│       └── app_ui.py        # User interface components using Tkinter
├── requirements.txt          # List of dependencies
└── README.md                 # Documentation for the project
```

## Installation
To set up the project, follow these steps:

1. Clone the repository:
   ```
   git clone <repository-url>
   cd time-cost-optimization-app
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage
To run the application, execute the following command:
```
python src/main.py
```

## Features
- Input handling for task data, durations, costs, and deadlines using a user-friendly Tkinter interface.
- Optimization of task durations and costs based on user-defined deadlines.
- Visualization of task schedules through Gantt charts and diagonal charts.
- Calculation of critical paths and slack times for project management.

## Contributing
Contributions are welcome! Please feel free to submit a pull request or open an issue for any enhancements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.
1. pyinstaller --onefile --name time_cost_optimization main.py
2. Xong stop edit file đó thành 
"# time_cost_optimization.spec
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=['.'],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='time_cost_optimization',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='time_cost_optimization',
)"
3. C:\Users\Admin\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.10_qbz5n2kfra8p0\LocalCache\local-packages\Python310\Scripts\pyinstaller.exe time_cost_optimization.spec#   N C K H  
 