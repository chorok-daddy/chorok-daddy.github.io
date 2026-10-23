## Overview

The system distinguishes known and unknown objects in port CCTV and converts image positions into coordinates for operational systems.

## Results

- Detection/classification rates were approximately 95%/90% in night rain, 95%/95% in daytime rain and 97%/97% in daytime on held-out CCTV footage.
- Tests at designated points in two images yielded a mean position error of 0.1697 m and a maximum of 0.6022 m.
- Reported average processing speed was 20 fps on a desktop and 5 fps on an embedded PC. Outputs included object class, position and time.

## Contributions

Separated object detection from similarity matching. Within the learned domain, reference images extend recognized categories without retraining, while unmatched objects are treated as unknown. Semi-automatic data generation and camera calibration connect detection to location.

## Evaluation scope

Figures apply to the reported CCTV footage and designated points. Reference-image extension was not established for substantially different domains.

*Source: 2020 port unknown-object recognition final report, system evaluation section.*
