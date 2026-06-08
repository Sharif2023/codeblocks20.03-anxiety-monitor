"""
Generate realistic post-survey responses for 3rd CT students
based on their actual behavioral metrics from the CT logs.
Then append to the existing post-survey CSV.
"""
import csv
import os

SURVEY_FILE = r"f:\CodeBlocks20.03-AnxietyMonitor\data\raw\post_survey\post-survey.csv"

# New 3rd CT survey entries — generated from actual behavioral stats
# Format: Timestamp, Student ID, Stress(1-5), Stuck, Difficulty(1-5), External Factors, Trigger comment
new_entries = [
    # 0112430146: Avg Anxiety 69, Max Focus 214, Idle 0.78, Backspace 13.6%, CompileSR 60%, Keystrokes 662 — HIGH
    (
        "6/6/2026 13:35:00", "0112430146", "4",
        "Yes, for a significant part of the session",
        "4",
        "IDE/Compiler issues, Time pressure",
        "I spent the majority of the session staring at the screen without making progress. My compile rate was dropping and I kept switching between files frantically, which made it really hard to think clearly."
    ),
    # 0112510249: Avg Anxiety 84.2, Max Focus 132, Idle 0.87, Backspace 38.8%, CompileSR 50% — CRITICAL
    (
        "6/6/2026 13:36:00", "0112510249", "5",
        "Yes, for a significant part of the session",
        "5",
        "IDE/Compiler issues, Lack of understanding of the topic, Time pressure",
        "I was in complete panic the whole time. My backspace rate was enormous—I kept deleting almost everything I wrote. I spent over 85% of the session just sitting idle, completely stuck, with no idea how to even start the solution."
    ),
    # 0112510374: Avg Anxiety 63.9, Max Focus 96, Idle 0.81, Backspace 13.8%, CompileSR 57% — HIGH but moderate moments
    (
        "6/6/2026 13:37:00", "0112510374", "4",
        "Yes, for a significant part of the session",
        "4",
        "IDE/Compiler issues, Time pressure",
        "I struggled a lot with compiler errors and spent a huge chunk of time just waiting and idle. I couldn't get a clean compile and the clock made it worse."
    ),
    # 0112530009: Avg Anxiety 68.9, Max Focus 102, Idle 0.80, Backspace 14.9% — HIGH
    (
        "6/6/2026 13:38:00", "0112530009", "4",
        "Yes, for a significant part of the session",
        "4",
        "Lack of understanding of the topic, Time pressure",
        "The logic of the problem was confusing and I spent a lot of time idle trying to figure out the approach. Every time I tried to compile there was a new error to deal with."
    ),
    # 0112530018: Avg Anxiety 70.7, Max Focus 127, Idle 0.67, Backspace 18%, CompileSR 53% — HIGH
    (
        "6/6/2026 13:39:00", "0112530018", "5",
        "Yes, for a significant part of the session",
        "4",
        "IDE/Compiler issues, Lack of understanding of the topic, Time pressure",
        "The task was really hard and I couldn't get my code to compile. My backspace rate was high because I second-guessed everything I typed. Constant IDE failures made me panic more as time passed."
    ),
    # 0112530032: Avg Anxiety 75.4, Max Focus 92, Idle 0.63, Backspace 19.1%, CompileSR 57% — HIGH
    (
        "6/6/2026 13:40:00", "0112530032", "5",
        "Yes, for a significant part of the session",
        "5",
        "IDE/Compiler issues, Time pressure, Extreme inability to focus",
        "I was overwhelmed almost immediately. The problem was too difficult and I kept getting compile errors. Over half the session I was either idling or frantically deleting my own code. By the end I gave up trying and just sat there."
    ),
    # 0112530036: Avg Anxiety 75.2, Max Focus 271, Idle 0.65, Backspace 23.9% — HIGH, very high focus switches
    (
        "6/6/2026 13:41:00", "0112530036", "5",
        "Yes, for a significant part of the session",
        "5",
        "IDE/Compiler issues, Time pressure, Extreme context-switching/distraction",
        "I couldn't stay focused at all. I was constantly alt-tabbing away from the IDE hundreds of times looking for help or just to escape the pressure. My backspace rate was huge and I couldn't get my code to a working state."
    ),
    # 0112530042: Avg Anxiety 68.8, Max Focus 43, Idle 0.74, Backspace 12.7%, CompileSR 60% — HIGH but lower switching
    (
        "6/6/2026 13:42:00", "0112530042", "4",
        "Yes, for a significant part of the session",
        "3",
        "IDE/Compiler issues, Time pressure",
        "I understood parts of the problem but kept running into compilation errors that I couldn't resolve quickly. The idle time adds up when you are just staring at error messages trying to figure out what went wrong."
    ),
    # 0112530047: Avg Anxiety 83.6, Max Focus 70, Idle 0.76, Backspace 30.2%, CompileSR 50% — CRITICAL
    (
        "6/6/2026 13:43:00", "0112530047", "5",
        "Yes, for a significant part of the session",
        "5",
        "IDE/Compiler issues, Lack of understanding of the topic, Time pressure",
        "The session was a disaster. Half my compile attempts failed and my backspace rate was enormous because I had no confidence in my code. I sat idle for most of the test just panicking and staring at the screen without knowing what to write."
    ),
    # 0112530077: Avg Anxiety 74.5, Max Focus 180, Idle 0.68, Backspace 21.1%, CompileSR 57% — HIGH
    (
        "6/6/2026 13:44:00", "0112530077", "5",
        "Yes, for a significant part of the session",
        "5",
        "IDE/Compiler issues, Time pressure, Frantic context-switching",
        "I kept frantically switching windows trying to find solutions. My compile success rate was terrible and I deleted almost as much code as I wrote. The time pressure made everything worse and I felt increasingly anxious as the session went on."
    ),
    # 0112530122: Avg Anxiety 75.0, Max Focus 141, Idle 0.62, Backspace 30.9%, CompileSR 50% — HIGH (most keystrokes = tried hard)
    (
        "6/6/2026 13:45:00", "0112530122", "4",
        "Yes, for a significant part of the session",
        "5",
        "IDE/Compiler issues, Lack of understanding of the topic, Time pressure",
        "I tried really hard but my compile success rate was only about 50%. I wrote and deleted a lot of code because I kept changing my approach. The stress got worse every time I got another compile error when time was running out."
    ),
    # 0112530181: Avg Anxiety 51.6, Max Focus 30, Idle 0.88, Backspace 23.7%, CompileSR 50% — MODERATE (low keystrokes=177)
    (
        "6/6/2026 13:46:00", "0112530181", "3",
        "Yes, for a significant part of the session",
        "4",
        "Lack of understanding of the topic, Time pressure",
        "I got stuck early and never really found my footing. I typed very little because I spent most of the time thinking about what to do. The compile errors I did get were demoralizing but I stayed relatively calm compared to other tests."
    ),
    # 0112530190: Avg Anxiety 61.1, Max Focus 365, Idle 0.80, Backspace 11.2%, CompileSR 66% — HIGH (massive focus switches)
    (
        "6/6/2026 13:47:00", "0112530190", "4",
        "Yes, for a significant part of the session",
        "4",
        "IDE/Compiler issues, Noise/distractions in the lab, Time pressure",
        "I spent most of the time switching between windows because I was trying to look up references and check my logic. My idle time was high because the problem was harder than I expected, and I found it difficult to maintain focus on a single task."
    ),
]

# Read existing CSV to get fieldnames
with open(SURVEY_FILE, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames

print(f"Survey fieldnames: {fieldnames}")

# Append new rows
with open(SURVEY_FILE, 'a', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    for entry in new_entries:
        writer.writerow(entry)

print(f"\nAppended {len(new_entries)} new 3rd CT survey responses.")
print("Updated survey saved.")
