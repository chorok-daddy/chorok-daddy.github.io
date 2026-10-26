## Overview

The project combines cargo shape, position, barcode and damage recognition. Two related 2022 contracts cover a recognition prototype and a learning database.

## Contributions

- Combined RGB cameras and LiDAR to process image and three-dimensional volume information.
- Connected outputs to cargo-loading decision systems through defined interfaces.
- The related database report documents point-cloud acquisition and visualization of occupied and unoccupied container space.

## Results

| Measure | Formal test result in the 2022 report | Conditions |
|---|---|---|
| Position and volume | mIoU 0.867 | Ten unseen normal cargo types, ten repetitions each |
| Classification and barcode | 100% joint success | Both functions had to succeed |
| Damage recognition | 94% success | Two groups with normal and damaged cargo, 100 trials |

Results were tracked through per-trial logs. These figures apply to the reported test conditions.

*Source: 2022 cargo-recognition prototype final report, chapter 5. Results from the separate 2021 report are not combined.*
