# S-Curve Generator and Email Dispatcher

This repository provides a Python script designed to:
1. Prompt for user inputs (expected daily output and total working days).
2. Create a list based on these inputs.
3. Transform the list into an S-curve with configurable bounds.
4. Send the transformed data via email, along with a user-defined message.

---

## Table of Contents

- [Introduction](#introduction)
- [How It Works](#how-it-works)
  - [User Prompts](#user-prompts)
  - [S-Curve Transformation](#s-curve-transformation)
  - [Email Dispatch](#email-dispatch)
- [Running the Script](#running-the-script)
- [Customizing the Script](#customizing-the-script)
  - [Adjusting Bounds](#adjusting-bounds)
  - [Modifying Email Settings](#modifying-email-settings)
- [Dependencies](#dependencies)
- [License](#license)

---

## Introduction

This script is useful for scenarios where you need to simulate or forecast a gradual “ramp-up” and “ramp-down” pattern (i.e., an S-curve) for daily outputs over a specified number of days. After generating the curve, the script gives you the option to email the results to a designated recipient, making it ideal for reporting or updates.

---

## How It Works

### User Prompts
1. **Expected Working Average**: A floating-point number representing the average daily output you anticipate.
2. **Expected Working Days**: An integer specifying how many days you want to forecast.

The script constructs an initial list of daily outputs, each set to the **Expected Working Average**, repeated for the total **Expected Working Days**.

### S-Curve Transformation
The `transform_to_s_curve` function applies the following steps:
1. **Cumulative Sum**: Converts the baseline list into its cumulative sum.
2. **Normalization**: Scales the cumulative values to a [0, 1] range.
3. **Centering**: Computes a shifting factor to move the peak of the curve to around the middle.
4. **Modified Tanh**: Uses a hyperbolic tangent function (`tanh`) to transform the data into an S-shape.
5. **Peak and Tail Adjustments**: 
   - Adjusts the peak location toward the center of the timeline.
   - Applies a more aggressive decrease (“tail”) towards the end.
6. **Rescaling**: 
   - Re-scales the transformed curve to lie within user-defined bounds (`lowerBound` and `upperBound`).
   - Ensures the total of the transformed list matches the total of the original data.

### Email Dispatch
After generating the S-curve:
1. The script prompts you for an additional message to include in the email.
2. It appends the transformed data points to your message.
3. `sendEmail` is invoked to deliver the message via SMTP (configured for Gmail by default, but can be customized).

---

## Running the Script

1. **Clone or download** this repository.
2. **Install dependencies** (see [Dependencies](#dependencies)).
3. **Open a terminal** in the script directory.
4. **Run**:  
   ```bash
   python <script_name>.py
   Follow the prompts:
5. **Enter your expected average (float)**  
   **Enter your expected working days (integer)**  
   **Provide a custom message for the email when prompted**

