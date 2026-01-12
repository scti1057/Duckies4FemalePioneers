# HKA Robogistics DuckieRace: Female Pioneers Workshop

**Maintainers:** Paul Glaser, Tim Schäfer, Felix Wietschel  
**Repository:** `HKA_Robogistics_DuckieRace`

## 📖 Introduction

Welcome to the **Duckies4FemalePioneers** repository! This project is designed for the "Female Pioneers" workshop to introduce students (approx. 14 years old) to the world of robotics, Python programming, and the Robot Operating System (ROS).

The code in this repository runs on **Duckiebots DB21J**, small autonomous vehicles based on the differential drive configuration (similar to Turtlebots). The workshop is divided into progressive challenges that teach the fundamentals of robot perception and control.

## 🛠️ Prerequisites

Before you begin, ensure you have the following hardware and software ready:

### Hardware

* **Duckiebot**: A fully assembled Duckiebot (e.g., DB19, DB21, or J4 model).
* **Development Computer**: A laptop (Linux/Ubuntu recommended, or Windows/macOS with Docker Desktop).

### Software

* **Docker Desktop**: Required to run the containers.
* **Duckietown Shell (dts)**: The command-line interface used to build and run code on the robot.
* **Git**: For version control.

## 📦 Installation

1. **Clone the Repository:**
    Open your terminal and clone this repository to your local workspace:

    ```bash
    git clone https://github.com/scti1057/Duckies4FemalePioneers.git
    cd Duckies4FemalePioneers
    ```

1. **Verify Project Structure:**
    Ensure your directory contains the following key files:
    * `Dockerfile`: Defines the system environment.
    * `packages/`: Contains the source code for the challenges.
    * `dependencies-py3.txt`: Lists Python libraries (e.g., `ultralytics`, `pygame`).
    * `build_run_challenge_1.sh`, `build_run_challenge_2.sh`, etc.: Scripts to launch the challenges.

## 🚀 Usage & Challenges

The workshop is structured into specific challenges. You will modify the Python files in the `src` folders to complete the tasks.

### Challenge 1: Remote Control

**Goal:** Learn how to control the robot's motors using keyboard inputs.

* **File to Edit:** `packages/challenge_1/src/crtl_arrow_keys.py`
* **Tasks:**
    1. Implement logic for driving forward and backward (Up/Down keys).
    2. Implement logic for turning left and right.
    3. Implement speed control logic.

### Challenge 2: Geometric Patterns & Safety

**Goal:** Program the robot to drive autonomously in patterns and stop for obstacles.

* **File to Edit:** `packages/challenge_2/src/HardCodedDriveNode.py`
* **Tasks:**
    1. **Driving Logic:** Use `Twist2DStamped` messages and `time.sleep()` to make the robot drive in specific shapes (e.g., a square).
    2. **Emergency Stop:** Use data from the Time-of-Flight (ToF) sensor to set velocity to 0 if an obstacle is too close.

### Challenge 3: Lane Following (Advanced)

**Goal:** Use the camera to detect lanes and drive autonomously.

* **File to Edit:** (Refer to instructor guidelines for Challenge 3 specific files).
* **Context:** This utilizes the `followlane` package and may involve calibration.

---

## 💻 Building and Running the Code

We use the Duckietown Shell (`dts`) to build a Docker container and run it on the robot.
Additionaly we provide convenient shell scripts (`build_run_challenge_x.sh`) to automate the building and running process.

### 1. Configure Your Robot Name

Before running any script, you must update it to target your specific Duckiebot.

1. Open the `.sh` file corresponding to the challenge you want to run (e.g., `build_run_challenge_1.sh`) in a text editor.
2. Locate the command line starting with `dts devel run`.
3. Replace `gustav` with the hostname of your Duckiebot.
    * *Example:* Change `-R gustav` to `-R my-duckiebot-db21`.

**File Content Example (`build_run_challenge_1.sh`):**

```bash
#!/bin/bash
dts devel build -f
dts devel run -X -R gustav -L challenge_1  # <--- CHANGE "gustav" HERE
```

*[Source: ```build_run_challenge_1.sh```]*

*(Note: If you get a "Permission denied" error, run chmod +x build_run_challenge_*.sh to make the scripts executable.)*

### 2. Run a Challenge

Execute the script for the desired challenge from your terminal.

#### To run Challenge 1

```bash
# Uses launcher 'challenge_1'
./build_run_challenge_1.sh
```

#### To run Challenge 2

```bash
# Uses launcher 'challenge_2'
./build_run_challenge_2.sh
```

#### To run Challenge 3

```bash
# Uses launcher 'challenge_3'
./build_run_challenge_3.sh
```

### ℹ️ What do these scripts do?

These scripts perform two main actions automatically:

**Build (**```dts devel build -f```**):** Compiles your code and rebuilds the Docker container to ensure your latest changes are included.

**Run (**```dts devel run ...```**):** Launches the container on your robot with specific configurations:

* ```-X```: Enables **X11 forwarding**, allowing you to see graphical windows (like camera streams or plots) from the robot on your computer.

* ```-L challenge_x```: Selects the specific **launcher** file for that challenge, ensuring the correct nodes start.

## 🧹 Troubleshooting

* **"Container already running" errors:** If you cannot start a new program because a previous one is still active, use the cleanup script:

    ```bash
    ./docker_cleanup.sh
    ```

* **Missing Dependencies:** If you see import errors, ensure dependencies-py3.txt is up to date and rebuild using dts devel build -f.

## 📄 License

This project includes a LICENSE file (see LICENSE.pdf). Please refer to it for usage rights.
