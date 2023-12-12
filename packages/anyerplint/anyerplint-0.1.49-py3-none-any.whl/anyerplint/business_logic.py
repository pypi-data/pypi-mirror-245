import os
import re
import shutil
import urllib.request
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import IO
from xml.etree import ElementTree
from xml.etree.ElementTree import Element

import yaml

from . import __version__, util

ROOT = Path(__file__).absolute().parent


@dataclass
class Library:
    variables: set[str]
    loopvariables: set[str]
    calls: set[str]
    functions: set[str]
    jumps: set[str]
    tags: set[str]
    # if true, accumulate everything found to library
    teaching: bool


# aggregate full report here
full_report: dict[str, int] = {}


# ruff lead this alone man
emit = print


def do_import(fnames: str) -> None:
    target_dir = get_app_local_dir()
    if not os.path.isdir(target_dir):
        os.makedirs(target_dir)
    for f in fnames:
        if f.startswith("http"):
            lastpart = f.split("/")[-1]
            emit(lastpart)

            if not lastpart.endswith(".zip"):
                lastpart = "downloaded.zip"
            tfile = Path(target_dir) / lastpart
            emit("Fething:", f, "->", tfile)
            urllib.request.urlretrieve(f, tfile)
        elif f.endswith(".zip"):
            emit("Copying:", f, "->", target_dir)
            shutil.copy(f, target_dir)
        else:
            emit("Not a zip file:", f)


def get_app_local_dir() -> Path:
    local_app_data = os.getenv("LOCALAPPDATA")
    if local_app_data:
        return Path(local_app_data) / "anyerplint"
    raise Exception("Could not find LOCALAPPDATA")


def do_check(
    libs: list[str],
    targets: list[str],
    teaching: bool,
    nostdlib: bool = False,
) -> dict[str, str | dict[str, list[str]]]:
    emit(f"AnyErpLintVersion: {__version__.strip()}")

    lib_vars = Library(
        variables=set(),
        calls=set(),
        functions=set(),
        jumps=set(),
        tags=set(),
        teaching=teaching,
        loopvariables=set(),
    )

    # always feed the "standard library, except when unit testing (nostdlib)

    if not nostdlib:
        local_app_data = get_app_local_dir()
        feed_lib(lib_vars, local_app_data)

    for lib in libs:
        feed_lib(lib_vars, Path(lib))

    has_errors = False
    all_errors: dict[str, str | dict[str, list[str]]] = {}
    for target in targets:
        if os.path.isdir(target):
            errs = check_dir(lib_vars, Path(target))
        else:
            assert target.lower().endswith(".xml")
            try:
                r = parse_file(target, teaching)
            except (ElementTree.ParseError, PermissionError, UnicodeDecodeError) as e:
                all_errors[target] = report_fatal(Path(target), e)
                has_errors = True
                continue
            error_report = report(lib_vars, target, r)
            errs = {target: error_report} if error_report else {}
        if errs:
            all_errors.update(errs)
            has_errors = True

    if lib_vars.teaching:
        write_lib(lib_vars)

    if has_errors:
        emit("Errors found: >")
        rep = sorted((k, v) for (k, v) in full_report.items())
        for line in rep:
            emit("  ", line[0], ";", line[1])

    return all_errors


def write_lib(lib_vars: Library) -> None:
    def write_file(fname: Path, lines: list[str]) -> None:
        emit("  - ", fname)
        f = open(fname, "wb")
        for line in lines:
            try:
                enc = line.strip().encode()
            except UnicodeEncodeError:
                # skip bad lines for now
                continue
            f.write(enc)
            f.write(b"\n")

    emit("Writing found function to:")

    stdlib = get_app_local_dir()
    calls_file = stdlib / "builtin_calls.txt"
    write_file(
        calls_file, sorted(call for call in lib_vars.calls if is_valid_call(call))
    )

    functions_file = stdlib / "builtin_functions.txt"
    write_file(functions_file, sorted(lib_vars.functions))

    jumps_file = stdlib / "builtin_jumps.txt"
    write_file(jumps_file, sorted(lib_vars.jumps))

    tags_file = stdlib / "builtin_tags.txt"
    write_file(tags_file, sorted(lib_vars.tags))

    vars_file = stdlib / "builtin_vars.txt"
    write_file(vars_file, sorted(lib_vars.variables))

    loopvars_file = stdlib / "builtin_loopvars.txt"
    write_file(loopvars_file, sorted(lib_vars.loopvariables))


