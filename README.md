# Waypoint Generator for Mobile Manipulator Picking Task
> Author: Loh Xin Zhi    
> Email: [lohx0015\@e.ntu.edu.sg](mailto:lohx0015@e.ntu.edu.sg) ; [lxzraizer\@gmail.com](mailto:lxzraizer@gmail.com)  

This repository is part of a Final Year Project in Nanyang Techonological University under the School of Mechanical and Aerospace Engineering in AY 2023/24

---

## Dependencies
Additional Python packages utilize are:
> `shapely` : for set operation with geometery representing the regions  
> `matplotlib` : for visualisation of the geometry results  

To install them, in the terminal:
```
pip install shapely matplotlib
```

## Demo
There are 2 demo code in this repository. Run [`waypoint_demo.py`](./waypoint_demo.py) to see the result of generating the waypoints needed. Alternatively, the [`waypoint_demo.ipynb`](./waypoint_demo.ipynb) Jupyter Notebook shows step by step how each function works to generate the waypoints.

The [`waypoint.py`](./waypoint.py) contains all the custom functions utilised in the demo. 

## Example Results
![image](./images/Example_results.png)
