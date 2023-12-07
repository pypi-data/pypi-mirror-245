Version 0.12.0
==============

Make

public struct <A:AsRef<Str>>IRI(A)

to enable the use of horned in a multithreaded environment


Version next
============

Support fully multi file ontology parsing


Version next
============

Parser Headbutting.

The RDF parser near miss, add strict/lax mode


Version next
==============

Clean up command line code. Add a multiplexer `horned-owl dump` ->
`horned-dump`

Version next
==============

Consider tighter integration with other crates, especially for
IRIs. Bump quick-xml version so it's compatible with what ever we are
using for RDF parsing.


Other Changes that I'd like to makes
====================================


Think about Errors
------------------

These are not well thought out at the moment.

These have been re-written to take advantage of more recent changes in
the Rust error trait. But there is a lot of inconsistency in the
handling -- in some cases, very detailed, in others very blunt. Error
types from individual files could be co-ordinated. And the commands
should probably stop returning such specific errors.


Removing a layer of complexity in Axiom
---------------------------------------

`Axiom` is currently complicated because it has an extra layer on
indirection. Each variant of the enum is takes a different struct,
rather than using struct like variants in the Enum. This was done
to support typing in methods and means, for example, that the
`axiom_mapped` index has a sensible return type. But it makes querying
the ontology structures harder.

At the moment, there is a choice, but if Rust support enum variants as
types, I could have my cake and eat it.
