# Putting it together

Three people build three parts on three computers. This guide is about making
them one program, and about getting files from one person to another.

1. [Agree on the joins first](#1-agree-on-the-joins-first) (everyone, first session)
2. [What actually has to be shared](#2-what-actually-has-to-be-shared)
3. [Choose how you'll share](#3-choose-how-youll-share)
   - [Option A: Git](#option-a-git)
   - [Option B: Email](#option-b-email)
   - [Option C: USB stick](#option-c-usb-stick)
4. [Joining the parts](#4-joining-the-parts) (same for every option)
5. [When it works on my computer but not yours](#5-when-it-works-on-my-computer-but-not-yours)

---

## 1. Agree on the joins first

The parts meet in exactly two places. Decide what each looks like **in your
first session**, write it down, and don't change it without telling everyone.

**Join 1: GUI ↔ model.** The GUI hands over a camera frame and gets
detections back.

- What goes in: a PIL image? A NumPy array? At what size?
- What comes out: for each can, what exactly? In what order? In which
  pixels (the original frame's, or the resized one's)?
- What comes out when there's no can?

**Join 2: GUI ↔ grab and drop.** The GUI's buttons start the arm routines.

- What does the GUI call, and with what arguments? (The routines need some
  way to send servo commands. Does the GUI pass its robot connection in, or
  do they open their own?)
- Does the call return straight away, or only when the arm has finished? How
  does the GUI find out it's done, or that it failed?
- How does the GUI stop a routine halfway?

Once these are agreed, each person writes a **stand-in** for their side on day
one: a detector that always returns one made-up box, a grab function that
prints "grabbing…" and waits three seconds. Now the GUI builder can build and
test everything without waiting, and the real versions drop in later without
anything else changing.

Also agree on the boring things: **one folder layout**, **file names**, and
**one Python version** for the whole group.

A layout that works:

```
your_project/
├── HOW_TO_RUN.md
├── requirements.txt
├── main.py              starts the GUI
├── gui/                 Part 1
├── vision/              Part 2: training script, detector wrapper, TRAINING_NOTES.md
├── arm/                 Part 3: grab and drop routines
└── models/
    └── best.pt          the trained weights the GUI loads
```

One person, one folder. If each of you only edits your own folder, you can't
overwrite each other's work, whichever sharing method you use.

---

## 2. What actually has to be shared

| Share | Don't share |
|---|---|
| Your `.py` files | `.venv/` (hundreds of megabytes, and it only works on the computer that made it) |
| `models/best.pt` (a few MB) | The training photos (everyone downloads them from the TA's link) |
| `requirements.txt` | `runs/` folders (training output; keep them on the trainer's computer) |
| `HOW_TO_RUN.md` and your notes | `__pycache__/` folders |

Everyone builds their own virtual environment from `requirements.txt`. If one
of you installs a new package, add it to `requirements.txt` and tell the others.

---

## 3. Choose how you'll share

| | Good for | Watch out for |
|---|---|---|
| **A. Git** | Groups where at least one person is comfortable with it. Keeps every version; merges changes | **Not installed on the lab PCs.** The learning curve, if nobody has used it |
| **B. Email** | Most groups in this lab. Nothing to install | "Which one is the latest?" Mail systems that block code attachments |
| **C. USB stick** | The lab, when the Wi-Fi is busy being the robot's network | Forgetting the stick. Unplugging it too early |

**Which one?** Git is the industry standard, and if you plan to write
software for a living you will use it every day. But the lab PCs don't have
it. You're allowed to install it, but it doesn't stay installed: every person
who wants Git has to install it again each time they come in, out of lab time
you don't have much of. **For this lab, email is likely the more practical
choice.** Use Git if your group already knows it and is happy to pay that
cost.

You can mix them: Git for code, a USB stick to get `best.pt` onto the lab
computer when it's connected to the robot's Wi-Fi and has no internet.

That last point catches every group once: **while your computer is on the
robot's Wi-Fi, it probably has no internet.** Pull, download or receive what
you need *before* you switch networks, or keep a USB stick handy.

---

### Option A: Git

**Every session, on every lab PC you use:** install Git first. It isn't on
the lab PCs and it doesn't stay installed between sessions. Download the
installer from [git-scm.com](https://git-scm.com/download/win), accept the
defaults, then open a **new** PowerShell window and check with
`git --version`.

**Set up, once (one person):**

1. Create a **private** repository on GitHub. Private matters: a public
   repository shares your solution with the whole class.
2. Add your group members as collaborators (repository **Settings →
   Collaborators**).
3. Put the agreed folder layout in it, with a `.gitignore` so the things in
   the "don't share" column never get committed. The
   [.gitignore](../.gitignore) in this repository is a reasonable start.

**Set up, once (everyone):**

```bash
git clone <your repository's URL>
cd <the folder it created>
```

Then make your virtual environment and `pip install -r requirements.txt`.

**Every time you sit down to work:**

```bash
git pull                      # get everyone else's changes FIRST
```

**Every time you have something that works:**

```bash
git status                    # what did I change?
git add gui/                  # add YOUR folder (not "git add ." until you trust your .gitignore)
git commit -m "Add strafe buttons"
git pull                      # in case someone pushed while you worked
git push
```

Commit small and often. A commit that says what it does ("Fix box scaling")
is a save point you can go back to.

**If `git pull` reports a conflict,** two people changed the same lines of the
same file. Git marks the spot in the file with `<<<<<<<`, `=======` and
`>>>>>>>`. Open it, keep what should be kept, delete the markers, then
`git add` the file and `git commit`. Do it together with the other person. The
one-person-one-folder rule is what keeps this rare.

**New weights:** replacing `models/best.pt` and committing it is fine; it's
small. Don't commit every experiment, only the one the group should be using.

---

### Option B: Email

**Sending:**

1. Zip **your part's folder only**, not the whole project and not `.venv`:
   right-click the folder → **Compress to ZIP file** (or **Send to →
   Compressed folder**).
2. Name the zip so nobody has to guess: `gui_v3_nov12.zip`, not `gui.zip`
   or `final_FINAL2.zip`. Number goes up by one every time you send.
3. In the email, say what changed since the last version and anything the
   others have to do (a new package to install, a renamed function).

**Receiving:**

1. Save the zip and unzip it somewhere temporary.
2. **Replace the whole folder** for that part in your copy of the project:
   delete (or rename) the old `gui/`, move the new one in. Don't merge file by
   file; that's how half-old, half-new code happens.
3. Run it straight away and tell the sender whether it worked.

**If the mail system rejects the attachment:** some block `.py` files or zips
that contain them. Share the zip through OneDrive or Google Drive and email
the link instead. Model weights can go the same way.

**Keeping track:** email has no memory of what the "current" version is, so
give one person that job. They keep the one complete, working copy; everyone
else sends parts to them and gets the assembled project back from them.

---

### Option C: USB stick

**Before you start:**

- Keep **one project folder** on the stick with the agreed layout.

**Copying your work on:**

1. Copy your part's folder onto the stick, **replacing** the stick's copy of
   that folder. Copy only your own folder.
2. Add a line to a `CHANGES.txt` on the stick: date, your name, what changed.
   It takes ten seconds and answers "whose version is this?".
3. **Eject the stick** before pulling it out (**Safely Remove Hardware** in
   the taskbar). Pulling it out mid-write is how files end up empty.

**Copying work off:**

1. Copy the folders you need from the stick **onto your computer's disk**,
   replacing your old copies of other people's folders.
2. Run from your disk, not from the stick. It's slower from the stick, and the
   stick leaves when its owner does.

**The stick is not a backup.** It gets lost, and it's the only copy the
moment someone edits a file directly on it. Each of you keeps your own part
somewhere else as well.

---

## 4. Joining the parts

However the files reached you, the steps from here are the same.

1. **One computer has everything.** Pick the lab PC you'll use for the demo
   and put the complete project on it.
2. **Build the environment there**, in the order given in
   [Getting started](../README.md#5-getting-started): the CUDA build of
   PyTorch first, then `pip install -r requirements.txt`. Check that
   `torch.cuda.is_available()` is `True` on *this* PC. Your model runs on its
   GPU during the demo, and a CPU-only install will make the live boxes lag.
3. **Join one thing at a time, without the robot first.**
   - Swap the stand-in detector for the real one. Run the model on a few saved
     camera frames. Do boxes come out? Are they in the right place?
   - Swap the stand-in grab for the real one, with the robot off. Does
     pressing the button call it? Does the GUI stay alive while it "runs"?
4. **Then with the robot, in this order:** connection and camera → driving →
   arm sliders → live detection with boxes → grab → drop → a full run.
   When something breaks, you know it was the last thing you added.
5. **Do full runs.** Start point, find the can, grab, return, drop. Several
   times, with the person who will drive on the day.
6. **Freeze it.** Once a version does a full run, save a copy of the whole
   project (a Git commit, a dated zip, a dated folder on the stick) before
   anyone improves anything. If the improvement breaks it the night before
   the demo, you still have a version that works.

Aim to reach step 4 by the **end of the second session**.

---

## 5. When it works on my computer but not yours

| Symptom | Usual cause |
|---|---|
| `ModuleNotFoundError` for a package | It isn't in `requirements.txt`, or the virtual environment isn't activated |
| `ModuleNotFoundError` for one of your own files | The program was started from a different folder. Agree on where it's run from, and write that in `HOW_TO_RUN.md` |
| `FileNotFoundError` for the model or a pose file | A path like `C:\Users\alex\...` that exists on one computer only. Build paths relative to the code's own location |
| Model loads but finds nothing | Not the same `best.pt`, or a different confidence threshold. Check the file's date and size |
| Boxes are in the wrong place | The two sides of Join 1 disagree about which pixels the coordinates are in |
| The GUI freezes during a grab | The grab routine blocks the GUI's thread. That's Join 2 |
| It can't reach the robot | A different `ROBOT_IP` in one of the files. Keep the address in one place |
| It's much slower | The model is running on the CPU: this environment has the CPU-only build of PyTorch. Check `torch.cuda.is_available()` |
| Different behaviour, same code | Different Python or package versions. Compare `python --version` and `pip list` |
