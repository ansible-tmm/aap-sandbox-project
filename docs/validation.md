# Candidate validation

Recorded November 25, 2026. **OpenShift end-to-end validation is still pending.**

## Completed checks

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
