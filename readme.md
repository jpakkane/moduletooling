# C++ modules tooling testbed

This repository contains a simulation environment for experimenting
with C++ module building integration. It has a fake compiler, linker
and scanner and a script that generates source trees that build with
these tools using Ninja.

With these anyone can participate in trying to come up with a workable
way of building C++ modules reliably and efficiently. This entire code
base is only a few hundred lines of Python, which is a lot simpler to
grok than a full C++ compiler.

The current setup builds one Ninja dyndep file per target. As an
exercise the curious reader might want to try converting the setup so
that each file is scanned with a separate process. It's not as obvious
as one might expect. Another challenge would be to expand the
generator to build two targets, where one imports modules created by
the other.
