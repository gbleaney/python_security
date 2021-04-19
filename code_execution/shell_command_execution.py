import os
import shlex
import subprocess
import asyncio
from .execution_base import Exploit
from typing import List


class ShellExploit(Exploit):
    category_name = "Shell Command Execution"
    def generate_payload(shell_command: str) -> str:
        return shell_command


class SubprocessCallExploit(ShellExploit):
    vulnerable_function = subprocess.call

    def run_payload(shell_command: str) -> None:
        args = shlex.split(shell_command)
        subprocess.call(args)


class SubprocessRunExploit(ShellExploit):
    vulnerable_function = subprocess.run

    def run_payload(shell_command: str) -> None:
        args = shlex.split(shell_command)
        subprocess.run(args)


class SubprocessCheckCallExploit(ShellExploit):
    vulnerable_function = subprocess.check_call

    def run_payload(shell_command: str) -> None:
        args = shlex.split(shell_command)
        subprocess.check_call(args)


class SubprocessCheckOutputExploit(ShellExploit):
    vulnerable_function = subprocess.check_output

    def run_payload(shell_command: str) -> None:
        args = shlex.split(shell_command)
        subprocess.check_output(args)



class SubprocessPopenExploit(ShellExploit):
    vulnerable_function = subprocess.Popen

    def run_payload(shell_command: str) -> None:
        args = shlex.split(shell_command)
        subprocess.Popen(args)


class WaitingProtocol(asyncio.SubprocessProtocol):
    def __init__(self, exit_future):
        self.exit_future = exit_future

    def process_exited(self):
        self.exit_future.set_result(True)


class AsyncioSubprocessExecExploit(ShellExploit):
    vulnerable_function = asyncio.events.AbstractEventLoop.subprocess_exec

    async def run_payload(shell_command: str) -> None:
        args = shlex.split(shell_command)
        loop = asyncio.get_event_loop()
        exit_future = asyncio.Future(loop=loop)
        transport, _ = await loop.subprocess_exec(lambda: WaitingProtocol(exit_future), *args)
        await exit_future
        transport.close()


class SubprocessGetStatusOutputExploit(ShellExploit):
    vulnerable_function = subprocess.getstatusoutput

    def run_payload(shell_command: str) -> None:
        subprocess.getstatusoutput(shell_command)


class SubprocessGetOutputExploit(ShellExploit):
    vulnerable_function = subprocess.getoutput

    def run_payload(shell_command: str) -> None:
        subprocess.getoutput(shell_command)


class AsyncioCreateSubprocessShellExploit(ShellExploit):
    vulnerable_function = asyncio.subprocess.create_subprocess_shell

    async def run_payload(shell_command: str) -> None:
        proc = await asyncio.subprocess.create_subprocess_shell(shell_command)
        await proc.communicate()


class OSPopenExploit(ShellExploit):
    vulnerable_function = os.popen

    def run_payload(shell_command: str) -> None:
        proc = os.popen(shell_command)
        proc.close()


class OSSystemExploit(ShellExploit):
    vulnerable_function = os.system

    def run_payload(shell_command: str) -> None:
        os.system(shell_command)


class AsyncioSubprocessShellExploit(ShellExploit):
    vulnerable_function = asyncio.events.AbstractEventLoop.subprocess_shell

    async def run_payload(shell_command: str) -> None:
        loop = asyncio.get_event_loop()
        exit_future = asyncio.Future(loop=loop)
        transport, _ = await loop.subprocess_shell(lambda: WaitingProtocol(exit_future), shell_command)
        await exit_future
        transport.close()


class OSExeclpExploit(ShellExploit):
    vulnerable_function = os.execlp

    def run_payload(shell_command: str) -> None:
        pid = os.fork()
        if pid == 0:
            # We're the child
            args = shlex.split(shell_command)
            program = args[0]
            os.execlp(program, *args)
        else:
            # We're the parent
            os.waitpid(pid, 0)


class OSExeclpeExploit(ShellExploit):
    vulnerable_function = os.execlpe

    def run_payload(shell_command: str) -> None:
        pid = os.fork()
        if pid == 0:
            # We're the child
            args = shlex.split(shell_command)
            program = args[0]
            os.execlpe(program, *args, os.environ)
        else:
            # We're the parent
            os.waitpid(pid, 0)


class OSExecvpExploit(ShellExploit):
    vulnerable_function = os.execvp

    def run_payload(shell_command: str) -> None:
        pid = os.fork()
        if pid == 0:
            # We're the child
            args = shlex.split(shell_command)
            program = args[0]
            os.execvp(program, args)
        else:
            # We're the parent
            os.waitpid(pid, 0)


class OSExecvpeExploit(ShellExploit):
    vulnerable_function = os.execvpe

    def run_payload(shell_command: str) -> None:
        pid = os.fork()
        if pid == 0:
            # We're the child
            args = shlex.split(shell_command)
            program = args[0]
            os.execvpe(program, args, os.environ)
        else:
            # We're the parent
            os.waitpid(pid, 0)


