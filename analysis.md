## Purpose

This document describes the analyses that can be used to study molecular-dynamics (MD) simulations of lithium manganese oxide, particularly Li₂MnO₃, with varying lithium-vacancy concentrations.

It is intended as a user-facing catalogue: a researcher should be able to identify what an analysis measures, what scientific question it answers, which data it needs, and which results it produces without reading the source code first.

> **Implementation and filename note**
>
> The exact analysis scripts, command-line options, and output filenames have not yet been audited against the complete software repository. Consequently, filenames shown below are **suggested logical names or common input conventions**, not a guarantee that the current implementation already uses them. The site-assignment format described in the relevant section reflects the data format discussed for this project. Before this document is published as a definitive reference, each entry should be checked against the corresponding script and tested on a representative dataset.
>
> Analyses are labelled as:
> - **Core candidate** — directly relevant to the current Li₂MnO₃ workflow and previously discussed for this project.
> - **Optional extension** — scientifically useful, but should only be described as available in the software after an implementation and validation check.

---

## 1. Overview

| Analysis | Main scientific question | Typical required data | Main results |
|---|---|---|---|
| Site occupation | Which crystallographic sites are occupied by Li and Mn? | Site-assignment data; site reference | Site populations, occupation fractions, time series |
| Antisite analysis | Do Li and Mn occupy sites normally associated with the other species? | Site-assignment data with atom and site species | Antisite counts and fractions |
| Local composition analysis | What is the local chemical composition around a site, atom, or region? | Structure or trajectory; neighbourhood definition | Local composition counts, fractions, and distributions |
| Coordination analysis | How many neighbours of each species surround each atom? | Trajectory or structure; cutoff or neighbour definition | Coordination-number distributions and time series |
| Structural parameters | How does the structure evolve during heating, cooling, or production MD? | Trajectory and/or thermodynamic log | Lattice/geometry descriptors, structural time series |
| Simulated X-ray diffraction (XRD) | How does the predicted diffraction pattern change with temperature or defects? | Structure or representative trajectory frames | Diffraction pattern and peak positions/intensities |
| Li mean-squared displacement (MSD) | How far do Li ions move over time? | Time-ordered trajectory with atom identities | MSD curves, optionally resolved by species or direction |
| Li diffusion coefficient | What is the effective Li diffusivity over a selected time interval? | MSD data or trajectory; timestep and sampling interval | Diffusion coefficient and fit diagnostics |
| Site-transition matrix | Which crystallographic sites do Li ions move between? | Time-resolved site assignments | Transition counts and probabilities |
| Migration network | Which site-to-site pathways are used most often? | Site-transition data; site labels/coordinates | Network, edge weights, normalized transition frequencies |
| Jump frequency | How often do Li ions perform identified site-to-site jumps? | Time-resolved site assignments; frame interval | Jump counts and rates |
| Structure–transport correlation | How do defects or structural descriptors relate to Li mobility? | Structural/occupation data and transport metrics | Comparative tables and correlation plots |
| Energy and temperature monitoring | Did the simulation remain thermally and numerically well behaved? | MD thermodynamic log | Energy/temperature time series and summary statistics |

The actual set of available analyses depends on the scripts installed in the software. An entry in this catalogue is not, by itself, proof that the corresponding analysis is already implemented.

---

## 2. Shared input data and conventions

### 2.1 Molecular-dynamics trajectory

A trajectory contains atomic positions across simulation frames and, depending on the file format, may also contain atom types, cell vectors, velocities, or other per-frame properties.

**Typical formats:** LAMMPS dump, extended XYZ, XDATCAR, or another trajectory format supported by the analysis scripts.

**Used by:** MSD and diffusion, coordination, structural evolution, simulated XRD from selected frames, and potentially local-composition analysis.

**Important requirements:**
- Atom identities must remain consistent between frames for displacement and jump tracking.
- The simulation cell and periodic-boundary information must be available for correct minimum-image distances and unwrapped displacements.
- The timestep and trajectory output interval must be known to convert frame indices into physical time.
- A trajectory should be divided into appropriate thermal or dynamical windows when the simulation protocol includes heating, cooling, and production stages. Combining these stages into one transport fit can produce misleading results.

### 2.2 Site-assignment data

