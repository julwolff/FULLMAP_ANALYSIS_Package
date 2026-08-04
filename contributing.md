# Contributing to FULLMAP_ANALYSIS_Package

Thank you for contributing to FULLMAP_ANALYSIS_Package.

This document describes the recommended workflow for adding new features, analyses, and improvements.

---

# Development Workflow

## 1. Create a dedicated branch

Never work directly on `main`.

Before starting any development, create a dedicated branch:

```bash
git checkout main
git pull

git checkout -b my_new_feature
```

Examples:

```bash
git checkout -b add_bond_analysis
```

```bash
git checkout -b improve_xrd_module
```

```bash
git checkout -b bugfix_site_assignment
```

When your work is complete:

```bash
git add .
git commit -m "Add bond analysis"
git push origin add_bond_analysis
```

Then create a Pull Request on GitHub.

---

# Project Structure

All source code is located under:

```text
src/
│
├── analysis/
│   ├── dynamics/
│   ├── structure/
│   ├── thermodynamics/
│   └── sites/
│
├── averaging/
│
├── analysis.py
│
└── average_analysis.py
```

---

# Adding a New Analysis

## Step 1: Create the analysis module

All scientific analyses must be implemented inside:

```text
src/analysis/
```

Choose the appropriate category.

### Dynamics

```text
src/analysis/dynamics/
```

Examples:

```text
msd.py
jumps.py
residence.py
```

### Structure

```text
src/analysis/structure/
```

Examples:

```text
rdf.py
coordination.py
distortion.py
xrd.py
```

### Thermodynamics

```text
src/analysis/thermodynamics/
```

Examples:

```text
energy.py
```

### Sites

```text
src/analysis/sites/
```

Examples:

```text
create_sites.py
assign_sites.py
occupancy.py
defects.py
```

---

## Step 2: Export the function

Each package contains an `__init__.py`.

Example:

```python
# src/analysis/structure/__init__.py

from .rdf import *
from .coordination import *
from .distortion import *
from .xrd import *
```

When adding:

```text
bond_lengths.py
```

update:

```python
from .bond_lengths import *
```

---

## Step 3: Add a selection flag

Edit:

```text
src/config/analysis_selection.py
```

and create a switch:

```python
RUN_BOND_LENGTHS = True
```

Example:

```python
RUN_RDF = True
RUN_XRD = True
RUN_BOND_LENGTHS = True
```

This allows users to activate or deactivate the analysis without modifying the code.

---

## Step 4: Add configuration variables

If your analysis requires parameters, add them to:

```text
src/config/analysis_config.py
```

Example:

```python
BOND_CUTOFF = 3.0
```

or

```python
VACANCY_RADIUS = 1.5
```

All user-tunable parameters must be stored here.

Avoid hardcoding analysis parameters inside modules.

---

## Step 5: Register the analysis in analysis.py

Edit:

```text
src/analysis.py
```

Import the new function:

```python
from src.analysis.structure import *
```

or explicitly:

```python
from src.analysis.structure import (
    compute_bond_lengths
)
```

Then add the execution block:

```python
if RUN_BOND_LENGTHS:

    compute_bond_lengths(
        u,
        cutoff=BOND_CUTOFF
    )
```

---

# Adding a New Averaging Routine

If the analysis creates a new output format requiring specific averaging rules:

## Step 1

Create a corresponding averaging module inside:

```text
src/averaging/
```

Example:

```text
bond_lengths.py
```

## Step 2

Export the new averaging function in:

```python
# src/averaging/__init__.py

from .bond_lengths import *
```

## Step 3

Add an entry to:

```text
src/config/averaging_selection.py
```

Example:

```python
AVERAGING = {

    ...

    "bond_lengths": True
}
```

## Step 4

Register the averaging routine inside:

```text
src/average_analysis.py
```

Example:

```python
if AVERAGING.get(
    "bond_lengths",
    False):

    average_bond_lengths(...)
```

---

# Output Files

Every analysis should write its results into the current structure directory.

Examples:

```text
msd_Li.dat

rdf_evolution.dat

energy.dat

site_occupancy.dat

jump_matrix.dat
```

Output files should:

- be human-readable
- contain a descriptive header
- have stable formats between versions

Example:

```text
# Time(ps) MSD(A²)

0.000 0.000
0.020 0.001
...
```

---

# Naming Rules

Use:

```python
compute_xxx()
```

for analysis functions.

Examples:

```python
compute_rdf()
compute_xrd_series()
compute_site_occupancy()
```

Use:

```python
average_xxx()
```

for averaging functions.

Examples:

```python
average_xrd()
average_jump_matrix()
```

---

# Testing

Whenever possible:

1. Run the analysis on a small test structure.
2. Check that output files are generated.
3. Verify that averaging works correctly.
4. Ensure that no existing analysis is broken.

A dedicated test case should be added whenever a new analysis type is introduced.

---

# Coding Guidelines

## Keep modules focused

Each module should perform one specific task.

Good:

```text
rdf.py
```

contains RDF-related functions only.

Avoid:

```text
rdf.py
```

containing RDF, MSD, XRD and site analyses together.

---

## Avoid hardcoded parameters

Bad:

```python
cutoff = 2.5
```

inside the analysis script.

Good:

```python
cutoff = CUTOFF_MNO
```

defined in:

```text
src/config/analysis_config.py
```

---

## Use configuration files

All user-editable quantities should be located in:

```text
src/config/
```

This includes:

- cutoffs
- trajectory names
- XRD settings
- timestep
- site assignment radius
- analysis switches

---

## Preserve output compatibility

Whenever possible, maintain the format of existing output files to avoid breaking downstream workflows and averaging routines.

---

## Write documentation

All public functions should contain:

```python
"""
Short description.

Parameters
----------
...

Returns
-------
...
"""
```

---

# Typical Workflow for Adding a New Analysis

Suppose a contributor wants to add a bond-length analysis.

1. Create:

```text
src/analysis/structure/bond_lengths.py
```

2. Export it:

```python
from .bond_lengths import *
```

inside:

```text
src/analysis/structure/__init__.py
```

3. Add:

```python
RUN_BOND_LENGTHS = True
```

to:

```text
src/config/analysis_selection.py
```

4. Add:

```python
BOND_CUTOFF = 3.0
```

to:

```text
src/config/analysis_config.py
```

5. Register execution in:

```text
src/analysis.py
```

6. If averaging is required:

   - create

```text
src/averaging/bond_lengths.py
```

   - export it in

```text
src/averaging/__init__.py
```

   - add

```python
"bond_lengths": True
```

to:

```text
src/config/averaging_selection.py
```

   - register it in:

```text
src/average_analysis.py
```

7. Test on a small dataset.

---

# Thank You

Thank you for helping improve FULLMAP_ANALYSIS_Package.

Contributions, bug reports, feature requests, documentation improvements, and new scientific analyses are all welcome.