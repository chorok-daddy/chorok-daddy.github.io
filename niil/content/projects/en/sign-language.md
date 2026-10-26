## Sign-gesture recognition with an ordinary camera

The project developed a CNN-based recognition method that combines nine sampled video frames into a single image. It learns gestures without a separate hand-trajectory extraction step and uses data covering variations in people, clothing, backgrounds and gesture speed.

## Key results

The March 2020 completion report states that all three criteria were met.

| Evaluation item | Criterion met |
|---|---|
| Recognition distance | 5 m |
| Recognition environments | At least 27 |
| Recognition accuracy | 85% |

## Contributions

- **Temporal information in one image:** Combined nine frames to classify gestures without separately extracting hand trajectories.
- **Region and similarity models:** Designed preprocessing networks for gesture-region extraction across distances and similarity networks for distinguishing consecutive gestures.
- **Semi-automatic data generation:** Developed an algorithm to generate varied training data and studied parameter optimization and overfitting reduction.

These results provide a technical foundation for camera-based IoT interaction for people who cannot readily use voice commands.

## Evaluation scope

The figures are **criteria reported as met** in the completion report summary, not exact final measurements. The public summary does not provide the full test conditions. They do not describe unrestricted sign-language translation accuracy or guaranteed commercial IoT performance.

*Source: [NTIS research report](https://www.ntis.go.kr/outcomes/popup/srchTotlRschRpt.do?cmd=view&rstId=REP-2020-01111842337), March 2020, TRKO202100001466, research-results summary, p. 2.*
