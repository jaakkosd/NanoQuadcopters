# NanoQuadcopters

NanoQuadcopters is experimental testbed for autonomous flight with nano quadcopters. This repository includes Matlab simulation files and potential field path planning files. Documentation of the project is in doc folder, please read that first.

## Testing the example

Set up the environment by following doc's instructions in section 2.

Clone this repository:

```bash
git clone git@github.com:jaakkosd/NanoQuadcopters.git
```

Navigate to the potentialFieldPathPlanning directory:

```bash
cd NanoQuadcopters/potentialFieldPathPlanning
```

Attach Crazyradio Dongle to the computer.

Check from PFPP.py which CFs are hardcoded to the file and power them on.

Put Crazyflie to the floor. In two CF example I recommend using coordinates approximately (-2,0) and (2,0). There are no restrictions where CFs should be placed, but it is recommended to compare starting points to goal points and simulate the test case with Matlab first.

Run the code:
```bash
python3 PFPP.py
```
