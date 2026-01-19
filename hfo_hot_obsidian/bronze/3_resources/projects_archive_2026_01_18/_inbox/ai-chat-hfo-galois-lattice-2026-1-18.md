Locked.

### P0→P7 commanders (power word, JADC2-aligned “tile” domain, and swarm capability)

|   Port | Commander                                              | Power word     | JADC2-aligned domain                                                                | What they should eventually do                                                                                                                                                                             |
| -----: | ------------------------------------------------------ | -------------- | ----------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **P0** | **Lidless Legion**                                     | **OBSERVE**    | **ISR** (intelligence/surveillance/recon) ([NATO][1])                               | Collect signals + evidence with provenance; anomaly detection; confidence-scored observations; “never blink.”                                                                                              |
| **P1** | **Web Weaver**                                         | **BRIDGE**     | **Data Fabric** (integration + consistent access) ([IBM][2])                        | Bind boundaries: schemas/envelopes/trace context; connector/adapters; contract registry + compatibility rules.                                                                                             |
| **P2** | **Mirror Magus**                                       | **SHAPE**      | **Digital Twin** (synced mirror at defined fidelity) ([Digital Twin Consortium][3]) | **Your correction applied:** mint tokens/variants, run spikes/prototypes, and “shape” the environment via controlled edits; canonicalization + tuning bundles; drift detection between mirror and reality. |
| **P3** | **Spore Storm**                                        | **INJECT**     | **Effect Delivery** (effects-based approach) ([RAND Corporation][4])                | Deliver effects through **target-specific adapters**; execute only within authority; emit execution receipts; reversible/flagged changes.                                                                  |
| **P4** | **Harmonic Hydra** *(replaces Red Regnant as primary)* | **DISRUPT**    | **Red Team / adversary emulation** ([IBM][5])                                       | “Hydra venom / nematocysts” = durable adversarial payload injection: fuzz/chaos/probes that sting assumptions; prove controls fail-closed; keep an evolving exploiter playbook.                            |
| **P5** | **Pyre Praetorian**                                    | **IMMUNIZE**   | **Force Protection** (protect people/systems/assets) ([doctrine.af.mil][6])         | Own policy gates, tripwires/canary/revert, least privilege; enforce fail-closed arming/commit/cancel semantics.                                                                                            |
| **P6** | **Kraken Keeper**                                      | **ASSIMILATE** | **AAR** (after-action review / learning loop) ([first.army.mil][7])                 | Distill outcomes into doctrine: intended vs actual, receipts, regression notes; update SSOT/knowledge graph; publish “what’s proven.”                                                                      |
| **P7** | **Spider Sovereign**                                   | **NAVIGATE**   | **C2** (command and control) ([505th Combat Command Wing][8])                       | Set mission intent + constraints; allocate work; pick next actions; enforce stop-rules and sequencing via HIVE/8 dyads.                                                                                    |

---

## The 8×8 lattice (diagonal = commanders, anti-diagonal = HIVE/EVIH dyads)

**Anti-diagonal dyads (i + j = 7):**

* **P0+P7 = Hindsight = Hunt**
* **P1+P6 = Insight = Interlock**
* **P2+P5 = Validated Foresight = Validate**
* **P3+P4 = Evolve = Evolve**

|        | P0                               | P1                                  | P2                                    | P3                                       | P4                                    | P5                                              | P6                                 | P7                                 |
| ------ | -------------------------------- | ----------------------------------- | ------------------------------------- | ---------------------------------------- | ------------------------------------- | ----------------------------------------------- | ---------------------------------- | ---------------------------------- |
| **P0** | **Lidless Legion** (OBSERVE/ISR) |                                     |                                       |                                          |                                       |                                                 |                                    | **Hindsight / Hunt**               |
| **P1** |                                  | **Web Weaver** (BRIDGE/Data Fabric) |                                       |                                          |                                       |                                                 | **Insight / Interlock**            |                                    |
| **P2** |                                  |                                     | **Mirror Magus** (SHAPE/Digital Twin) |                                          |                                       | **Validated Foresight / Validate**              |                                    |                                    |
| **P3** |                                  |                                     |                                       | **Spore Storm** (INJECT/Effect Delivery) | **Evolve / Evolve**                   |                                                 |                                    |                                    |
| **P4** |                                  |                                     |                                       | **Evolve / Evolve**                      | **Harmonic Hydra** (DISRUPT/Red Team) |                                                 |                                    |                                    |
| **P5** |                                  |                                     | **Validated Foresight / Validate**    |                                          |                                       | **Pyre Praetorian** (IMMUNIZE/Force Protection) |                                    |                                    |
| **P6** |                                  | **Insight / Interlock**             |                                       |                                          |                                       |                                                 | **Kraken Keeper** (ASSIMILATE/AAR) |                                    |
| **P7** | **Hindsight / Hunt**             |                                     |                                       |                                          |                                       |                                                 |                                    | **Spider Sovereign** (NAVIGATE/C2) |

### Alias lock (so you stop drifting)

* Canonical: **HIVE/8 loop**
* Facets (aliases): **Hindsight/Insight/Validated Foresight/Evolve** == **Hunt/Interlock/Validate/Evolve**
* Anti-diagonal rule: **P(i) ↔ P(7−i)** (the symmetry constraint)

If you want the *rest of the 64 cells* filled next, specify what the **non-diagonal cells mean** in your lattice (common choices: “information flow”, “authority edges”, “tool slots”, or “artifact types”).

[1]: https://www.nato.int/en/what-we-do/deterrence-and-defence/joint-intelligence-surveillance-and-reconnaissance?utm_source=chatgpt.com "Joint Intelligence, Surveillance and Reconnaissance - NATO"
[2]: https://www.ibm.com/think/topics/data-fabric?utm_source=chatgpt.com "What Is a Data Fabric?"
[3]: https://www.digitaltwinconsortium.org/2020/12/digital-twin-consortium-defines-digital-twin/?utm_source=chatgpt.com "Digital Twin Consortium Defines Digital Twin"
[4]: https://www.rand.org/content/dam/rand/pubs/monograph_reports/2006/MR1477.pdf?utm_source=chatgpt.com "Effects-Based Operations (EBO)"
[5]: https://www.ibm.com/think/topics/red-teaming?utm_source=chatgpt.com "What is Red Teaming? | IBM"
[6]: https://www.doctrine.af.mil/Portals/61/documents/AFDP_3-10/3-10-AFDP-Force-Protection.pdf?utm_source=chatgpt.com "3-10-AFDP-Force-Protection.pdf"
[7]: https://www.first.army.mil/Portals/102/FM%207-0%20Appendix%20K.pdf?utm_source=chatgpt.com "After Action Reviews - First Army"
[8]: https://www.505ccw.acc.af.mil/News/Commentaries/Display/Article/3139068/command-and-control-terms-of-reference/?utm_source=chatgpt.com "Command and Control Terms of Reference"
