"""
AI Background Perceptual Load Task (v4)

Implements a letter-detection task with background manipulation
to examine attentional load under different visual backgrounds.

Design:
- Perceptual Load: Low vs High
- Background Type: AI-generated, Internet, Paper, Solid
- 2 × 4 factorial design

Author: Neha Gajbhiye
Status: Research prototype
"""
from psychopy import visual, core, event, gui, data
import random
import os
import csv
from datetime import datetime

# =========================
# Experiment Info
# =========================

exp_info = {
    "Participant": "",
    "Session": "1",
}
dlg = gui.DlgFromDict(exp_info, title="AI Background Load Task")
if not dlg.OK:
    core.quit()

# =========================
# Window Setup
# =========================

win = visual.Window(
    size=[1280, 720],
    fullscr=True,
    units="pix",
    color=[0, 0, 0]
)

# =========================
# Stimuli Setup
# =========================

# Fixation cross
fixation = visual.TextStim(win, text="+", height=40, color=[1, 1, 1])

# Background image stimulus (will be updated per trial)
bg_image = visual.ImageStim(win, size=(800, 1200))

# Letter string stimulus
letter_stim = visual.TextStim(win, text="", height=60, color=[1, 1, 1])

# Instruction and thanks texts
instruction_text = visual.TextStim(
    win,
    text=(
        "Welcome to the Cognitive Psychology Experiment.\n\n"
        "You will see a series of letter strings presented on different backgrounds.\n"
        "Your task is to indicate whether the target letter 'X' is present or absent.\n\n"
        "Press 'Z' if the letter X is present.\n"
        "Press 'M' if the letter X is absent.\n\n"
        "Try to respond as quickly and accurately as possible.\n\n"
        "Press SPACE to begin."
    ),
    height=28,
    wrapWidth=1000,
    color=[1, 1, 1]
)

thanks_text = visual.TextStim(
    win,
    text="Thank you for your time!\n\nYou have completed the experiment.",
    height=32,
    wrapWidth=1000,
    color=[1, 1, 1]
)

# =========================
# Background Images Loading
# =========================

# Folder structure:
# backgrounds/
#   ai/
#   internet/
#   paper/
#   solid/

bgFolder = "backgrounds"

backgroundTypes = ["ai", "internet", "paper", "solid"]
bgImages = {}

for bg_type in backgroundTypes:
    folder_path = os.path.join(bgFolder, bg_type)
    if not os.path.isdir(folder_path):
        print(f"Warning: Folder not found for background type '{bg_type}': {folder_path}")
        bgImages[bg_type] = []
        continue

    files = [
        os.path.join(folder_path, f)
        for f in os.listdir(folder_path)
        if f.lower().endswith((".png", ".jpg", ".jpeg", ".bmp"))
    ]
    if len(files) == 0:
        print(f"Warning: No image files found for background type '{bg_type}' in {folder_path}")
    bgImages[bg_type] = files

# =========================
# Trial Structure
# =========================

# Conditions:
#  - Perceptual Load: low / high
#  - Background Type: ai / internet / paper / solid
#
# We use 5 trials per cell:
#  2 loads × 4 backgrounds × 5 trials = 40 trials total

loads = ["low", "high"]