Site-assignment data map each atom in each frame to a crystallographic site or site class. This is essential for occupation, antisite, jump, and migration-network analyses.

A previously discussed table had a header resembling:

```text
# Frame AtomID AtomType SiteID Distance SiteType
```

However, example rows contained seven fields, for example:

```text
0 1 Li 0 Li 0.140181 108a
```

The data should therefore be interpreted according to the actual writer used to generate it, rather than relying on the header alone. The likely seven-column interpretation is:

| Column | Meaning | Example |
|---|---|---|
| `Frame` | Trajectory frame index | `0` |
| `AtomID` | Persistent atom identifier | `1` |
| `AtomType` | Actual species of the atom | `Li` |
| `SiteID` | Identifier of the assigned site | `0` |
| `SiteAtomType` | Species normally associated with the reference site | `Li` |
| `Distance` | Atom-to-site assignment distance, in the writer's distance unit | `0.140181` |
| `SiteType` | Crystallographic site label | `108a` |

**Required validation:** confirm this interpretation against the file-producing script. In particular, do not confuse `AtomType` with `SiteAtomType`: their comparison is what allows an antisite to be identified.

**Typical filename:** `site_assignment.dat` (use the actual generated filename if it differs).

### 2.3 Reference-site data

A reference-site file describes the expected crystallographic sites, their labels, coordinates, and—where relevant—the species normally associated with each site.

**Typical information:** site ID, species, crystallographic label (for example, `108g`, `108h`, `54b`, or `54c`), and reference coordinates.

**Used by:** site assignment, occupation, antisite, transition, and migration-network analyses.

The reference structure must use a coordinate system and periodic cell consistent with the trajectory. If the simulation reconstructs strongly or changes cell dimensions, the assignment method and reference may need special treatment.

### 2.4 Thermodynamic log

An MD log commonly contains step number, time, temperature, potential energy, total energy, pressure, and other engine-dependent quantities.

**Used by:** thermal stability checks and the segmentation of heating, cooling, equilibration, and production intervals.

**Typical filename:** `log.lammps` for a LAMMPS run; other engines use different names and formats.

### 2.5 Structure file

A structure file represents one configuration, usually the initial structure, a minimized structure, or a selected trajectory frame.

**Typical formats:** CIF, POSCAR/CONTCAR, LAMMPS data, or XYZ accompanied by cell information.

**Used by:** structural descriptors, coordination analysis, and simulated XRD.

---

## 3. Site occupation analysis

**Status:** Core candidate

### What it measures

Site occupation analysis determines which species occupy the crystallographic sites during the simulation. For Li₂MnO₃, it can track the occupation of Li-associated and Mn-associated sites, and separate the results by crystallographic site class.

Possible quantities include:
- number of Li atoms assigned to each site class;
- number of Mn atoms assigned to each site class;
- occupation fraction for each species and site class;
- fraction of sites that are occupied, where vacancies are explicitly represented;
- time evolution of occupation during heating, cooling, or production.

### Scientific questions

- Does the initial site distribution persist during thermal treatment?
- At what stage does cation rearrangement become apparent?
- Are some site classes more frequently occupied by a given species?
- Does changing the Li-vacancy concentration alter the occupation statistics?

### Required input

- **Required:** time-resolved site-assignment data, such as `site_assignment.dat`.
- **Required for interpretation:** the column definitions and site labels used by the assignment writer.
- **Optional:** reference-site data if the assignment file does not contain enough site information.

### Outputs

Suggested outputs (confirm actual names in the implementation):
- `site_occupation.csv` — counts or fractions by frame, species, and site class;
- `site_occupation_summary.csv` — averages over a selected frame or time window;
- `site_occupation.png` — occupation time series or summary plot.

### Interpretation notes

State whether reported fractions are normalized by all reference sites, occupied sites only, or atoms of a given species. These definitions are not interchangeable, especially when vacancies are present. The selected time window should also be reported.

---

## 4. Antisite analysis

**Status:** Core candidate

### What it measures

An antisite is an atom occupying a site normally associated with another species. For a Li/Mn system, an atom assigned to a site whose reference species differs from the atom's actual species is an antisite according to the chosen assignment model.

For the seven-column site-assignment interpretation above, the basic comparison is:

