# 🧠 RAM Timing Viewer for Intel CPUs 🧠

A **lightweight** and **intuitive** tool designed to give you real-time insights into the **RAM timings** of Intel CPUs. Whether you're an enthusiast tweaking your memory settings or a casual user curious about your DDR modules, this tool makes it easy to monitor and understand how your RAM is performing.

This viewer supports **Intel 12th, 13th, and 14th generation** processors, and future Intel CPU generations may also be supported (fingers crossed 🤞).

> ⚠️ **Note:** Currently, this tool is **Intel-only** and does **not support AMD platforms**.

---

## 🚀 Features

- 🔍 **Comprehensive Memory Timings:** View detailed information about your memory timings, including **Primary**, **Secondary**, and **Tertiary** timings.
- 💾 **DDR4 & DDR5 Support:** Whether you're using DDR4 or DDR5 RAM, this tool supports both generations of memory.
- 📊 **Real-time Data Display:** Instantly see your RAM timings in a clean, easy-to-read format.
- 🧩 **Minimal & Clean UI:** Focus on what's important, with a simple and user-friendly interface.
- 🔒 **Fully Offline:** No data collection. All the information is stored locally on your machine, ensuring privacy and security.
- 📁 **Open Source:** Free to use, contribute to, or modify. Hosted on [GitHub](link-to-repo).

---

## 💻 Supported Platforms

The tool is designed to work with the following Intel CPU generations:

| Generation          | Supported  | Notes                                  |
|---------------------|------------|----------------------------------------|
| Intel 10th Gen & Below | ❌         | Not supported. Older Intel CPUs not compatible. |
| Intel 12th Gen (Alder Lake) | ✅       | Full support for 12th gen (Alder Lake). |
| Intel 13th Gen (Raptor Lake) | ✅       | Full support for 13th gen (Raptor Lake). |
| Intel 14th Gen (Raptor Lake Refresh) | ✅ | Full support for 14th gen (Raptor Lake Refresh). |
| Future Intel Generations | 🚧        | Ongoing testing, may work for future releases. |

**Note:** Future Intel generations may require updates to ensure compatibility. Stay tuned for updates and improvements!

---

## 🛠️ Installation for Source Code

If you want to run the **RAM Timing Viewer** from the source code, you can follow the steps below.

### Prerequisites:

Before running the tool, ensure you have the following installed:

- **Python 3.x** (preferably the latest stable release).
- Required Python libraries:
  - `customtkinter` – for the graphical user interface.
  - `wmi` – for Windows Management Instrumentation (to fetch system data).
  - `pyinstaller` – for packaging the application (if you want to compile it yourself).

To install the dependencies, run:

```bash
pip install customtkinter wmi pyinstaller
