"""Check project syntax and render templates without accessing OpenShift.

Run inside the selected execution environment: python3 tests/check.py
Requires ansible-core and its PyYAML dependency; installs nothing.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
ROLE = ROOT / "roles" / "sandbox_vm"


def run_playbook(
    path: Path, *, syntax_only: bool, inventory: Path | None = None
) -> dict:
    command = ["ansible-playbook", "-i", str(inventory) if inventory else "localhost,"]
    if syntax_only:
        command.append("--syntax-check")
    command.append(str(path))
    result = subprocess.run(
        command,
        cwd=ROOT,
        env={**os.environ, "ANSIBLE_CONFIG": str(ROOT / "ansible.cfg")},
        capture_output=True,
        text=True,
        timeout=120,
        check=False,
    )
    report = {"playbook": path.name, "returncode": result.returncode}
    if result.returncode:
        report.update(stdout=result.stdout, stderr=result.stderr)
    return report


def main() -> int:
    sources = [
        *ROOT.glob("playbooks/*.yml"),
        *ROOT.glob("roles/**/*.yml"),
        *ROOT.glob("tests/playbooks/*.yml"),
        *ROOT.glob("dependencies/*.yml"),
    ]
    for path in sources:
        yaml.safe_load(path.read_text())

    report = {
        "yaml_files": len(sources),
        "ssh_keygen_available": bool(shutil.which("ssh-keygen")),
        "syntax": [],
    }
    with tempfile.TemporaryDirectory(prefix="aap-sandbox-check-") as directory:
        temporary = Path(directory)
        # Import every role task file statically, including the action files
        # normally loaded dynamically. --syntax-check executes none of them.
        role_check = temporary / "role-syntax.yml"
        role_check.write_text(
            yaml.safe_dump(
                [
                    {
                        "name": "Parse every sandbox role action without running it",
                        "hosts": "localhost",
                        "gather_facts": False,
                        "tasks": [
                            {
                                "name": f"Parse {path.stem}",
                                "ansible.builtin.import_role": {
                                    "name": "sandbox_vm",
                                    "tasks_from": path.stem,
                                },
                            }
                            for path in sorted((ROLE / "tasks").glob("*.yml"))
                        ],
                    }
                ]
            )
        )
        playbooks = [
            *sorted(ROOT.glob("playbooks/*.yml")),
            *sorted(ROOT.glob("tests/playbooks/*.yml")),
            role_check,
        ]
        for path in playbooks:
            report["syntax"].append(run_playbook(path, syntax_only=True))

        render_check = temporary / "render-templates.yml"
        render_check.write_text(
            yaml.safe_dump(
                [
                    {
                        "name": "Render candidate manifests locally without applying them",
                        "hosts": "localhost",
                        "connection": "local",
                        "gather_facts": False,
                        "vars_files": [
                            str(ROLE / "defaults" / "main.yml"),
                            str(ROLE / "vars" / "main.yml"),
                        ],
                        "vars": {
                            "vm_name": "aap-lab-validation",
                            "ocp_namespace": "render-check-only",
                            # A placeholder, not a usable SSH key. No VM is created.
                            "__sandbox_vm_public_key": "ssh-ed25519 PUBLIC_KEY_PLACEHOLDER",
                            "__sandbox_vm_cloud_init": (
                                "{{ lookup('ansible.builtin.template', '"
                                + str(ROLE / "templates" / "cloud-init.yml.j2")
                                + "') }}"
                            ),
                            "rendered_vm": (
                                "{{ lookup('ansible.builtin.template', '"
                                + str(ROLE / "templates" / "virtual-machine.yml.j2")
                                + "') | from_yaml }}"
                            ),
                            "rendered_cloud_init": "{{ __sandbox_vm_cloud_init | from_yaml }}",
                        },
                        "tasks": [
                            {
                                "name": "Check template structure and secret separation",
                                "ansible.builtin.assert": {
                                    "that": [
                                        "rendered_vm.spec.runStrategy == 'Manual'",
                                        "'running' not in rendered_vm.spec",
                                        "rendered_vm.spec.domain is not defined",
                                        "rendered_vm.spec.template.spec.domain.cpu.cores == 1",
                                        "rendered_vm.spec.dataVolumeTemplates[0].spec.storage.resources.requests.storage == '30Gi'",
                                        "rendered_vm.metadata.namespace == 'render-check-only'",
                                        "rendered_vm.metadata.labels['app.kubernetes.io/part-of'] == 'aap-sandbox-project'",
                                        "rendered_vm.spec.template.metadata.labels['app.kubernetes.io/part-of'] == 'aap-sandbox-project'",
                                        "rendered_vm.spec.template.spec.volumes[1].cloudInitNoCloud.userData.startswith('#cloud-config\\n')",
                                        "'userDataSecretRef' not in rendered_vm.spec.template.spec.volumes[1].cloudInitNoCloud",
                                        "rendered_vm.spec.template.spec.accessCredentials[0].sshPublicKey.source.secret.secretName == 'aap-lab-validation-cloudinit'",
                                        "rendered_vm.spec.template.spec.accessCredentials[0].sshPublicKey.propagationMethod == {'noCloud': {}}",
                                        "'PUBLIC_KEY_PLACEHOLDER' not in (rendered_vm | to_json)",
                                        "rendered_cloud_init.user == 'cloud-user'",
                                        "'ssh_authorized_keys' not in rendered_cloud_init",
                                        "__sandbox_vm_cloud_init | length < 512",
                                        "not rendered_cloud_init.ssh_pwauth",
                                        "'chpasswd' not in rendered_cloud_init",
                                    ]
                                },
                            }
                        ],
                    }
                ],
                width=160,
            )
        )
        report["templates"] = run_playbook(render_check, syntax_only=False)

        inventory = temporary / "inventory.yml"
        inventory.write_text(
            yaml.safe_dump(
                {
                    "all": {
                        "vars": {
                            "vm_name": "aap-lab-validation",
                            "ocp_namespace": "render-check-only",
                        },
                        "hosts": {
                            "render-check-only-aap-lab-validation": {},
                        },
                    }
                }
            )
        )
        inventory_check = temporary / "check-inventory.yml"
        inventory_check.write_text(
            yaml.safe_dump(
                [
                    {
                        "name": "Check the existing inventory-variable interface locally",
                        "hosts": "localhost",
                        "connection": "local",
                        "gather_facts": False,
                        "roles": [
                            {
                                "role": "sandbox_vm",
                                "sandbox_vm_action": "check_inventory",
                            }
                        ],
                    }
                ]
            )
        )
        report["inventory"] = run_playbook(
            inventory_check, syntax_only=False, inventory=inventory
        )

    print(json.dumps(report, indent=2))
    return int(
        not report["ssh_keygen_available"]
        or any(item["returncode"] for item in report["syntax"])
        or report["templates"]["returncode"] != 0
        or report["inventory"]["returncode"] != 0
    )


if __name__ == "__main__":
    sys.exit(main())
