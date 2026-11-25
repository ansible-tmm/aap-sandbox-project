# Clean-context handoff: registration-first sandbox learning path

## Latest user decision

Registration is **no longer deferred**. Verify or fix real RHEL registration
before package-management and Timesync exercises. Do not avoid registration
just because the image already has a package installed.

Use **one retained VM and automation identity** for the remaining implementation,
tests and UI review. Do not repeatedly destroy and recreate the environment.
Stop the VM during long pauses if needed; retain its disk, keys and identity.

## Goal and guardrails

Deliver a lean beginner AAP sandbox learning path for RHEL VMs on OpenShift
Virtualization. Preserve the working implementation; do not restart from scratch.

- AAP-only test configuration writes are authorized.
- OpenShift changes require explicit confirmation of the resource/action scope
  before applying them. Prior test approval is not blanket approval for new work.
- Obtain approval for registering a test consumer in the selected Red Hat
  organization and for the final unregistration/cleanup.
- No automatic cluster-policy, RBAC expansion, quota, networking or other
  namespace changes. Stop and ask if a restriction blocks the approved path.
- Never put real tokens, passwords or private keys in Git, the guide, checkpoints
  or intentional job output. Ask for access separately; do not copy old tokens
  into this handoff or retrieve administrator secrets as a workaround.
- No learner SSH-key generation, uploads, Machine credential or additional AAP
  bootstrap-token steps. Keep standard AAP credentials and the supported EE.
- Use actual playbooks through AAP; APIs may configure, launch and inspect jobs.
- No oversized-payload fixtures, generic installer framework or unnecessary
  repetition of the already completed VM/ServiceAccount test matrix.

## Repository and evidence

Repository: `ansible-tmm/aap-sandbox-project`.
Working branch: `lab/supported-ee-validation`; do not merge or push to `main`
without approval.

Read these before editing, using targeted sections rather than this old chat:

1. `README.md` — architecture, inputs and security boundaries.
2. `docs/validation.md` — real test evidence, corrections and remaining work.
3. `docs/learning-path.md` — revised working draft, not yet final publication.
4. `playbooks/rhel_register.yml`, `playbooks/rhel_timesync.yml`, and the shared
   `roles/sandbox_vm/` implementation.

Functional source at `d11a722` passed real tests; `999dbf8` records the subsequent
ServiceAccount results and core guide rewrite. Later handoff/documentation
commits do not imply a new functional test. Inspect actual HEAD.
The original key-redacted guide is preserved in commit `7f87ce6`.
Remote `main` was deliberately left at its original revision.

### Tested environment

- AAP 2.7 / Controller 4.8.12; OpenShift 4.22.22.
- Existing **Default execution environment**, pinned image in `README.md`.
- Actual EE: ansible-core 2.16.19 / Python 3.12.15.
- `redhat.openshift` 6.0.0; `redhat.openshift_virtualization` 2.3.0;
  `kubernetes.core` 6.4.0; `redhat.rhel_system_roles` 1.120.5.
- Use existing local Know MCP and Red Hat Docs MCP if available; discover tools
  rather than guessing them. Know's local Ansible version is not the EE version.
  Certified content was not available through public Galaxy fallback; installed
  EE content and official documentation are authoritative.

### Already proven — do not redo without a reason

Both user-token and namespace-scoped ServiceAccount authentication passed:
Create/clone, first inventory IP population, fresh-job SSH/sudo, stop/start,
inventory refresh, SSH/sudo again, and complete deletion.

The ServiceAccount used only the existing `edit` ClusterRole bound within its
namespace. No extra cross-namespace grant was needed. A requested 720-hour token
was issued for exactly 30 days on this cluster.

All test VM resources, both Secrets, temporary ServiceAccount/RoleBinding and
temporary AAP ServiceAccount credential were removed. Inventory had zero hosts;
namespace storage returned to its baseline of 2 PVCs / 18 GiB. No test VM is
currently retained. Obtain fresh/separately supplied access for the next phase.

### Existing AAP test bench

These IDs belong to the previously supplied instance; verify names/state before
using them, particularly if the user supplies a different instance:

- Default EE: 2.
- Project: 8, `AAP sandbox validation`, last runtime source `d11a722`.
- Inventory: 3; source: 7.
- Templates: Create 9, Delete 10, Start 11, Stop 12, SSH verification 13.
- Original test OpenShift user-token credential: 5, restored after testing.
- Temporary ServiceAccount credential 6 was deleted.
- Diagnostic Machine credentials are not part of the learner workflow.
- No RHEL registration credential, RHEL role test templates or actual workflow
  template had been configured at the last checkpoint.

Discover the approved namespace from the test inventory and confirm scope with
the user. Do not place personal instance URLs or authentication values in Git.

## Important findings to preserve

- `Manual` is enforced by Sandbox policy for its idler, not merely an old
  collection workaround. Do not replace it with `Always`.
- Full cloud-init `userDataSecretRef` was rejected by the Sandbox webhook.
  It requires an inline **`user` string**, not merely a `users` list.
- Working pattern: minimal non-sensitive inline bootstrap plus
  `accessCredentials.sshPublicKey.propagationMethod.noCloud`, referencing the
  public-key Secret. Sandbox mutation adds its own keys; admitted inline data
  was 832 bytes. Do not embed the project's keys in the VM manifest.
