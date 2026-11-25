# Explore Ansible Automation Platform in a ready-to-use sandbox

## Revision status and sources

This guide is based on a transcription of the Red Hat Developer learning path as
published on **November 25, 2026**, captured on that date. It is not a recovered
copy of the pages as they appeared at their original publication in May 2025.

The original baseline transcription, with key material replaced by placeholders,
is preserved in Git commit `7f87ce6`. This working draft updates the verified
VM experience for AAP 2.7 and OpenShift 4.22.22:

- Use the existing default supported EE, not a custom image.
- Keep the one-time OpenShift ServiceAccount and namespace `edit` binding.
- Generate and store SSH identities automatically; no learner key generation,
  key copying, file upload, or Machine credential.
- Use the `playbooks/` paths for job templates.
- Wait for guest-agent networking and authenticated SSH before Create finishes.

> **Validation scope:** the normal VM lifecycle, inventory, SSH/sudo and cleanup
> passed with both a user token and the namespace-scoped ServiceAccount token.
> Registration is deferred, Timesync has not run, and the workflow-visualizer
> walkthrough below has not yet been executed as a Workflow Job Template.
> Validation used API-launched component jobs, not a full manual UI walkthrough.
> The retained provisioning screens and revised copy need final editorial UI
> review. See [validation results](validation.md).

The validation branch is not merged into `main`. The project instructions below
therefore explicitly select `lab/supported-ee-validation` for review/testing.
Coordinate the final source-control revision and publication after approval.

Site navigation and footers are omitted. Images and original interactive guides
remain linked rather than copied; recordings may still show the older setup.

### Published sources

