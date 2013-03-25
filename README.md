pycow
=====

Copy-on-write for Python

The current implementation is very simplistic and naive but still potentially useful.

TODO
----

1) Object rollback (rollback an object to its original state)
2) Versioned object (maintain all the deltas applied to the object and be able to go back and forth in history)
