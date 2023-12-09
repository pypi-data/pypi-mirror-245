# Cursed - a Vim Inspired Text Editor Written in Pure Python

## Quickstart

Want to try out the editor without installing anything?

Just clone the repo and run `./main.py file_to_edit.txt`

Like vim, press "a" or "i" to get into "insert mode".

Press control+s to save.
Press control+c to exit.

## Features

- Only dependency is the python standard library
- Supports some of vim's key bindings
- Very simple.  No configuration.
- Doesn't appear to crash all the time ;)

## Motivation

I've been a vim user for many years and while I do love vim,
I wanted _complete_ control over my text editor, so I decided
to write one.

## Support Expectations

While I am passionate about excellent software, I have:
- a day job as a software engineer (which I'm very lucky to love and enjoy)
- and a beautiful family (which I love more)

Therefore, it is natural that all those things are going to be a higher priority
for me than adding features and fixing bugs to this project.

So while I am honored by the fact you are considering using this software, and
I'm eager to hear feedback via issues and merge requests, I respectfully ask
that you remember that this is a hobby project and that it will be supported as
such.

So please do not be a jerk, and I'll promise not to be a jerk as well!


## Design Decisions

These are some rules of thumb I'm trying to keep in mind as I write the cursed editor.

- Prefer a "clean" implementation over feature additions.   I'm more interested in
  the long term maintenance of this project than rapidly and hastily adding features.
- Stick to the standard library.   The fewer dependencies a project has, the easier
  it is to deploy.   This may become a challenge once we start trying to deal with things
  like the clipboard, but we'll cross that bridge when we get there.

## ideas for further development
Please see the [Issues Page](https://gitlab.com/grocksalot/cursed_editor/-/issues)

## Rationalle behind not supporting arbitrarily large files.
So I have determined that this program should NOT support arbitrarily large files.

Here is why:
	- copying the file to edit into a temporary location would be a huge cost
	  of disk space
	- there is not a reliable way of locking files in a cross platform way when
	  we have no control over what other programs may be accessing the file
	- doing the accounting and overhead of caching where linefeeds are located
	  and where edits have been made is extremely complicated.

So my conclusion is that just loading the whole file into memory will be a
lot easier, so we will not support files which can't fit into memory


## Getting Started Developing The Cursed Editor

### Setting up the environment.

I like to try to make it very easy to set up development environments for
my projects.   Currently, we have the following requirements:

- a linux/unix like Operating System
- poetry - https://python-poetry.org/docs/#installation
- and a python interpreter

### Running the tests

After cloning the repo, it's best to get a baseline for performance and
functionality of the application.   Try checking out the `main` branch
and running the tests by issuing the following command.

`poetry run poe test`

Or if you are already in a `poetry shell`, simply running `poe test` will
do the same thing.

This project uses Poe The Poet (https://pypi.org/project/poethepoet/) to
declare and run project related tasks.   The `test` task does all the
same things we check for during a merge request into the main branch.

Therefore, all the tests should pass (on linux/unix).

I do not currently own a mac and so I cannot be certain that this will
work on a mac.  However, I know that this will not work on windows for
the following reasons:
- The windows version of Python does not include the `curses` module.
- The tests of application.py rely on the `tty` module of the standard
  library, which only works on unix.

Aside from this, however, if for some strange reason the tests fail
despite being run on linux, It's proabably an issue.

Either something is wrong with the software, or the environment setup
of this documentation is not accurate or intuitive.   I'd be happy to help
out if any issues are encountered at this phase.

### Details on the checks run by `poe test`

For a listing of all poe jobs simply run

`poe`

#### Code Formatting

We currently use black for formatting, but in case we ever decide to change
this running

`poe format`

Will always do the same format operation as the main branch of the repo.

Currently `black .` will also, work but if, in the future we move away from
black, `poe format` will still do the "official formatting".

#### Lint checks

Currently we are using pylint for static analysis.   I've written a custom
pylint plugin for this project, and might write more over time, so I pretty
satisfied sticking with pylint for now.

`poe lint`

really just does `pylint .`

### The pyproject.toml file

This project make heavy use of the features of pyproject.toml, I'd prefer
that all project configuration (pylint, coverage, black, poe, etc) stay
in the pyproject.toml file if possible.
