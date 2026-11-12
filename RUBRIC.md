# Marking rubric — 35 marks

| Part                                                                  | Marks  | Marked how                    |
| --------------------------------------------------------------------- | ------ | ----------------------------- |
| [1. The Cockpit (GUI)](#part-1-the-cockpit-gui--10-marks)             | 10     | From execution and submission |
| [2. The Eyes (CNN)](#part-2-the-eyes-cnn--15-marks)                   | 15     | Live, on the robot's camera   |
| [3. The Hunt (robotic task)](#part-3-the-hunt-robotic-task--10-marks) | 10     | Live, a full run on the robot |
| **Total**                                                             | **35** |                               |

Attendance penalties
(see the [main README](README.md#3-time-attendance-and-what-this-is-worth))
are applied to each person separately, after the work is marked.

Half marks may be given where a criterion is partly met.

**The Lab Demonstrator reserves the right to assign marks according to
individual participation in the event of a noticeably uneven distribution of
labour.**

---

## Part 1: The Cockpit (GUI) — 10 marks

Instructions: [last-can-gui](https://github.com/ccorbett0116/last-can-gui).

| #   | Criterion                       | Marks  | Full marks when                                                                                                                                |
| --- | ------------------------------- | ------ | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | Boxes around recognised objects | 1.5    | Detections from your own model are drawn on the live image, in the right place, and follow the can as it moves                                 |
| 2   | On-screen driving controls      | 1.5    | Forward, back, strafe left, strafe right, rotate left and rotate right all work from the GUI, and the robot stops when the control is released |
| 3   | Arm servo controls              | 1.5    | Every servo in the arm, including the gripper, has its own slider or control, labelled so you can tell which is which                          |
| 4   | Live camera feed                | 1      | The robot's camera is shown live in the GUI                                                                                                    |
| 5   | Keyboard driving                | 1      | The robot can be driven in every direction from the keyboard                                                                                   |
| 6   | Grab and Drop buttons           | 1      | One button starts the grab routine and another starts the drop routine                                                                         |
| 7   | Grab and Drop from the keyboard | 0.5    | Both routines can also be started with a key press                                                                                             |
| 9   | Style and functionality         | 2      | See below                                                                                                                                      |
|     | **Total**                       | **10** |                                                                                                                                                |

**Style and functionality (2 marks).** The "make it pretty" mark covers how
the GUI looks _and_ how well it works as a tool:

| Marks | What it looks like                                                                                                                                                                                                                                                   |
| ----- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 2     | Clear, organised layout. Related controls are grouped and labelled. The GUI shows the robot's state (connected or not, what it's doing). It stays responsive, starts without errors and handles a missing robot gracefully. A new user could operate it without help |
| 1     | It works, but it's cluttered or unlabelled, gives little feedback, or has rough edges such as freezing or errors in the console                                                                                                                                      |
| 0     | The starter's appearance with controls bolted on, or hard to use at all                                                                                                                                                                                              |

**Latency display (requirement 8) is optional** and has no marks of its own. A
working one, with a note on what it measures, counts in your favour in the
style and functionality mark.

---

## Part 2: The Eyes (CNN) — 15 marks

Instructions: [last-can-eyes](https://github.com/ccorbett0116/last-can-eyes).

Tested live, with your model on the robot's camera.

| Criterion                      | Marks  | Full marks when                                                                                                                                                                                                                                 |
| ------------------------------ | ------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Recognises the can             | 5      | A single target can in plain view is detected reliably, with a steady box that fits the can, at the distances the robot works at                                                                                                                |
| Different angles and positions | 4      | It's still detected when turned around, lying on its side, near, far, and toward the edges of the frame                                                                                                                                         |
| Several cans at once           | 3      | Each target can in the frame gets its own box; none are missed or merged                                                                                                                                                                        |
| Rejects the wrong cans         | 1      | Other kinds of Red Bull can, and other objects, get **no** box, while the target can in the same view still does                                                                                                                                |
| Training process               | 2      | You submit a working training script for a YOLO detection model, adapted from the sample or your own, and a `TRAINING_NOTES.md` that states the model, settings, data split, validation results and what you changed after testing on the robot |
| **Total**                      | **15** |                                                                                                                                                                                                                                                 |

For the four accuracy criteria:

| Share of the marks | What it looks like                                                                   |
| ------------------ | ------------------------------------------------------------------------------------ |
| All                | Works nearly every time in the test                                                  |
| About half         | Works in the easy cases and fails in the harder ones, or the box flickers on and off |
| None               | Rarely or never works, or the model wasn't trained by your group                     |

---

## Part 3: The Hunt (robotic task) — 10 marks

Instructions: [last-can-grabber](https://github.com/ccorbett0116/last-can-grabber).

One full run, driven through your own GUI, starting on the floor at the start
point with the can out of view.

| Criterion               | Marks  | Full marks when                                                                                                                     |
| ----------------------- | ------ | ----------------------------------------------------------------------------------------------------------------------------------- |
| Finds the can           | 2      | The driver reaches the can using the GUI, and the model detects it in frame, both while the robot is moving and once it has stopped |
| Grabs the can           | 4      | A press of Grab starts the sequence, the sequence finishes by itself, and the robot ends up holding the can securely                |
| Brings it home          | 1      | The robot is driven back to the start point with the can still in the gripper                                                       |
| Drops the can           | 2      | A press of Drop starts the procedure; the can is released close to the start point and **horizontally**                             |
| Reliability and control | 1      | The run works without restarts or rescues, the arm and wheels move in a controlled way, and nothing is knocked over or strained     |
| **Total**               | **10** |                                                                                                                                     |

**Grabs the can (4 marks)** in more detail:

| Marks | What it looks like                                                                          |
| ----- | ------------------------------------------------------------------------------------------- |
| 4     | The can is picked up cleanly and held securely                                              |
| 3     | Picked up, but the grip is poor (the can slips or tilts badly), or it took a second attempt |
| 2     | The sequence runs and touches or moves the can but doesn't end up holding it                |
| 1     | A grab sequence runs from the button but doesn't reach the can                              |
| 0     | No grab sequence                                                                            |

**Drops the can (2 marks):** 1 mark for a controlled release close to the
start point, 1 mark for the can being released horizontally.

---

## Also required

This carries no marks, but there is nothing to mark without it
(see [What to submit](README.md#6-what-to-submit)):

- One group submission: code, model weights, `HOW_TO_RUN.md`.

---

## Bonus: 1%

There is a short, **anonymous** [feedback form](forms/feedback_form.md) on
Brightspace. If at least **60% of the class** submits it, **everyone gets a 1%
bonus**. A blank form still counts.
