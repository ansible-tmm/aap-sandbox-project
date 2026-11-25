# Candidate validation

Recorded November 25, 2026. **OpenShift end-to-end validation is still pending.**

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

The final supported-EE check ran as AAP ad hoc diagnostic **#4**, using the
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

## What these checks do not establish

No candidate playbook has created a VM or Secret, started/stopped a guest,
retrieved its real SSH identity, or deleted its storage. No registration or
Timesync operation was run. Module availability and template correctness are
not proof of API admission, storage provisioning, network reachability, or
guest authentication.

The next approved test is the normal Create → inventory sync → fresh-job SSH
verification → Stop → Start → Delete sequence described in the README.
Its test-branch push and named OpenShift resources require confirmation first.

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
- Created no VM, DataVolume, or boot PVC. The two managed Secrets remain for
  the normal retry/cleanup path.

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
Secrets. The final fresh lifecycle run with the stronger readiness gate is
still pending.

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
