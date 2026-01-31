# smalisp 

A very simple language server for smali with definition support & auto-completion.

| Code completion | Docs |
| --------------- | ---- |
| <img width="1920" height="1048" alt="image" src="https://github.com/user-attachments/assets/b7ce2159-a76d-4ee5-9003-aa31ab1d2a6e" /> | <img width="1920" height="1048" alt="image" src="https://github.com/user-attachments/assets/898c49ba-5295-490a-a97c-619b2bd8226f" /> |

# Installation

## pip
```shell
pip install -U smalisp
```

## From source
```shell
pip install -U git+https://github.com/AbhiTheModder/smalisp.git
```

## Extensions & Setup

### Zed Extension
Prerequisites: Zed editor installed.

- Extension path: `extensions/zed`.

**Option 1: Install from Zed Extensions**
1. Open the Extensions page in Zed.
2. Search for "smalisp".
3. Click Install.

**Option 2: Local Development**
1. Open the Extensions page in Zed.
2. Click the "**Install Dev Extension**" button (or run the `zed: Install Dev Extension` command).
3. Select the directory containing your Zed extension (the folder that contains the manifest and source).

Reference: https://zed.dev/docs/extensions/developing-extensions#developing-an-extension-locally

### VSCode Extension
Prerequisites: VSCode installed.

- Extension path: `extensions/vscode`.
- [Marketplace](https://marketplace.visualstudio.com/items?itemName=qbtaumai.smalisp)

**Option 1: Install from Marketplace**
1. Open VSCode Extensions view (Ctrl+Shift+X)
2. Search for "smalisp"
3. Click Install

OR,
Launch VS Code Quick Open (`Ctrl+P`), paste the following command, and press enter.
```
ext install qbtaumai.smalisp
```

Alternatively, run `code --install-extension qbtaumai.smalisp` from the terminal.

**Option 2: Local Development**
1. Build or obtain the VSIX package for the extension from the releases page of this repository.
2. In VSCode, go to Extensions view, click the three-dot menu, choose Install from VSIX..., and select the downloaded `.vsix` file.
3. Alternatively, run `code --install-extension path/to/extension.vsix` from the terminal.


### Helix
- Prerequisites: Helix installed.

Install/ensure `smalisp` is installed in your Python environment (e.g. `pip install -U smalisp`). For older Helix versions, edit `~/.config/helix/languages.toml` and add the following:

```toml
[language-server.smalisp]
command = "smalisp" # Or path to smalisp binary

[[language]]
name = "smali"
language-servers = [ "smalisp" ]
```

- The PR has been merged and Smalisp is now supported directly by Helix if installed from source or in upcoming Helix versions.

### Vim/NeoVim
- Associate smali filetype with file extensions:

```vim
autocmd BufNewFile,BufRead *.smali setlocal filetype=smali
```

- In order to install syntax highlighting declare it with your plugin manager (for example vim-plug):

```vim
Plug 'Snape3058/vim-smali'
```

- [coc.vim](https://github.com/neoclide/coc.nvim)

```vim
Plug 'neoclide/coc.nvim', {'branch': 'release'}
```

```json
{
 "languageserver": {
  "smalisp": {
   "command": "smalisp",
   "filetypes": ["smali"]
  }
 }
}
```

- [vim-lsp](https://github.com/prabirshrestha/vim-lsp)

```vim
Plug 'prabirshrestha/vim-lsp'

autocmd User lsp_setup call lsp#register_server({
    \ 'name': 'smalisp',
    \ 'cmd': {server_info->['smalisp']},
    \ 'whitelist': ['smali'],
})
```

### Emacs (lsp-mode)
- Prerequisites: Emacs with lsp-mode and eglot options.
- Setup: enable lsp for `smali-mode` and configure the server to run `smalisp`.
- See lsp-mode docs for exact config syntax.
