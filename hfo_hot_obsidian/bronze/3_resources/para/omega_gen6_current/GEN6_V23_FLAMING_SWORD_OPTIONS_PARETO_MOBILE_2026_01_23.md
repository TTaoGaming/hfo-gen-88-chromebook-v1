# Medallion: Bronze | Mutation: 0% | HIVE: V

# Gen6 v23 — Flaming Sword Options (Babylon.js) for Mid-Range Mobile (Pareto)

Timestamp (user context): 2026-01-23

## Goal

Pick a **PHOENIX CORE**-style “flaming sword” visualization that:

- Looks good in motion (even with small/fast hand movement)
- Is **Pareto-optimal** on mid-range mobile (avoid fill-rate + postprocess traps)
- Has clear **meter-coupled** visuals: **fill → locked → drain**
- Stays compatible with your v23 posture: visualization-first, no changes to trigger semantics.

## Mobile Reality (what usually hurts)

- **Transparency + additive blending over big screen area** (fill-rate / overdraw) is the #1 silent killer.
- **Glow/Highlight layers** can be expensive; community guidance notes GlowLayer can effectively increase draw calls (because it renders meshes to a separate glow texture). Use sparingly and/or include only specific meshes.
  - Reference discussion: <https://forum.babylonjs.com/t/how-to-deal-with-this-model/36365>
  - Glow inclusion/exclusion behavior: <https://forum.babylonjs.com/t/glowlayer-inclusive-and-exclusive-methods/55445>
- **Particles**: CPU particles can be fine at low counts; GPU particles can scale better but are WebGL2-dependent and have their own edge cases.
  - GPU particles docs: <https://doc.babylonjs.com/features/featuresDeepDive/particles/particle_system/gpu_particles/>
- **Procedural textures** can be Pareto-friendly for flames (GPU-generated), but can still become fill-rate heavy if used as large transparent billboards.
  - Procedural textures overview: <https://doc.babylonjs.com/features/featuresDeepDive/materials/using/proceduralTextures>
- General Babylon optimization tips (great “checklist”): <https://forum.babylonjs.com/t/best-practices-for-optimizing-babylon-js-scenes-not-just-on-lower-end-devices/58688>

## Best Sword Options (ranked)

### Option A (Recommended Default): “Phoenix Core Pareto” (Mesh emissive core + cheap flame accents)

**Technique**

- Blade uses **emissive cyan core** (+ Fresnel rim) to read as “energy blade”.
- Flames are **tiny accents**: low-count sparks + very small flame sheath near the blade (don’t fill the screen).
- Fake “glow” using a **second, slightly scaled shell mesh** with alpha (instead of GlowLayer).

**Why it’s Pareto**

- Mesh-based emissive reads well even at low FPS.
- Avoids full-scene postprocess and keeps transparency area bounded.

**Meter mapping**

- `meter01` drives blade extension + emissive intensity.
- `locked` drives a more saturated cyan + higher flame intensity.

**Knobs**

- Shell mesh alpha (0.05–0.25), sparks emit rate (20–120), flame sheath size.

---

### Option B: “CPU Particle Sheath” (classic flame blade)

**Technique**

- A single CPU `ParticleSystem` emitting along the blade volume.

**Pros**

- Looks like “real flame” fast.
- Easy to tune (emit rate, lifetime, size gradients).

**Cons (mobile)**

- Particle overdraw is easy to blow up.
- Requires discipline: keep capacity modest and keep particles small.

**Knobs**

- Capacity ~500–2000; `emitRate` ~100–600; lifetime ~0.15–0.5.

Particle guide (for intuition / parameter ranges):

- <https://babylonjs.medium.com/visual-effects-with-particles-a-guide-for-beginners-5f322445388d>

---

### Option C: “Cross-Planes + Texture Scroll” (procedural-looking flames without procedural textures)

**Technique**

- 2–4 intersecting planes around the blade, each with an additive flame texture.
- Animate UV offsets + slight per-plane wobble.

**Pros**

- Very stable cost: a handful of meshes, no big particle counts.
- Strong silhouette for a sword.

**Cons**

- Can look “billboard-y” if camera gets too close.

**Knobs**

- Plane count (2–4), texture scale, scroll speed, alpha.

---

### Option D: “Trail Slash” (TrailMesh + sparks) — best for motion cues

**Technique**

- Attach `TrailMesh` to the sword tip so motion creates a ribbon trail.
- Add a few sparks on top.

**Pros**

- Looks excellent during swings (reads as power).

**Cons**

- Trail mesh updates vertices each frame; too many trails can add cost.
- Needs motion to look good.

References:

- TrailMesh discussion (UVs / mapping): <https://forum.babylonjs.com/t/trail-mesh-with-uvs-completed/47965>
- TrailMesh VFX demo thread: <https://forum.babylonjs.com/t/trailmesh-vfx-demo/51071>

---

## “Do This, Not That” (Pareto checklist)

- Prefer **emissive materials + small accents** over full-screen additive particle fog.
- Keep flame FX close to blade; avoid giant billboards.
- Avoid (or strictly limit) GlowLayer on mobile; fake glow with a shell mesh.
- Keep textures small (e.g., 256–512) and reuse the same texture across presets.
- Consider device scaling for mobile: set a reasonable hardware scaling level and cap maxZ.
  - Optimization list includes `engine.setHardwareScalingLevel()` guidance: <https://forum.babylonjs.com/t/best-practices-for-optimizing-babylon-js-scenes-not-just-on-lower-end-devices/58688>

## Recommendation

Start with **Option A** as your “always-on” sword (most robust on mid-range mobile), then add either:

- Option D trail for COMMIT-only moments, or
- Option B if you want “classic flame”, but keep it tightly bounded.

## Next Step (implementation)

Demo (Babylon) files in `omega_gen6_current/`:

- `omega_gen6_v23_flaming_sword_demo.html` (preset picker + meter UI)
- `omega_gen6_v23_flaming_sword_demo_0_phoenix.html` (preset 0)
- `omega_gen6_v23_flaming_sword_demo_1_cpu_sheath.html` (preset 1)
- `omega_gen6_v23_flaming_sword_demo_2_cross_planes.html` (preset 2)
- `omega_gen6_v23_flaming_sword_demo_3_trail_slash.html` (preset 3)

A Babylon demo page with 4 presets + a looping meter (fill → locked → drain) so you can visually pick your favorite for v23.