- `<vm_name>-ssh` stores the per-VM private/public identity;
  `<vm_name>-cloudinit` stores only `data.key` for public-key injection.
  Never reference the private-key Secret from the VM.
- Guest jobs retrieve the key through the OpenShift credential into a private
  temporary EE directory, mode 0600, with `no_log`, suppressed diffs and cleanup.
  Kubernetes Secret access is the security boundary; base64 is not encryption.
- Create/Start wait for `AgentConnected=True` and an IP on the guest-agent
  default interface before SSH. The earlier pod-only check raced inventory.
- Keep 1 vCPU / 2 GiB guest RAM / 30 GiB disk for this phase. The source is a
  30 GiB Block PVC; 20 GiB is not a drop-in clone-size change.
- Use `credentials/` association endpoints for AAP objects. A deprecated
  inventory-source `credential` field returned null despite a valid relation.
  Historical updates confirm the original user credential was attached.
- When switching credentials of the same type, remove the old association
  before adding the replacement. Change only the OpenShift association; retain
  the separate registration credential on Register jobs. Preserve and restore
  the original configuration.
- Dependency declarations are deliberately in `dependencies/collections.yml`,
  outside AAP auto-install paths; the supported EE already contains the content.

## Remaining implementation sequence

### 1. Inspect and settle registration inputs before provisioning

The current playbook uses `redhat.rhel_system_roles.rhc` with:

- `activation_key` -> `rhc_auth.activation_keys.keys`
- `organization_id` -> `rhc_organization`

Keep these public variable names unless an explicitly agreed change is needed.
The original guide's Red Hat service-account client-ID/client-secret mapping
was never functionally verified. Do not blindly relabel those values or claim
the old flow is broken solely from an assumption. OpenShift ServiceAccounts
and Red Hat subscription accounts are separate concepts.

Inspect the installed certified role/module and official RHEL documentation.
Agree a supported authentication method with the user and obtain authorized
registration values through protected AAP fields, not chat or Git.
Inspect the role's Insights/Lightspeed defaults and include any external
enrollment in the approval scope; do not silently expand the exercise.
Inspect existing credential types first. If required, use a minimal custom
credential with a secret activation key and organization ID, injecting the
existing variable names. Explain the learner-facing setup; do not add a new
bootstrap framework or learner AAP API-token requirement.

### 2. Prepare one retained test environment

Present the exact scope for approval: one namespace-scoped ServiceAccount,
namespaced `edit` binding, one VM, its DataVolume/PVC and two generated Secrets,
plus registration of that guest and an agreed small package installation.
Reuse the existing AAP test bench.

Review existing-VM Create reconciliation before workflow reruns: the current
role applies its VM manifest on each Create. Ensure reruns preserve keys,
platform-injected fields, Manual policy and existing disks. Fresh Create and
stop/start passed; a full Create rerun on an existing VM was not tested.
Make only a minimal change if inspection shows it is needed.

### 3. Validate actual registration, then package access

- Record baseline registration state and relevant packages without modifying it.
- Use a fresh unregistered guest to prove the credentials work. An already
  registered system or a skipped task is not proof of new registration.
- Do not unregister a preexisting/platform-owned consumer merely to force a test.
- Run the real Register playbook and verify the expected registration and repo
  access. Then install and verify a small approved package that was absent.
  Existing packages alone do not establish entitlement/repository access.
- Do not rely on `subscription-manager status` alone: Simple Content Access
  can report Disabled while identity and repository access are valid.
- Inspect redaction without printing registration secrets or consumer keys.
- Retain this VM; no intermediate destructive cleanup.

### 4. Validate Timesync on that registered VM

Run the real Timesync playbook. Verify effective configuration, enabled/running
Chrony, and sources/tracking status. If repository access or NTP connectivity
fails, diagnose narrowly; do not register with other credentials or change
network policy automatically.

### 5. Run the actual four-node AAP workflow

Use Workflow Job Template nodes with success edges:

`Create VM -> inventory-virt-sandbox sync -> RHEL Register -> RHEL Timesync`

Validate the real workflow engine, credentials/inventory inheritance, explicit
post-provision sync and the guide's update-on-launch settings. Reuse the retained
VM after checking safe reconciliation. Confirm reruns reuse its registration
identity rather than create duplicate consumers. Component jobs launched
sequentially by an external script do not count as this workflow test.

### 6. UI review, documentation and one final cleanup

Use the same environment for the learner-facing UI walkthrough and recordings.
Do not destroy the existing AAP instance to replay provisioning/subscription
screens; seek owner review or separate approval where necessary.

Finalize the guide, remove pending markers only for proven sections, review the
breaking `playbooks/` path migration, and coordinate an approved source-control
reference, PR/merge and publication. Do not promote `main` or publish the site
without approval.

At the end, explicitly unregister only the test consumer registered by this
work before deleting its VM. If unregistration fails, preserve the VM/certificate
for retry rather than silently orphan the consumer.
Then delete VM/storage/Secrets, refresh inventory, remove temporary identity
resources, restore AAP associations and verify cleanup independently.
Agree whether to retain the AAP test bench for handover.

## Context discipline

Keep a concise phase checkpoint and update `docs/validation.md`. Return filtered
API results, short failure excerpts and final tables—not whole event logs,
documentation chapters, old file versions or repeated plans. Read targeted
source sections. Keep secrets out of summaries. Optional RAM/disk tuning and
synthetic failure matrices are outside this remaining plan unless requested.
