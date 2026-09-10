# CR-DEA-RP-03: Federation Watchdog

Status: Proposed
Program: dea-release-package
Parent: CR-DEA-RP-02 (Federation Release Registry); CR-DEA-RP-01 (Release Package Program)
Related: CR-11 (Interoperability, Federation & Ecosystem Conformance); CR-9 (OpenDEA Runtime, Knowledge Graph & Interoperability Architecture); CR-AM-02 §11 (Compatibility Vocabulary); CR-ECF-001..008 (Enterprise Concept Framework)
Decision Type: Architectural (Sub-System Implementation)
Implementation: Implemented by `dea-release-package/.github/workflows/watchdog.yml` plus the `dea_release_package.watchdog` toolkit module

---

## 1. Decision Statement

The Release Package Program establishes a **Federation Watchdog** that monitors the federation for drift, asymmetric compatibility, missing assets, and mandate mismatches.

The governing principle is:

> **The watchdog is the federation's eye. It flags what humans haven't acknowledged. It does not fix what humans haven't decided.**

The Federation Watchdog therefore:

- runs three jobs (pin coherence, cross-version compatibility, asset drift) on nightly cron and on `workflow_dispatch`;
- reads the Federation Release Registry (CR-DEA-RP-02) as its substrate;
- opens GitHub Issues on `dea-release-package` for every divergence that is *unacknowledged*;
- computes a derived release timeline + dependency graph (`timeline/<year>-<quarter>.yaml`);
- is signal-vs-noise-disciplined: silent divergence is flagged; acknowledged divergence is not.

The Federation Watchdog does NOT:

- modify any registry manifest (the registry is append-only);
- modify any catalog repo (corrections belong to per-catalog CRs);
- enforce compliance (enforcement is a separate concept, handled in CR-DEA-RP-01 §8);
- generate human-readable release notes (that belongs to CR-DEA-RP-04).

---

## 2. Why This Decision Is Necessary

The registry (CR-DEA-RP-02) records what *was* released. The watchdog answers *whether what was released composes correctly*. Three irreducible gaps require a watchdog:

1. **Pin divergence.** Two sibling repos can release against different ECF pins within a 90-day window. Without a watchdog, the divergence is invisible until a downstream consumer breaks.

2. **Asymmetric compatibility claims.** Repo R can claim `compatible` with repo T at tag X. Repo T's manifest may have moved to a different tag, may have a contradictory claim, or may be silent on R entirely. Without a watchdog, the asymmetry decays silently.

3. **Missing assets.** A registry manifest can list an asset in `asset_inventory` that is absent from the GitHub Release, or whose checksum doesn't match. Without a watchdog, consumers import a broken file.

---

## 3. Decision Drivers

The Federation Watchdog addresses:

1. **Pin coherence** : ECF and metamodel pin alignment across the federation;
2. **Compatibility reciprocity** : symmetric claims across peer releases;
3. **Mandate reconciliation** : release-note mandates acknowledged by the target release;
4. **Asset presence** : every listed asset exists with the declared checksum;
5. **Tamper evidence** : the published artifact matches what CI built;
6. **Federation timeline** : release history across all repos with dependency relationships;
7. **Signal-vs-noise discipline** : flagging acknowledged divergence is noise;
8. **Human decision support** : the watchdog's flags drive per-catalog CRs.

---

## 4. The Three Watchdog Jobs

### 4.1 Job 1 : Pin Coherence Watchdog

**Input:** every release manifest in the federation registry released in the last 90 days.

**Logic:**

```
For each pair (R1, R2) where R1 != R2 and both released within window:
  If R1.ecf_pin != R2.ecf_pin:
    divergence = pin_divergence(R1, R2, axis='ecf_pin')
    If not divergence.acknowledged:
      flag = open_issue(
        severity='high' if divergence.age > 7 days else 'medium',
        body=f"Pin divergence: {R1.repo}@{R1.tag} on {R1.ecf_pin}; {R2.repo}@{R2.tag} on {R2.ecf_pin}; gap: {divergence.age} days"
      )
```

`acknowledged` means: the *newer* of the two releases' CHANGELOG explicitly mentions the pin change in a section titled "Pin Changes" or "Breaking Changes."