| Resource | Published date | Author(s) | Source |
| --- | --- | --- | --- |
| Overview | May 7, 2025 | Leonardo Gallego, Craig Brandt | [Red Hat Developer overview](https://developers.redhat.com/learn/ansible/explore-ansible-automation-platform-ready-use-sandbox) |
| Lesson 1: Provision a Developer Sandbox instance | May 8, 2025 | Leonardo Gallego | [Red Hat Developer lesson 1](https://developers.redhat.com/learning/learn:ansible:explore-ansible-automation-platform-ready-use-sandbox/resource/resources:provision-developer-sandbox-instance) |
| Lesson 2: Create a registry credential, execution environment, service account, and dynamic inventory | May 8, 2025 | Leonardo Gallego | [Red Hat Developer lesson 2](https://developers.redhat.com/learning/learn:ansible:explore-ansible-automation-platform-ready-use-sandbox/resource/resources:create-registry-credential-execution-environment-service-account-and-dynamic-inventory) |
| Lesson 3: Configure job templates and use cases | May 12, 2025 | Leonardo Gallego | [Red Hat Developer lesson 3](https://developers.redhat.com/learning/learn:ansible:explore-ansible-automation-platform-ready-use-sandbox/resource/resources:configure-job-templates-and-use-cases) |

### Contents

- [Overview](#overview)
- [Lesson 1: Provision a Developer Sandbox instance](#lesson-1-provision-a-developer-sandbox-instance)
- [Lesson 2: Use the supported execution environment and configure dynamic inventory](#lesson-2-use-the-supported-execution-environment-and-configure-dynamic-inventory)
- [Lesson 3: Configure job templates and use cases](#lesson-3-configure-job-templates-and-use-cases)

---

## Overview

Original learning path: 4 resources | 45 mins | Published on May 7, 2025

[Leonardo Gallego](https://developers.redhat.com/author/leonardo-gallego)
[Craig Brandt](https://developers.redhat.com/author/craig-brandt)

Connect Ansible Automation Platform to your Developer Sandbox, provision a RHEL
VM, discover it through dynamic inventory, and manage its lifecycle without
manually handling SSH keys.

### Overview: Explore Ansible Automation Platform in a ready-to-use sandbox

![Ansible-sandbox-LP-feature-image](https://developers.redhat.com/sites/default/files/Ansible-sandbox-LP-feature-image.png)

Red Hat Ansible Automation Platform in the Developer Sandbox is a one-click deployment that you can use to learn and experiment with for 30 days. For this learning path, you will get access to a fully working instance of Ansible Automation Platform to try all of the features, including Event-Driven Ansible and private automation hub.

#### In this learning path, you will:

- Learn how to provision Ansible Automation Platform in the Developer Sandbox.
- Create a dedicated namespace-scoped OpenShift credential.
- Use the default supported execution environment and dynamic inventory.
- Provision, start, stop and delete a RHEL VM through job templates.
- Explore workflow design and prepare the follow-on RHEL configuration exercises.

The core exercise uses one VM with one vCPU, 2 GiB guest RAM and a 30 GiB
boot disk. The provided RHEL boot source is backed by a 30 GiB Block PVC.
These are the tested settings, not a claim about minimum RHEL runtime sizing.

#### Details

**Related products:**

- [Developer Sandbox](https://developers.redhat.com/developer-sandbox)
- [Red Hat Ansible Automation Platform](https://developers.redhat.com/products/ansible/overview)
- [Red Hat OpenShift](https://developers.redhat.com/products/openshift/overview)

**Related topics:** [Automation](https://developers.redhat.com/topics/automation/all)

**Technical level:** Beginner

---

## Lesson 1: Provision a Developer Sandbox instance

May 8, 2025

[Leonardo Gallego](https://developers.redhat.com/author/leonardo-gallego)

**Related topics:** [Automation](https://developers.redhat.com/topics/automation/all)

**Related products:** [Red Hat Ansible Automation Platform](https://developers.redhat.com/products/ansible/overview)

![Ansible-sandbox-LP-feature-image](https://developers.redhat.com/sites/default/files/Ansible-sandbox-LP-feature-image.png)

In order to complete the steps of this learning path, the first thing you need to do is go to the [Developer Sandbox page](https://developers.redhat.com/developer-sandbox) and get a free instance of Ansible Automation Platform in the Developer Sandbox. If you don’t have a redhat.com account, you will be required to create one. You'll also be getting a Red Hat OpenShift Sandbox cluster and joining the [Red Hat Developer program](https://developers.redhat.com/about).

### In this lesson, you will:

- Provision Ansible Automation Platform in the Developer Sandbox.
- Subscribe to your instance.
- Set up the required settings to integrate Ansible Automation Platform with your Developer Sandbox instance.

---

### Provision Ansible Automation Platform in the Developer Sandbox

[Interactive guide embedded in the published lesson](https://demo.arcade.software/hCaq4jsAc1wMsd6gD3Ch)

Start by navigating to sandbox.redhat.com. Once there, follow these instructions to provision your Ansible Automation Platform sandbox:

1. For this lesson, you have two options to provision your sandbox instance:
   1. You can watch the interactive guide above
   2. or follow the steps and instructions below the video.
2. Go to [sandbox.redhat.com](https://sandbox.redhat.com/).
3. Select the **Developer Sandbox** card.
4. Click **Get started**.
5. Accept the modal.
6. Look for the Ansible Automation Platform card and click **Provision**.
7. Close the modal.

   **Note**: It might take up to 30 minutes to provision.

8. Wait for the Ansible Automation Platform card to show a Ready status and click **Launch**.
9. Copy the provided password from the modal pop-up.
10. Click **Log into Ansible Automation Platform**.

### Log into Ansible Automation Platform

A new browser tab will open with the Ansible Automation Platform login screen.

If login opens the dashboard directly, subscription setup is already complete:
continue to **Create an OpenShift credential**. Follow the subscription steps
below only when the setup wizard is displayed.

1. Enter admin for the username.
2. Paste the password you copied in Step 9 of the previous section then select **Log in**.
3. You will be presented with the Subscription screen. Click the **Username / Password** button.
4. Enter your redhat.com username.

   **Note**: This is your personal redhat.com account. Not the provided admin account.

5. Enter your password for your redhat.com account.
6. Click the **Subscription** field dropdown arrow.
7. Select the **Red Hat Developer Subscription for Individuals** option.
8. Click **Next**.
9. Read the End User License Agreement. Tick the checkbox if you agree.
10. Click **Next** then **Finish**.

Welcome to Ansible Automation Platform!

### Create an OpenShift credential

To be able to go through the exercises of this learning path, we will be integrating the Ansible Automation Platform sandbox to the Developer Sandbox by creating a credential in Ansible Automation Platform that will allow it to access our OpenShift cluster and apply our automation.

Later, using Ansible Automation Platform, we will deploy a Red Hat Enterprise Linux virtual machine (VM) in our Red Hat OpenShift Virtualization instance using this credential.

Watch the following interactive guide to create the OpenShift credentials in Ansible Automation Platform or follow the instructions below:

[Interactive guide embedded in the published lesson](https://demo.arcade.software/Y7i3om8ZThHcIPwm4VES)

Before getting your credentials, let’s log into the Developer Sandbox and verify your namespace.

1. Your namespace should be composed of your `<username>` and a `-dev` suffix. For example: `johnnybgoode-dev`.
2. In the **Sandbox** section of the Hybrid Cloud Console, find the OpenShift card and click **Launch**.
3. A new browser tab will open. Log in by selecting **DevSandbox**.
4. You are now in the main OpenShift Sandbox dashboard. In the left sidebar, click the first dropdown showing **Developer**, and select **Administrator**.
5. In the top navigation bar to the right, click on the **console icon** to open a terminal window.

   **Note**: It will take a moment. If it asks you to select a project, select the one mentioned above with the `-dev` suffix.

6. To verify your namespace is correct, type `oc project`.
7. It will display a message similar to:

   `“Using project "<username>-dev" from context named "<username>-context" on server "https://ip:443".”`

8. Your namespace is `<username>-dev`. **Note**: Take note of your namespace for the next steps.

#### Step 1: Create an OpenShift ServiceAccount token

Create a dedicated automation identity once for your namespace. AAP will use
its token through `credential-ocp`; you will not need a separate SSH credential.

1. The terminal should already be open from the previous steps, but if it isn't, click the console icon in the top navigation bar to open a new terminal window.
2. Confirm that the active project is your `<username>-dev` namespace, then run:

   ```bash
   NAMESPACE="$(oc project -q)"
   oc create serviceaccount "sa-${NAMESPACE}" --namespace "${NAMESPACE}"
   oc create rolebinding sa-aap-sandbox-role --namespace "${NAMESPACE}" \
     --clusterrole=edit --serviceaccount="${NAMESPACE}:sa-${NAMESPACE}"
   oc create token "sa-${NAMESPACE}" --namespace "${NAMESPACE}" --duration=720h
   ```

3. Copy the token for the credential form below. Treat it as a password; do not
   put it in Git, inventory variables, or these instructions.

The RoleBinding references the existing `edit` ClusterRole **only within your
namespace**. It is not a cluster-wide binding. This access includes the VM and
Secret operations required by the playbooks.

The API honored the requested 30 days in validation. Token duration is still
subject to server policy: check warnings and the actual expiration. Keep the
ServiceAccount and binding while using the sandbox; do not delete them when
deleting an individual VM.
If the token expires, request another token for the same ServiceAccount and
update `credential-ocp`; do not recreate the VM or its SSH identity just to
refresh API access.

### Step 2: Gather the Server URL

You are now in the main Developer Sandbox dashboard:

1. In the top navigation bar to the right, click on your username dropdown for a menu.
2. Click **Copy login command**.
3. This will open a new browser tab. Click **Display Token** at the top left.
4. Copy the full Server URL (starting from https). You can find it in the `server=https://…` line.

### Create an OpenShift credential using a token

1. In the Ansible Automation Platform sidebar, select the **Automation Execution** > **infrastructure** dropdown, then the **Credentials** option.
2. In the new screen, click on **Create credential**.
3. Fill out the following details:
   - Name: credential-ocp
   - Credential Type: OpenShift or Kubernetes API Bearer Token
   - OpenShift or Kubernetes API Endpoint: \<paste the Server URL from step 2 above\>
   - API authentication bearer token: \<paste the token here\>
   - Verify SSL: Checked
4. Select **Create credential**.

Choose execution environments on projects, inventory sources and job templates,
not on this credential. The same `credential-ocp` is reused throughout the lab.

---

## Lesson 2: Use the supported execution environment and configure dynamic inventory

May 8, 2025

[Leonardo Gallego](https://developers.redhat.com/author/leonardo-gallego)

**Related topics:** [Automation](https://developers.redhat.com/topics/automation/all)

**Related products:** [Red Hat Ansible Automation Platform](https://developers.redhat.com/products/ansible/overview)

![Ansible-sandbox-LP-feature-image](https://developers.redhat.com/sites/default/files/Ansible-sandbox-LP-feature-image.png)

Now that AAP can access your namespace, select the supplied execution environment
and configure an inventory that discovers the VMs created by this project.

### In this lesson, you will:

- Use the default supported execution environment.
- Create a dynamic inventory.

---

### Use the default supported execution environment

An execution environment contains Ansible, collections and the libraries used
to execute automation. AAP 2.7's supplied supported EE includes the content
needed for the tested VM lifecycle.

1. Go to **Automation Execution > Infrastructure > Execution Environments**.
2. Find **Default execution environment**, using the AAP 2.7
   `ee-supported-rhel9` image.
3. Use this existing entry wherever the following instructions request an EE.
   Do not select the Minimal execution environment.

There is no custom EE to build, no `ee-sandbox` to create, and no Quay credential
to configure for this revision. The exact tested image and collection versions
are recorded in the [repository README](../README.md).

The OpenShift ServiceAccount created in Lesson 1 is the only automation identity
needed for the core VM exercise. The separate Red Hat registration account
exercise remains deferred; it is not required to generate SSH keys or provision
the VM.

### Create a dynamic inventory for OpenShift Virtualization

Now we will continue our Ansible Automation Platform sandbox integration to the Developer Sandbox by creating a dynamic inventory, which will automatically populate our Ansible Automation Platform inventory with the VMs available in our cluster.

An inventory in Ansible Automation Platform is a collection of hosts or systems that Ansible can manage. It defines the infrastructure targets for automation and can be grouped and organized to control where and how playbooks run.

A dynamic inventory automatically pulls host information from external sources like cloud providers or CMDBs. In this case, we will be sourcing from OpenShift Virtualization for the VMs. To do this:

1. In the Ansible Automation Platform sidebar, go to **Infrastructure** > **Inventory** option then select **Create inventory**.
2. Fill out the form with the following:
   - Name: inventory-sandbox
   - Organization: Default
   - Extra variables:

   ```yaml
   vm_name: rhel9-server
   ocp_namespace: <your-namespace>
   ```

3. Select **Create inventory**.
4. In the inventory, click the **Sources** tab then **Create source**.
5. Fill out the form with the following:
   - Name: inventory-virt-sandbox
   - Execution environment: Default execution environment
   - Source: OpenShift Virtualization
   - Credential: credential-ocp
   - Verbosity: 1 (info)
   - Overwrite: Checked
   - Overwrite variables: Checked
   - Update on launch: Checked
   - Extra variables:

   ```yaml
   namespaces:
     - <your-namespace>
   label_selector: app.kubernetes.io/part-of=aap-sandbox-project
   host_format: "{namespace}-{name}"
   ```

6. Select **Create source**.
7. In the new screen with the inventory details, select **Launch inventory update** in the top right corner.
8. The Last job status will switch to Running and should display Success when it finishes.

It is normal for this first update to discover **zero VMs** before Create VM
has run. The label selector keeps unrelated VMs out of the lab inventory.

You do not enter a VM password or public key here. Create VM generates the
identity and configuration automatically.

---

## Lesson 3: Configure job templates and use cases

May 12, 2025

[Leonardo Gallego](https://developers.redhat.com/author/leonardo-gallego)

**Related topics:** [Automation](https://developers.redhat.com/topics/automation/all)

**Related products:** [Red Hat Ansible Automation Platform](https://developers.redhat.com/products/ansible/overview)

![Ansible-sandbox-LP-feature-image](https://developers.redhat.com/sites/default/files/Ansible-sandbox-LP-feature-image.png)

Import the project, create lifecycle templates, and run the VM exercise using
the one OpenShift credential from Lesson 1.

### In order to get full benefit from taking this lesson, you need:

- A Red Hat Developer account.

### In this lesson, you will:

- Import playbooks.
- Build job templates.
- Provision and discover a RHEL VM with no manual SSH-key setup.
- Stop, restart and clean up the VM.
- Prepare a workflow and the follow-on RHEL exercises.

---

### Import ready-to-use playbooks

The first step to managing your sandbox is creating a project:

1. In the Ansible Automation Platform sidebar, go to **Automation Execution > Projects** then click **Create project**.
2. Fill out the following details:
   - Name: aap-sandbox-project
   - Organization: Default
   - Default execution environment: Default execution environment
   - Source control type: Git
   - Source control URL: https://github.com/ansible-tmm/aap-sandbox-project.git
   - Source control branch/tag/commit: `lab/supported-ee-validation`
3. Select **Create project**.
4. Wait for the project sync to succeed.

> **Publication note:** the validation branch is required while this revision
> remains unmerged. Update the source-control revision to the approved release
> when publishing; do not omit it and accidentally use the old `main` playbooks.

### How SSH access is prepared automatically

Do **not** create `credential-ssh` or generate/upload an SSH key.

Create VM generates a unique per-VM key pair inside its execution environment.
It stores the identity in `<vm_name>-ssh` and the public key separately in
`<vm_name>-cloudinit`. KubeVirt injects the public key at boot; only minimal
non-sensitive user configuration is inline.

Guest jobs retrieve the identity through `credential-ocp`, use a temporary
permission-`0600` file inside the EE, and remove that file afterward.
No key is committed, pasted into instructions, or entered as an inventory
variable. The namespace ServiceAccount supplies API access, not the guest's
SSH identity.

Anyone allowed to read the SSH Secret can obtain the private key. This is a
dedicated, disposable sandbox design; a Kubernetes Secret is not encrypted
merely because its data is base64-encoded.

### Create the four VM lifecycle templates

1. Go to **Automation Execution > Templates**.
2. From **Create template**, choose **Create job template**.
3. Use these common settings:
   - Job type: Run
   - Inventory: inventory-sandbox
   - Project: aap-sandbox-project
   - Execution environment: Default execution environment
   - Credentials: credential-ocp
   - Limit: leave blank
   - Enable concurrent jobs: Unchecked
4. Create one template for each row:

   | Name | Playbook |
   | --- | --- |
   | Create VM | `playbooks/ocp_vm_create.yml` |
   | Delete VM | `playbooks/ocp_vm_delete.yml` |
   | Start VM | `playbooks/ocp_vm_start.yml` |
   | Stop VM | `playbooks/ocp_vm_stop.yml` |

5. Select **Create job template** after completing each form.

Do not limit Create or Start to `localhost`: each uses a second play to verify
SSH to the VM. Use the selected VM name consistently throughout this one-VM
exercise, and do not run competing lifecycle jobs simultaneously.

### Provision the VM and refresh inventory

1. Launch **Create VM**.
2. Wait for Success. The job clones the RHEL boot disk, starts the VM, waits
   for the guest-agent network report and verifies authenticated SSH. The
   validation runs took several minutes; allow provisioning to finish.
3. Open `inventory-sandbox` and its `inventory-virt-sandbox` source.
4. Select **Launch inventory update** and wait for Success.
5. In the inventory's **Hosts** tab, find `<your-namespace>-rhel9-server`.
   Its variables should include `ansible_host`.

Create's temporary in-job host does not replace a saved inventory update.
An explicit sync after provisioning discovers the newly created VM.

The Sandbox requires `runStrategy: Manual` for its idler. Create explicitly
starts the VM, so a separate Start launch is not needed immediately afterward.

### Stop and restart the VM

1. Launch **Stop VM** and wait for Success.
2. Launch **Start VM** and wait for Success. This job also checks networking
   and authenticated SSH.
3. Refresh `inventory-virt-sandbox` so saved inventory reflects the current
   address.

The disk and identity Secrets persist across stop/start. If the Sandbox later
idles the VM, use Start again before running guest automation.

### Follow-on RHEL configuration exercises

> **Not yet validated:** registration is deferred, and Timesync has not been
> executed. These settings describe the retained playbooks, not completed tests.

When the follow-on exercises are ready, use the same project, inventory,
supported EE and `credential-ocp`:

| Name | Playbook | Privilege escalation |
| --- | --- | --- |
| RHEL Register | `playbooks/rhel_register.yml` | Enabled |
| RHEL Timesync | `playbooks/rhel_timesync.yml` | Enabled |

Both playbooks retrieve the generated SSH identity automatically. The supplied
image's passwordless sudo access has been verified; no additional Machine
credential is required.

**Registration remains deferred.** `rhel_register.yml` still consumes
`activation_key` and `organization_id` and uses `redhat.rhel_system_roles.rhc`.
The original Hybrid Cloud Console client-ID/client-secret mapping has not been
verified and is not repeated here as an instruction. Authentication input setup
must be finalized before enabling this exercise. Do not commit registration
secrets or paste them into the guide.

The planned Timesync exercise uses `redhat.rhel_system_roles.timesync` with
`0.rhel.pool.ntp.org` preferred and `1.rhel.pool.ntp.org` as a pool.
Package/repository requirements and the role execution still need validation;
do not assume registration is either required or unnecessary until checked.

### Build a Workflow Job Template

> **Draft walkthrough:** the component VM jobs and explicit inventory updates
> passed in sequence, but this visualizer-defined workflow has not yet been run.
> The RHEL nodes also remain pending as described above.

Start with the core provisioning sequence:

```text
Create VM → inventory-virt-sandbox sync
```

1. Go to **Automation Execution > Templates**.
2. From **Create template**, choose **Create workflow job template**.
3. Enter:
   - Name: workflow-sandbox-rhel
   - Organization: Default
   - Inventory: inventory-sandbox
   - Limit: leave blank
   - Enable concurrent jobs: Unchecked
4. Select **Create workflow job template**. The workflow visualizer opens.
5. Select **Add step**:
   - Node type: Template
   - Job template: Create VM
   - Finish the node wizard. The root's edge type is Always.
6. From the Create VM node, add a subsequent step:
   - Node type: Inventory Sync
   - Inventory source: inventory-virt-sandbox
   - Edge type: Run on success
   - Finish the node wizard.
7. Select **Save** to save the workflow. Closing the visualizer without saving
   discards its changes.

The explicit inventory node runs **after** provisioning, so the new VM can be
discovered. It must select the source `inventory-virt-sandbox`, not just its
parent inventory. Child templates supply their own EE and credentials.

After the RHEL exercises are verified, extend the graph with two more
**Template** nodes, each connected with **Run on success**:

```text
Create VM
    → inventory-virt-sandbox sync
        → RHEL Register
            → RHEL Timesync
```

Use **RHEL Register** for the third node and **RHEL Timesync** for the fourth.
Save the entire graph. Do not launch this four-node extension before the
registration inputs and both RHEL exercises have been validated.

This walkthrough follows the
[AAP 2.7 workflow visualizer documentation](https://docs.redhat.com/en/documentation/red_hat_ansible_automation_platform/2.7/develop-con_controller_workflow_visualizer).
Its actual execution remains a separate validation step.

### Clean up the disposable VM

1. Launch **Delete VM** and wait for Success.
2. Refresh `inventory-virt-sandbox`; the generated host should disappear.

Delete removes the VM, boot DataVolume/PVC and both generated Secrets.
**The VM's disk contents are lost.** Keep your ServiceAccount, RoleBinding,
`credential-ocp`, project and inventory for another run.

Creating the VM again generates a new identity automatically; no local key
files or credential uploads need to be repeated.

### Summary

You connected AAP to your namespace with a dedicated ServiceAccount, used the
default supported EE, discovered a RHEL VM through dynamic inventory, and
managed its lifecycle with automatic SSH credentials and cleanup.
The follow-on RHEL exercises and full workflow remain draft sections until
their remaining validation is complete.

Ready to learn more about how Ansible automates? Try these learning paths:

- [Foundations of Ansible](https://developers.redhat.com/learn/ansible/foundations-ansible)
- [Get started with Ansible Playbooks](https://developers.redhat.com/learn/ansible/get-started-ansible-playbooks)
- [Streamline automation in OpenShift Dev Spaces with Ansible](https://developers.redhat.com/learn/openshift/streamline-automation-openshift-dev-spaces-ansible)