# Letter sets
target_letter = "X"
non_target_letters = [l for l in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" if l != target_letter]

# We will control presence/absence:
# aim: 3 target-present, 2 target-absent per condition (approx).

trials = []

for load in loads:
    for bg_type in backgroundTypes:
        # For each cell, create 5 trials:
        # We'll add a flag 'target_present': True/False
        # 3 True, 2 False
        cell_trials = [True, True, True, False, False]
        random.shuffle(cell_trials)
        for present in cell_trials:
            trials.append({
                "load": load,
                "background_type": bg_type,
                "target_present": present
            })

# Randomize order
random.shuffle(trials)

# =========================
# Trial Count Check
# =========================

print(f"Total trials: {len(trials)}")
# Should be 40

# =========================
# Helper Functions
# =========================

def make_letter_string(load_type, target_present):
    """Create a 6-letter string based on load and target presence."""
    if load_type == "low":
        # Low load: if target present, XXXXX, else all same non-X letter
        if target_present:
            return target_letter * 6
        else:
            # all the same, but different from X
            letter = random.choice(non_target_letters)
            return letter * 6
    else:
        # High load:
        #  - 1 target X + 5 different non-target letters (if present)
        #  - 6 non-target letters (none are X) if absent
        letters = []
        if target_present:
            letters.append(target_letter)
            # pick 5 distinct non-targets
            chosen = random.sample(non_target_letters, 5)
            letters.extend(chosen)
        else:
            # 6 non-target letters, all distinct or at least not X
            chosen = random.sample(non_target_letters, 6)
            letters.extend(chosen)
        random.shuffle(letters)
        return "".join(letters)


def get_background_image(bg_type):
    """Pick a random image path from the given type."""
    files = bgImages.get(bg_type, [])
    if not files:
        return None
    return random.choice(files)


# =========================
# Data Logging
# =========================

results = []

# Output file
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename_base = f"ai_background_load_results_v4_{exp_info['Participant']}_{timestamp}.csv"
out_dir = "data"
os.makedirs(out_dir, exist_ok=True)
filepath = os.path.join(out_dir, filename_base)

# =========================
# Instructions
# =========================

instruction_text.draw()
win.flip()

keys = event.waitKeys(keyList=["space", "escape"])
if "escape" in keys:
    win.close()
    core.quit()

# =========================
# Main Trial Loop
# =========================

global_clock = core.Clock()
trial_clock = core.Clock()

for i, trial in enumerate(trials, start=1):
    load_type = trial["load"]
    bg_type = trial["background_type"]
    target_present = trial["target_present"]

    # -------------------------
    # Fixation
    # -------------------------
    jitter = random.uniform(3.5, 5.5)  # seconds
    fixation_time = jitter
    trial_clock.reset()
    while trial_clock.getTime() < fixation_time:
        fixation.draw()
        win.flip()

    # -------------------------
    # Choose background image
    # -------------------------
    img_path = get_background_image(bg_type)
    if img_path is not None:
        bg_image.image = img_path
    else:
        # fallback: plain grey if no image is found
        bg_image.image = None
        win.color = [0, 0, 0]

    # -------------------------
    # Create letter string for this trial
    # -------------------------
    letters = make_letter_string(load_type, target_present)
    letter_stim.text = letters

    # -------------------------
    # Present background + letters
    # -------------------------
    event.clearEvents()
    trial_clock.reset()
    rt = None
    response_key = None
    correct = None

    # Part 1: 200 ms with letters + background
    while trial_clock.getTime() < 0.2:
        if img_path is not None:
            bg_image.draw()
        letter_stim.draw()
        win.flip()
        # Collect response during this window (if any)
        keys = event.getKeys(keyList=["z", "m", "escape"], timeStamped=trial_clock)
        if keys and response_key is None:
            response_key, rt = keys[0]

    # Part 2: after 200 ms, letters disappear, background remains
    # Continue till response or max 1.5 s from letter onset
    max_dur = 1.5
    while trial_clock.getTime() < max_dur and response_key is None:
        if img_path is not None:
            bg_image.draw()
        win.flip()
        keys = event.getKeys(keyList=["z", "m", "escape"], timeStamped=trial_clock)
        if keys and response_key is None:
            response_key, rt = keys[0]

    # Check for escape
    if response_key == "escape":
        break

    # Determine correctness
    if response_key is None:
        correct = 0
    else:
        # 'z' = target present, 'm' = target absent
        if target_present and response_key == "z":
            correct = 1
        elif (not target_present) and response_key == "m":
            correct = 1
        else:
            correct = 0

    # Store trial data
    results.append({
        "participant": exp_info["Participant"],
        "session": exp_info["Session"],
        "trial_index": i,
        "load": load_type,
        "background_type": bg_type,
        "target_present": int(target_present),
        "letters": letters,
        "response_key": response_key if response_key is not None else "",
        "rt": rt if rt is not None else "",
        "correct": correct
    })

# =========================
# End of Experiment
# =========================

thanks_text.draw()
win.flip()
core.wait(3.0)

win.close()
core.quit()

# =========================
# Save Data to CSV
# (Executed after window close)
# =========================

fieldnames = [
    "participant", "session", "trial_index",
    "load", "background_type", "target_present",
    "letters", "response_key", "rt", "correct"
]

with open(filepath, mode="w", newline="", encoding="utf-8") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for row in results:
        writer.writerow(row)

print(f"Data saved to {filepath}")
