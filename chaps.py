"""
Chaps, a relative dir pants wrapper for Python targets.

Chaps makes it easier to interact with your Pants Build System without having
to type out lengthy path names.

Let's say you're in your project dir and want to build a binary. So you:

  $ cd ~/workspace/source ; ./pants binary path/to/target:target

That's just a pain.  This is where chaps comes in:

  $ chaps binary :target

How about just running your code?  We have you covered:

  $ chaps run :target -- args

Interested in dropping into an iPython REPL?  You're golden:

  $ chaps repl :target

Working in your tests directory and want to run tests?   Chaps has a shortcut for
that, too:

  $ chaps test :target

If you're looking to resolve formatting issues, look no more for the fmt goal:

  $ chaps fmt :target

If you need to clean up after Pants, try out the clean command:

  $ chaps clean

Note: chaps only works with targets in your current work directory (cwd).  Fall
back to calling pants directly if you need something else.
"""
# pylint: disable=E0401,E0611,E1101

from __future__ import absolute_import, print_function

from chaps import lib
from twitter.common import app, log

log.LogOptions().disable_disk_logging()


@app.command(name="binary")
def binary_goal(args):
  """Create a binary using pants."""

  targets = lib.targets(lib.rel_cwd(), args)

  if targets is None:
    app.error("No target given.")

  log.debug("chaps targets: %s", targets)

  pants_args = "binary {0}".format(targets)
  lib.pants(pants_args)


@app.command(name="fmt")
def fmt_goal(args):
  """Fix common format issues using pants fmt goal."""

  targets = lib.targets(lib.rel_cwd(), args)

  if targets is None:
    app.error("No target given.")

  log.debug("chaps targets: %s", targets)

  pants_args = "fmt {0}".format(targets)
  lib.pants(pants_args)


@app.command(name="list")
def list_goal():
  """List relative path pants targets."""
  path = lib.rel_cwd()
  pants_args = "list {0}:".format(path)

  lib.pants_list(pants_args)


@app.command(name="repl")
def repl_goal(args):
  """Enter an ipython REPL."""

  targets = lib.targets(lib.rel_cwd(), args)

  if targets is None:
    app.error("No target given.")

  log.debug("chaps targets: %s", targets)

  pants_args = "repl --repl-py-ipython {0}".format(targets)
  lib.pants(pants_args)


@app.command(name="run")
def run_goal(args):
  """Run a target using pants."""

  single_target = args[0]
  targets = lib.targets(lib.rel_cwd(), [single_target])

  if targets is None:
    app.error("No target given.")

  run_args = " ".join(args[1:])

  log.debug("chaps targets: %s", targets)

  pants_args = "run {0} {1}".format(targets, run_args)
  lib.pants(pants_args)


@app.command(name="clean")
@app.command(name="clean-all")
@app.command(name="wash")
def clean_goal(args):
  """Clean pants."""

  log.debug("chaps clean")
  lib.pants("clean-all")


@app.command_option(
  "--all", action="store_true", dest="all", default=False,
  help="Test all targets in path name similar to cwd.",
)
@app.command_option(
  "--coverage", action="store_true", dest="coverage", default=False, help="Python test coverage.",
)
@app.command_option(
  "--failfast", action="store_true", default=False, help="Python stop on first error.",
)
@app.command_option(
  "--verbose", action="store_true", default=False, help="Python test verbosity.",
)
@app.command(name="test")
def test_goal(args, options):
  """Use test.pytest goal with pants."""

  if options.all:
    targets = "%s::" % lib.rel_cwd().replace('src', 'tests')
  else:
    targets = lib.targets(lib.rel_cwd(), args)

  log.debug("chaps targets: %s", targets)

  pants_args = "test.pytest  {0} {1} {2}".format(
    "--coverage=%d" % int(options.coverage),
    "--test-pytest-options='%s'" % lib.pytest_options(options),
    targets,
  )
  lib.pants(pants_args)


app.set_usage_based_on_commands()
app.main()
