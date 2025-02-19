# Video Tagging and Extraction Scripts

This repository contains two Python scripts for working with a **SQLite database** (`.ritt` format) that stores metadata for video files. The scripts allow filtering, extracting, and organizing `.mp4` files based on their tags.

## Table of Contents
- **Scripts Overview**
- **Installation**
- **Usage**
- **Script Details**
  - `tag_filter_ritt.py`
  - `extract_videos&tags.py`
- **Requirements**

---

## Scripts Overview

| Script | Purpose |
|--------|---------|
| **`tag_filter_ritt.py`** | Filters and retrieves `.mp4` files based on **specific tags** in the database. |
| **`extract_videos&tags.py`** | Extracts video-tag relationships and organizes them into **categories**, saving the results in a CSV file. |

---

## Installation

1. Clone this repository:

   **git clone <repository-url>**  
   **cd <repository-folder>**

2. Install required dependencies:

   **pip install -r requirements.txt**

---

## Usage

### Running `tag_filter_ritt.py`:

**python tag_filter_ritt.py**

This script:
- Connects to the **SQLite database** (`.ritt`).
- Filters **video files** that match a **specific set of tags**.
- Searches for corresponding `.mp4` files in a given directory.
- Prints the **matching files and their counts**.

### Running `extract_videos&tags.py`:

**python extract_videos&tags.py**

This script:
- Extracts all **videos and their associated tags** from the **SQLite database**.
- Categorizes the extracted tags into predefined **families** (e.g., shot type, quality, lighting conditions).
- Searches for the corresponding `.mp4` files.
- Saves the organized data into a CSV file.

---

## Script Details

### `tag_filter_ritt.py`
This script is designed to **filter video files** based on specific **tags** stored in the SQLite database. It performs the following steps:

1. **Connects to the SQLite database** and searches for records that match the provided tags.
2. **Extracts video file names** associated with the matching tags.
3. **Searches for `.mp4` files** in the specified directory.
4. **Prints the list of matching files** along with the number of times each file appears.

This script is useful when you need to **retrieve a subset of videos** from a large dataset based on specific filtering criteria.

---

### `extract_videos&tags.py`
This script is designed to **extract video-tag relationships** and save them into a structured CSV file. It performs the following steps:

1. **Extracts all videos and their IDs** from the SQLite database.
2. **Extracts all available tags** and associates them with their corresponding videos.
3. **Categorizes the extracted tags** into predefined families:
   - Camera angle (e.g., orbital, higher, lower)
   - Shot type (e.g., close-up, panoramic)
   - Environment (e.g., indoor, outdoor)
   - Lighting conditions (e.g., backlight, shadows)
   - Quality (e.g., poor, best)
   - Camera movement (e.g., static, dynamic)
   - Density (e.g., low, high)
4. **Finds the corresponding `.mp4` files** in the directory.
5. **Saves the results in a CSV file** for further analysis.

This script is useful when you need a structured dataset that links **videos to their descriptive tags**.

---

## Requirements

- **Python 3.x**
- **SQLite3**
- **JSON support** (built-in)
- **CSV support** (built-in)
- **OS module** (built-in)

Ensure that your `.ritt` database file and `.mp4` footage are accessible from the paths specified in the scripts.

---

## Notes

- If the **database file is missing**, the scripts will **raise an error**.
- If any `.mp4` file is **not found**, it will be **skipped**.
- The **CSV output** is generated in the script's directory and can be modified to save elsewhere.

---

## Author
Developed for **video metadata processing** and **automatic tagging**.
