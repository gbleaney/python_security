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
    import asyncssh

    async with asyncssh.connect('ssh.example.com' username="username", password="password") as conn:
        result = await conn.run(command)

    # ssh2-python
    # Source: https://pypi.org/project/ssh2-python/
    from ssh2.session import Session
    import socket

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('ssh.example.com', 22))

    session = Session()
    session.handshake(sock)

    session.userauth_password("username", "password")

    channel = session.open_session()
    channel.execute(command)
    channel.wait_eof()
    channel.close()
    channel.wait_closed()

    # twisted.conch
    # Source: https://twistedmatrix.com/documents/current/conch/examples/index.html
    # https://stackoverflow.com/questions/22196373/sshcommandclientendpoint-twisted-how-to-execute-more-than-one-commands
    # https://twistedmatrix.com/documents/current/conch/howto/conch_client.html
    from twisted.conch.endpoints import SSHCommandClientEndpoint
    from twisted.internet.protocol import Factory
    from twisted.internet import reactor

    endpoint = SSHCommandClientEndpoint.newConnection(
        reactor,
        command,
        "username",
        "ssh.example.com",
        22,
        password="password"
    )
    factory = Factory()
    d = endpoint.connect(factory)
    d.addCallback(lambda protocol: protocol.finished)

    # trigger
    # Source: https://trigger.readthedocs.io/en/latest/examples.html#execute-commands-asynchronously-using-twisted
    from trigger.netdevices import NetDevices
    nd = NetDevices()
    dev = nd.find('ssh.example.com')
    dev.execute([command])

    # parallel-ssh
    # Source: https://github.com/ParallelSSH/parallel-ssh
    from pssh.clients import SSHClient

    client = SSHClient('ssh.example.com')
    host_out = client.run_command(command)

    # scrapli (can use paramiko, ssh2, asyncssh as transport)
    # Source: https://github.com/carlmontanari/scrapli
    from scrapli import Scrapli

    conn = Scrapli(host='ssh.example.com' auth_username="username", auth_password="password")
    conn.open()
    conn.send_command(command)

    # redexpect (based on ssh2-python)
    # Source: https://github.com/Red-M/RedExpect/blob/master/examples/run_whoami.py
    import redexpect
    expect = redexpect.RedExpect()
    expect.login(hostname="ssh.example.com", username="username", password="password", allow_agent=True, timeout=1.5)
    expect.command(command)

    # netmiko (based on paramiko)
    # Source: https://pypi.org/project/netmiko/
    from netmiko import ConnectHandler
    net_connect = ConnectHandler(host="ssh.example.com", username="username", password="password")
    output = net_connect.send_command(command)
