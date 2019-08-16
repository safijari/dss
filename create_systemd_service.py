from bash import bash
import os

base_str="""[Unit]
Description={description}

[Service]
Type={service_type}
User={service_user}
ExecStart={start_command}
# Restart=on-failure
{restart_block}
# Other restart options: always, on-abort, etc

[Install]
WantedBy={target}.target"""


def make_systemd_service(name, description, service_user, start_command, service_type='simple', restart_on_fail=True, wanted_by='multi-user'):
    if restart_on_fail:
        restart_block = "Restart=on-failure"

    service_str = base_str.format(**locals())

    path = f"/etc/systemd/system/{name}.service"

    assert not os.path.exists(path), f"Service at {path} already exists, won't overwrite."

    with open(path, 'w') as ff:
        ff.write(service_str)

    print("enabling service")
    enable_cmd = bash(f'sudo systemctl enable {name}')

    print(enable_cmd.stdout)
    print(enable_cmd.stderr)

    print("starting service")

    enable_cmd = bash(f'sudo systemctl start {name}')

    print(enable_cmd.stdout)
    print(enable_cmd.stderr)

    print("statusing service")

    enable_cmd = bash(f'sudo systemctl status {name}')

    print(enable_cmd.stdout)
    print(enable_cmd.stderr)
