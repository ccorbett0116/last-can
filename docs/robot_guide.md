# Robot guide: the JetRover and its Jetson Orin

Everyone in the group should read sections 1 to 3. Sections 4 to 8 are the
reference you'll come back to.

1. [Meet the robot](#1-meet-the-robot)
2. [Safety and care](#2-safety-and-care)
3. [Connecting](#3-connecting)
4. [Finding out what the robot can do: topics](#4-finding-out-what-the-robot-can-do-topics)
   (including [the arm's servos](#the-arm-finding-and-learning-the-servos))
5. [Using the camera](#5-using-the-camera)
6. [Writing code that uses the robot](#6-writing-code-that-uses-the-robot)
7. [The Jetson Orin](#7-the-jetson-orin)
8. [Troubleshooting](#8-troubleshooting)

---

## 1. Meet the robot

The **JetRover** is a bigger relative of the TurboPi from the earlier labs.

| Part     | What it is                                                       | Compared with the TurboPi                                |
| -------- | ---------------------------------------------------------------- | -------------------------------------------------------- |
| Computer | **NVIDIA Jetson Orin**, running Linux and ROS 2                  | Much more powerful than the Raspberry Pi, and has a GPU  |
| Wheels   | Four **mecanum** wheels: forward/back, strafe, rotate            | Same idea, same `Twist` message                          |
| Arm      | Several **bus servos** in a chain, with a **gripper** at the end | New. The TurboPi had two small PWM servos for the camera |
| Camera   | A depth camera with an ordinary colour image                     | You use the colour image                                 |

Two things work differently from the TurboPi's servos:

- **Bus servos take a position from 0 to 1000**, not a pulse width in
  microseconds. 500 is roughly the middle of the servo's travel.
- **Every servo has an ID number**, and one message can move several servos
  at once. The message also carries a `duration`: how many seconds the servos
  get to reach the new position.

Which IDs exist, which joint each one is, and how far each can safely travel
is for you to find out. [Section 4](#the-arm-finding-and-learning-the-servos)
shows you how.

---

## 2. Safety and care

The robot is heavy, the arm is strong, and every group shares the same
robots. Look after it.

**Before the wheels turn**

- The first time you test anything that drives, put the robot **on a stand or
  box so the wheels are off the ground**.
- Keep speeds low (0.1 to 0.2 m/s) until you trust your code.
- Run it on the floor, never on a table.
- Every program that drives must have a **stop** that always works, and must
  stop the robot when it closes. A robot keeps doing what the last `/cmd_vel`
  message told it.

**Before the arm moves**

- Clear the space around it. Keep hands, faces, cables and laptops out of reach.
- Move **one servo at a time, slowly** (a `duration` of 1 to 2 seconds) until
  you know which way each one goes and where it stops.
- **Never leave a servo pushing against something** it can't move: the
  chassis, the floor, its own limit, a can it is crushing. A stalled servo
  overheats within seconds and can burn out. If a servo is buzzing or getting
  hot, back it off immediately.
- Don't move the arm by hand while it's powered. Don't lift the robot by the arm.

**Power**

- Keep the robot plugged in unless you are actively moving it: battery life is limited.

**The software on the robot belongs to everyone**

- Don't update, upgrade or uninstall anything on the Jetson, and don't edit
  the robot's own files. If you think something on the robot needs changing,
  ask your TA.
- If you put your own files on the robot, keep them in one folder named after
  your group, and take them off when you're done.

---

## 3. Connecting

Your programs run on a lab PC and reach the robot over Wi-Fi,
the same as in the earlier labs.

1. Turn the robot on and give it a minute or two to boot.
2. Connect your computer to the **robot's Wi-Fi network**. The network name (SSID) is shown on the robot's faceplate once it has started, and each robot has its own. The password is `hiwonder`.
3. Check you can reach it:

   ```bash
   ping 192.168.149.1
   ```

   `192.168.149.1` is the usual address when you're on the robot's own Wi-Fi.
   If your TA gives you a different one, change `ROBOT_IP` at the top of each
   script you run.

4. Check the two services your GUI depends on:

   | Service                          | Port | Quick test                                                                                                          |
   | -------------------------------- | ---- | ------------------------------------------------------------------------------------------------------------------- |
   | **rosbridge** (commands, topics) | 9090 | `python tools/list_topics.py` prints a list of topics                                                               |
   | **web_video_server** (camera)    | 8080 | Open `http://192.168.149.1:8080` in a browser: it lists every camera topic, and clicking one shows the live picture |

   The browser page is also the easiest way to find out what the camera
   topics are called.

### SSH (only if you need it)

Most of this lab can be done from the lab PC without ever logging in to the
robot: [tools/list_topics.py](../tools/list_topics.py) lists and watches
topics, and the browser shows the camera. **Use SSH only when you need
something those can't give you**, such as the fields inside a message type
(`ros2 interface show`), who is listening to a topic, or a proper shutdown.

From PowerShell on the lab PC, while connected to the robot's Wi-Fi:

```powershell
ssh ubuntu@192.168.149.1
```

- The username is `ubuntu` and the password is `ubuntu`. Nothing appears on
  screen while you type the password; that's normal. Press Enter when done.
- The first time, SSH asks whether you trust this computer. Type `yes`.
- You now have a terminal **on the Jetson**. Commands you type run there, not
  on your computer. Type `exit` to come back.

You're logged in to a robot every group shares, with a password that lets
you change anything. **Look, don't change**: no installing, updating or
editing the robot's own files (see [Safety and care](#2-safety-and-care)).

---

## 4. Finding out what the robot can do: topics

Nobody is going to hand you a complete list of this robot's topics. Finding
them is a skill, and it takes about five minutes once you know the commands.

Everything the robot senses or does passes through a **topic**: a named
channel carrying messages of one fixed **type**. To use a topic you need three
facts: its **name**, its **type**, and the **fields** inside that type.

### From the lab PC (no SSH)

```bash
python tools/list_topics.py                 # every topic and its type
python tools/list_topics.py servo           # only topics with "servo" in the name
python tools/list_topics.py --echo /cmd_vel # watch messages arrive (Ctrl+C to stop)
```

This gives you names and types. It can't show you the fields inside a type;
for that you need the robot's own tools.

### On the robot (over SSH)

| You want to know                                    | Command                                            |
| --------------------------------------------------- | -------------------------------------------------- |
| What topics exist?                                  | `ros2 topic list`                                  |
| ...and their types?                                 | `ros2 topic list -t`                               |
| Only the ones about servos?                         | `ros2 topic list -t \| grep servo`                 |
| Who publishes and who listens to a topic?           | `ros2 topic info /cmd_vel -v`                      |
| What fields does a message type have?               | `ros2 interface show geometry_msgs/msg/Twist`      |
| What is on the topic right now?                     | `ros2 topic echo /some/topic` (Ctrl+C to stop)     |
| Just one message, please                            | `ros2 topic echo /some/topic --once`               |
| How often do messages arrive?                       | `ros2 topic hz /some/topic`                        |
| What programs (nodes) are running?                  | `ros2 node list`                                   |
| What does one node publish, subscribe to and offer? | `ros2 node info /some_node`                        |
| What services exist?                                | `ros2 service list -t`                             |
| Send one message by hand                            | `ros2 topic pub --once <topic> <type> "<message>"` |

If `ros2` says "command not found", the terminal hasn't loaded the ROS
environment. Ask your TA how it's set up on your robot.

### A worked example: how do I drive?

**1. Find the topic.** Driving is done with velocity commands, so look for one:

```bash
ros2 topic list -t | grep cmd_vel
```

```
/cmd_vel [geometry_msgs/msg/Twist]
```

**2. Check something is listening.**

```bash
ros2 topic info /cmd_vel -v
```

Look at the subscription count. If nothing subscribes to a topic, you can
publish to it all day and the robot won't move. If you find more than one
velocity topic, this is how you tell which one the motors actually obey.

**3. Look at the message.**

```bash
ros2 interface show geometry_msgs/msg/Twist
```

```
Vector3  linear
        float64 x
        float64 y
        float64 z
Vector3  angular
        float64 x
        float64 y
        float64 z
```

**4. Try it by hand, wheels off the ground.**

```bash
ros2 topic pub --once /cmd_vel geometry_msgs/msg/Twist "{linear: {x: 0.1}}"
ros2 topic pub --once /cmd_vel geometry_msgs/msg/Twist "{}"
```

The first drives forward slowly. The second (all zeros) stops. Have the stop
command typed and ready before you send the first one.

**5. Put it in your code.** The topic name, the type and the field names go
into a rosbridge `publish` message, exactly as you did in Lab 1.

### The arm: finding and learning the servos

The starter code moves one servo, with this topic:

```
/ros_robot_controller/bus_servo/set_position
        [ros_robot_controller_msgs/msg/ServosPosition]
```

The rest of the arm works the same way. What you have to find out is which
servos exist and what each one does. The same five steps apply.

**1. Find everything that mentions servos.**

```bash
python tools/list_topics.py servo            # from the lab PC
ros2 topic list -t | grep -i servo           # on the robot
ros2 service list -t | grep -i servo         # services too: some things are asked for, not published
```

**2. Look at the message.**

```bash
ros2 interface show ros_robot_controller_msgs/msg/ServosPosition
```

A type that contains another type shows the inner one indented underneath.
Compare what you see with the message `set_servo()` builds in
`gui_starter.py` (in [last-can-gui](https://github.com/ccorbett0116/last-can-gui)): a `duration`, and a list of
`{id, position}` pairs. One message can carry several pairs, which is how a
whole pose is sent at once.

**3. Find the ID numbers.** You have several sources, and it's worth using
more than one:

- **Look at the arm.** Count the joints from the base to the gripper. Bus
  servos usually have their ID on a sticker or written on the case.
- **Ask the robot.** Among the topics and services from step 1, is there one
  that **reports** servo state rather than setting it? `ros2 interface show`
  its type to see what it wants and what it returns. A topic you read with
  `ros2 topic echo`; a service you call with
  `ros2 service call <name> <type> "<request>"`.
- **Read the manual.** The JetRover is a Hiwonder robot and its documentation
  is public. Generative AI can help you search it, but check what it tells
  you against the robot.

**4. Move one servo, a little, slowly.** From the lab PC:

```bash
python last-can-grabber/arm_pose_example.py --servo 1 --pos 520 --time 2.0
```

or on the robot:

```bash
ros2 topic pub --once /ros_robot_controller/bus_servo/set_position ros_robot_controller_msgs/msg/ServosPosition "{duration: 2.0, position: [{id: 1, position: 520}]}"
```

Positions are **absolute**. Sending 500 to a servo that is sitting at 900
swings it a long way, so if you can read where a servo is (step 3), start
from that number and change it by 20 or 30. Watch which joint moves and which
way. If nothing moves, that ID may not exist, or the servo may already be
there.

**5. Write it down.** Fill in a table like this for every servo, and share it
with the whole group on day one. The GUI builder needs it for the sliders and
the arm wrangler needs it for every pose.

| ID  | Joint         | When the number goes up, it moves... | Safe minimum | Safe maximum | Notes |
| --- | ------------- | ------------------------------------ | ------------ | ------------ | ----- |
| 1   | base rotation |                                      |              |              |       |
|     |               |                                      |              |              |       |

The safe range is the range where the joint doesn't hit the chassis, the
floor, the camera or the rest of the arm. It depends on where the other
joints are, so leave a margin.

### Topics the starter code uses

These were correct on the lab's robots when this was written. **Check them on
yours.** Robots get updated, and a wrong topic name fails silently: nothing
crashes, and nothing moves.

| Purpose         | Topic                                          | Type                                           |
| --------------- | ---------------------------------------------- | ---------------------------------------------- |
| Drive           | `/cmd_vel`                                     | `geometry_msgs/msg/Twist`                      |
| Move arm servos | `/ros_robot_controller/bus_servo/set_position` | `ros_robot_controller_msgs/msg/ServosPosition` |
| Colour camera   | `/depth_cam/rgb/image_raw`                     | `sensor_msgs/msg/Image`                        |

### rosbridge in one paragraph

You met rosbridge in Lab 1: a websocket on port 9090 that turns JSON into ROS
messages and back. The operations you need are `advertise` (announce you'll
publish to a topic), `publish`, `subscribe` (messages then arrive as JSON),
and `call_service`. [tools/list_topics.py](../tools/list_topics.py) is a
short, complete example of the last two.

---

## 5. Using the camera

The camera's colour image is a ROS topic like any other, but you don't read
it through rosbridge. A program on the robot called **web_video_server**
turns image topics into ordinary web addresses on port 8080, and that is what
your code connects to.

**See what there is.** Open `http://192.168.149.1:8080` in a browser. It
lists every image topic the robot has. Click one to watch it. This needs no
code and is the quickest way to check the camera is alive, to find the right
topic name, and to watch the robot while someone else drives.

**The addresses.** Put the topic name in the URL:

| You want                    | Address                                                                      |
| --------------------------- | ---------------------------------------------------------------------------- |
| A live stream               | `http://192.168.149.1:8080/stream?topic=/depth_cam/rgb/image_raw&type=mjpeg` |
| A smaller or lighter stream | add `&width=640&height=480` and/or `&quality=65` (JPEG quality, 1 to 100)    |
| One single picture          | `http://192.168.149.1:8080/snapshot?topic=/depth_cam/rgb/image_raw`          |

**In your code**, there are two easy ways to read the stream:

- `read_mjpeg()` in `gui_starter.py` ([last-can-gui](https://github.com/ccorbett0116/last-can-gui)) reads it with
  nothing but the standard library and hands you each frame as a **PIL
  image**.
- OpenCV reads the same address:
  `cv2.VideoCapture("http://.../stream?topic=...&type=mjpeg")`, then
  `ok, frame = capture.read()`. OpenCV is already installed (it comes with
  `ultralytics`) and gives you each frame as a **NumPy array**.

The two disagree about colour order: PIL images are **RGB**, OpenCV arrays
are **BGR**. Mix them up and red and blue swap, which matters when you're
looking for a blue-and-silver can. Know which one you're handing to your
model and which one you're drawing on screen.

**Save frames for testing.** The snapshot address gives you real pictures
from the robot's own camera, which you can then use with the robot switched
off: to test the model, to test your box drawing, to add to your training
data. From PowerShell:

```powershell
curl.exe -o frame01.jpg "http://192.168.149.1:8080/snapshot?topic=/depth_cam/rgb/image_raw"
```

**Things that go wrong:**

- **Don't subscribe to the raw image topic through rosbridge.** It works, but
  every frame arrives as a huge block of JSON text, and you'll get a few
  frames a second at best. Use the stream.
- **Delay builds up if you fall behind.** Frames arrive whether or not you're
  ready for them. Always work on the newest frame and throw the rest away,
  as the starter does.
- **Every open stream costs the robot CPU and Wi-Fi.** Several people can
  watch at once, but close the streams you aren't using.
- **Look at where the camera is mounted.** If it moves when the arm moves,
  what your model sees depends on the arm's pose.

---

## 6. Writing code that uses the robot

Every part of the robot is reached the same way, so learn the pattern once.

**There are three ways to talk to the robot**, and each has a rosbridge
operation:

| You want to                                          | ROS calls it           | rosbridge message                                                                                                |
| ---------------------------------------------------- | ---------------------- | ---------------------------------------------------------------------------------------------------------------- |
| Tell the robot to do something (drive, move a servo) | Publishing to a topic  | `{"op": "advertise", "topic": ..., "type": ...}` once, then `{"op": "publish", "topic": ..., "msg": {...}}`      |
| Keep reading something (a sensor, a state)           | Subscribing to a topic | `{"op": "subscribe", "topic": ..., "type": ...}`; messages then arrive as `{"op": "publish", ...}`               |
| Ask one question and get one answer                  | Calling a service      | `{"op": "call_service", "service": ..., "args": {...}}`; the answer arrives as `{"op": "service_response", ...}` |

The starter GUI publishes. [tools/list_topics.py](../tools/list_topics.py)
subscribes and calls services, in under a hundred lines; copy from it.

**For each new thing you want the robot to do:**

1. **Name.** Find the topic or service (section 4).
2. **Type and fields.** `ros2 interface show <type>`. The JSON you send has
   exactly those field names, nested the same way.
3. **By hand first.** Make it work once with `ros2 topic pub` or a
   five-line script before it goes anywhere near your GUI. If it doesn't work
   by hand, the problem is the robot or the message, not your program.
4. **One function.** Wrap it in one small function with a plain name
   (`drive(x, y, turn)`, `move_servos(positions, seconds)`,
   `read_servo(id)`). The rest of your code calls the function and never
   builds a message itself.
5. **Check it arrives.** `python tools/list_topics.py --echo <topic>` in a
   second window shows what your code is really sending.

**Habits that save time:**

- **Keep everything about the robot in one file**: the IP address, the topic
  names and types, the servo IDs and their safe ranges, the speeds. All three
  of you import it. When a topic name turns out to be wrong, it's fixed once.
- **A wrong name fails silently.** Publishing to a topic that doesn't exist
  is not an error: rosbridge creates it and nothing listens. If the robot
  ignores you, check the name and type character by character before you
  debug anything else.
- **Know what repeats and what doesn't.** Driving is a velocity that has to
  be sent again and again, and a zero to stop. A servo position is sent once
  and the servo goes there and holds.
- **Never wait on the GUI's thread.** `time.sleep()`, a network read or a
  model call inside tkinter's thread freezes the window and the Stop button
  with it. Slow work goes on another thread, and only the main thread
  touches the window.
- **Print what you send** while you're building. A line in the console for
  every command costs nothing and answers "did the button do anything?".
- **Keep a notes file** of what you found: topic names, servo table, poses
  that work. Three sessions spread over three weeks is long enough to forget.
- **Ask an AI, but hand it the facts.** Paste in the real topic list, the
  `ros2 interface show` output and the starter function. Without them it
  will guess, convincingly.

---

## 7. The Jetson Orin

The Jetson is a small Linux computer with an NVIDIA GPU, built for running
neural networks on robots.

**It is not a normal PC.** Its processor is ARM, not Intel or AMD, so
software built for an ordinary PC doesn't simply install. PyTorch in particular
needs a special NVIDIA build that matches the Jetson's system software. A
plain `pip install torch` on the Jetson gets you a version that can't use the
GPU, and can break what's already there.

**That's why we recommend running your model on the lab PC**, not on the
robot. Your GUI already receives every camera frame; run the model on those
frames where the GUI runs. The lab PC's GPU is far stronger than the
Jetson's, nothing has to be installed on the robot, and nothing you do can
break it for the next group.

**Never train on the Jetson.** See [last-can-eyes](https://github.com/ccorbett0116/last-can-eyes) for
where to train.

Useful commands over SSH:

| Command             | What it shows                                                                                                              |
| ------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| `tegrastats`        | Live CPU, GPU, memory and temperature. The Jetson's replacement for `nvidia-smi`, which doesn't exist here. Ctrl+C to stop |
| `free -h`           | Memory in use                                                                                                              |
| `df -h`             | Disk space                                                                                                                 |
| `top`               | What's using the CPU                                                                                                       |
| `hostname -I`       | The robot's IP addresses                                                                                                   |
| `sudo shutdown now` | Shut down safely before switching off                                                                                      |

If the robot is sluggish or the camera stutters, `tegrastats` will usually
tell you why: something is using all the CPU, or the board is hot and slowing
itself down.

---

## 8. Troubleshooting

| Symptom                                       | Likely cause                                                    | Try                                                                                                                                       |
| --------------------------------------------- | --------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| `ping` gets no reply                          | Wrong Wi-Fi network, or the robot is still booting              | Check which network your computer is on; wait a minute; check the IP with your TA                                                         |
| GUI status stays red                          | rosbridge isn't reachable                                       | Can you ping? Does `python tools/list_topics.py` connect? Is `ROBOT_IP` right in the script you're running?                               |
| Connected, but the robot doesn't move         | Wrong topic name or type, or nothing subscribes to it           | `ros2 topic info <topic> -v` on the robot; then `ros2 topic echo <topic>` while you press the button, to see whether your messages arrive |
| Robot moves the wrong way                     | A sign or an axis is swapped                                    | Test each direction one at a time, wheels off the ground                                                                                  |
| Camera area stays black                       | Wrong camera topic, or the camera node isn't running            | Open `http://<robot ip>:8080` in a browser and see which topics are listed                                                                |
| Camera is seconds behind                      | Frames are queuing somewhere                                    | Draw only the newest frame and drop the rest; don't run the model on every frame; lower the stream quality or size                        |
| Connected and the camera works, but neither the wheels nor the arm respond, for anyone | The robot's motor controller program has stopped. It happens occasionally | Tell your TA, who can restart it |
| Arm doesn't respond                           | Wrong servo ID, wrong topic, or the message has the wrong shape | `ros2 interface show` the type and compare it field by field with what you send                                                           |
| A servo buzzes or gets hot                    | It's stalled against something                                  | Move it back **now**; find its safe range                                                                                                 |
| Robot keeps driving after your program closed | The last message it got wasn't a stop                           | Send zeros when the window closes, and whenever a key is released                                                                         |
| It worked a minute ago                        | Battery low, or the Wi-Fi dropped                               | Check the battery; check you're still on the robot's network                                                                              |

When you ask your TA for help, bring three things: what you did, what you
expected, and what happened instead.
