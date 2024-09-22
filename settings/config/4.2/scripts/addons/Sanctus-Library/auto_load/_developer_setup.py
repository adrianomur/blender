
def main():
    from pathlib import Path

    file = Path(__file__)
    auto_load_dir = file.parent

    vsc_snippets_file = auto_load_dir.joinpath('_vsc_code_snippets.json')

    addon_dir = auto_load_dir.parent
    vscode_dir = addon_dir.joinpath('.vscode')
    if not vscode_dir.exists():
        vscode_dir.mkdir()
    al_snippets_file = vscode_dir.joinpath('al_snippets.code-snippets')
    al_snippets_file.write_text(vsc_snippets_file.read_text())

if __name__ == "__main__":
    main()
