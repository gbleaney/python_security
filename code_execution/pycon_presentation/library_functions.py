import os
import subprocess
import asyncio

def entry_point(command: str):
    os.system(command)
    subprocess.call(command.split(" "))
    asyncio.subprocess.create_subprocess_shell(command)


from typing import List, Mapping

def get_protocol_factory() -> asyncio.SubprocessProtocol:
    pass

def find_in_path(program: str) -> str:
    pass

def get_environment() -> Mapping[str, str]:
    pass

def shell_entry_point(args: List[str]):
    program = args[0]
    path = find_in_path(program)
    remaining_args = args[1:]
    command = " ".join(args)
    environment = get_environment()

    subprocess.run(args)
    subprocess.check_call(args)
    subprocess.check_output(args)

    subprocess.Popen(args)

    subprocess.getstatusoutput(command)
    subprocess.getoutput(command)

    asyncio.subprocess.create_subprocess_exec(program, remaining_args)
    asyncio.subprocess.create_subprocess_shell(command)

    # TODO
    loop = asyncio.get_event_loop()
    loop.subprocess_exec(get_protocol_factory(), args)
    loop.subprocess_shell(get_protocol_factory(), command)

    os.execl(path, *remaining_args)
    os.execle(path, *remaining_args, environment)
    os.execlp(program, *remaining_args)
    os.execlpe(program, *remaining_args, environment)
    os.execv(path, remaining_args)
    os.execve(path, remaining_args, environment)
    os.execvp(program, remaining_args)
    os.execvpe(program, remaining_args, environment)

    os.popen(command)

    # TODO
    os.posix_spawnp(path, remaining_args, environment)
    os.posix_spawn(path, remaining_args, environment)

    os.spawnl(os.P_WAIT, path, *remaining_args)
    os.spawnle(os.P_WAIT, path, *remaining_args, environment)
    os.spawnlp(os.P_WAIT, program, *remaining_args)
    os.spawnlpe(os.P_WAIT, program, *remaining_args, environment)
    os.spawnv(os.P_WAIT, path, remaining_args)
    os.spawnve(os.P_WAIT, path, remaining_args, environment)
    os.spawnvp(os.P_WAIT, program, remaining_args)
    # TODO
    os.spawnvpe(os.P_WAIT, program, remaining_args, environment)

    os.system(command)

import code
import test
import _testcapi
import _xxsubinterpreters


def python_entry_point(source_code: str):
    inperpreter = code.InteractiveInterpreter()
    inperpreter.runsource(source_code)
    inperpreter.runcode(code.compile_command(source_code))

    console = code.InteractiveConsole()
    console.push(source_code)

    test.support.run_in_subinterp(source_code)
    _testcapi.run_in_subinterp(source_code)
    _xxsubinterpreters.run_string(source_code)