def is_valid_call(call: str) -> bool:
    return True


def feed_lib(lib_vars: Library, libdir: Path) -> None:
    def feed_set(set: set[str], fobj: IO[bytes]) -> None:
        set.update(line.decode().strip() for line in fobj.readlines())

    def visit_file(fname: str, fobj: IO[bytes]) -> None:
        if fname.endswith("_calls.txt"):
            feed_set(lib_vars.calls, fobj)
        elif fname.endswith("_functions.txt"):
            feed_set(lib_vars.functions, fobj)
        elif fname.endswith("_jumps.txt"):
            feed_set(lib_vars.jumps, fobj)
        elif fname.endswith("_tags.txt"):
            feed_set(lib_vars.tags, fobj)
        elif fname.endswith("_vars.txt"):
            feed_set(lib_vars.variables, fobj)
        elif fname.endswith("_loopvars.txt"):
            feed_set(lib_vars.loopvariables, fobj)

    if not libdir.exists():
        return

    # files on file system
    for p in libdir.glob("*_*.txt"):
        visit_file(str(p), p.open("rb"))

    # files in all the zip files
    for f in libdir.glob("*.zip"):
        zf = zipfile.ZipFile(f, "r")
        for zn in zf.namelist():
            visit_file(zn, zf.open(zn, "r"))


def report_fatal(fname: Path, ex: Exception) -> str:
    message = f"FATAL, {ex}"
    emit(f"{fname}: {message}")
    return message


def should_skip_file(fpath: Path) -> bool:
    with util.open_text_file(fpath) as f:
        text = f.read(10000)
        return not ("<erpConnector" in text or "<section" in text)


def check_dir(lib_vars: Library, root: Path) -> dict[str, dict[str, list[str]]]:
    errs = {}
    for f in root.glob("**/*.xml"):
        try:
            if should_skip_file(f):
                emit(f"{f}: SKIP nontemplate")
                continue
            r = parse_file(f, lib_vars.teaching)
        except (ElementTree.ParseError, PermissionError, UnicodeDecodeError) as e:
            # TODO: Add this to the report
            report_fatal(f, e)
            continue

        errlist = report(lib_vars, str(f), r)
        if errlist:
            errs[str(f)] = errlist
            full_report[str(f)] = len(errlist)

    return errs


@dataclass
class Parsed:
    var_decl: set[str]
    var_used: set[str]
    alltags: set[str]
    calls: set[str]
    jumps: set[str]
    syntax_errors: list[str]
    loop_var_decl: set[str]
    loop_var_use: set[str]
    used_functions: set[str]
    full_content: str


def add_linenumbers(cont: str, needles: list[str]) -> list[str]:
    hits: list[list[int]] = [[] for i in range(len(needles))]
    for linenum, line in enumerate(cont.splitlines()):
        for _in, n in enumerate(needles):
            if n in line:
                hits[_in].append(linenum)

    return [
        n + " - line " + ", ".join(map(str, hits[idx]))
        for (idx, n) in enumerate(needles)
    ]


