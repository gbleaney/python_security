def run_ssh(args: List[str])
    command = " ".join(args)

    # paramiko
    # Source: http://docs.paramiko.org/en/stable/api/client.html#paramiko.client.SSHClient
    from paramiko.client import SSHClient
    client = SSHClient()
    client.load_system_host_keys()
    client.connect('ssh.example.com')
    stdin, stdout, stderr = client.exec_command(command)

    # pexpect
    # Source: https://pexpect.readthedocs.io/en/stable/api/pxssh.html
    from pexpect import pxssh
    s = pxssh.pxssh()
    s.login("ssh.example.com", "username", "password")
    s.sendline(command)

    # fabric
    # Source: https://docs.fabfile.org/en/1.12.1/tutorial.html
    from fabric.api import run
    run(command)

    # spur
    # Source: https://pypi.org/project/spur/
    import spur
    shell = spur.SshShell(hostname="ssh.example.com", username="username", password="password")
    with shell:
        result = shell.run(args)

    # asyncssh
    # Source: https://asyncssh.readthedocs.io/en/latest/

    # scrapli
    # Source: https://github.com/carlmontanari/scrapli

    # ssh2-python
    # Source: https://pypi.org/project/ssh2-python/

    # twisted.conch
    # Source: https://twistedmatrix.com/documents/current/conch/examples/index.html

    # trigger
    # Source: https://trigger.readthedocs.io/en/latest/examples.html#execute-commands-asynchronously-using-twisted

    # parallel-ssh
    # Source: https://github.com/ParallelSSH/parallel-ssh

    # redexpect (based on ssh2-python)
    # Source: https://github.com/Red-M/RedExpect/blob/master/examples/run_whoami.py
    expect = redexpect.RedExpect()
    expect.login(hostname="ssh.example.com", username="username", password="password", allow_agent=True, timeout=1.5)
    expect.command(command)

    # netmiko (based on paramiko)
    # Source: https://pypi.org/project/netmiko/
