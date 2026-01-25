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

### Zed Extension (Local Development)
Prerequisites: Zed editor installed.

- Extension path: `extensions/zed`.

1. Open the Extensions page in Zed.
2. Click the Install Dev Extension button (or run the `zed: Install Dev Extension` command).
3. Select the directory containing your Zed extension (the folder that contains the manifest and source).

Reference: https://zed.dev/docs/extensions/developing-extensions#developing-an-extension-locally

Note: These dev extensions are not yet officially accepted in the Zed extension registry; acceptance is expected soon.

### VSCode Extension (Local Development)
Prerequisites: VSCode installed.

- Extension path: `extensions/vscode`.

1. Build or obtain the VSIX package for the extension from the releases page of this repository.
2. In VSCode, go to Extensions view, click the three-dot menu, choose Install from VSIX..., and select the downloaded `.vsix` file.
3. Alternatively, run `code --install-extension path/to/extension.vsix` from the terminal.

Note: The VSCode extension is not yet published in the official VSCode Marketplace; use local VSIX for testing.


### Helix
- Prerequisites: Helix installed.

Install/ensure `smalisp` is installed in your Python environment (e.g. `pip install -U smalisp`). Then edit `~/.config/helix/languages.toml` and add the following:

```toml
[language-server.smalisp]
command = "smalisp" # Or path to smalisp binary

[[language]]
name = "smali"
language-servers = [ "smalisp" ]
```

- Official integration PR for Helix has been submitted; Smalisp should be available out-of-the-box soon.

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