```text
AtomType != SiteAtomType
```

This comparison should only be used after confirming the file schema and the meaning of `SiteAtomType`.

### Scientific questions

- How many Li-on-Mn-site and Mn-on-Li-site assignments occur?
- Does antisite disorder increase during heating?
- Does the system retain disorder after cooling?
- How does antisite prevalence depend on initial vacancy concentration?

### Required input

- **Required:** site-assignment data containing both actual atom species and reference-site species.
- **Recommended:** frame indices and persistent atom IDs, to follow changes over time.

### Outputs

Suggested outputs:
- `antisite_counts.csv` — counts by antisite type and frame;
- `antisite_fractions.csv` — normalized fractions with the normalization definition documented;
- `antisite_evolution.png` — time evolution of antisite counts or fractions.

### Limitations

A geometric assignment does not by itself prove a stable crystallographic defect. At high temperature, atoms may be displaced far from ideal sites, and the classification can depend on the assignment cutoff, site definition, and handling of vacancies. Report these parameters and inspect borderline assignments.

---

## 5. Local composition analysis

**Status:** Core candidate / implementation details to verify

### What it measures

Local composition analysis characterizes the chemical makeup of a local environment. Depending on the implemented definition, the local environment may be defined around a crystallographic site, an atom, a fixed-radius sphere, a neighbour shell, or a spatial region.

Possible quantities include:
- counts of Li, Mn, and O within the selected environment;
- normalized local species fractions;
- differences in local composition between vacancy concentrations;
- distributions of local environments across sites or frames.

### Scientific questions

- Do vacancies occur in chemically distinct local environments?
- Is the local Li/Mn/O composition spatially heterogeneous?
- Does local composition correlate with antisite disorder or Li mobility?
- Are particular environments associated with frequently used migration pathways?

### Required input

The precise input depends on how the current LCA implementation defines a local environment. Typical requirements are:
- a structure or trajectory with atomic coordinates and species;
- periodic-cell information;
- a neighbourhood definition (distance cutoff, neighbour count, or site-based rule);
- optionally, reference-site or site-assignment data.

If the existing script uses a precomputed local-environment file, that file must be documented explicitly.

### Outputs

Suggested outputs:
- `local_composition.csv` — local species counts or fractions;
- `local_composition_summary.csv` — distributions or averages grouped by site/environment;
- `local_composition.png` — optional plots.

### Limitations

Local-composition results depend on the neighbourhood definition and cutoff. Different definitions can lead to different counts, particularly in distorted structures. Always record the cutoff or neighbour rule and whether periodic boundaries are applied.

---

## 6. Coordination analysis

**Status:** Optional extension unless an existing script is confirmed

### What it measures

Coordination analysis counts neighbours around each atom, often separated by species. For example, it can determine the number of oxygen neighbours around Li or Mn, or the number of Li neighbours around a selected site.

Possible outputs include coordination-number distributions, average coordination numbers, and changes in coordination over time.

### Required input

- A structure or trajectory with species, coordinates, and cell information.
- A documented distance cutoff or a defined neighbour-finding method.
- Optionally, site assignments to group atoms by crystallographic site.

### Outputs

Suggested outputs:
- `coordination.csv` — per-frame or per-atom coordination values;
- `coordination_summary.csv` — distributions and averages;
- `coordination.png` — coordination distributions or time series.

### Limitations

A single cutoff can be inappropriate for multiple pair types. Cutoffs should be justified using pair-distribution functions or structural knowledge. Thermal vibrations may cause rapid switching around the cutoff; time-averaging or a hysteresis criterion may be needed for event-based interpretations.

---

## 7. Structural evolution and structural parameters

**Status:** Core candidate / exact descriptors to verify

### What it measures

Structural analysis monitors how the configuration evolves during minimization, heating, cooling, and production. Depending on the available data and implementation, descriptors may include:
- cell lengths, angles, and volume;
- selected bond-length or interatomic-distance distributions;
- changes in local coordination;
- deviations from the initial or reference structure;
- temperature-dependent structural changes.

### Required input

- A trajectory or a sequence of structure files.
- Cell information for each frame if the cell changes.
- Optionally, a thermodynamic log to align structural changes with temperature and energy.

### Outputs

