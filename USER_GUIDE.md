# AnxietyMonitor Plugin - User Guide

## How to Use the Plugin

Once the plugin is installed in CodeBlocks 20.03, here's how to start monitoring, collect data, and stop sessions.

---

## Quick Start (3 Steps)

1. **Start Monitoring** → Click the **Start** button or use the menu
2. **Code Normally** → The plugin collects data automatically every 30 seconds
3. **Stop Monitoring** → Click the **Stop** button when done

**Your data is automatically saved** to a CSV file throughout the session.

---

## Detailed Instructions

### 1. **Starting a Monitoring Session**

#### Method A: Using Toolbar Buttons (Easiest)
Look for the AnxietyMonitor toolbar buttons in CodeBlocks:
- Click the **▶ Start** button on the toolbar

#### Method B: Using the Menu
- Go to **Plugins → Anxiety Monitor → Start Monitoring**

**What Happens:**
- A popup appears: "Monitoring Started!"
- Shows the CSV file location where data will be saved
- The plugin starts collecting behavioral metrics every 30 seconds
- A timer begins running in the background

**CSV File Location:**
Data is saved to: `[Your User Directory]/AnxietyMonitor/session_YYYYMMDD_HHMMSS.csv`

Example: `C:\Users\YourName\AnxietyMonitor\session_20260123_163000.csv`

---

### 2. **While Monitoring is Active**

#### What the Plugin Tracks (Automatically)
The plugin monitors **12 behavioral metrics** while you code:

| Metric | What It Measures |
|--------|------------------|
| **Typing Speed** | Words per minute (WPM) |
| **Error Rate** | Compile/build errors per minute |
| **Backspace Usage** | % of backspace key presses |
| **Pause Ratio** | % of time spent not typing |
| **Mouse Activity** | Clicks and movement patterns |
| **Build Frequency** | How often you compile |
| **File Switches** | Project/file navigation frequency |
| **Code Deletions** | Lines deleted |
| **Undo/Redo** | Undo and redo operations |
| **Search Usage** | Find/replace frequency |
| **Speed Variance** | Typing speed inconsistency |

#### Real-Time Display
If the AnxietyMonitor panel is visible, you'll see:
- **Current Anxiety Score** (0-100 scale)
- **Risk Level** (LOW / MODERATE / HIGH)
- **Live Metrics** (errors, typing speed, pause ratio, etc.)
- **Recent Events** log
- **Trend Indicator** (improving/worsening)

#### Data Collection Frequency
- Metrics are collected **continuously** as you type and interact with CodeBlocks
- Data is written to CSV **every 30 seconds** automatically
- **Auto-save** ensures no data is lost if CodeBlocks crashes

---

### 3. **Pausing the Session (Optional)**

If you need to take a break but don't want to end the session:

#### To Pause:
- Click the **⏸ Pause** button on the toolbar
- Or: **Plugins → Anxiety Monitor → Pause Monitoring**

**What Happens:**
- Data collection stops
- Current data is saved to CSV
- Popup: "Monitoring Paused"

#### To Resume:
- Click the **▶ Resume** button
- Or: **Plugins → Anxiety Monitor → Resume Monitoring**

**What Happens:**
- Data collection resumes
- Continues writing to the same CSV file
- Popup: "Monitoring Resumed"

---

### 4. **Stopping a Monitoring Session**

When you're done coding and want to end the session:

#### To Stop:
- Click the **⏹ Stop** button on the toolbar
- Or: **Plugins → Anxiety Monitor → End Monitoring**

**What Happens:**
1. All pending data is **immediately saved** to CSV
2. Timer stops
3. Session ends
4. Popup shows:
   - "Monitoring Stopped"
   - Number of rows written
   - CSV file location

**CSV File is Complete:**
Your data file is now ready for analysis!

---

## CSV Data Format

The output CSV file contains one row per measurement interval (every 30 seconds):

```csv
session_id,timestamp,anxiety_score,risk_level,typing_speed_wpm,error_rate,...
session_20260123_163000,2026-01-23 16:30:30,35.2,MODERATE,45.3,1.2,...
session_20260123_163000,2026-01-23 16:31:00,38.5,MODERATE,42.1,1.5,...
```