def report(lib_vars: Library, fname: str, p: Parsed) -> dict[str, list[str]]:
    undeclared_vars = p.var_used - p.var_decl
    undeclared_vars.difference_update(lib_vars.variables)
    unknown_loop_variables = p.loop_var_use - p.loop_var_decl
    unknown_loop_variables.difference_update(lib_vars.loopvariables)

    if lib_vars.teaching:
        lib_vars.calls.update(p.calls)
        lib_vars.functions.update(f for f in p.used_functions if f.isupper())
        lib_vars.jumps.update(p.jumps)
        lib_vars.tags.update(p.alltags)
        lib_vars.variables.update(undeclared_vars)
        lib_vars.loopvariables.update(unknown_loop_variables)

    errors = {}

    if undeclared_vars:
        errors["Unknown variables"] = add_linenumbers(
            p.full_content, sorted(undeclared_vars)
        )

    unknown_calls = p.calls
    unknown_calls.difference_update(lib_vars.calls)
    if unknown_calls:
        errors["Unknown calls"] = sorted(unknown_calls)

    unknown_functions = p.used_functions
    unknown_functions.difference_update(lib_vars.functions)
    if unknown_functions:
        errors["Unknown functions"] = add_linenumbers(
            p.full_content, sorted(unknown_functions)
        )

    unknown_jumps = p.jumps
    unknown_jumps.difference_update(lib_vars.jumps)
    if unknown_jumps:
        errors["Unknown jumps"] = sorted(unknown_jumps)

    unknown_tags = p.alltags
    unknown_tags.difference_update(lib_vars.tags)
    if unknown_tags:
        errors["Unknown tags"] = sorted(unknown_tags)

    if p.syntax_errors:
        errors["Other errors"] = list(p.syntax_errors)

    if unknown_loop_variables:
        errors["Unknown loop variables"] = sorted(unknown_loop_variables)

    if errors:
        emit(yaml.dump({fname: errors}, width=200).strip())

    return errors


key_params: dict[str, str] = {
    "bw_file_functions": "command",
    "bw_table_method": "command",
    "bw_string_functions": "operation",
    "bw_ws_function": "method",
}


def summarize_call(node: Element) -> str:
    name = node.attrib["name"].lower()
    full = name
    params = {
        p.attrib["name"]: (p.text or "TEXTMISSING") for p in node.iter("parameter")
    }
    suboperation_param_name = key_params.get(name)
    if suboperation_param_name:
        suboperation = params.get(suboperation_param_name, "UNK")
        full += "." + suboperation

    return full + " - " + ",".join(sorted(params))


def summarize_output(node: Element) -> str:
    type = node.attrib.get("type", "NOTYPE")
    params = {p.attrib.get("name", "NONAME") for p in node.iter("parameter")}

    return "Output " + type + " - " + ",".join(sorted(params))


def summarize_tag(node: Element) -> str:
    at = " " + " ".join(sorted(node.attrib.keys())) if node.attrib else ""
    full = "<" + node.tag + at + ">"
    return full


def brace_check(s: str) -> list[str]:
    stack: list[tuple[str, int]] = []
    lines = s.splitlines()
    closers = {"{": "}", "[": "]", "(": ")"}
    errors: list[str] = []
    for lnum, line in enumerate(lines, 1):
        flush_stack = False
        in_quote = False
        for cnum, ch in enumerate(line, 1):
            if ch == '"':
                # only care about quotes if we are in some nested operation already, top level quotes are not considered
                if stack:
                    in_quote = not in_quote

            if in_quote:
                continue

            if ch in "{([":
                stack.append((ch, lnum))
            if ch in "})]":
                try:
                    from_stack, _ = stack.pop()
                except IndexError:
                    errors.append(
                        f"Too many closing braces at line {lnum}, looking at '{ch}' on col {cnum}: ==> {line[cnum-10:cnum]} <==: {line.strip()}",
                    )
                    flush_stack = True
                    break

                expected = closers[from_stack]
                if expected != ch:
                    errors.append(
                        f"Expected brace {expected}, got {ch} at line {lnum} col {cnum}: {line.strip()}",
                    )
                    flush_stack = True
                    break
        if flush_stack:
            stack = []
    if stack:
        pretty_stack = ", ".join(f"{ch} {l}" for ch, l in stack)
        errors.append(
            f"File ended with mismatched braces, remaining in stack (char, linenum): {pretty_stack}",
        )
    return errors


# xxx not really needed due to new logic
MAGIC_VAR_NAMES = {"error", "return", "response", "invoice.i"}


def describe_node(n: Element) -> str:
    return "<" + n.tag + str(n.attrib) + ">"


def describe_jump(n: Element) -> str:
    params = sorted(
        child.attrib.get("name", "NONAME").strip() for child in n.iter("parameter")
    )
    target = n.attrib.get("jumpToXPath", "NOXPATH")
    prefix = "//section[@name='"
    if target.startswith(prefix):
        target = "..." + target[len(prefix) :].rstrip("]'")

    desc = (
        "Jump "
        + n.attrib.get("jumpToXmlFile", "NOFILE")
        + " -- "
        + target
        + " -- "
        + " ".join(params)
    )
    return desc.strip()


