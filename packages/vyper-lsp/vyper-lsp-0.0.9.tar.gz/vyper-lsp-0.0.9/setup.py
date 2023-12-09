# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vyper_lsp', 'vyper_lsp.analyzer', 'vyper_lsp.grammar']

package_data = \
{'': ['*'],
 'vyper_lsp.analyzer': ['.build/*', '.hypothesis/unicode_data/14.0.0/*']}

install_requires = \
['lark>=1.1.7,<2.0.0',
 'loguru>=0.6.0,<0.7.0',
 'lsprotocol>=2023.0.0b1,<2024.0.0',
 'packaging>=23.1,<24.0',
 'pydantic>=1.10,<2.0',
 'pygls>=1.1.2,<2.0.0',
 'tree-sitter>=0.20.1,<0.21.0',
 'vvm>=0.2.0,<0.3.0',
 'vyper>=0.3.7,<0.4.0']

entry_points = \
{'console_scripts': ['vyper-lsp = vyper_lsp.main:main']}

setup_kwargs = {
    'name': 'vyper-lsp',
    'version': '0.0.9',
    'description': 'Language server for Vyper, a pythonic smart contract language',
    'long_description': '# Vyper LSP Server\n\n## Requirements\n\nVyper LSP requires a minimum vyper version of 0.3.7. For full support, it is also required that the Vyper version installed in your virtual environment is capable of compiling your contract.\n\nFor example, a vyper contract with `#pragma version 0.3.8` cannot be compiled with `0.3.10`, so you must install `vyper==0.3.8` if you want full support while working with this contract.\n\nA contract with `#pragma version >=0.3.8` will work fine with any installed vyper version greater than the requirement, so you can get full support while editing this contract if you have the latest vyper version installed.\n\n## Install Vyper-LSP\n\n### via `pipx`\nI like `pipx` because it handles creating an isolated env for executables and putting them on your path.\n\n`pipx install git+https://github.com/vyperlang/vyper-lsp.git`\n\n### via `pip`\nYou can install using `pip` if you manage your environments through some other means:\n\n> TODO: publish on pypi\n\n`pip install git+https://github.com/vyperlang/vyper-lsp.git`\n\n## Verify installation\n\nCheck that `vyper-lsp` is on your path:\n\nIn your terminal, run `which vyper-lsp`. If installation was succesful, you should see the path to your installed executable.\n\n## Editor Setup\n\n### Emacs\n\nThe following emacs lisp snippet will create a Vyper mode derived from Python Mode, and sets up vyper-lsp.\n\n``` emacs-lisp\n(define-derived-mode vyper-mode python-mode "Vyper" "Major mode for editing Vyper.")\n\n(add-to-list \'auto-mode-alist \'("\\\\.vy\\\\\'" . vyper-mode))\n\n(with-eval-after-load \'lsp-mode\n  (add-to-list \'lsp-language-id-configuration\n               \'(vyper-mode . "vyper"))\n  (lsp-register-client\n   (make-lsp-client :new-connection\n                    (lsp-stdio-connection `(,(executable-find "vyper-lsp")))\n                    :activation-fn (lsp-activate-on "vyper")\n                    :server-id \'vyper-lsp)))\n```\n\n### Neovim\n\nAdd the following to your `neovim` lua config.\n\nIt should be at `~/.config/nvim/init.lua`\n\n``` lua\nvim.api.nvim_create_autocmd({ "BufEnter" }, {\n  pattern = { "*.vy" },\n  callback = function()\n    vim.lsp.start({\n      name = "vyper-lsp",\n      cmd = { "vyper-lsp" },\n      root_dir = vim.fs.dirname(vim.fs.find({ ".git" }, { upward = true })[1])\n    })\n  end,\n})\n\nvim.api.nvim_create_autocmd({ "BufEnter" }, {\n  pattern = { "*.vy" },\n  callback = function()\n    vim.lsp.start({\n      name = "vyper-lsp",\n      cmd = { "vyper-lsp" },\n      root_dir = vim.fs.dirname(vim.fs.find({ ".git" }, { upward = true })[1])\n    })\n  end,\n})\n\nvim.api.nvim_set_keymap(\'n\', \'gd\', \'<Cmd>lua vim.lsp.buf.definition()<CR>\', { noremap = true, silent = true })\nvim.api.nvim_set_keymap(\'n\', \'gD\', \'<Cmd>lua vim.lsp.buf.declaration()<CR>\', { noremap = true, silent = true })\nvim.api.nvim_set_keymap(\'n\', \'gr\', \'<Cmd>lua vim.lsp.buf.references()<CR>\', { noremap = true, silent = true })\nvim.api.nvim_set_keymap(\'n\', \'gi\', \'<Cmd>lua vim.lsp.buf.implementation()<CR>\', { noremap = true, silent = true })\nvim.api.nvim_set_keymap(\'n\', \'K\', \'<Cmd>lua vim.lsp.buf.hover()<CR>\', { noremap = true, silent = true })\nvim.api.nvim_set_keymap(\'n\', \'<C-k>\', \'<Cmd>lua vim.lsp.buf.signature_help()<CR>\', { noremap = true, silent = true })\nvim.api.nvim_set_keymap(\'n\', \'[d\', \'<Cmd>lua vim.lsp.diagnostic.goto_prev()<CR>\', { noremap = true, silent = true })\nvim.api.nvim_set_keymap(\'n\', \']d\', \'<Cmd>lua vim.lsp.diagnostic.goto_next()<CR>\', { noremap = true, silent = true })\n\n```\n\n\n### VS Code\n\nSee `vyper-lsp` VS Code extension\n',
    'author': 'z80',
    'author_email': 'z80@ophy.xyz',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<3.12',
}


setup(**setup_kwargs)
