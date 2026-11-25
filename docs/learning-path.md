# Explore Ansible Automation Platform in a ready-to-use sandbox

## Snapshot information

This is the baseline transcription of the Red Hat Developer learning path as
published on **November 25, 2026**, captured on that date. It is not a recovered
copy of the pages as they appeared at their original publication in May 2025.

The published instructions, examples, variable names, execution environment,
and job-template playbook assignments are preserved, including inconsistencies.
No proposed fixes, supported-EE migration, or workflow walkthrough have been
incorporated into this baseline.

Transcription conventions:

- Public and private SSH key material is replaced with
  `<lab-ssh-public-key>` and `<lab-ssh-private-key>` placeholders.
  These placeholders are not usable credentials.
- Formatting, heading levels, and whitespace are normalized for Markdown.
- Site navigation, repeated learning-path navigation, and site footers are omitted.
- Images remain linked to their original locations. Embedded interactive guides
  are represented by links.
- This section and the contents list are repository additions, not published
  lesson instructions.

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
- [Lesson 2: Create a registry credential, execution environment, service account, and dynamic inventory](#lesson-2-create-a-registry-credential-execution-environment-service-account-and-dynamic-inventory)
- [Lesson 3: Configure job templates and use cases](#lesson-3-configure-job-templates-and-use-cases)

---

## Overview

Learning path | 4 resources | 45 mins | Published on May 7, 2025

[Leonardo Gallego](https://developers.redhat.com/author/leonardo-gallego)
[Craig Brandt](https://developers.redhat.com/author/craig-brandt)

Automate time-consuming tasks like credentials, accounts, and templates, and create a centralized process with Ansible Automation Platform and the Developer Sandbox.

Access the Developer Sandbox

### Overview: Explore Ansible Automation Platform in a ready-to-use sandbox

![Ansible-sandbox-LP-feature-image](https://developers.redhat.com/sites/default/files/Ansible-sandbox-LP-feature-image.png)

#### Warning

The following learning path may contain outdated information. This may lead to a few steps not working as expected. We are working to correct this and appreciate your patience at this time.

Red Hat Ansible Automation Platform in the Developer Sandbox is a one-click deployment that you can use to learn and experiment with for 30 days. For this learning path, you will get access to a fully working instance of Ansible Automation Platform to try all of the features, including Event-Driven Ansible and private automation hub.

#### In this learning path, you will:

- Learn how to provision Ansible Automation Platform in the Developer Sandbox.
- Automate configuration management tasks on RHEL.
- Execute automation content by creating the required credentials, projects, inventories and job templates.

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

1. Enter admin for the username.
2. Paste the password you copied in Step 8 of the previous section then select **Log in**.
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

First, let’s create a ServiceAccount token to get 30-day access to the Developer Sandbox:

1. The terminal should already be open from the previous steps, but if it isn't, click the console icon in the top navigation bar to open a new terminal window.
2. Enter the following commands. Note: Replace `<your-namespace>` with your namespace.

   ```plaintext
   oc create serviceaccount sa-<your-namespace>
   oc create rolebinding sa-aap-sandbox-role --clusterrole=edit --serviceaccount=<your-namespace>:sa-<your-namespace>
   oc create token  sa-<your-namespace> --duration=$((30*24))h
   ```

3. Copy the token into your clipboard or somewhere safe.

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
   - Execution environment: ee-sandbox
   - OpenShift or Kubernetes API Endpoint: \<paste the Server URL from step 2 above\>
   - API authentication bearer token: \<paste the token here\>
4. Select **Create credential**.

Congratulations. You have provisioned your Developer Sandbox account and created an OpenShift credential using a token. In the next lesson, you'll learn all about tokens, credentials, and execution environments.

---

## Lesson 2: Create a registry credential, execution environment, service account, and dynamic inventory

May 8, 2025

[Leonardo Gallego](https://developers.redhat.com/author/leonardo-gallego)

**Related topics:** [Automation](https://developers.redhat.com/topics/automation/all)

**Related products:** [Red Hat Ansible Automation Platform](https://developers.redhat.com/products/ansible/overview)

![Ansible-sandbox-LP-feature-image](https://developers.redhat.com/sites/default/files/Ansible-sandbox-LP-feature-image.png)

Now that you have provisioned your Developer Sandbox account, it's time to learn all about tokens, credentials, and execution environments.

### In this lesson, you will:

- Create a registry credential.
- Build an execution environment.
- Create a service account.
- Create a dynamic inventory.

---

### Ansible Execution Environments

We will be using a custom Ansible Execution Environment as part of the exercises in this learning path. Ansible Execution Environments are dedicated containerized environments that include everything needed to run Ansible automation, including ansible-core, collections, and Python dependencies. For now, we will provide you with pre-built execution environments for the Ansible Automation Platform sandbox. You will be able to experiment with creating your own later on if you choose to.

### Create the execution environment

We will be using a custom Ansible Execution Environment as part of the exercises in this learning path. Ansible Execution Environments are dedicated containerized environments that include everything needed to run Ansible automation, including `ansible-core`, collections, and Python dependencies. For now, we will provide you with pre-built execution environments for the Ansible Automation Platform sandbox. You will be able to experiment with creating your own later on if you choose to.

Now we can proceed to create the execution environment in Ansible Automation Platform:

1. In the Automation Platform Sandbox sidebar, go to **Automation Execution** > **Infrastructure**, then select **Execution Environments**.
2. In the new screen, select **Create execution environment**.
3. Fill out the form with the following:
   - `Name: ee-sandbox`
     - `Image: quay.io/acme_corp/aap_sandbox_ee`
   1. Select **Create execution environment**.

### Create a Red Hat Service Account

An account can be either a user account or a service account. A user account authenticates human users in your organization. A service account authenticates applications or services without human intervention. Users create service accounts on Red Hat Hybrid Cloud Console for the following reasons:

- An application or service needs access to specific resources.
- The application or service needs to access resources without the need for human intervention.
- The application or service needs to access resources from multiple locations.

When you create a Red Hat service account, you generate a client ID and a secret. The service account uses the ID and secret to access services on the Red Hat Hybrid Cloud Console. The client ID identifies the service account with the resource, much like a username identifies a user. The secret provides a similar function as a password. The secret appears once when you create the service account. Copy and save the secret and protect it as you would any password.

Once you create client IDs and secrets, you will add them to our inventory variables in the next step:

1. From the [Red Hat Hybrid Cloud Console](https://sandbox.redhat.com/), go to **Settings > Service Accounts** and click **Create service account**.
2. Enter a Service account name and a short description then click **Create**.
3. Copy the generated Client ID and Client secret values to a secure location. You’ll specify these credentials when configuring a connection to a service.

   **Note**: After you save the Client ID and secret to a secure location.

4. Select the confirmation **check box** in the credentials window and close the window.

The service account and its Client ID appear on the [**Service Accounts**](https://console.redhat.com/iam/service-accounts/) page.

In the next step, for Ansible Automation Platform sandbox configuration purposes, we will refer to:

- Client ID as Organization ID = `<your-organization-id>`
- Secret as Activation Key = `<your-activation-key>`

### Create a dynamic inventory for OpenShift Virtualization

Now we will continue our Ansible Automation Platform sandbox integration to the Developer Sandbox by creating a dynamic inventory, which will automatically populate our Ansible Automation Platform inventory with the VMs available in our cluster.

An inventory in Ansible Automation Platform is a collection of hosts or systems that Ansible can manage. It defines the infrastructure targets for automation and can be grouped and organized to control where and how playbooks run.

A dynamic inventory automatically pulls host information from external sources like cloud providers or CMDBs. In this case, we will be sourcing from OpenShift Virtualization for the VMs. To do this:

1. In the Ansible Automation Platform sidebar, go to **Infrastructure** > **Inventory** option then select **Create inventory**.
2. Fill out the form with the following:
   - Name: inventory-sandbox
   - Organization: Default
   - Extra variables:

   ```plaintext
   vm_name: rhel9-server
   ocp_namespace: <your-namespace>
   vm_password: 123qwe
   activation_key: <your-activation-key>
   organization_id: <your-organization-id>
   ssh_public_key: <lab-ssh-public-key>
   ```

3. Select **Create inventory**.
4. In the inventory, click the **Sources** tab then **Create source**.
5. Fill out the form with the following:
   - Name: inventory-virt-sandbox
   - Execution environment: ee-sandbox
   - Source: OpenShift Virtualization
   - Credential: credential-ocp
   - Verbosity: 1 (info)
   - Overwrite: Checked
   - Update on launch: Checked
   - Extra variables:

   ```plaintext
   namespaces:
     - <your-namespace>
   ```

6. Select **Create source**.
7. In the new screen with the inventory details, select **Launch inventory update** in the top right corner.
8. The Last job status will switch to Running and should display Success when it finishes.

Good job. You've provisioned a Developer Sandbox instance and configured your execution environment. In the next lesson, you'll apply what you've learned to create templates and manage your use cases.

---

## Lesson 3: Configure job templates and use cases

May 12, 2025

[Leonardo Gallego](https://developers.redhat.com/author/leonardo-gallego)

**Related topics:** [Automation](https://developers.redhat.com/topics/automation/all)

**Related products:** [Red Hat Ansible Automation Platform](https://developers.redhat.com/products/ansible/overview)

![Ansible-sandbox-LP-feature-image](https://developers.redhat.com/sites/default/files/Ansible-sandbox-LP-feature-image.png)

Now that you've transitioned your Developer Sandbox instance into Ansible Automation Platform and customized your execution environment, this lesson will show you how to manage your credentials and templates.

### In order to get full benefit from taking this lesson, you need:

- A Red Hat Developer account.

### In this lesson, you will:

- Import playbooks.
- Build job templates.
- Configure use cases

---

### Import ready-to-use playbooks

The first step to managing your sandbox is creating a project:

1. In the Ansible Automation Platform sidebar, go to **Automation Execution > Projects** then click **Create project**.
2. Fill out the following details:
   - Name: aap-sandbox-project
   - Organization: Default
   - Execution environment: ee-sandbox
   - Source control type: Git
   - Source control URL: https://github.com/ansible-tmm/aap-sandbox-project.git
3. Select **Create project**.

### Create a machine credential

Now it's time to access the VM:

1. In the Ansible Automation Platform sidebar, go to **Automation Execution > Infrastructure** then select the **Credentials** option.
2. In the new screen, select **Create credential**.
3. Fill out the form with the following:
   - Name: credential-ssh
   - Credential Type: Machine
   - Username: cloud-user
   - Private key:

   ```plaintext
   <lab-ssh-private-key>
   ```

### Create a RHEL 9 VM in OpenShift Virtualization

Now we can create the VM:

1. In the Ansible Automation Platform sidebar, go to **Automation Execution → Templates**.
2. Click **Create template** then choose the **Create job** template.
3. Fill out the following:
   - Name: Create VM
   - Job type: Run
   - Inventory: inventory-sandbox
   - Project: aap-sandbox-project
   - Playbook: ocp_vm_create.yml
   - Execution environment: ee-sandbox
   - Credentials: credential-ocp
4. Select **Create job template**.

### Delete a RHEL 9 VM in OpenShift Virtualization

Here's how to delete a RHEL VM:

1. In the Ansible Automation Platform sidebar, go to **Automation Execution → Templates**.
2. Click **Create template** then choose the **Create job** template.
3. Fill out the following:
   - Name: Delete VM
   - Job type: Run
   - Inventory: inventory-sandbox
   - Project: aap-sandbox-project
   - Playbook: ocp_vm_create.yml
   - Execution environment: ee-sandbox
   - Credentials: credential-ocp
4. Select **Create job template**.

### Start the RHEL VM in OpenShift Virtualization

Now let’s add a job template to start the VM we created:

1. In the Ansible Automation Platform sidebar, go to **Automation Execution → Templates**.
2. Click the **Create template** button, and choose **Create job template**.
3. Fill out the following:
   - Name: Start VM
   - Job type: Run
   - Inventory: inventory-sandbox
   - Project: aap-sandbox-project
   - Playbook: ocp_vm_create.yml
   - Execution environment: ee-sandbox
   - Credentials: credential-ocp
4. Select **Create job template**.

### Stop the RHEL VM in OpenShift Virtualization

Here's how to stop the VM we created:

1. In the Ansible Automation Platform sidebar, go to **Automation Execution → Templates**.
2. Click the **Create template** button, and choose **Create job template**.
3. Fill out the following:
   - Name: Stop VM
   - Job type: Run
   - Inventory: inventory-sandbox
   - Project: aap-sandbox-project
   - Playbook: ocp_vm_create.yml
   - Execution environment: ee-sandbox
   - Credentials: credential-ocp
4. Select **Create job template**.

### Register the RHEL VM to Red Hat

Time to add a job template to register the RHEL VM to Red Hat:

1. In the Ansible Automation Platform sidebar, go to **Automation Execution → Templates**.
2. Click the **Create template** button, and choose **Create job template**.
3. Fill out the following:
   - Name: RHEL Register
   - Job type: Run
   - Inventory: inventory-sandbox
   - Project: aap-sandbox-project
   - Playbook: rhel_register.yml
   - Execution environment: ee-sandbox
   - Credentials: credential-ssh
   - Privilege escalation: Checked
4. Select **Create job template.**

### Configure time sync in the RHEL VM

Configure your template:

1. In the Ansible Automation Platform sidebar, go to **Automation Execution → Templates**.
2. Click the **Create template** button, and choose **Create job template**.
3. Fill out the following:
   - Name: RHEL Timesync
   - Job type: Run
   - Inventory: inventory-sandbox
   - Project: aap-sandbox-project
   - Playbook: rhel_timesync.yml
   - Execution environment: ee-sandbox
   - Credentials: credential-ssh
   - Privilege escalation: Checked
4. Select **Create job template**.

### Summary

In this learning path, you started your Ansible Automation Platform journey by provisioning a Developer Sandbox instance and creating custom execution environments. Along the way, you've learned how to create credentials, inventories, projects, and templates that helped you create your Ansible Automation Platform sandbox.

Ready to learn more about how Ansible automates? Try these learning paths:

- [Foundations of Ansible](https://developers.redhat.com/learn/ansible/foundations-ansible)
- [Get started with Ansible Playbooks](https://developers.redhat.com/learn/ansible/get-started-ansible-playbooks)
- [Streamline automation in OpenShift Dev Spaces with Ansible](https://developers.redhat.com/learn/openshift/streamline-automation-openshift-dev-spaces-ansible)
