import os
import sys
import json
import re


class NotFound(Exception):
    pass


try:
    import rich
    from rich.pretty import pprint
    from rich.table import Table
    from rich.console import Console
except ModuleNotFoundError:
    rich = None

from argparse import ArgumentParser
from netrc import netrc

from .helpers import CommandLineHandler
from . import AUTHENTICATION_URL, EtnaSession, EtnaAPIError
from urllib.parse import urlparse


def looks_like_a_student_login(s):
    pos = s.find("_")
    length = len(s)
    return length <= 8 and pos > -1 and pos == length - 2


def get_student_id(client, login_or_id):
    if not login_or_id:
        return None
    try:
        # try to parse a student_id
        return int(login_or_id)
    except ValueError:
        # else, should be a login
        students = client.find_student(login_or_id)
        if len(students) < 1:
            raise NotFound("no such student login")
        return students[0]["id"]


def date(arg_value: str):
    if re.match(r"^\d\d\d\d-\d\d-\d\d$", arg_value) is None:
        raise argparse.ArgumentTypeError("invalid value")
    return arg_value


class StudentsCli(CommandLineHandler):
    "search, display students"

    aliases_for_list = ["ls"]

    def options_for_list(self, p: ArgumentParser):
        p.add_argument("es_query", nargs="*", help="optional filters (ES simple query)")

    def command_list(self, opts, client):
        if not opts.es_query:
            q = "*"
        else:
            q = " ".join(f"+{part}" for part in opts.es_query)
        size = 100
        offset = 0
        students = client.find_students(q, size=size)
        while len(students) == offset + size:
            offset = len(students)
            students += client.find_students(q, size=size, _from=offset)
        print(json.dumps(students, indent=2))
        return 0

    def options_for_show(self, p: ArgumentParser):
        p.add_argument("student_id_or_login", nargs=1, help="student id or login")

    def _get_one_student_by_login(self, client, login):
        students = client.find_student(student_login=login)
        if len(students) == 1:
            return students[0]
        return None

    def command_show(self, opts, client):
        query = opts.student_id_or_login[0]
        if looks_like_a_student_login(query):
            student = self._get_one_student_by_login(client, query)
        else:
            try:
                student_id = int(query)
                student = client.get_student(student_id)
            except ValueError:
                print("invalid login or id:", query)
                return 1
            except EtnaAPIError as E:
                if "404" in str(E):
                    student = None
                else:
                    raise
        pprint(student)


class TermsCli(CommandLineHandler):
    "list/search terms"

    aliases_for_list = ["ls"]

    def options_for_list(self, p: ArgumentParser):
        p.add_argument(
            "words", nargs="*", help="words to be matched in term's full-name"
        )

    def command_list(self, opts, client):
        if not opts.words:
            q = "*"
        else:
            q = " ".join(f"+{part}" for part in opts.words)
            q = "full_term_name:(" + q + ")"
        terms = client.find_terms(q=q)
        if opts.output_format == "json":
            print(json.dumps(terms, indent=4))
            return 0
        table = Table()
        table.add_column("id")
        table.add_column("name")
        for term in sorted(terms, key=lambda t: t["id"]):
            table.add_row(str(term["id"]), term["full_term_name"])
        Console().print(table)
        return 0


class LogsCli(CommandLineHandler):
    "search logs-api"

    aliases_for_list = ["ls"]

    def options_for_list(self, p: ArgumentParser):
        p.add_argument("--student", type=str, help="filter by login or student_id")
        p.add_argument(
            "-t",
            "--type",
            action="append",
            help="select log event types (can be used multiple times).",
        )
        p.add_argument("--after", type=date, help="filter logs on and after YYYY-MM-DD")
        p.add_argument("--before", type=date, help="filter logs before YYYY-MM-DD")
        p.add_argument(
            "es_query", nargs="*", help="extra search arguments (ES simple query)."
        )

    def command_list(self, opts, client):
        "query logs-api to search for logs"
        student_id = get_student_id(client, opts.student)
        if opts.es_query:
            q = " ".join(opts.es_query)
        else:
            q = None
        logs = client.find_logs(
            q=q,
            student_id=student_id,
            after=opts.after,
            before=opts.before,
            types=opts.type,
        )
        if opts.output_format == "json":
            print(json.dumps(logs, indent=4))
            return 0
        table = Table()
        for col in "id", "type", "start", "end", "meta":
            table.add_column(col)

        def split_date(d):
            return "\n".join(d[0:19].split("T"))

        for log in sorted(logs["hits"], key=lambda t: t["id"]):
            table.add_row(
                str(log["id"]),
                log["type"],
                split_date(log["start"]),
                split_date(log["end"]),
                json.dumps(log["metas"]),
            )
        Console().print(table)
        print(f"{len(logs['hits'])} of {logs['total']} results.")
        return 0


class EtnaCli(CommandLineHandler):
    "Interract with ETNA API."

    aliases_for_terms = ["term"]
    command_terms = TermsCli()

    command_students = StudentsCli()
    command_logs = LogsCli()

    def error(self, *messages):
        for m in messages:
            sys.stderr.write(m)
        sys.stderr.write("\n")

    def env_credentials(self, opts):
        creds = {}
        if "ETNA_USER" in os.environ:
            creds["username"] = os.environ["ETNA_USER"]
        if "ETNA_PASSWORD" in os.environ:
            creds["password"] = os.environ["ETNA_PASSWORD"]
        return creds

    def netrc_credentials(self, opts):
        url = urlparse(AUTHENTICATION_URL)
        creds = netrc().authenticators(url.netloc)
        if creds:
            return dict(username=creds[0], password=creds[2])
        else:
            return {}

    def credentials(self, opts):
        creds = self.netrc_credentials(opts)
        creds.update(self.env_credentials(opts))
        if creds.get("username") and creds.get("password"):
            return creds
        self.error("please provide your credentials. See --help for more info")
        return None

    def config(self, opts):
        config = {}
        creds = self.credentials(opts)
        if not creds:
            return None
        config.update(creds)
        return config

    def command_identity(self, opts, client):
        "display identity infos from auth"
        identity = client.identity()
        if opts.output_format == "json":
            print(json.dumps(client.identity(), indent=4))
        else:
            pprint(identity)

    def command_shell(self, opts, client):
        try:
            from IPython import embed
            api = client
            embed()
        except ImportError:
            print("\nPlease run 'pip install --user ipython' for a better experience...\n")
            import code
            variables = { 'api': client }
            shell = code.InteractiveConsole(variables)
            shell.interact()

    def options_for_graphql(self, p: ArgumentParser):
        p.add_argument("query", nargs=1, help="graphql query")

    def command_graphql(self, opts, client):
        r = client.graphql(opts.query[0])
        if opts.output_format == "json":
            print(json.dumps(r, indent=2))
        else:
            pprint(r)

    def common_options(self, p: ArgumentParser):
        p.add_argument(
            "-o",
            "--output-format",
            choices=["json"],
            help="choose output format. may not work with all commands",
        )

    def dispatch(self, handler, opts):
        if rich is None:
            print("The `rich` module is required to use the cli.")
        config = self.config(opts)
        if config is None:
            return 1
        client = EtnaSession(**config)
        try:
            return handler(opts, client)
        except Exception as E:
            raise
            print("Error: " + str(E))
            return 1


def cli_main():
    app = EtnaCli()
    return app.run()
