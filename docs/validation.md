# Candidate validation

Recorded November 25, 2026. **The normal VM lifecycle passed on commit
`d11a722`, using the pinned AAP 2.7 supported EE and OpenShift 4.22.22.**

The namespace-scoped OpenShift ServiceAccount credential flow also passed
without playbook changes. Registration, Timesync and the final workflow
execution remain untested. The latest user decision requires real registration
and proven package access before Timesync, using one retained test environment.
See [implementation handoff](implementation-handoff.md). The verified
learner-copy sections have been rewritten; UI review and RHEL/workflow
validation remain pending before publication.

## Completed preflight checks for the first candidate

| Check | Result |
| --- | --- |
| Local `ansible-lint --offline` | Passed, no failures or warnings |
| YAML parsing | Passed for 20 source files |
| Six documented job-template paths | All resolve under `playbooks/` |
| Supported EE entry-point syntax | All six playbooks and `tests/playbooks/verify_ssh.yml` passed |
| Supported EE shared-role syntax | Every task file statically imported and parsed |
| VM/cloud-init rendering | Passed; Manual strategy, Secret reference, public-key-only cloud-init |
| Inventory input compatibility | `vm_name` and `ocp_namespace` resolved from inventory on implicit localhost |
| `ssh-keygen` in the supported EE | Available |

The first candidate's supported-EE check ran as AAP ad hoc diagnostic **#4**, using the
pinned default image documented in the [README](../README.md). The actual
ansible-core version was **2.16.19**. The local linter used ansible-core
2.20.5; that local check alone could not resolve the expanded role's missing
local collections, so the supported EE was used for the authoritative syntax
check.

The diagnostic received only a localhost inventory and an empty, placeholder
Machine credential required by the ad hoc launch API. That diagnostic-only
credential is not a requirement of the candidate learner workflow. No
OpenShift credential was supplied.

The 24 source files sent to that check had this combined SHA-256:

```text
a516b1b121a17960359f10b5f1ba5c93639fe82ce930aaa44e4265d20c3f67ad
```

The source set was `ansible.cfg`, the six playbooks, role YAML/templates,
the SSH-verification playbook, `tests/check.py`, and the dependency manifest.
Documentation was not part of that source fingerprint.

To repeat the local-only checks inside the chosen EE:

```bash
python3 tests/check.py
```

## Limits of the preflight checks

The preflight checks above did not create a VM or Secret, start/stop a guest,
retrieve its real SSH identity, or delete storage. Module availability and
template correctness alone did not prove admission, provisioning or SSH.
The subsequent real runs below established those outcomes for the tested path.

The real runs used an explicitly approved test branch and named disposable
resources. Repeating cluster-changing tests still requires confirmation.

## First real Create VM run

Candidate commit `bdac26f` was pushed only to `lab/supported-ee-validation`.
The isolated AAP test project synced that exact commit successfully without
extra Galaxy downloads, and discovered all seven intended playbooks.

Create VM job **#6**:

- Generated the per-VM SSH identity automatically in the supported EE.
- Created the SSH Secret and full cloud-init Secret successfully.
- Was rejected at VM admission by
  `users.virtualmachines.validating.webhook.sandbox`: a user must be configured
  in the cloud-init volume.
- Created no VM, DataVolume, or boot PVC. The two managed Secrets were retained
  for the retry, reused by job #10, and removed by job #15.

The public Sandbox webhook implementation explains the rejection: its validator
requires an inline `user` string, and its mutator appends platform SSH keys to
inline user data. It also enforces `Manual` to work with the Sandbox idler.
This explains why caller-side payload measurements alone cannot establish the
size ultimately checked by KubeVirt.

The revised candidate uses OpenShift's documented `accessCredentials` /
`noCloud` public-key Secret mechanism plus a minimal, non-sensitive inline user
bootstrap. The private key remains in the separate SSH identity Secret, never
referenced by the VM. No admission or cluster policy is changed.

Revised-source preflight in supported-EE diagnostic **#8** passed all syntax,
template and inventory-interface checks on ansible-core 2.16.19. The source
fingerprint for that check is:

```text
39c5d5341a102eb3233f9731accd170626f861bac1cc7c398a2a1f2ee2902809
```

References:

