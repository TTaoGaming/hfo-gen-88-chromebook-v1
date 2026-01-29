# Medallion: Bronze | Mutation: 0% | HIVE: V

# GitOps Improvements (Forge/Bronze) — Transition to Policy-as-Code

Date (UTC): 2026-01-29

## Current GitOps baseline (what you already do well)

- **Low-load batching + explicit allowlists:** `.gitops/batches.json` defines small, path-scoped batches (tracked vs untracked).
- **Evidence-first execution:** `scripts/hfo_gitops_batcher.py` writes a proof bundle with `gitops_receipt.json` + logs under `artifacts/proofs/`.

This is a strong base for a swarm because it is deterministic, auditable, and doesn’t rely on expensive repo-wide untracked scans.

## Goal

Transition GitOps from “commit batching + hooks” → “fail-closed governance” where:

- policy is machine-checkable,
- enforcement happens *before* merge and *at* deployment,
- every decision is evidence-backed.

## Best ways to improve (prioritized toward Policy-as-Code)

### 1) Policy-as-Code gates (pre-merge + admission)

**What:** Encode rules as policies and enforce them in two places:

- **Pre-merge (CI / local checks):** validate the exact manifests/artifacts that would be applied.
- **Admission (cluster):** reject non-compliant resources at apply time.

**How this maps to your repo:**
- Your GitOps batcher already creates a stable proof surface (`gitops_receipt.json` + committed paths). That becomes the input to policy validation.
- Start with a minimal rule-set that blocks your known failure modes (bad provenance headers, forbidden paths, missing schemas, unsafe symlinks, etc.).

**External proof (sources):**
- OPA Gatekeeper overview (Kubernetes): https://kubernetes.io/blog/2019/08/06/opa-gatekeeper-policy-and-governance-for-kubernetes/
- GitOps security with policy-as-code (Flux/ArgoCD patterns): https://policyascode.dev/blog/gitops-security-policy-as-code-flux-argocd/

**Why it’s exemplar:** your “truth surface” becomes a contract, not a human convention.

### 2) Drift detection + reconciliation via a GitOps controller (Argo CD or Flux)

**What:** Move from “Git is the ledger” to “Git is the desired state,” with an in-cluster agent continuously reconciling live state against Git.

**How this maps to your repo:**
- If you are (or will be) deploying Kubernetes resources, this is the canonical GitOps loop.
- Your proof bundles can become the audit trail for *why* a reconciliation happened (or failed).

**External proof (sources):**
- Argo CD docs (drift detection + GitOps CD): https://argo-cd.readthedocs.io/en/stable/
- Core GitOps principle (agents detect drift): https://www.plural.sh/blog/what-is-gitops/

### 3) Supply-chain integrity: signed artifacts + provenance (Sigstore/cosign + SLSA)

**What:** Require cryptographic signatures and provenance for what gets deployed.

**How this maps to your repo:**
- Add signing to CI outputs and enforce verification via policy (ties directly into Option 1).
- Use your proof bundles as the operator-grade “receipt,” while signatures/provenance are the cryptographic “receipt.”

**External proof (sources):**
- Sigstore overview: https://www.sigstore.dev/

### 4) Progressive delivery with automated rollback (policy-driven)

**What:** Don’t treat “merge to main” as “100% rollout.” Use canary/blue-green and auto-rollback on failed health checks.

**How this maps to your repo:**
- This is where policy + drift + evidence converge:
  - policy decides what can roll out,
  - controller manages rollout,
  - receipts/proof bundles explain the chain of custody.

**External proof (source for the GitOps pull + reconcile model that progressive delivery builds on):**
- https://www.plural.sh/blog/what-is-gitops/

## Minimal transition plan (Bronze → Silver)

- Bronze: add one small, concrete policy gate (start pre-merge).
- Bronze: add a “policy report” artifact into each GitOps proof bundle.
- Silver: enforce the same policies at admission (fail-closed).
- Silver: require signed artifacts + provenance and verify in policy.

## Repo anchors

- `.gitops/batches.json`
- `scripts/hfo_gitops_batcher.py`
- Recent proof receipts under `artifacts/proofs/gitops_*`
