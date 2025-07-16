# 🔬 Acoustic Nucleation Rhythm Labeling and Analysis for Cryogenic Boiling Events

This repository contains the tools, visualizations, and statistical analyses used in the study **"Influence of Concurrent Boiling Events on Acoustic Nucleation Rhythms in Cryogenic Systems"**. The study investigates how multiple boiling sources interact and affect the timing and consistency of bubble nucleation in cryogenic environments using acoustic signal data.

### 📘 Reference Paper

Read the full research paper here:  
👉 **[Influence of Concurrent Boiling Events on Acoustic Nucleation Rhythms in Cryogenic Systems](https://AndrewJMart.github.io/AcousticConcurrentBoiling/Influence_of_Concurrent_Boiling_Events_on_Acoustic_Nucleation_Rhythms_in_Cryogenic_Systems.pdf)**

> **Martinez, Andrew**  
> *California Polytechnic State University, 2025*

This paper outlines the motivation, methodology, statistical analysis, and results behind the acoustic boiling interference study using manually labeled cryogenic experiments.


## 🧠 Project Summary

Cryogenic boiling experiments produce acoustic signals that reveal rhythmic patterns of bubble formation. This project provides a manual labeling tool and analysis pipeline to explore how the presence of multiple boiling sources affects the regularity of these events.

Key contributions:
- Interactive **Dash app** for manually labeling nucleation events.
- Group-wise statistical analysis on **inter-nucleation intervals**.
- Visual and quantitative evidence that concurrent boiling disrupts rhythmic consistency.
- Companion paper and exploratory data notebook included.

---

## 📂 Repository Structure

```
.
├── DashLabeler.py                # Dash app for manual peak labeling
├── HandLabeledData/             # Directory where labeled peaks are saved
├── SortedData/                  # Raw time-series data from boiling experiments
├── DataExploration.ipynb        # Jupyter notebook for data analysis and visualization
├── Influence_of_Concurrent_...  # Full paper PDF describing the methodology and results
└── README.md                    # Project overview (this file)
```

---

## 🛠 Features

### 📊 Dash Labeling Tool
- Load and visualize acoustic signals.
- Manually tag peaks by rhythmic group (e.g., Rhythm 1, Rhythm 2).
- Zoom, pan, and interact with signals.
- Save labeled peaks to CSV with timestamps and amplitude values.

### 📈 Statistical Analysis
- Compare standard deviations of inter-nucleation intervals across:
  - Single Rhythm
  - Dominant Rhythm
  - Lesser Rhythm
  - Rhythm with Random Interference
- Use of Shapiro-Wilk, Levene’s test, and Mann–Whitney U test to determine significance.

### 📁 Hand-Labeled Data
CSV exports contain structured peak data per experimental run, preserving the original folder structure for easy access and reproducibility.

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Install dependencies:
  ```bash
  pip install dash plotly pandas
  ```

### Run the App

```bash
python DashLabeler.py
```

Then open your browser to `http://127.0.0.1:8050`.

Ensure that the `./SortedData/` folder contains subfolders with CSV runs before launching.

---

## 📘 Reference Paper

> **Martinez, Andrew.**  
> *"Influence of Concurrent Boiling Events on Acoustic Nucleation Rhythms in Cryogenic Systems."*  
> California Polytechnic State University, 2025.

PDF included in this repository.

---

## 📈 Results Summary

- **Single-source boiling** produces the most consistent nucleation rhythms.
- **Concurrent boiling sources** introduce significant variability.
- Statistical evidence supports that **rhythmic interference** is real and measurable.

These findings may inform safer and more effective cryogenic fuel monitoring systems for spaceflight applications.

---

## 📬 Contact

For questions or collaborations, reach out to:  
**Andrew Martinez**  
📧 amart89531@gmail.com

---

## 🧪 Acknowledgements

This work was supported by research collaborations with NASA and Cal Poly San Luis Obispo.
