# aap-sandbox-project

Beginner-focused Ansible Automation Platform sandbox automation for RHEL VMs
on OpenShift Virtualization.

Follow the [learning path](docs/learning-path.md) to configure AAP, provision
a VM, register RHEL, configure Timesync, and run a four-node workflow.
SSH identities are generated automatically; no manual key handling or custom
execution environment is required.

## Repository layout

```text
.
├── ansible.cfg                   # Finds the shared project role
├── dependencies/
│   └── collections.yml           # Explicit developer dependency manifest
├── docs/
│   ├── learning-path.md          # Step-by-step learner instructions
│   └── credential-type-redhat-registration.yml # Importable AAP credential type
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

Existing AAP templates using root-level playbook names must be updated to the
`playbooks/` paths. No compatibility wrappers are kept at the root.
There is no static inventory or EE build directory: AAP supplies dynamic
inventory, and the supported EE already supplies the required content.

## Environment versions

Reference environment used on November 25, 2026, for troubleshooting version
differences. These are not minimum-version requirements.

| Component | Version |
| --- | --- |
| Ansible Automation Platform | 2.7 |
| Automation controller | 4.8.12 |
| OpenShift | 4.22.22 |
| Kubernetes | v1.35.9 |
| OpenShift Dev Spaces | 3.31 (user-reported) |
| Execution environment | Default execution environment (`ee-supported-rhel9`) |
| ansible-core in the EE | 2.16.19 |
| Python in the EE | 3.12.15 |

## Execution environment

Use AAP 2.7's **Default execution environment**, tested for installed content at:

```text
registry.redhat.io/ansible-automation-platform-27/ee-supported-rhel9@sha256:2318369ab1c83013228371694016836c058e0b891f405fa0ae8af83a54e7ba39
```

Collections used from that EE:

| Collection | Version |
| --- | --- |
| `redhat.openshift` | 6.0.0 |
| `redhat.openshift_virtualization` | 2.3.0 |
| `kubernetes.core` | 6.4.0 |
| `redhat.rhel_system_roles` | 1.120.5 |

No custom EE build or Quay credential is required.
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

Set these variables on `inventory-sandbox`:

```yaml
vm_name: rhel9-server
ocp_namespace: <your-namespace>
```

The playbooks do not require `ssh_public_key`, `vm_password`, or a Machine
credential. All six job templates use `credential-ocp`, the OpenShift or
Kubernetes API Bearer Token credential. Never put the token in inventory
variables, Git, or job output.

Create one OpenShift ServiceAccount with the existing `edit` ClusterRole bound
only in your namespace. Its token goes in `credential-ocp`; no cluster-wide
binding is required. Request a token with `oc create token` as described in
the learning path. Token duration is subject to server policy: check the
actual issued expiration and warnings. Retain this identity across VM
create/delete cycles; when its token expires, request a replacement and update
`credential-ocp`.

`rhel_register.yml` consumes `activation_key` and `organization_id`.
This is the method recommended by the official RHEL
system-roles documentation, mapped to `redhat.rhel_system_roles.rhc` as
`rhc_auth.activation_keys.keys` and `rhc_organization`. Supply them through a
credential of the minimal custom type defined in
[docs/credential-type-redhat-registration.yml](docs/credential-type-redhat-registration.yml):
the activation key is a secret field that AAP masks and injects under the
existing variable name. Never put registration secrets in Git, inventory
variables, or job output.

Registering with the `rhc` role follows the role defaults: it installs
`insights-client` and `rhc`, and connects the guest to Red Hat Lightspeed
(Insights) with auto-update and remediation enabled. Unregistering the guest
(`rhc_state: absent`) removes both the RHSM consumer and the Lightspeed
connection. The built-in Insights credential type cannot be attached to job
templates; use the custom registration type linked above.

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

## How SSH access works

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

**Unregister a registered guest from RHSM and disconnect Red Hat Lightspeed
before deleting it.** Delete VM does not perform unregistration. If
unregistration fails, retain the VM so you can retry rather than orphaning its
consumer record.

Create does not adopt existing unmanaged VMs or disks. If an existing VM loses
its SSH Secret, the playbook fails rather than generate a replacement identity
that the existing guest would not recognize.

### Sandbox-specific cloud-init policy

The Sandbox admission webhook requires an inline cloud-init `user` field;
a `users` list alone or an entire bootstrap referenced through
`userDataSecretRef` does not satisfy that check. Its mutating webhook also
appends platform-managed SSH keys to inline user data.

The VM follows OpenShift's documented static-key injection pattern:
minimal, non-sensitive inline user configuration plus a separate public-key
Secret referenced through `accessCredentials`. Generated project keys are not
embedded in the VM manifest. The RHEL image supplies its default cloud user's
sudo configuration; the separate SSH-verification job checks passwordless sudo.

`Manual` is also enforced by the Sandbox webhooks for compatibility with the
Sandbox idler. It is not merely an old collection workaround.

Internet NTP (UDP/123) was unreachable in the tested Sandbox. Timesync applies
the intended configuration and starts chronyd, but actual synchronization with
internet NTP pools is not demonstrated; `chronyc tracking` can report
"Not synchronised".

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

## Local checks

Inside the chosen EE, run:

```bash
python3 tests/check.py
```

This parses YAML, syntax-checks every entry-point playbook and role task file,
checks for `ssh-keygen`, and renders the VM/cloud-init templates with a
nonfunctional public-key placeholder. It also checks the existing inventory
variable interface against a local-only fixture. It neither generates real
credentials nor calls OpenShift. It is not an end-to-end provisioning test.

`tests/playbooks/verify_ssh.yml` provides a separate AAP job to check guest
SSH/sudo access using `credential-ocp`, without changing guest configuration.

## Historical reference

The development [validation notes](https://github.com/ansible-tmm/aap-sandbox-project/blob/beef06bd03be1dc7987f6fa7d044ee1bb5898011/docs/validation.md)
and [implementation handoff](https://github.com/ansible-tmm/aap-sandbox-project/blob/beef06bd03be1dc7987f6fa7d044ee1bb5898011/docs/implementation-handoff.md)
are preserved at revision `beef06b` for reference, not as current setup instructions.
