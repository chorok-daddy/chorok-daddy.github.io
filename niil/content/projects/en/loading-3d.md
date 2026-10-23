## Overview

An RGB-D loading-assistance system recognizes goods and loading space alongside nearby workers, connecting perception to ROS-based logistics robot control.

## Results

| Measure | 2018 report | Scope |
|---|---|---|
| Goods recognition | 97.5% accuracy | Color/depth ensemble model |
| Worker recognition | 98.3% success | Four failures in 238 frames from approximately five minutes of video |
| Worker position | Approximately 3–4 cm error | Reported measurement examples |
| Integration | RGB 30 fps; depth 90 fps | Operation in a ROS environment |

## Contributions

Calculated placement position and orientation from goods geometry and free space, incorporated worker detection and localization, and integrated the algorithms into a working ROS system.

## Evaluation scope

Results apply to the report's limited tests. Worker recognition is a per-frame measure, not per-person accuracy. Initial dimensional requirements are distinguished from the final goods/worker recognition results.

*Source: December 2018 3D loading-assistance final report, chapter 4.*
