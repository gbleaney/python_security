from .execution_base import Exploit


class SSHExploit(Exploit):
    category_name = "SSH Command Execution"
    def generate_payload(shell_command: str) -> str:
        return shell_command

class ParamikoExploit(ShellExploit):
    vulnerable_function = "paramiko.client.SSHClient.exec_command"
    notes = "This category hasn't been fully explored"
    source = "http://docs.paramiko.org/en/stable/api/client.html#paramiko.client.SSHClient"

class AsyncSSHExploit(ShellExploit):
    vulnerable_function = "asyncssh.connection.SSHClientConnection.run"
    notes = "This category hasn't been fully explored"
    source = "https://asyncssh.readthedocs.io/en/latest/"

class TwistedExploit(ShellExploit):
    vulnerable_function = "twisted.conch.endpoints.SSHCommandClientEndpoint.newConnection"
    notes = "This category hasn't been fully explored"
    source = "https://twistedmatrix.com/documents/current/conch/examples/index.html"

class TriggerExploit(ShellExploit):
    vulnerable_function = "trigger.netdevices.NetDevice.run_commands"
    notes = "This category hasn't been fully explored"
    source = "https://trigger.readthedocs.io/en/latest/examples.html#execute-commands-asynchronously-using-twisted"

class ParalelSSHExploit(ShellExploit):
    vulnerable_function = "pssh.clients.SSHClient.run_command"
    notes = "This category hasn't been fully explored"
    source = "https://github.com/ParallelSSH/parallel-ssh"

class NetmikoExploit(ShellExploit):
    vulnerable_function = "netmiko.ConnectHandler.send_command"
    notes = "This category hasn't been fully explored"
    source = "https://pypi.org/project/netmiko/"

class RedexpectExploit(ShellExploit):
    vulnerable_function = "redexpect.RedExpect.command"
    notes = "This category hasn't been fully explored"
    source = "https://github.com/Red-M/RedExpect/blob/master/examples/run_whoami.py"

class ScrapliExploit(ShellExploit):
    vulnerable_function = "scrapli.Scrapli.send_command"
    notes = "This category hasn't been fully explored"
    source = "https://github.com/carlmontanari/scrapli"

class SpurExploit(ShellExploit):
    vulnerable_function = "spur.SshShell.run"
    notes = "This category hasn't been fully explored"
    source = "https://pypi.org/project/spur/"

class FabricExploit(ShellExploit):
    vulnerable_function = "fabric.api.run"
    notes = "This category hasn't been fully explored"
    source = "https://docs.fabfile.org/en/1.12.1/tutorial.html"

class PexpectExploit(ShellExploit):
    vulnerable_function = "pexpect.pxssh.pxssh.sendline"
    notes = "This category hasn't been fully explored"
    source = "https://pexpect.readthedocs.io/en/stable/api/pxssh.html"

class SSH2Exploit(ShellExploit):
    vulnerable_function = "ssh2"
    notes = "Not implemented in pure Python. This category hasn't been fully explored"
    source = "https://pypi.org/project/ssh2-python/"
