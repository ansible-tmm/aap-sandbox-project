# aap-sandbox-project

Beginner-focused Ansible Automation Platform sandbox automation for RHEL VMs
on OpenShift Virtualization.

> **VM lifecycle validated:** the pinned supported EE completed fresh VM
> provisioning, inventory sync, automatic SSH/sudo access, stop/start and cleanup.
> Both user-token and namespace-scoped ServiceAccount authentication passed.
> The guide now reflects the verified core flow. Registration is deferred;
> Timesync, workflow execution and the final provisioning-screen UI review
> remain pending before publication.

## Repository layout

```text
.
├── ansible.cfg                   # Finds the shared project role
├── dependencies/
│   └── collections.yml           # Explicit developer dependency manifest
├── docs/
│   ├── learning-path.md          # Published-guide transcription and revisions
│   └── validation.md             # Recorded checks and remaining test gate
├── playbooks/                    # Select these paths in AAP job templates
│   ├── ocp_vm_create.yml
│   ├── ocp_vm_delete.yml
│   ├── ocp_vm_start.yml
│   ├── ocp_vm_stop.yml
│   ├── rhel_register.yml
│   └── rhel_timesync.yml
├── roles/
│   └── sandbox_vm/
│       ├── defaults/main.yml     # Settings and existing inventory-var mappings
│       ├── tasks/                # Lifecycle, generated keys, SSH setup/cleanup
│       ├── templates/            # VM manifest and minimal user bootstrap
│       ├── vars/main.yml         # Internal resource labels
│       └── README.md
└── tests/
    ├── check.py                  # Local syntax/template checks; no cluster calls
    └── playbooks/verify_ssh.yml   # Fresh-job SSH check without guest changes
```

The original guide is preserved in commit `7f87ce6`. Existing AAP templates
using root-level playbook names must be updated to the `playbooks/` paths
when adopting this revision. No compatibility wrappers are kept at the root.
There is no static inventory or EE build directory: AAP supplies dynamic
inventory, and the supported EE already supplies the required content.

## Execution environment

Use AAP 2.7's **Default execution environment**, tested for installed content at:

```text
registry.redhat.io/ansible-automation-platform-27/ee-supported-rhel9@sha256:2318369ab1c83013228371694016836c058e0b891f405fa0ae8af83a54e7ba39
```

Observed content: ansible-core 2.16.19, `redhat.openshift` 6.0.0,
`redhat.openshift_virtualization` 2.3.0, `kubernetes.core` 6.4.0, and
`redhat.rhel_system_roles` 1.120.5.

No custom EE build or Quay credential is required for this candidate.
The pinned image must remain pullable by the execution environment.

Dependencies are declared in `dependencies/collections.yml`, deliberately
outside AAP's automatic project-sync requirements paths. The supported EE
already includes them; project sync should not introduce another certified
content download or Automation Hub credential requirement.

For a separately configured developer environment with certified-content access:

```bash
ansible-galaxy collection install -r dependencies/collections.yml
```

## AAP inputs

Keep these existing variables on `inventory-sandbox`:

```yaml
vm_name: rhel9-server
ocp_namespace: <your-namespace>
```

The candidate does not require `ssh_public_key`, `vm_password`, or a Machine
credential. All six job templates use `credential-ocp`, the OpenShift or
Kubernetes API Bearer Token credential. Never put the token in inventory
variables, Git, or job output.

The original Lesson 1 authentication setup is sufficient: one OpenShift
ServiceAccount with the existing `edit` ClusterRole bound only in the learner's
namespace. Its token goes in `credential-ocp`; no extra cluster-wide grant was
needed in the real test. The API honored a requested 30-day duration on the
tested cluster. Check the server's actual issued expiration and warnings.
Learners retain this identity across VM create/delete cycles; our temporary
test identity was removed only as validation cleanup.

`rhel_register.yml` still consumes `activation_key` and `organization_id`
exactly as before. Their authentication flow remains under review; this
revision does not reinterpret service-account credentials or change the role's
authentication parameters. Supply real registration secrets securely, not in Git.

For `inventory-virt-sandbox`, select the supported EE, the OpenShift Virtualization
source, and `credential-ocp`. Source variables:

```yaml
namespaces:
  - <your-namespace>
label_selector: app.kubernetes.io/part-of=aap-sandbox-project
host_format: "{namespace}-{name}"
```

The label selector limits inventory to this lab's VMs. Guest playbooks check
that the target is the selected `ocp_namespace` / `vm_name` host, not an unrelated
inventory entry. Sync inventory after provisioning or restarting.

## How the candidate SSH flow works

1. **Create VM** generates a per-VM Ed25519 key pair inside its EE if the SSH
   Secret does not exist. Existing identities are reused, not rotated.
2. `<vm_name>-ssh` stores the private and public key. `<vm_name>-cloudinit`
   stores **only the public key**, for static injection into cloud-init at boot.
3. The VM uses `accessCredentials.sshPublicKey` with `propagationMethod.noCloud`
   to reference that public-key Secret. A tiny inline cloud-init document
   identifies `cloud-user` and disables password/root SSH login.
   The VM retains `runStrategy: Manual`; the playbook explicitly starts it and
   waits for the guest-agent network report and an authenticated SSH connection.
