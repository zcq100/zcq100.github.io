---
layout: post
title: "vim配置文件"
description: 
headline: 
modified: 2017-05-01 23:06:10 +0800
category: personal
tags: ["vim"]
image: 
  feature: 
comments: true
mathjax: 
---

{% highlight VimL %}

set enc=utf-8
set nocompatible              " be iMproved, required
filetype off                  " required
syntax on

set ts=4
set sw=4

set number
set autoindent
set smartindent
set ruler
set hls
set showmatch

let mapleader = "\<Space>"

"F2去除空行
nnoremap <F2> :g/^\s*$/d<CR>

set t_Co=256
set guifont=Courier\ 18

" set the runtime path to include Vundle and initialize
set rtp+=~/.vim/bundle/Vundle.vim
call vundle#begin()
" alternatively, pass a path where Vundle should install plugins
"call vundle#begin('~/some/path/here')

" let Vundle manage Vundle, required
Plugin 'VundleVim/Vundle.vim'
Plugin 'scrooloose/nerdtree'
Plugin 'Xuyuanp/nerdtree-git-plugin'
Plugin 'jistr/vim-nerdtree-tabs'
Plugin 'fholgado/minibufexpl.vim'
Plugin 'vim-airline/vim-airline'
Plugin 'ctrlpvim/ctrlp.vim'

Plugin 'godlygeek/tabular'
"Plugin 'plasticboy/vim-markdown'

Plugin 'elzr/vim-json'
Plugin 'vim-ruby/vim-ruby'
Plugin 'flazz/vim-colorschemes'
Plugin 'tomasr/molokai'

Plugin 'tpope/vim-unimpaired'
Plugin 'tpope/vim-repeat'
Plugin 'tpope/vim-fugitive'
Plugin 'tpope/vim-rails'
Plugin 'tpope/vim-surround'
Plugin 'tpope/vim-speeddating'
Plugin 'tpope/vim-bundler'
Plugin 'tpope/vim-ragtag'
Plugin 'tpope/vim-endwise'
Plugin 'tpope/vim-commentary'
Plugin 'tpope/vim-cucumber'
Plugin 'tpope/vim-markdown'
Plugin 'tpope/vim-haml'
Plugin 'tpope/timl'

Plugin 'henrik/vim-ruby-runner'

Plugin 'thoughtbot/vim-rspec'

Plugin 'kchmck/vim-coffee-script'
Plugin 'pangloss/vim-javascript'
Plugin 'slim-template/vim-slim'
Plugin 'mattn/emmet-vim'

Plugin 'terryma/vim-smooth-scroll'


" The following are examples of different formats supported.
" Keep Plugin commands between vundle#begin/end.
" plugin on GitHub repo
"Plugin 'tpope/vim-fugitive'
" plugin from http://vim-scripts.org/vim/scripts.html
" Plugin 'L9'
" Git plugin not hosted on GitHub
"Plugin 'git://git.wincent.com/command-t.git'
" git repos on your local machine (i.e. when working on your own plugin)
"Plugin 'file:///home/gmarik/path/to/plugin'
" The sparkup vim script is in a subdirectory of this repo called vim.
" Pass the path to set the runtimepath properly.
"Plugin 'rstacruz/sparkup', {'rtp': 'vim/'}
" Install L9 and avoid a Naming conflict if you've already installed a
" different version somewhere else.
" Plugin 'ascenator/L9', {'name': 'newL9'}
" 中文
" All of your Plugins must be added before the following line


call vundle#end()            " required
filetype plugin indent on    " required
" To ignore plugin indent changes, instead use:
"filetype plugin on
"
" Brief help
" :PluginList       - lists configured plugins
" :PluginInstall    - installs plugins; append `!` to update or just :PluginUpdate
" :PluginSearch foo - searches for foo; append `!` to refresh local cache
" :PluginClean      - confirms removal of unused plugins; append `!` to auto-approve removal
"
" see :h vundle for more details or wiki for FAQ
" Put your non-Plugin stuff after this line
"


"NERDTree 
map <C-n> :NERDTreeToggle<CR>
autocmd bufenter * if (winnr("$") == 1 && exists("b:NERDTree") && b:NERDTree.isTabTree()) | q | endif
" Automatically open a NERDTree if no files where specified
autocmd vimenter * if !argc() | NERDTree | endif

"vim-nerdtree-tabs
" 在终端启动vim时，共享NERDTree
let g:nerdtree_tabs_open_on_console_startup=1
" 忽略一下文件的显示
let NERDTreeIgnore=['\.pyc','\~$','\.swp']
" 显示书签列表
let NERDTreeShowBookmarks=1

"nerdtree-git-plug
let g:NERDTreeIndicatorMapCustom = {
    \ "Modified"  : "✹",
    \ "Staged"    : "✚",
    \ "Untracked" : "✭",
    \ "Renamed"   : "➜",
    \ "Unmerged"  : "═",
    \ "Deleted"   : "✖",
    \ "Dirty"     : "✗",
    \ "Clean"     : "✔︎",
    \ "Unknown"   : "?"
    \ }

"MiniBuffer
let g:miniBufExplMapWindowNavVim = 1   
let g:miniBufExplMapWindowNavArrows = 1   
let g:miniBufExplMapCTabSwitchBufs = 1   
let g:miniBufExplModSelTarget = 1  
let g:miniBufExplMoreThanOne=0

map <F11> :MBEbp<CR>
map <F12> :MBEbn<CR>

"vim-markdown
"禁止折叠
let g:vim_markdown_folding_disabled = 1

"emet-vim
let g:user_emmet_install_global = 0
autocmd FileType html,css EmmetInstall

{% endhighlight %}
