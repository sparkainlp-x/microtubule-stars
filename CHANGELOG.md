# Changelog

## 0.1.0 (unreleased)

- Reporting: `python -m microtubule_stars` now also prints the seed-to-seed SD of dwell and the paired per-seed effect of the drive with a deterministic 5000-resample bootstrap 95% interval and the number of seeds where the drive helped; README gains the matching table and notes that the phase-locking value has no null control. The simulation and the existing table values are unchanged.
- Documentation only: added a Provenance statement that says which files are derived from the package received under Mun Seok Lee's name and by how much, that he is not an author of this release and has not endorsed it.
- First commit: the package exactly as received (`spec/microtubule-stars/`).
- Authorship: Jean-François Brisson. Mun Seok Lee is credited in the acknowledgements only.
- Framing: SYNTHETIC classical Kuramoto only. README title/lede no longer imply a real "holographic brain" under cosmic influence. RESEARCH.md trimmed to a short literature note with "not simulated in this repo"; Orch OR / consciousness claim-y wording removed from public materials.
- "Verified" headings replaced by "Measured in this repo".
- Packaged as `microtubule_stars` with input validation, a CLI (`python -m microtubule_stars`), 18 pytest tests (warnings are errors), and CI on Python 3.10 to 3.13.
- Added README, DESIGN.md, CHANGELOG, CITATION.cff and .zenodo.json.