- [OpenShift 4.22 SSH-key management](https://docs.redhat.com/en/documentation/openshift_container_platform/4.22/html/virtualization/managing-vms)
- [Sandbox validator](https://github.com/codeready-toolchain/member-operator/blob/master/pkg/webhook/validatingwebhook/validate_vm_request.go)
- [Sandbox mutator](https://github.com/codeready-toolchain/member-operator/blob/master/pkg/webhook/mutatingwebhook/vm_mutate.go)

## Revised Create VM run and inventory timing

Commit `7af4ac7`, Create VM job **#10**, succeeded in approximately **199 seconds**:

- Reused the SSH identity from the first attempt.
- Provisioned and booted the VM with Manual strategy and 2 GiB guest RAM.
- Completed authenticated SSH verification.
- Had **832 bytes** of inline cloud-init after Sandbox mutation.
- Referenced only the public-key Secret from the VM. A separate read-only check
  confirmed the two stored public keys match and neither the SSH identity Secret
  nor the generated public-key value appears in the VM manifest.

Inventory update **#12** succeeded but captured a transient guest-agent interface
report without IP fields. Update **#13** then populated the address without any
VM or networking changes. The candidate's startup readiness now waits for both
`AgentConnected=True` and an IP on the guest-agent-reported default interface,
rather than accepting only the earlier pod-derived IP.

The separate fresh-EE job **#14** succeeded using only the OpenShift credential:
Ansible returned `pong`, passwordless sudo returned exit code 0, and temporary
SSH files were removed. Secret read/staging task results were censored.

Delete VM job **#15** succeeded in approximately **31 seconds**. Independent
read-only API checks then returned 404 for the VM, DataVolume, PVC and both
Secrets.

## Final fresh lifecycle: passed

The final run used commit `d11a722`, the pinned supported EE and only the
explicitly associated OpenShift credential. No Machine credential, learner-made
SSH key, or AAP API credential was supplied to the playbooks.

An intermediate test-harness guard incorrectly treated the deprecated
inventory-source `credential` field's null value as a missing credential.
The actual `credentials/` relation is authoritative. A later read-only audit of
inventory updates #12, #13, #16 and #20 confirmed that all already used the
intended user-token credential. The earlier description of a missing
association was incorrect. The guard was corrected to inspect the relation;
this was a harness change, not a learner-playbook or authentication fix.

| Stage | AAP job/update | Result | Execution time |
| --- | --- | --- | --- |
| Project sync | 17 | Passed; exact tested revision | 2.7 s |
| Fresh Create VM | 18 | Passed; new identity generated automatically | 259.4 s |
| First inventory sync | 20 | Passed; one host with an address, no retry | 5.3 s |
| Fresh-EE SSH and sudo | 21 | Passed | 10.4 s |
| Stop VM | 22 | Passed | 19.3 s |
| Start VM | 23 | Passed; authenticated SSH verified | 49.3 s |
| Inventory refresh | 24 | Passed; address present | 5.3 s |
| Fresh-EE SSH and sudo after restart | 25 | Passed | 11.2 s |
| Delete VM | 26 | Passed | 30.8 s |
| Inventory cleanup | 27 | Passed; zero hosts | 5.3 s |

The VM retained `runStrategy: Manual`, used 2 GiB guest RAM and a 30 GiB boot
disk, and had 832 bytes of inline user data after Sandbox mutation. Its only
SSH access-credential reference was to the public-key Secret.

Secret-handling task results were censored. The monitored job events contained
no detected private-key or token markers. Temporary local monitoring-token
files were removed after each monitor finished.

Independent read-only cleanup verification returned 404 for:

- VirtualMachine and VirtualMachineInstance
- DataVolume and boot PVC
- SSH identity Secret and cloud-init public-key Secret

No matching test launcher pod, volume snapshot, or PVC remained. Namespace storage quota
returned to its starting usage of **2 PVCs / 18 GiB**, and the isolated AAP
inventory had **zero hosts**. Existing workloads, RBAC, quotas and networking
were not changed. Remote `main` was not updated.

The test AAP project, inventory source, templates and encrypted OpenShift
credential remain available for the next approved checks.

## Namespace-scoped ServiceAccount: passed

The same improved playbooks at `d11a722` were tested again, changing only the
OpenShift authentication identity:

- Temporary ServiceAccount `aap-lab-validation`.
- Namespaced RoleBinding `aap-lab-validation-edit` referencing the existing
  `edit` ClusterRole, with only that ServiceAccount as its subject.
- No ClusterRole, ClusterRoleBinding, or grant in another namespace was created
  or modified.
- TokenRequest requested **720 hours** and received exactly **30 days** with no
  warnings, matching the original Lesson 1 request on this cluster.
- The token was stored in an encrypted, temporary AAP OpenShift credential.
  No plaintext ServiceAccount token was written locally or committed.
- All five isolated validation templates and the inventory source were verified
  to use only that credential before the test.

The test identity's names differed from the guide only to isolate and identify
the temporary resources. Its permissions and authentication mechanism matched
the published ServiceAccount/namespace-edit setup. This was not a test of the
old playbooks or manual SSH-key instructions.

| Stage | AAP job/update | Result | Execution time |
| --- | --- | --- | --- |
| ServiceAccount inventory preflight | 28 | Passed | 5.0 s |
| Create VM and clone the shared RHEL image | 29 | Passed; new keys generated automatically | 175.8 s |
| Inventory sync | 30 | Passed; address present | 5.3 s |
| Fresh-EE SSH and sudo | 31 | Passed | 10.3 s |
| Stop VM | 32 | Passed | 14.4 s |
| Start VM | 33 | Passed | 55.3 s |
| Inventory refresh | 34 | Passed; address present | 5.3 s |
| Fresh-EE SSH and sudo after restart | 35 | Passed | 10.5 s |
| Delete VM | 36 | Passed | 30.8 s |
| Inventory cleanup | 37 | Passed; zero hosts | 5.1 s |

The VM retained Manual strategy, 2 GiB guest RAM and a 30 GiB boot disk.
Inline user data was 832 bytes after Sandbox mutation. Monitored events
contained no detected private-key or tested ServiceAccount-token markers.

Afterward, the isolated AAP templates and source were restored to their original
test credential, and the temporary AAP ServiceAccount credential was deleted.
The temporary RoleBinding and ServiceAccount were then deleted with UID
preconditions, revoking the test identity without touching other resources.
Independent API checks confirmed all VM resources, both Secrets, the identity
resources and temporary AAP credential were absent. Storage returned to
**2 PVCs / 18 GiB** and inventory to **zero hosts**. Temporary monitoring files
were removed.

Learners should keep their one-time ServiceAccount/RoleBinding while they use
the sandbox. Normal Delete VM does not remove that reusable automation identity.

### Remaining validation

- Reconcile the original service-account client-ID/secret instructions with
  the registration role's activation-key/organization-ID inputs, then verify
  fresh registration with approved credentials. Registration was deferred
  during the core tests but is now required for the next phase.
- Prove package/repository access by installing a small approved package that
  was not already present; do not infer it from preinstalled packages.
- Execute Timesync and the actual four-node learner workflow on the same
  retained VM. Unregister the test consumer before final VM cleanup.
- Complete the provisioning-screen UI review and the remaining role/workflow
  validation before publishing the revised learner instructions.

## Guide revision

The working learning path now uses the verified core experience rather than
retaining obsolete SSH setup as active instructions:

- Kept the one-time OpenShift ServiceAccount/namespace-edit approach, with
  namespace-explicit commands and an issued-expiration caveat.
- Selected the existing default supported EE; removed custom EE/Quay setup.
- Removed manual SSH key generation, key blocks, uploads, Machine credentials,
  VM passwords and public-key inventory inputs.
- Documented all six `playbooks/` paths and the one OpenShift credential.
- Explained post-provision inventory sync, lifecycle actions and cleanup.
- Added the documentation-based workflow visualizer walkthrough, explicitly
  marked as not yet executed as a Workflow Job Template.
- Marked registration and Timesync as pending rather than presenting the
  unverified Red Hat client-ID/client-secret mapping as working instructions.

The original account setup and key-redacted source text remain in commit
`7f87ce6`. The working project instructions explicitly select the validation
branch because the new layout is not merged into `main`.

## Resource sizing review

The existing defaults are retained for the first real test: **2 GiB guest RAM
and a 30 GiB boot disk**.

- The sandbox's `rhel9` DataSource currently references a **30 GiB Block PVC**
  on `gp3`. Reducing the target to 20 GiB is not a drop-in replacement for this
  source-cloning path; it needs a separately validated image/storage approach.
- [RHEL 9 installation requirements](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/9/html/interactively_installing_rhel_from_installation_media/system-requirements-and-supported-architectures_rhel-installer)
  list 1.5 GiB for local-media installation on x86_64. This is installation
  guidance, not proof that a preinstalled cloud guest cannot run in 1 GiB.
  A lower runtime allocation must be assessed against the actual registration
  and system-role workload before becoming the beginner-lab default.

The admitted test VM's launcher `compute` container reserved **2316 MiB**
for the 2 GiB guest plus virtualization overhead. Its CPU request was **100m**
and CPU limit **1**, despite exposing one vCPU to the guest. These are resource
allocations, not measured guest workload utilization.