### 4.2 Job 2 : Cross-Version Compatibility Watchdog

**Input:** every release manifest in the federation registry released in the last 180 days.

**Logic:**

```
For each release R:
  For each compatibility_claim C in R.compatibility_claims:
    target = lookup(C.target_repo, C.target_tag)
    If target is None:
      flag = open_issue(
        severity='high',
        body=f"{R.repo}@{R.tag} claims {C.relationship} with {C.target_repo}@{C.target_tag}, but no release at that tag exists in the registry"
      )
      continue
    If target.compatibility_claims has a claim about R:
      If claim is asymmetric:
        flag = open_issue(
          severity='medium',
          body=f"Asymmetric claim: {R.repo}@{R.tag} claims {C.relationship} with {target.repo}@{target.tag}; target claims {reverse_claim} with R"
        )
    If R.compatibility.release_note_consistency == 'incompatible':
      For each mandate in R.release_notes that names target:
        If mandate not in target.release_notes.acknowledgements:
          flag = open_issue(
            severity='medium',
            body=f"Mandate unacknowledged: {R.repo}@{R.tag} mandates X for {target.repo}@{target.tag}; target's release notes are silent"
          )
```

### 4.3 Job 3 : Asset Drift Watchdog

**Input:** every release manifest in the federation registry.

**Logic:**

```
For each release R:
  For each (asset_name, expected_sha256) in R.asset_checksums:
    actual = fetch_and_hash(f"https://github.com/{R.repo}/releases/download/{R.tag}/{asset_name}")
    If actual != expected_sha256:
      flag = open_issue(
        severity='critical',
        body=f"Asset drift: {R.repo}@{R.tag}/{asset_name} expected {expected_sha256}, actual {actual}"
      )
  For each asset in R.asset_inventory:
    If asset not in R.asset_checksums:
      flag = open_issue(
        severity='high',
        body=f"Missing checksum: {R.repo}@{R.tag}/{asset} is listed in inventory but has no checksum"
      )
  For each asset in R.asset_checksums:
    If asset not in R.asset_inventory:
      flag = open_issue(
        severity='low',
        body=f"Extra checksum: {R.repo}@{R.tag}/{asset} has a checksum but is not in inventory"
      )
```

### 4.4 Derived Timeline + Dependency Graph

**Input:** every release manifest in the federation registry, sorted by `released_at`.

**Output:** `federation-registry/timeline/<year>-<quarter>.yaml`:

```yaml
window: 2026-Q3
computed_at: 2026-09-12T03:00:00Z
releases:
  - date: 2026-09-07
    repo: technehub-labs/dea-catalog-business-capabilities
    tag: v1-alpha.1
    peer_pins: {}
    claims: []
  - date: 2026-09-08
    repo: technehub-labs/dea-catalog-processes
    tag: v0.4.2
    peer_pins: { dea-catalog-business-capabilities: v1-alpha.1 }
    depends_on:
      - repo: technehub-labs/dea-catalog-business-capabilities
        tag: v1-alpha.1
        relationship: requires
  - date: 2026-09-12
    repo: technehub-labs/dea-catalog-business-capabilities
    tag: v1-alpha.3
    peer_pins: { dea-catalog-processes: v0.4.2 }
    breaks:
      - repo: technehub-labs/dea-catalog-processes
        tag: "<=v0.4.2"
        reason: "ECF pin advance"
```

The timeline is regenerated nightly. A quarterly "release coordination report" is generated as a PR for human review.

---

## 5. Issue Management

### 5.1 Issue structure

```yaml
# GitHub Issue on technehub-labs/dea-release-package
title: "[watchdog/{job}] {one-line summary}"
labels:
  - watchdog/{job-name}
  - severity/{severity}
  - catalog/{repo-name}        # if the issue names a specific catalog
body: |
  ## Summary
  {one-line description}

  ## Evidence
  {registry entries, links, SHA hashes}

  ## Recommended action
  {one-paragraph suggested fix path; references the relevant CR-DEA-RP-NN}

  ## Auto-resolve
  This issue will auto-close when:
  {condition that resolves the issue}
```

### 5.2 Auto-resolution

Each watchdog issue carries an auto-resolve condition:

| Job | Resolves when |
|---|---|
| Pin coherence | The newer release's CHANGELOG mentions the pin change, OR the older pin is updated. |
| Cross-version compatibility | The asymmetric claim is corrected, OR the target release adds a reciprocal claim, OR the claim is removed. |
| Asset drift | The asset checksum in the registry matches the GitHub Release asset. |

Auto-resolution is implemented via a watchdog "resolver" job that re-runs after any registry PR merges.

### 5.3 Signal-vs-noise discipline

The watchdog's noise control is the "acknowledged divergence" rule:

- **Pin coherence**: divergence is *acknowledged* if the newer release's CHANGELOG explicitly mentions the pin change.
- **Cross-version compatibility**: a missing reciprocal claim is *acknowledged* if the target release notes "intentionally silent on X" or carries an explicit deprecation.
- **Asset drift**: missing checksums in pre-program historical releases are grandfathered (auto-resolve with a `grandfathered` label).

The result: the watchdog flags *unacknowledged* divergence. Acknowledged divergence is the per-catalog CR's responsibility.

---

## 6. The Workflow File

```yaml
# dea-release-package/.github/workflows/watchdog.yml
name: Federation Watchdog

on:
  schedule:
    - cron: '0 3 * * *'              # nightly at 03:00 UTC
  workflow_dispatch:
    inputs:
      job_filter:
        description: 'Run only specific jobs (pin-coherence|cross-version|asset-drift|all)'
        required: false
        default: 'all'

jobs:
  pin-coherence:
    if: ${{ github.event.inputs.job_filter == 'all' || github.event.inputs.job_filter == 'pin-coherence' }}
    runs-on: ubuntu-latest
    steps:
      - checkout (fetch-depth: 0)
      - setup python
      - run: python -m dea_release_package.watchdog.pin_coherence --output issues/pin-coherence-$(date).yaml
      - uses: peter-evans/create-issue-from-file@v4
        with:
          filename: issues/pin-coherence-$(date).yaml

  cross-version:
    if: ${{ github.event.inputs.job_filter == 'all' || github.event.inputs.job_filter == 'cross-version' }}
    runs-on: ubuntu-latest
    steps:
      - checkout (fetch-depth: 0)
      - setup python
      - run: python -m dea_release_package.watchdog.cross_version --output issues/cross-version-$(date).yaml
      - uses: peter-evans/create-issue-from-file@v4
        with:
          filename: issues/cross-version-$(date).yaml

  asset-drift:
    if: ${{ github.event.inputs.job_filter == 'all' || github.event.inputs.job_filter == 'asset-drift' }}
    runs-on: ubuntu-latest
    steps:
      - checkout (fetch-depth: 0)
      - setup python
      - run: python -m dea_release_package.watchdog.asset_drift --output issues/asset-drift-$(date).yaml
      - uses: peter-evans/create-issue-from-file@v4
        with:
          filename: issues/asset-drift-$(date).yaml

  timeline:
    runs-on: ubuntu-latest
    steps:
      - checkout (fetch-depth: 0)
      - setup python
      - run: python -m dea_release_package.watchdog.timeline --output federation-registry/timeline/$(quarter).yaml
      - run: git diff --quiet federation-registry/timeline/ || git add ... && git commit && git push

  resolver:
    needs: [pin-coherence, cross-version, asset-drift, timeline]
    runs-on: ubuntu-latest
    steps:
      - checkout (fetch-depth: 0)
      - setup python
      - run: python -m dea_release_package.watchdog.resolve
              # Re-runs all jobs against current state; closes issues whose
              # auto-resolve condition is now satisfied
      - uses: actions/github-script@v7
        with:
          script: |
            for issue in ...: github.rest.issues.update({state: 'closed', ...})
```

---

## 7. The Watchdog Toolkit Module

`dea-release-package/toolkit/src/dea_release_package/watchdog/` exposes:

| Module | Purpose |
|---|---|
| `pin_coherence.py` | Job 1 logic; emits issues. |
| `cross_version.py` | Job 2 logic; emits issues. |
| `asset_drift.py` | Job 3 logic; emits issues. |
| `timeline.py` | Derived timeline + dependency graph. |
| `resolve.py` | Auto-resolution loop. |
| `models.py` | Pydantic models for issue bodies, severities, conditions. |

The toolkit's tests cover:

- pin divergence with and without acknowledgement;
- asymmetric claims with reciprocal claims, with missing claims, with explicit deprecations;
- asset drift with checksum match, mismatch, missing checksum, extra checksum;
- timeline computation across quarters with cross-repo dependencies.

---

## 8. Failure Modes and Mitigations

| Failure mode | Mitigation |
|---|---|
| Watchdog opens an issue for an acknowledged divergence | Acknowledgement rule is documented in the issue body; false positives reviewed by maintainers. |
| Watchdog misses a divergence | Watchdog's `dispatch` action supports ad-hoc re-runs against any subset of the registry. |
| Watchdog job fails on a registry parse error | Job failures open a critical issue; the registry is expected to be always-valid (CR-DEA-RP-02 §10.1). |
| Watchdog opens thousands of issues on a large registry | Severity gating (`medium` and above); `low` severities are batched into a single weekly digest. |
| Cross-repo auth for issue creation on a third-party repo | Watchdog issues are always opened on `dea-release-package`, never on the catalog repo. Cross-repo notification is the responsibility of the catalog repo's CI. |

---

## 9. Consequences

### Positive

- The federation has a continuous monitor for drift, asymmetry, missing assets, and mandate mismatches.
- Watchdog issues carry structured bodies with evidence and recommended actions.
- The derived timeline provides quarterly release coordination artifacts.
- Signal-vs-noise discipline keeps the watchdog useful.

### Negative

- The watchdog is a new long-running CI surface; failures in the watchdog block visibility into the federation.
- Auto-resolution requires a resolver job, which can itself fail; resolver failure is a critical issue.
- Acknowledgement rules depend on per-repo CHANGELOG discipline; a CHANGELOG that doesn't mention a pin change is flagged (which may be correct or may be noise).
- The watchdog's first week will surface a lot of pre-existing divergence; expect a burst of issues to triage.

---

## 10. Rejected Alternatives

### A : Inline flagging in catalog repos

Each catalog repo's CI flags drift in its own context.

Rejected because:

- Pin divergence requires reading other repos' registries.
- Asymmetric claims require comparing claims across repos.
- The federation view cannot live in any single repo.

### B : Hard-fail enforcement

The watchdog blocks merges on divergence.

Rejected because:

- Merges are a per-repo concern; the watchdog is a federation concern.
- Hard-fail conflates "the federation has drift" with "this PR is broken."
- Acknowledged drift is sometimes intentional; blocking merges prevents it.

### C : Manual review by humans

Each release requires a human to review cross-repo relationships.

Rejected because:

- Doesn't scale past 3-4 repos.
- Humans miss what machines catch.

### D : Real-time event-driven watchdog

Watchdog fires on every registry PR merge, not on a cron.

Rejected because:

- Race conditions with concurrent merges.
- Harder to compute timeline aggregates.
- Cron is good enough; 24h latency is acceptable for drift detection.

---

## 11. Explicit Non-Decisions

This CR does NOT decide:

- The exact issue body template format (deferred to toolkit);
- The cross-repo notification mechanism for catalog teams (deferred to per-catalog adoption CRs);
- The quarterly report format (deferred to toolkit; the timeline is the primary artifact);
- Whether the watchdog opens issues on catalog repos in addition to `dea-release-package` (decision: no, always on `dea-release-package`; cross-repo notification is a separate concern).

---

## 12. Decision Summary

The Federation Watchdog:

- runs three jobs on nightly cron and on dispatch;
- reads the Federation Release Registry;
- opens GitHub Issues on `dea-release-package` for unacknowledged divergence;
- auto-resolves issues when their conditions are met;
- computes a derived release timeline + dependency graph;
- is signal-vs-noise-disciplined: acknowledged divergence is not flagged.

The watchdog is the federation's eye; it does not fix what humans haven't decided.

---

## 13. Required Follow-On CRs

- **CR-DEA-RP-04** : Visibility Surfaces; consumes the watchdog's flags for the index page and release-note annexes.
- **Per-catalog adoption CRs** : each catalog repo's adoption CR names a catalog-side notification path for watchdog issues.

---

*Status: Proposed. Parent: CR-DEA-RP-02 (Federation Release Registry); CR-DEA-RP-01 (Release Package Program).*