4. Each guest job retrieves the private key through `credential-ocp`, stages it
   in a private temporary EE directory with file mode `0600`, and removes the
   files in an `always` block.
5. **Delete VM** removes the managed VM, its DataVolume and both Secrets,
   and waits for CDI to garbage-collect the owned PVC. The boot disk is disposable.

Create does not adopt existing unmanaged VMs or disks. If an existing VM loses
its SSH Secret, the playbook fails rather than generate a replacement identity
that the existing guest would not recognize.

### Sandbox-specific cloud-init policy

The first real run generated both Secrets successfully, but the Sandbox
admission webhook rejected a VM whose entire user data was referenced through
`userDataSecretRef`. The Sandbox validates an inline `user` field; a `users`
list alone does not satisfy that check. Its mutating webhook also appends
platform-managed SSH keys to inline user data.

The candidate follows OpenShift's documented static-key injection pattern:
minimal, non-sensitive inline user configuration plus a separate public-key
Secret referenced through `accessCredentials`. Generated project keys are not
embedded in the VM manifest. The RHEL image supplies its default cloud user's
sudo configuration; the separate SSH-verification job checks passwordless sudo.

`Manual` is also enforced by the Sandbox webhooks for compatibility with the
Sandbox idler. It is not merely an old collection workaround.

- [OpenShift 4.22 static SSH-key injection](https://docs.redhat.com/en/documentation/openshift_container_platform/4.22/html/virtualization/managing-vms)
- [Sandbox VM validation implementation](https://github.com/codeready-toolchain/member-operator/blob/master/pkg/webhook/validatingwebhook/validate_vm_request.go)
- [Sandbox VM mutation implementation](https://github.com/codeready-toolchain/member-operator/blob/master/pkg/webhook/mutatingwebhook/vm_mutate.go)

### Security boundaries

- This is a disposable, single-user sandbox design, not an enterprise key vault.
  Anyone able to read the SSH Secret can obtain the guest's private key.
  Base64 encoding does not encrypt a Kubernetes Secret; cluster RBAC and the
  platform's at-rest encryption policy govern its protection.
- The generated private key is never included in cloud-init, the guest disk, project
  content, inventory variables, or intentional job output.
- Secret-handling tasks use `no_log` and suppress diffs. Temporary key files
  are outside project and artifact directories. Job termination can bypass
  `always`; the EE's ephemeral filesystem is the remaining cleanup boundary.
- SSH host keys use trust-on-first-use (`accept-new`) in a job-local
  known-hosts file. This is not persistent host-key pinning across jobs.
- Do not run competing lifecycle jobs for the same VM. Leave AAP's concurrent
  job execution disabled and use a sequential workflow.
- Check mode is explicitly refused: the credential-generation and boot/SSH
  sequence is not implemented as an admission-validation dry run.

## Candidate validation

See [recorded validation results](docs/validation.md) for completed local and
supported-EE checks, their scope, and the remaining end-to-end test.

Inside the chosen EE, run:

```bash
python3 tests/check.py
```

This parses YAML, syntax-checks every entry-point playbook and role task file,
checks for `ssh-keygen`, and renders the VM/cloud-init templates with a
nonfunctional public-key placeholder. It also checks the existing inventory
variable interface against a local-only fixture. It neither generates real
credentials nor calls OpenShift. It is not an end-to-end provisioning test.

Review the diff and approve a dedicated test-branch push before pointing an AAP
test project at it. AAP-only syntax diagnostics can be run without cluster
credentials, but provisioning and guest operations require separate approval.

Approved test scope must name the namespace and disposable VM, two Secrets,
DataVolume and PVC. Defaults request one vCPU, 2 GiB guest memory and a 30 GiB
disk. Check current quotas before applying; do not change existing workloads
or quotas automatically.

The normal test sequence is:

1. Run `playbooks/ocp_vm_create.yml`.
2. Sync the inventory source.
3. Run `tests/playbooks/verify_ssh.yml` as a separate AAP job using only
   `credential-ocp`. This proves a fresh EE can retrieve and use the identity
   and that the image permits the sudo access required by the system roles.
4. Run Stop VM, Start VM, then refresh inventory.
5. Repeat the separate SSH/sudo verification after restart.
6. Run Delete VM and confirm the VM, DataVolume, PVC, and both Secrets are gone.
7. Refresh inventory and confirm the generated host is removed.

No oversized cloud-init fixture is required. Registration and Timesync are
separate subsequent checks; the first provisioning test must not silently
change Red Hat registration or guest time configuration.

## Structure guidance

The layout follows the Red Hat Community of Practice guidance to keep entry-point
playbooks readable and reusable behavior in roles, without packaging a small
lab as a collection:

- [Automation structures](https://redhat-cop.github.io/automation-good-practices/structures/)
- [Playbooks](https://redhat-cop.github.io/automation-good-practices/playbooks/)
- [Roles](https://redhat-cop.github.io/automation-good-practices/roles/)
