# `adk web` and `adk deploy` find the agent by importing this package, so this
# file is where tracing gets switched on. Importing instrumentation runs it.
from . import instrumentation  # noqa: F401
from . import agent  # noqa: F401
