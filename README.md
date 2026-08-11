# ERPNext Timesheet Automation

A small automation tool for submitting timesheets to **ERPNext**.

This project was created after dealing with the repetitive frustration and issues that come with manually filling and submitting timesheets. The goal is simple: automate the process and let the computer suffer instead.

## Current Version

**Version:** `1.0`

This is the initial version and currently has a few limitations:

* No speech-to-text support yet.
* Designed for users assigned to **a single project**.
* Does not currently support users working across multiple projects.
* User-specific customization is limited.

Future versions may expand support for multiple projects and provide additional ways to enter timesheet information.

---

## Requirements

Make sure you have **Python** installed on your system.

Install the required Python packages:

```powershell
py -m pip install playwright pyinstaller
```

This is enough to run the script directly from an IDE or terminal.

---

## Running the Script

You can run the script directly using Python:

```powershell
py timesheet_script.py
```

However, if you want to create a standalone executable and configure it to run automatically as a scheduled task, follow the steps below.

---

## Creating the Executable

### 1. Configure Playwright

In PowerShell, set the Playwright browser path:

```powershell
$env:PLAYWRIGHT_BROWSERS_PATH="0"
```

### 2. Install Chromium

Install the Chromium browser required by Playwright:

```powershell
py -m playwright install chromium
```

### 3. Build the Executable

Use PyInstaller to package the script into a standalone executable:

```powershell
py -m PyInstaller --onefile --noconsole --collect-all playwright --name "ERPNext_Timesheet" timesheet_script.py
```

After the build completes, the executable will be located in:

```text
dist\ERPNext_Timesheet.exe
```

---

## Creating a Windows Scheduled Task

To automatically run the timesheet automation on specific weekdays, you can create a Windows Scheduled Task.

Open **PowerShell or Command Prompt as Administrator** and run:

```cmd
schtasks /create /tn "ERPNextTimesheetAuto" /tr "C:\Users\{your-user}\Documents\ERPNext_Timesheet.exe" /sc weekly /d MON,TUE,WED,THU,FRI /st {time-in-24-hour-format}
```

### Example

For a user named `Admin`, running the executable at **5:15 PM** every weekday:

```cmd
schtasks /create /tn "ERPNextTimesheetAuto" /tr "C:\Users\Admin\Documents\ERPNext_Timesheet.exe" /sc weekly /d MON,TUE,WED,THU,FRI /st 17:15
```

### Schedule Parameters

| Parameter                | Description                        |
| ------------------------ | ---------------------------------- |
| `/tn`                    | Name of the scheduled task         |
| `/tr`                    | Path to the executable to run      |
| `/sc weekly`             | Runs the task on a weekly schedule |
| `/d MON,TUE,WED,THU,FRI` | Runs Monday through Friday         |
| `/st 17:15`              | Start time in 24-hour format       |

> **Note:** Make sure the executable path is correct before creating the scheduled task.

---

## Managing the Scheduled Task

### Check the Task

To verify that the scheduled task exists:

```cmd
schtasks /query /tn "ERPNextTimesheetAuto"
```

### Delete the Task

If you want to remove the scheduled task:

```cmd
schtasks /delete /tn "ERPNextTimesheetAuto" /f
```

---

## Project Structure

A typical project structure looks like:

```text
ERPNext-Timesheet/
│
├── timesheet_script.py
├── README.md
│
└── dist/
    └── ERPNext_Timesheet.exe
```

---

## Notes

This project is primarily intended to automate a personal/repetitive workflow around ERPNext timesheet submission.

The current `1.0` release intentionally keeps the workflow simple and assumes that the user has **one assigned project**. Support for more complex timesheet scenarios can be added in future versions.