class OSSpawnlpExploit(ShellExploit):
    vulnerable_function = os.spawnlp

    def run_payload(shell_command: str) -> None:
        args = shlex.split(shell_command)
        program = args[0]
        os.spawnlp(os.P_WAIT, program, *args)


class OSSpawnlpeExploit(ShellExploit):
    vulnerable_function = os.spawnlpe

    def run_payload(shell_command: str) -> None:
        args = shlex.split(shell_command)
        program = args[0]
        os.spawnlpe(os.P_WAIT, program, *args, os.environ)


class OSSpawnvpExploit(ShellExploit):
    vulnerable_function = os.spawnvp

    def run_payload(shell_command: str) -> None:
        args = shlex.split(shell_command)
        program = args[0]
        os.spawnvp(os.P_WAIT, program, args)


class OSSpawnvpeExploit(ShellExploit):
    vulnerable_function = os.spawnvpe

    def run_payload(shell_command: str) -> None:
        args = shlex.split(shell_command)
        program = args[0]
        os.spawnvpe(os.P_WAIT, program, args, os.environ)


class AsyncioCreateSubprocessExecExploit(ShellExploit):
    vulnerable_function = asyncio.subprocess.create_subprocess_exec

    async def run_payload(shell_command: str) -> None:
        args = shlex.split(shell_command)
        program = args[0]
        await asyncio.subprocess.create_subprocess_exec(program, *args)



class ShellPathExploit(ShellExploit):
    def generate_payload(shell_command: str) -> str:
        return shlex.join(["/bin/bash", "-c", shell_command])


class OSPosixSpawnpExploit(ShellPathExploit):
    vulnerable_function = os.posix_spawnp

    def run_payload(shell_command: str) -> None:
        args = shlex.split(shell_command)
        path = args[0]
        pid = os.posix_spawnp(path, args, os.environ)
        os.waitpid(pid, 0)


class OSPosixSpawnExploit(ShellPathExploit):
    vulnerable_function = os.posix_spawn

    def run_payload(shell_command: str) -> None:
        args = shlex.split(shell_command)
        path = args[0]
        pid = os.posix_spawn(path, args, os.environ)
        os.waitpid(pid, 0)



class OSExeclExploit(ShellPathExploit):
    vulnerable_function = os.execl

    def run_payload(shell_command: str) -> None:
        args = shlex.split(shell_command)
        path = args[0]

        pid = os.fork()
        if pid == 0:
            # We're the child
            os.execl(path, *args)
        else:
            # We're the parent
            os.waitpid(pid, 0)


class OSExecleExploit(ShellPathExploit):
    vulnerable_function = os.execle

    def run_payload(shell_command: str) -> None:
        args = shlex.split(shell_command)
        path = args[0]

        pid = os.fork()
        if pid == 0:
            # We're the child
            os.execle(path, *args, os.environ)
        else:
            # We're the parent
            os.waitpid(pid, 0)


class OSExecvExploit(ShellPathExploit):
    vulnerable_function = os.execv

    def run_payload(shell_command: str) -> None:
        args = shlex.split(shell_command)
        path = args[0]

        pid = os.fork()
        if pid == 0:
            # We're the child
            os.execv(path, args)
        else:
            # We're the parent
            os.waitpid(pid, 0)


class OSExecveExploit(ShellPathExploit):
    vulnerable_function = os.execve

    def run_payload(shell_command: str) -> None:
        args = shlex.split(shell_command)
        path = args[0]

        pid = os.fork()
        if pid == 0:
            # We're the child
            os.execve(path, args, os.environ)
        else:
            # We're the parent
            os.waitpid(pid, 0)


class OSSpawnlExploit(ShellPathExploit):
    vulnerable_function = os.spawnl

    def run_payload(shell_command: str) -> None:
        args = shlex.split(shell_command)
        path = args[0]

        os.spawnl(os.P_WAIT, path, *args)


class OSSpawnleExploit(ShellPathExploit):
    vulnerable_function = os.spawnle

    def run_payload(shell_command: str) -> None:
        args = shlex.split(shell_command)
        path = args[0]

        os.spawnle(os.P_WAIT, path, *args, os.environ)


class OSSpawnvExploit(ShellPathExploit):
    vulnerable_function = os.spawnv

    def run_payload(shell_command: str) -> None:
        args = shlex.split(shell_command)
        path = args[0]

        os.spawnv(os.P_WAIT, path, args)


class OSSpawnveExploit(ShellPathExploit):
    vulnerable_function = os.spawnve

    def run_payload(shell_command: str) -> None:
        args = shlex.split(shell_command)
        path = args[0]

        os.spawnve(os.P_WAIT, path, args, os.environ)