def _replace_with_empty(match: re.Match[str]) -> str:
    comment = match.group(0)
    empty_lines = "\n" * comment.count("\n")
    return empty_lines


def replace_commented_xml_with_empty_lines(xml_string: str) -> str:
    comment_pattern = "<!--(.*?)-->"
    result = re.sub(comment_pattern, _replace_with_empty, xml_string, flags=re.DOTALL)
    return result


def replace_cdata_with_empty_lines(xml_string: str) -> str:
    cdata_pattern = r"<!\[CDATA\[(.*?)\]\]>"
    result = re.sub(cdata_pattern, _replace_with_empty, xml_string, flags=re.DOTALL)
    return result


def is_illegal_password(name: str, value: str) -> bool:
    if "passw" not in name.lower():
        return False
    stripped = (value or "").strip()
    if not stripped:
        return False
    if stripped.startswith("{"):
        # password should always be references to variables or expressions, never literal values
        return False
    return True


def parse_file(fname: str | Path, teaching: bool = False) -> Parsed:
    tree = ElementTree.parse(fname)
    raw_cont = util.open_text_file(fname).read()
    comments_removed = replace_commented_xml_with_empty_lines(raw_cont)

    vardecl = {
        v.attrib.get("name", "unknown_var"): (v.text or "")
        for v in tree.iter("variable")
    }
    all_params = {
        v.attrib.get("name", "unknown_var"): (v.text or "")
        for v in tree.iter("parameter")
    }

    propaccess = {
        (match.group(1), match.group(2))
        for match in re.finditer("([a-zA-Z.]+),(\\w+)", comments_removed)
    }
    varuse = {name for expr_type, name in propaccess if expr_type.lower() == "v"}
    used_functions = {
        expr_type + "," + name
        for expr_type, name in propaccess
        if expr_type.lower() == "f"
    }

    # what to do with p params?
    otherpropaccess = {k for k, v in propaccess if k.lower() not in ["v", "f", "p"]}
    otherpropaccess.difference_update(MAGIC_VAR_NAMES)
    calls = {summarize_call(v) for v in tree.iter("builtInMethodParameterList")}
    outputs = {summarize_output(v) for v in tree.iter("output")}
    calls.update(outputs)
    alltags = {summarize_tag(t) for t in tree.iter()}
    loop_data_source_attribs = {n.attrib.get("loopDataSource") for n in tree.iter()}
    loop_data_sources = {
        ls.split(";")[0].lower() for ls in loop_data_source_attribs if ls
    }
    return_names = {
        n.attrib.get("name", "UNNAMED_RETURN").lower() for n in tree.iter("return")
    }
    loop_data_sources.update(return_names)

    jumps = {
        describe_jump(n) for n in tree.iter("method") if n.attrib.get("jumpToXmlFile")
    }

    errors = []

    if not teaching:
        cdata_removed = replace_cdata_with_empty_lines(comments_removed)
        errors.extend(brace_check(cdata_removed))

        no_text_allowed_tags = [
            "sections",
            "section",
            "method",
            "output",
            "outputCommands",
            "builtInMethodParameterList",
        ]
        for notext in no_text_allowed_tags:
            nodes = tree.iter(notext)
            for n in nodes:
                if n and n.text and n.text.strip():
                    errors.append(
                        "Node should not contain text: "
                        + describe_node(n)
                        + " -- "
                        + n.text.strip(),
                    )
        var_passwords = {v for v in vardecl if is_illegal_password(v, vardecl[v])}
        param_passwords = {
            p for p in all_params if is_illegal_password(p, all_params[p])
        }
        passwords = var_passwords | param_passwords
        if passwords:
            errors.append("Passwords contains literal text: " + ",".join(passwords))

    return Parsed(
        var_decl=set(vardecl),
        var_used=varuse,
        alltags=alltags,
        calls=calls,
        jumps=jumps,
        used_functions=used_functions,
        syntax_errors=errors,
        loop_var_decl=loop_data_sources,
        loop_var_use=otherpropaccess,
        full_content=comments_removed,
    )
