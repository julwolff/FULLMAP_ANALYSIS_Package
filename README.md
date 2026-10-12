**A modular workflow tool for preparing, running, and analysing molecular-dynamics simulations of Battery Materials .**

## Purpose

FullMapFlow aims to bring the main steps of a Li molecular-dynamics (MD) study into one reproducible workflow. It is intended to reduce repetitive manual work, standardise simulation campaigns, and make it easier to compare systems with different lithium-vacancy concentrations.

The project targets workflows that use **pymatgen** for structure handling and a **Slurm-based HPC cluster** for simulations.

## Development idea

The software is designed around small, reusable operations that can be run independently or combined into larger workflows:

1. **Structure preparation** — retrieve a structure, build a supercell, and generate lithium vacancies.
2. **Simulation preparation** — prepare input files and organise calculation directories.
3. **HPC execution** — transfer files, submit minimisation and production jobs, and manage Slurm dependencies.
4. **Result retrieval** — bring simulation outputs back for analysis.
5. **Analysis** — run existing analysis tools and compare results across simulation conditions.

The intended interface is a command-line application. Individual commands should remain useful on their own, while higher-level commands combine them into complete workflows or multi-condition simulation campaigns. Workflow state tracking and restart support are planned to help recover from failed or interrupted steps without repeating completed work.

## Current state

The project is at the **design and integration-planning stage**. Several operations in the existing research workflow are already automated, including lithium-vacancy generation, energy minimisation, production MD, and analysis. The main development task is to connect these tools and automate the remaining manual steps, particularly structure acquisition and supercell generation, HPC file transfer, job orchestration, and result retrieval.

The final command names, configuration format, supported analyses, and exact input/output filenames still need to be confirmed against the existing scripts. Features described as planned should not be considered implemented until integrated and tested.

## Design principles

- **Modular:** each operation can be run independently.
- **Composable:** simple commands can be combined into larger workflows.
- **Reproducible:** record simulation parameters, inputs, and outputs.
- **HPC-aware:** support Slurm job dependencies and remote execution.
- **Incremental:** reuse existing scripts where possible instead of rewriting working tools.

## Planned direction

Development will proceed by wrapping and testing existing scripts, implementing the missing automation steps, exposing operations through a consistent CLI, and then adding end-to-end workflows with status tracking and recovery.

---

*FullMapFlow is a working project name. The scope and feature status should be updated as implementation progresses.*
