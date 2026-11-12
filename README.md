# Final Lab: The Last Can

> _Year 2087. The grid is long gone, and so are the charging docks. The only
> robots still rolling are the ones that learned to run on something else:
> energy drinks. Nobody remembers who taught them. One blue-and-silver can
> keeps a rover alive for another day._
>
> _Your JetRover has just come back online in an abandoned lab. Its reserves
> are nearly empty. Its camera works, but it has no idea what a can looks
> like: so far it has tried to drink a fire extinguisher. Its arm works, but
> it has never picked anything up. And it has no cockpit: nobody can see what
> it sees or tell it where to go._
>
> _You are its crew. Give it eyes, give it hands, give it a cockpit, and bring
> a can home before the lights go out. It will not say thank you. It doesn't
> have a speaker._

That's the story. The assignment underneath it is this: **your group drives a
JetRover to a Red Bull can, the robot picks it up, you drive it back to where
it started, and it puts the can down.** To get there you build three things.

| Part                           | Repository                                                      | What you build                                                                                     | Marks  |
| ------------------------------ | --------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- | ------ |
| **1. The Cockpit** (GUI)       | [last-can-gui](https://github.com/ccorbett0116/last-can-gui)         | A control window: live camera with boxes around detected cans, driving, arm control, Grab and Drop | 10     |
| **2. The Eyes** (CNN)          | [last-can-eyes](https://github.com/ccorbett0116/last-can-eyes)       | A YOLO model, trained by you, that finds Red Bull cans in the robot's camera image                 | 15     |
| **3. The Hunt** (robotic task) | [last-can-grabber](https://github.com/ccorbett0116/last-can-grabber) | The grab and drop routines, and the full run: find, grab, return, drop                             | 10     |
|                                |                                                                 | **Total**                                                                                          | **35** |

The lab is spread over **four repositories**. This one describes the
assignment as a whole: the mission, the rules, the setup and the marking. Each
part then has its own repository with its own instructions and starter file.
The full marking scheme is in [RUBRIC.md](RUBRIC.md), and a summary is in
[How it's marked](#how-its-marked).

**Generative AI is allowed in this lab**, for anything you find it useful
for. See [Generative AI](#generative-ai-is-allowed).

---

## Contents

1. [The mission](#1-the-mission)
2. [What you're given, and what you're not](#2-what-youre-given-and-what-youre-not)
3. [Time, attendance and what this is worth](#3-time-attendance-and-what-this-is-worth)
4. [Working as a crew](#4-working-as-a-crew)
5. [Getting started](#5-getting-started)
6. [What to submit](#6-what-to-submit)
7. [Where everything is](#7-where-everything-is)

---

## 1. The mission

A run goes like this:

1. The robot starts **on the floor at the start point**. The can is somewhere
   **out of the camera's view**.
2. You **drive** the robot with your GUI until it finds the can. Your model
   must recognise the can in the camera image, whether the robot is moving or
   standing still, and your GUI must show it with a box.
3. You press **Grab**. The robot runs its grabbing sequence and ends up holding
   the can.
4. You **drive back** to the start point, by hand, with the can.
5. You press **Drop**. The robot puts the can down. The exact spot doesn't
   matter as long as it is close to the start point and the can is released
   **horizontally** (lying on its side, not standing up).

How the robot grabs is up to you. Be creative: there is more than one way to
do it and none of them is "the" answer.

---

## 2. What you're given, and what you're not

This lab is deliberately bare. You have done the groundwork in the earlier
labs (rosbridge and a teleop GUI in Lab 1, a sense-decide-act loop in Lab 2,
vision in Lab 3) and you are expected to use it.

**You get:**

- `gui_starter.py`, in [last-can-gui](https://github.com/ccorbett0116/last-can-gui):
  a tiny window that connects to the robot, shows the camera, and has one
  working example of a drive button, a key, and a servo slider.
- `train_mnist.py`, in [last-can-eyes](https://github.com/ccorbett0116/last-can-eyes):
  a working YOLO training script, for handwritten digits. Not for cans. It
  comes with a primer for people who have never trained a neural network.
- `arm_pose_example.py`, in [last-can-grabber](https://github.com/ccorbett0116/last-can-grabber):
  how to send the arm a pose, and how to play several in a row.
- [tools/list_topics.py](tools/list_topics.py) and
  [docs/robot_guide.md](docs/robot_guide.md), in this repository: how to find
  out what the robot can do, since nobody is going to hand you a list.
- The **training photos**, as one download (about 360 MB):
  <https://opencloud.colecorbett.ca/s/WrRfxtOfPprYiSj>. The
  [last-can-eyes](https://github.com/ccorbett0116/last-can-eyes) instructions
  say where to unzip them.

**You don't get:** a trained model, training code for cans, a grab routine, or
a finished GUI. Those are the assignment.

---

## 3. Time, attendance and what this is worth

**You have three lab sessions.** That is not much for this amount of work, and
robot time is the scarcest part of it. Anything that doesn't need the robot
(training, most of the GUI) should never be waiting for it: start a training
run on a lab PC's GPU and build something else while it works.

A plan that works:

| Week | By the end of the session                                                                                                                                            |
| ---- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1    | Everyone can connect to the robot. The GUI drives and shows the camera. A first model has been trained, even a bad one. Arm poses for the grab are being worked out. |
| 2    | The three pieces run **together** on one computer. Boxes appear on the live feed. A first full grab works at least sometimes.                                        |
| 3    | Tuning, reliability, full runs, demo.                                                                                                                                |

Put the pieces together in **week 2, not week 3**. Integration always takes
longer than the pieces did.

### Attendance

> **Arriving 15 minutes late or more counts as absent. Each absence or late
> arrival costs you 50% of your grade for this assignment.**

Two of them and your mark for the final lab is zero. The penalty is harsh on
purpose: there are only three sessions, and when you're missing, your group
loses a third of its hands and still has the same robot time.

If you are sick or have another reason to miss a lab, **contact your TA
before the lab**. Staying silent and bringing an explanation to the next
session is not acceptable and won't remove the penalty.

### Weight

This lab is worth **35% of your lab grade**. The lab grade is 25% of your
course grade, so this assignment alone is **8.75% of your final mark**.

### How it's marked

The 35 marks are the group's. [RUBRIC.md](RUBRIC.md) lists every criterion;
this is the shape of it.

| Part                 | Marks | How it's marked                                                                                                                                                                             |
| -------------------- | ----- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1. The Cockpit (GUI) | 10    | Mostly from what you submit: we run your program. 8 marks for features that work (boxes, driving, arm sliders, camera, keyboard, Grab and Drop), 2 for how well it looks and works as a tool |
| 2. The Eyes (CNN)    | 15    | Live, with your model on the robot's camera: 13 marks for what it detects and what it correctly ignores, 2 for your training script and `TRAINING_NOTES.md`                                 |
| 3. The Hunt (task)   | 10    | Live, one full run through your own GUI: find the can, grab it, bring it home, drop it on its side                                                                                          |

Things worth knowing before you plan your time:

- **The model is the biggest part**, and most of its marks are for the hard
  cases: odd angles, several cans at once, and _not_ boxing the wrong can. A
  model that only finds one upright can in the middle of the picture earns
  about a third of Part 2.
- **The grab is the largest single item in Part 3** (4 of 10), and it has
  part marks: a sequence that runs but misses still scores.
- **Half marks exist.** A criterion that is partly met gets part of its marks.
- **Parts 2 and 3 are marked on the robot, in the lab.** What works on your
  PC at home but not on the day doesn't count. Leave time for full runs.
- **Attendance is applied per person, after the group mark**: each absence or
  late arrival halves that person's grade (see above).
- **Individual marks can differ.** The Lab Demonstrator may adjust them if the
  work was noticeably uneven.
- **1% bonus** for the whole class if 60% submit the feedback form
  (see [What to submit](#6-what-to-submit)).

---

## 4. Working as a crew

The lab is designed so the three parts can be built **separately, by different
people, at the same time**, and joined at the end. Suggested split:

| Role            | Part                                                             | Needs the robot?       |
| --------------- | ---------------------------------------------------------------- | ---------------------- |
| Cockpit builder | [last-can-gui](https://github.com/ccorbett0116/last-can-gui)         | Sometimes, for testing |
| Vision trainer  | [last-can-eyes](https://github.com/ccorbett0116/last-can-eyes)       | No, until live testing |
| Arm wrangler    | [last-can-grabber](https://github.com/ccorbett0116/last-can-grabber) | Yes, most of the time  |

With more than three people, double up: the GUI splits well into driving and
arm controls, and the grab and the drop are two separate routines.

**Agree on how the pieces connect in the first session**, before anyone writes
much code: what the GUI calls to start a grab, what the detector returns, what
the files are called. [docs/putting_it_together.md](docs/putting_it_together.md)
covers this, and how to move code between you by **Git, email or USB stick**.
Use whichever suits your group, or anything else (OneDrive, a shared folder).

**Git is not installed on the lab PCs.** You are allowed to install it, but
it doesn't stay installed, so a group that wants Git has to install it at the
start of every session. Git is what industry uses and it's worth learning,
but for three sessions on these PCs **email is likely the more practical
choice**.

### Use your time wisely

Three sessions go quickly, and the usual way to lose one is for the whole
group to stand around one screen while one person types. **Split the work in
the first ten minutes and then actually split up.** Nobody should be waiting:
not for the robot, not for a training run, not for someone else's code.

- Marks follow the work. The Lab Demonstrator may adjust individual marks if
  the labour is noticeably uneven (see [RUBRIC.md](RUBRIC.md)).

### Working and testing on your own

Each part can be built and tested without the other two, and mostly without
the robot.

| Part              | Without the robot                                                                                                                                                                            | With the robot                         |
| ----------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------- |
| **GUI**           | The window, the layout, key handling and the buttons. It should start with the robot off and say it isn't connected. Draw boxes from a stand-in detector that always returns one made-up box | Camera feed, driving, sliders          |
| **Model**         | Training, validation numbers, and running the model on saved photos. Save a few frames from the robot's camera and test on those: they are what the model will really see                    | Live boxes on the feed                 |
| **Grab and drop** | The sequence code itself, with the sending function swapped for one that prints each pose                                                                                                    | Finding the poses, and every real test |

Stand-ins are what make this work: a detector that returns a fixed box, a
grab that prints "grabbing…" and waits three seconds. They are described in
[docs/putting_it_together.md](docs/putting_it_together.md).

**Everyone should be able to run the GUI.** As soon as the GUI builder has a
window that connects and shows the camera, they show the rest of the group
how to start it on their own PC: which folder, which command, where the
robot's address is set. The vision trainer can then watch their own model on
the live feed, and the arm wrangler can use the sliders to find poses, without
borrowing the GUI builder's computer or their time.

### Sharing the robot

You are all in the same room, and **several computers can be connected to the
robot at once**. Both rosbridge and the camera server accept more than one
connection, so each of you can join the robot's Wi-Fi from your own PC when
you need it.

- **Looking is free.** Any number of you can watch the camera or list topics
  at the same time.
- **Moving is not.** The robot obeys every command it receives, from anyone.
  Only one person drives or moves the arm at a time, and they say so out loud
  before they start.
- **Two open GUIs fight each other.** The starter sends a velocity ten times a
  second, including when that velocity is zero. A second copy left open on
  another PC keeps telling the robot to stop while the driver tells it to go.
  If you only want to watch, use the camera page in a browser
  (see [docs/robot_guide.md](docs/robot_guide.md#5-using-the-camera)), or
  close your GUI when it isn't your turn.
- While your PC is on the robot's Wi-Fi it probably has **no internet**. Join
  when you need the robot and leave when you don't.

### Generative AI is allowed

**You may use generative AI in this lab, in whatever way you find useful**:
ChatGPT, Claude, Copilot, Gemini or anything else. Use it to explain ROS, to
write and debug code, to design your GUI, to read an error message, to plan
your training. You don't need to ask permission or declare it.

To get good answers out of it:

- **It doesn't know your robot.** It will invent topic names and message
  fields that look right and aren't. Give it the real ones: paste the output
  of `python tools/list_topics.py` and `ros2 interface show <type>`, and the
  starter function you're extending.
- **It can't see the arm.** A pose it suggests is a guess. Anything that
  moves the robot gets tested slowly and with the space clear, whoever wrote
  it.
- **You are the one who demos it.** When the grab fails in front of your TA,
  you need to know your own code well enough to fix it in a few minutes.

---

## 5. Getting started

All the work is done on the **lab PCs**. They run Windows and have an
**NVIDIA GPU**, which is what makes training take minutes, not hours. The
setup below is in this order for a reason: get it wrong and everything still
runs, only on the CPU and many times slower.

**1. Get the code.** There are four repositories. On GitHub, download the ZIP
of each one (**Code → Download ZIP**): this one, and
[last-can-gui](https://github.com/ccorbett0116/last-can-gui),
[last-can-eyes](https://github.com/ccorbett0116/last-can-eyes) and
[last-can-grabber](https://github.com/ccorbett0116/last-can-grabber).

Unzip this one first. Then unzip the three parts **inside** the folder it
created, and rename them so the layout is:

```
last-can/                  this repository
├── last-can-gui/
├── last-can-eyes/
└── last-can-grabber/
```

(GitHub adds `-main` to the folder names; remove it, or the commands in these
instructions won't match.) Open PowerShell in the `last-can` folder.

The lab PCs don't have Git installed. If you've installed it yourself for
this session, you can clone instead:

```powershell
git clone https://github.com/ccorbett0116/last-can
cd last-can
git clone https://github.com/ccorbett0116/last-can-gui
git clone https://github.com/ccorbett0116/last-can-eyes
git clone https://github.com/ccorbett0116/last-can-grabber
```

One virtual environment, made in the `last-can` folder, serves all three
parts.

**2. Make a virtual environment.**

```powershell
py -m venv .venv
.venv\Scripts\activate
```

Your prompt now starts with `(.venv)`. Activate it again in every new
PowerShell window.

**3. Install PyTorch with CUDA support, before anything else.**

```powershell
pip install torch==2.11.0 torchvision==0.26.0 --index-url https://download.pytorch.org/whl/cu128
```

`pip install torch` on its own gives you a CPU-only build on Windows. The
`--index-url` part is what gets you the build that can use the GPU.

**4. Install the rest.**

```powershell
pip install -r requirements.txt
```

**5. Check that Python can see the GPU.**

```powershell
python -c "import torch; print(torch.cuda.is_available(), torch.cuda.get_device_name(0))"
```

It must print `True` and the name of the graphics card. If it prints `False`,
stop and fix it now: see the top of [requirements.txt](requirements.txt).
Every group member who trains or runs the model does this check on the PC
they use.

Then:

1. Everyone reads [docs/robot_guide.md](docs/robot_guide.md). It's short, and
   it covers robot safety.
2. Turn the robot on, connect to it, and run `python tools/list_topics.py`.
3. Run `python last-can-gui/gui_starter.py`. The status line should turn green
   and the camera should appear.
4. Split up and open your part's README: `last-can-gui/README.md`,
   `last-can-eyes/README.md` or `last-can-grabber/README.md`.

---

## 6. What to submit

**One submission per group**, to the course submission page:

- All of your code for the three parts.
- Your trained model weights (the `.pt` file your GUI loads).
- A short `HOW_TO_RUN.md`: what to install and which command starts your
  program. If we can't run it, we can't mark it.

Leave out the training photos, the `runs/` folders and your virtual
environment.

**The GUI is marked mostly from this submission**, so what you hand in must be
the version that works. The model and the robotic task are marked on the robot.

The Lab Demonstrator reserves the right to assign marks according to
individual participation in the event of a noticeably uneven distribution of
labour.

### Bonus: 1% for feedback

There is a short, **anonymous** feedback form on Brightspace, with three
questions: what you liked, what you didn't like, and any other comments
(see [forms/feedback_form.md](forms/feedback_form.md)). If at least **60% of
the class** submits it, **everyone gets a 1% bonus**. You can submit it blank
and it still counts toward the 60%. There is no penalty if the class falls
short.

---

## 7. Where everything is

**This repository** (the assignment as a whole):

```
last-can/
├── README.md                    this file
├── RUBRIC.md                    how each part is marked (35 marks)
├── requirements.txt             everything the three parts need (after PyTorch)
├── .gitignore                   a starting point, if your group uses Git
├── docs/
│   ├── robot_guide.md           the JetRover and its Jetson Orin: safety, connecting, finding topics
│   └── putting_it_together.md   joining your three parts; sharing by Git, email or USB
├── tools/
│   └── list_topics.py           list or watch the robot's topics from your computer
└── forms/
    └── feedback_form.md         the anonymous Brightspace feedback form (1% bonus)
```

**The three parts** (one repository each, unzipped inside this one):

```
last-can-gui/                    Part 1: The Cockpit
├── README.md                    instructions
└── gui_starter.py               minimal window: connect, camera, one of each control

last-can-eyes/                   Part 2: The Eyes
├── README.md                    instructions
├── PRIMER.md                    what a CNN and a YOLO detector are, from zero
├── FROM_DIGITS_TO_CANS.md       what to change in the sample to train on cans
├── train_mnist.py               sample YOLO training script (digits, not cans)
└── TRAINING_NOTES_template.md   the notes you hand in, with the headings filled in

last-can-grabber/                Part 3: The Hunt
├── README.md                    instructions
└── arm_pose_example.py          send the arm a pose; play a sequence of poses
```

Good luck. The rover is counting on you.
