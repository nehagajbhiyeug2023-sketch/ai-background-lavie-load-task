# ai-background-lavie-load-task
Perceptual load letter-detection task with background manipulation
# AI Background Load Task (Lavie Letter Search)

This repository contains a PsychoPy implementation of a Lavie-style letter search task adapted to test attentional capture by AI-related visual cues.

Participants perform a simple letter detection task (searching for the target letter **X**) under:

- **Perceptual load**:  
  - Low load (easy: repeated letters, e.g. `XXXXXX`)  
  - High load (hard: target among non-targets, e.g. `AKXTRF`)

- **Background type** (distractors):  
  - `ai` – GenAI / ChatGPT-like interface  
  - `internet` – non-AI internet (e.g. search / Wikipedia-like)  
  - `paper` – paper / physical document style  
  - `solid` – plain solid colour

The experiment uses a **2 × 4 within-subjects design** (Load × Background), with **5 trials per cell** (40 trials total).

---

## Requirements

- [PsychoPy](https://www.psychopy.org/) (tested with PsychoPy 2023+)
- Python environment where PsychoPy runs (usually via the PsychoPy standalone)

---

## File Structure

Place the script and background images in the following structure:

```text
your_experiment_folder/
│
├─ ai_background_load_task_v4.py
└─ backgrounds/
   ├─ ai/
   │   ├─ ai1.jpg
   │   ├─ ai2.jpg
   ├─ internet/
   │   ├─ internet1.jpg
   ├─ paper/
   │   ├─ paper1.jpg
   └─ solid/
       ├─ solid1.jpg
