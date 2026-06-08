========================================
FOR RESEARCHERS - QUICK START GUIDE
========================================

This folder contains everything needed for participant data collection.

========================================
DEPLOYMENT STEPS
========================================

1. ADMINISTER PRE-SURVEY
   - Have the participant fill out the pre-survey form
   - This establishes their baseline programming experience and baseline anxiety

2. COPY TO PARTICIPANT PC
   - Copy this entire folder to participant's Desktop
   - No installation needed

3. RUN VERIFICATION (RECOMMENDED)
   - Double-click: VERIFY_SETUP.bat
   - Checks Python and folder permissions
   - Fix any errors before proceeding

4. START DATA COLLECTION
   - Participant double-clicks: START_CLEAN_COLLECTOR.bat
   - Black window opens and stays open
   - They open CodeBlocks and code normally

5. COLLECT DATA AFTER SESSION
   - Participant presses Ctrl+C to stop
   - Navigate to: Documents\AnxietyMonitorData\
   - Copy CSV file: data_YYYYMMDD.csv
   - Rename immediately: P[ID]_data_YYYYMMDD.csv

6. ADMINISTER POST-SURVEY
   - Have the participant fill out the post-survey immediately after coding
   - This provides the ground truth stress label for machine learning

========================================
FILES IN THIS FOLDER
========================================

READ_ME_FIRST.txt
  → Participant instructions (give them this)

START_CLEAN_COLLECTOR.bat
  → Main launcher (they double-click this)

VERIFY_SETUP.bat
  → Pre-flight check (run first)

clean_collector.py
  → Data collector (don't edit)

PARAMETER_GUIDE.txt
  → Technical documentation (for you)

DATA_COLLECTION_APPROACH.txt
  → Research methodology (for papers)

README_RESEARCHER.txt
  → This file

========================================
REQUIREMENTS
========================================

✓ Windows 10 or 11
✓ Python 3.6+ installed
✓ CodeBlocks installed
✓ 50 MB free disk space

========================================
WHAT GETS COLLECTED
========================================

18 parameters every 30 seconds:
- Typing speed, latency, backspace rate
- Window focus, file name, language
- Compile attempts, success rate
- Pause ratio, session fragmentation
- Anxiety score (0-100), risk level

NO code content or keystrokes are logged.

========================================
CSV OUTPUT LOCATION
========================================

Path: C:\Users\[Username]\Documents\AnxietyMonitorData\
File: data_YYYYMMDD.csv (one file per day)

Format: UTF-8 CSV with 18 columns
Update: Every 30 seconds while CodeBlocks is active

========================================
TROUBLESHOOTING
========================================

"Python is not recognized"
→ Install Python: https://python.org
→ During install, check "Add Python to PATH"

"PermissionError"
→ Close CSV file if open in Excel
→ Check folder permissions

No data appearing
→ Verify CodeBlocks is active (window title says "CodeBlocks")
→ Type in CodeBlocks to generate keystrokes
→ Wait 30 seconds for first data row

Anxiety score always 0
→ Normal at start - needs keystrokes to calculate
→ Wait 2-3 minutes for meaningful scores

========================================
DATA QUALITY CHECKS
========================================

After collection, verify:
☑ CSV has more than 1 row (header + data)
☑ keystrokes_total is increasing
☑ window_focused shows TRUE when appropriate
☑ timestamp shows continuous 30-second intervals

========================================
RESEARCH VALIDATION
========================================

This collector implements metrics from:
- Lau (2018): Keystroke dynamics (89.5% accuracy)
- Yu et al. (2025): Anxiety ML model (97.8% accuracy)
- Becker (2016): Compiler error metrics
- Perera (2023): Real-time stress detection (83.6% accuracy)

See PARAMETER_GUIDE.txt for detailed metric definitions.

========================================
SUPPORT
========================================

For deployment issues:
- Check VERIFY_SETUP.bat output
- Review participant instructions
- Test on your own machine first

For research questions:
- See DATA_COLLECTION_APPROACH.txt
- Refer to implementation_plan.md (if available)
- Contact: [Your contact information]

========================================
VERSION INFO
========================================

Version: 1.0 (Research-Validated)
Date: January 2026
Status: Deployment-ready