### CSV Columns:
- `session_id` - Unique session identifier
- `timestamp` - Date and time of measurement
- `anxiety_score` - Calculated anxiety score (0-100)
- `risk_level` - LOW / MODERATE / HIGH
- `typing_speed_wpm` - Words per minute
- `error_rate` - Errors per minute
- `backspace_ratio` - % of backspace usage
- `pause_ratio` - % of idle time
- `mouse_clicks` - Number of mouse clicks
- `file_switches` - Number of file changes
- ...and more behavioral metrics

---

## Common Usage Scenarios

### Scenario 1: Single Coding Session
```
1. Start CodeBlocks
2. Click Start Monitoring
3. Code for 1-2 hours
4. Click Stop Monitoring when done
5. CSV file is saved automatically
```

### Scenario 2: Multiple Sessions Per Day
```
Morning Session:
1. Start Monitoring → Code → Stop Monitoring
   File: session_20260123_090000.csv

Afternoon Session:
2. Start Monitoring → Code → Stop Monitoring
   File: session_20260123_140000.csv
```
Each session creates a separate CSV file with a unique timestamp.

### Scenario 3: Long Session with Breaks
```
1. Start Monitoring
2. Code for 1 hour
3. Click Pause (lunch break)
4. Click Resume
5. Code for another hour
6. Click Stop
```
All data is saved to **one CSV file** with gap periods marked during pause.

---

## Tips for Best Data Quality

✅ **DO:**
- Start monitoring at the beginning of your coding session
- Let it run continuously while you code normally
- Stop monitoring when you finish coding
- Keep CodeBlocks open during active sessions

❌ **DON'T:**
- Don't modify the plugin settings during research studies
- Don't disable the plugin mid-session
- Don't manually edit the CSV files
- Don't delete old session files until the study is complete

---

## Viewing Your Data

### Location of CSV Files:
All session files are saved in:
- Windows: `C:\Users\[YourUsername]\AnxietyMonitor\`

### Opening CSV Files:
- **Excel/Google Sheets**: Open directly for quick viewing
- **Python/R**: Load for statistical analysis
- **Text Editor**: View raw CSV format

---

## Troubleshooting Data Collection

### Problem: No CSV file created
**Solution:**
- Check that you have write permissions in your user directory
- Verify the session actually started (popup message should appear)
- Check CodeBlocks logs: **Help → Debug → Display Logs**

### Problem: CSV file is empty
**Solution:**
- Make sure you **stopped** the session (don't just close CodeBlocks)
- Wait at least 30 seconds after starting before stopping
- Click Stop button explicitly to force final save

### Problem: Missing data rows
**Solution:**
- Data is only written every 30 seconds
- If you stop immediately after starting, you may have 0-1 rows
- Let the session run longer for more data points

---

## Understanding Your Anxiety Score

| Score Range | Risk Level | What It Means |
|-------------|------------|---------------|
| **0-33** | 🟢 LOW | Calm, focused coding |
| **34-66** | 🟡 MODERATE | Some stress indicators present |
| **67-100** | 🔴 HIGH | Multiple anxiety signals detected |

The score is calculated in real-time based on all 12 behavioral metrics.

---

## For Research Participants

If you're using this plugin for a research study:

1. **Keep the plugin active** for the entire study duration
2. **Start monitoring** at the beginning of each coding session
3. **Stop monitoring** at the end of each session
4. **Don't delete CSV files** - they'll be collected for analysis
5. **Report any issues** to the research team immediately

---

## Summary: Complete Workflow

```
┌─────────────────────────────────────────┐
│  1. Open CodeBlocks                     │
│  2. Click "Start Monitoring"            │
│     ↓                                   │
│  3. Code normally (monitored)           │
│     ↓                                   │
│  4. Data saved every 30 seconds         │
│     ↓                                   │
│  5. Click "Stop Monitoring"             │
│     ↓                                   │
│  6. CSV file complete ✓                 │
└─────────────────────────────────────────┘
```

**That's it!** The plugin handles all data collection automatically.