Suggested outputs:
- `structural_parameters.csv` — descriptors versus frame or time;
- `structural_summary.csv` — statistics for a selected interval;
- `structural_evolution.png` — time series or comparison plots.

### Limitations

A structural descriptor is not automatically a phase identification. Significant claims about phase transitions or long-range order may require additional analyses, such as diffraction, symmetry analysis, or comparison with validated reference structures.

---

## 8. Simulated X-ray diffraction (XRD)

**Status:** Core candidate previously discussed; verify implementation and method

### What it measures

Simulated XRD estimates a diffraction pattern from a crystal structure. Comparing patterns from initial, minimized, heated, or cooled configurations can help identify changes in lattice structure, peak positions, and relative intensities.

### Scientific questions

- Does the structure retain its characteristic diffraction features after thermal treatment?
- Do defects or vacancy concentrations alter peak positions or intensities?
- Are there signs consistent with structural rearrangement?

### Required input

- A structure file or selected trajectory frames.
- Lattice parameters and atomic species/coordinates.
- Radiation wavelength and calculation settings, if required by the implementation.

A single instantaneous MD frame may contain substantial thermal disorder. For meaningful comparisons, consider representative configurations, time-averaged approaches where appropriate, and consistent diffraction settings across systems.

### Outputs

Suggested outputs:
- `xrd_pattern.csv` — scattering angle or reciprocal-space coordinate and intensity;
- `xrd_pattern.png` — simulated diffraction plot;
- `xrd_comparison.png` — overlay of multiple structures or vacancy concentrations.

### Limitations

A simulated pattern depends on the structural model, radiation wavelength, thermal disorder treatment, and intensity approximation. Peak changes should not be assigned to a new phase without supporting evidence.

---

## 9. Lithium mean-squared displacement (MSD)

**Status:** Core candidate

### What it measures

The mean-squared displacement quantifies the average squared displacement of a selected set of atoms from their positions at a reference time:

\[
\mathrm{MSD}(t) = \left\langle |\mathbf{r}_i(t_0+t)-\mathbf{r}_i(t_0)|^2 \right\rangle_{i,t_0}.
\]

For Li₂MnO₃, the analysis normally focuses on Li atoms to investigate ionic mobility. Depending on the implementation, MSD may be calculated for all Li atoms or for selected groups.

### Scientific questions

- Is Li motion predominantly localized or diffusive over the sampled interval?
- Does Li mobility change with vacancy concentration?
- Is mobility different during heating, cooling, and production?
- Is motion anisotropic along different crystallographic directions?

### Required input

- A time-ordered trajectory containing Li coordinates and persistent atom identities.
- Simulation cell and periodic-boundary information.
- Timestep and trajectory frame interval.
- Correct handling of periodic boundary crossings, preferably through unwrapped coordinates or a validated displacement algorithm.
- A clearly defined time window.

### Outputs

Suggested outputs:
- `li_msd.csv` — MSD versus time;
- `li_msd.png` — MSD curve;
- `li_msd_components.csv` — optional directional components.

### Limitations

The MSD depends strongly on the selected time interval. Short-time vibrational motion can obscure long-time diffusion, while a short trajectory may not sample enough migration events. Periodic-boundary errors or inconsistent atom IDs can invalidate displacement estimates.

---

## 10. Lithium diffusion coefficient

**Status:** Core candidate; verify fitting implementation

### What it measures

The diffusion coefficient is commonly estimated from the long-time slope of the MSD using the Einstein relation. In three dimensions:

\[
D = \frac{1}{6}\frac{d\,\mathrm{MSD}(t)}{dt}.
\]

For a direction-specific analysis, the corresponding dimensionality and formula must be stated.

### Required input

- An MSD curve produced with a validated displacement calculation, or a trajectory from which MSD can be calculated.
- Time units, distance units, and the dimensionality of the fit.
- A defined fitting interval in the diffusive regime.

### Outputs

Suggested outputs:
- `li_diffusion_summary.csv` — fitted diffusion coefficient and units;
- `li_diffusion_fit.png` — MSD with the selected fit interval and fitted line;
- `li_diffusion_diagnostics.txt` — optional fit range, slope, uncertainty, and quality indicators.

### Limitations

