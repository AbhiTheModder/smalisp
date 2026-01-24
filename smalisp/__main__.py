import logging
import urllib.request
from pathlib import Path

import yaml
from lsprotocol import types
from pygls.cli import start_server
from pygls.lsp.server import LanguageServer

logging.basicConfig(level=logging.INFO, format="%(message)s")

GRAMMAR_URL = (
    "https://github.com/RevEngiSquad/smalig/raw/refs/heads/main/smalig/grammar.yaml"
)
GRAMMAR_PATH = Path(__file__).parent / "grammar.yaml"

if not GRAMMAR_PATH.exists():
    logging.info("Grammar file missing. Downloading...")
    urllib.request.urlretrieve(GRAMMAR_URL, GRAMMAR_PATH)


def load_smali_grammar():
    with open(GRAMMAR_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def create_instruction_lookup(grammar):
    lookup = {}
    for instruction in grammar:
        name = instruction.get("name", "").lower()
        if name:
            lookup[name] = instruction
    return lookup


SMALI_GRAMMAR = load_smali_grammar()
INSTRUCTION_LOOKUP = create_instruction_lookup(SMALI_GRAMMAR)

INSTRUCTION_COMPLETIONS = [
    types.CompletionItem(
        label=instruction["name"],
        kind=types.CompletionItemKind.Keyword,
        documentation=types.MarkupContent(
            kind=types.MarkupKind.Markdown,
            value=f"**{instruction['name']}**\n\n{instruction.get('short_desc', '')}\n\n**Syntax:** `{instruction.get('syntax', '')}`",
        ),
        insert_text=instruction["name"],
    )
    for instruction in SMALI_GRAMMAR
    if instruction.get("name")
]

server = LanguageServer("smalisp", "v1")


@server.feature(types.INITIALIZE)
def initialize(params: types.InitializeParams) -> types.InitializeResult:
    return types.InitializeResult(
        capabilities=types.ServerCapabilities(
            completion_provider=types.CompletionOptions(
                resolve_provider=False, trigger_characters=[" ", "\t"]
            )
        ),
        server_info=types.ServerInfo(name="smals", version="0.1.0"),
    )


@server.feature(types.TEXT_DOCUMENT_COMPLETION)
def completion(ls: LanguageServer, params: types.CompletionParams):
    document = ls.workspace.get_text_document(params.text_document.uri)
    line = document.lines[params.position.line]
    col = params.position.character

    i = 0
    n = len(line)
    while i < n and line[i].isspace():
        i += 1
    first_start = i
    while i < n and not line[i].isspace():
        i += 1
    first_end = i

    if not (first_start <= col <= first_end):
        return None

    start = first_start
    for i in range(col - 1, first_start - 1, -1):
        if line[i].isspace():
            start = i + 1
            break

    current_token = line[start:col]

    if not current_token.strip():
        return None

    items = [
        item
        for item in INSTRUCTION_COMPLETIONS
        if item.label.lower().startswith(current_token.lower())
    ]

    if not items:
        return None

    return types.CompletionList(is_incomplete=False, items=items)


@server.feature(types.TEXT_DOCUMENT_HOVER)
def hover(ls: LanguageServer, params: types.HoverParams):
    pos = params.position
    document_uri = params.text_document.uri
    document = ls.workspace.get_text_document(document_uri)

    try:
        line = document.lines[pos.line]
    except IndexError:
        return None

    i = 0
    while i < len(line) and line[i].isspace():
        i += 1
    start = i
    while i < len(line) and not line[i].isspace():
        i += 1
    end = i

    if not (start <= pos.character <= end):
        return None

    instruction_name = line[start:end].lower()
    instruction = INSTRUCTION_LOOKUP.get(instruction_name)
    if not instruction:
        return None

    hover_content = [
        f"## {instruction.get('name', 'Unknown').upper()}",
        f"**Opcode:** `0x{instruction.get('opcode', '00')}`",
        f"**Format:** `{instruction.get('format_id', 'Unknown')}`",
        f"**Syntax:** `{instruction.get('syntax', 'Unknown')}`",
        "",
        f"**{instruction.get('short_desc', 'No description')}**",
        "",
        instruction.get("long_desc", "No detailed description."),
        "",
    ]

    args_info = instruction.get("args_info", "")
    if args_info:
        hover_content.extend(["**Arguments:**", args_info, ""])

    example = instruction.get("example", "")
    example_desc = instruction.get("example_desc", "")
    if example:
        hover_content.extend(["**Example:**", f"```{example}```", ""])
        if example_desc:
            hover_content.extend([f"*{example_desc}*", ""])

    note = instruction.get("note", "")
    if note:
        hover_content.extend(["**Note:**", note, ""])

    return types.Hover(
        contents=types.MarkupContent(
            kind=types.MarkupKind.Markdown,
            value="\n".join(hover_content),
        ),
        range=types.Range(
            start=types.Position(line=pos.line, character=start),
            end=types.Position(line=pos.line, character=end),
        ),
    )


def main():
    start_server(server)


if __name__ == "__main__":
    main()