The MSD should be approximately linear over the chosen fit interval. A fitted slope from a non-linear or poorly sampled regime is not a reliable diffusion coefficient. Report the fit interval, uncertainty estimate, trajectory duration, temperature, and number of independent runs where possible. Do not compare coefficients obtained with inconsistent time windows or unit conventions.

---

## 11. Site-transition analysis

**Status:** Core candidate

### What it measures

Site-transition analysis tracks changes in the crystallographic site assigned to each atom between successive sampled frames. For Li transport, transitions can be counted between site classes such as `108g`, `108h`, `54b`, and `54c`, provided those labels match the reference-site definition used for the structure.

The analysis may produce:
- transition counts from one site class to another;
- transition matrices;
- row-normalized transition probabilities;
- time-dependent transition statistics.

### Scientific questions

- Which site-to-site transitions are observed?
- Which transitions are most frequent?
- Does the transition pattern change with temperature or vacancy concentration?
- Are some site classes mainly origins, destinations, or intermediate states?

### Required input

- Time-resolved site assignments.
- Persistent atom IDs so that the same Li atom can be followed across frames.
- Frame interval and, for rates, the physical time represented by each interval.
- Consistent site labels across all frames.

### Outputs

Suggested outputs:
- `site_transition_counts.csv` — raw transition counts;
- `site_transition_probabilities.csv` — normalized matrix;
- `site_transition_matrix.png` — heatmap or equivalent visualization.

### Important methodological choices

- **Sampling interval:** transitions occurring between saved frames may be missed.
- **Residence threshold:** requiring an atom to remain at a site for a minimum duration can suppress assignment noise.
- **Normalization:** row normalization gives the conditional probability of a destination given an origin; it is not the same as a transition rate.
- **Self-transitions:** decide whether frames where the site does not change should be included.
- **Vacancies:** clarify how an unoccupied site or an atom without a valid site assignment is represented.

---

## 12. Migration network

**Status:** Core candidate previously discussed; verify implementation

### What it measures

A migration network represents crystallographic sites or site classes as nodes and observed Li transitions as edges. Edge weights can encode raw counts, normalized probabilities, or rates.

This provides a compact representation of the migration pathways sampled during MD.

### Required input

- Site-transition data or time-resolved site assignments.
- Site labels and, if plotting spatially, reference coordinates.
- A defined weighting and normalization scheme.

### Outputs

Suggested outputs:
- `migration_network_edges.csv` — origin, destination, weight, and optional rate;
- `migration_network_nodes.csv` — site labels and optional coordinates;
- `migration_network.png` — graph visualization.

### Limitations

A frequently observed edge is not necessarily the lowest-energy or most probable pathway under all conditions; it is only frequent in the sampled trajectory. Results depend on trajectory length, sampling frequency, site assignment, and normalization. A network built from site classes loses some spatial detail compared with a network of individual crystallographic sites.

---

## 13. Jump frequency and transition rates

**Status:** Core candidate previously discussed; verify implementation

### What it measures

Jump-frequency analysis counts identified transitions over time. If the event definition and observation time are well defined, counts can be converted into rates.

Possible reporting levels include:
- total Li jumps per unit time;
- jumps per Li ion per unit time;
- frequencies for specific origin–destination pairs;
- frequencies grouped by site class or vacancy concentration.

### Required input

- Time-resolved site assignments or an event list.
- Persistent atom IDs.
- Physical time represented by each frame interval.
- Explicit event definitions, including any residence-time criterion.

### Outputs

Suggested outputs:
- `jump_events.csv` — optional event-by-event record;
- `jump_frequencies.csv` — counts and rates by transition;
- `jump_frequency.png` — comparison by transition or simulation condition.

### Limitations

A frame-to-frame site change is only an observed transition at the available sampling resolution. Multiple jumps between saved frames may be missed, while thermal fluctuations around assignment boundaries may create false events. Frequencies should not be compared unless sampling intervals and event definitions are consistent.

---

## 14. Structure–transport correlations

**Status:** Core candidate previously discussed; requires the relevant component analyses

### What it measures

This analysis compares structural or defect descriptors with transport observables. Potential comparisons include:
- Li vacancy concentration versus Li MSD or diffusion coefficient;
- antisite fraction versus Li mobility;
- local composition versus site-transition frequency;
- site occupation versus migration-network connectivity;
- temperature versus jump frequency or diffusion coefficient.

### Required input

- At least one structural/defect dataset, such as occupation, antisite, local-composition, or coordination results.
- At least one transport dataset, such as MSD, diffusion coefficient, transition counts, or jump frequencies.
- Consistent labels for simulation conditions, including vacancy concentration, temperature, run identifier, and analysis window.

### Outputs

Suggested outputs:
- `structure_transport_comparison.csv` — merged comparison table;
- `structure_transport_correlations.csv` — correlation statistics, if appropriate;
- `structure_transport.png` — scatter plots or comparative panels.

### Limitations

Correlation does not establish causation. Differences in temperature, simulation length, finite-size effects, initial configuration, and sampling can confound comparisons. Use independent replicas and uncertainty estimates when drawing quantitative conclusions.

---

## 15. Energy and temperature monitoring

**Status:** Optional extension unless an existing log-analysis script is confirmed

### What it measures

Thermodynamic monitoring checks whether the simulation behaves consistently with the intended protocol. Typical quantities include temperature, potential energy, total energy, pressure, and other variables recorded by the MD engine.

It can help identify equilibration periods, heating/cooling stages, unexpected drift, or unstable runs.

### Required input

- The MD engine's thermodynamic log, such as `log.lammps`.
- Column definitions and units.
- Optionally, the simulation protocol describing expected temperature stages.

### Outputs

Suggested outputs:
- `thermodynamics.csv` — cleaned time series;
- `thermodynamics_summary.csv` — averages and fluctuations over selected windows;
- `temperature.png` and `energy.png` — diagnostic plots.

### Limitations

A stable temperature alone does not demonstrate that a simulation is equilibrated or that the force field is physically accurate. Energy drift must be interpreted in light of the ensemble, thermostat/barostat, constraints, and simulation protocol.

---

## 16. Recommended analysis sequence

For a Li₂MnO₃ study with multiple Li-vacancy concentrations, a practical sequence is:

1. **Validate the run:** inspect temperature and energy logs, and confirm that the intended simulation stages completed.
2. **Validate the structural data:** check atom identities, cell information, frame count, and trajectory sampling.
3. **Analyze site assignments:** inspect assignment distances and the fraction of atoms that cannot be assigned reliably.
4. **Quantify occupation and antisites:** calculate these separately for heating, cooling, and production windows where appropriate.
5. **Analyze local structure:** use local composition and coordination descriptors to characterize defect environments.
6. **Analyze Li motion:** calculate MSD and fit diffusion coefficients only over a justified time interval.
7. **Analyze migration pathways:** calculate site-transition matrices, migration networks, and jump frequencies.
8. **Compare systems:** relate defect and structural descriptors to transport while keeping temperature, time windows, and normalization consistent.
9. **Compare diffraction patterns:** use consistent structural snapshots and settings to examine possible structural changes.

Not every step is necessarily implemented in the current software. The available command list should be generated from the actual package once the analysis scripts have been audited.

---

## 17. Minimum metadata to retain for reproducibility

For every analysis, record as many of the following as apply:

- simulation/run identifier;
- material and initial structure identifier;
- vacancy concentration and vacancy-generation seed;
- temperature and simulation stage;
- trajectory filename and frame range;
- timestep and frame-sampling interval;
- reference-site file and site-assignment parameters;
- cutoffs, neighbour definitions, and residence-time criteria;
- units and normalization definitions;
- software version and analysis command;
- output filenames;
- fit interval and uncertainty method for transport coefficients.

A result without its input files and analysis settings may be difficult to reproduce or compare fairly with another simulation.

---

## 18. How to turn this catalogue into definitive software documentation

Before release, audit each analysis implementation and replace the suggested filenames with exact names. For each supported analysis, document:

1. the exact command or Python entry point;
2. required and optional arguments;
3. exact input filenames, formats, columns, and units;
4. exact output filenames, columns, and units;
5. default parameters and their scientific meaning;
6. a minimal example using a small test dataset;
7. known limitations and validation status.

Analyses that are only proposed should remain labelled as planned or optional until implemented and tested. This distinction prevents users from mistaking a scientifically possible analysis for a feature already provided by the software.
"""
