---
Type: finding
Purpose: "What five independently built competition methods require as input, read from their entry points, and whether this journal could supply any of it."
Depends on: [docs/findings/foreign-method-composition.md]
Depended on by: [docs/corpus-index.md]
---

# Finding: Foreign Method Input Shapes

**Instrument.** Reading entry points and validation code. Nothing was vendored
and no wrappers were written.
**n.** 5 methods, selected by license availability out of twenty-one
competition submissions.
**Dates.** 2026-08-14.
**Operator.** One person, one afternoon, reading five repositories cold.

## Result

**For three of five methods the substrate and the methods do not meet. The
fourth meets only if payload is solved, and payload alone is not enough. The
fifth wants something further up than any of them.**

Every one of the five requires an authoring layer this journal does not carry.
They do not all require the same authoring layer, which is the part worth
knowing.

| Method | Entry point | Consumes | Meets the journal? |
|---|---|---|---|
| kyaloeric | `assess_graph(graph, case)` | `claims[{id,kind,text}]`, `edges[{from,to,type}]`, at least one `conclusion` | no |
| laihsienhao | `compute_cruxes(graph)` | `Claim{id,case,text,label,status,sources,confidence,author}`, `Edge{relation in {supports,depends_on},from,to,provenance}`, root theses | no |
| SimonSkade1 | `run(notes_dir)` | Obsidian note tree, eight node types including `hypothesis`, `argument`, `evidence-link`, `correlation-group`, with executable prior and evidence blocks | no |
| ReticleWorks | `extract_crux_map(query, panel_result)` | preserved separate judgments from several AI reviewers: `judgment` free text, `uncertainty.band`, `cited_sources`, `facts`, `stance_seed` | no |
| astrakhantsev | `load(corpus_path, concepts_path)` | `documents[{id, community, text}]` and `concepts[{term, owning_community, constrained_definition, naive_question}]` | not without three further things |

## Three want a claim graph

kyaloeric was established separately in `docs/findings/foreign-method-composition.md`.

laihsienhao is the same wall. Its edge vocabulary is `supports` and
`depends_on`, and a crux is a `depends_on`-only path from a claim up to a root
thesis. Typed edges and marked conclusions, under different names.

SimonSkade1 needs more rather than less: an eight-type node ontology where
observations link to hypothesis clusters through evidence-links, with
correlation groups for shared dependence, authored by a ten-step pipeline of
language-model agents. The runner is deterministic; the graph it runs over is not
something an instrument records.

## One wants a layer above a claim graph

ReticleWorks does not consume a graph. It consumes the preserved, separately
maintained judgments of several AI reviewers answering one narrow question, and
extracts a candidate crux from where they diverge. Supplying it would mean
running a reviewer panel first. The journal is not a smaller version of that
input, it is a different kind of thing.

## One wants a document corpus, and payload is necessary but not sufficient

This is the case that looked closest to meeting the journal, and reading it
closely made the fit looser rather than tighter.

astrakhantsev wants documents, which is what this substrate is about. The
journal already individuates objects by `object_hash` derived locally. So the
`id` field is free.

**It is not free after that.** A journal with full payload text stored locally
would still not satisfy `load()`. Three things are missing and payload
acquisition supplies none of them.

**A community partition that means discourse community.** The shipped corpus
partitions on `lipidology`, `cardiology-biomarker`, `nutrition-epi-methods`,
`lay-public-health`. The corpus template asks for passages "in that community's
own voice". A community is a group that names a shared concept its own way,
which is the entire subject of the method. The journal carries `host`, which is
a publisher. One host carries many communities and one community spans many
hosts. Mapping `host` onto `community` is the same co-occurrence invention that
`functions/concentration/GAP.md` refused, and it would produce a keyness table
about publishers while reading as a result about vocabulary.

**Short passages rather than payload.** The template asks for one to three
sentences, under roughly sixty words, in the community's voice. Full text stored
locally would still need a selection step, and choosing the passage that
represents how a community talks is a judgment rather than an extraction.

**A concepts file that is an answer key.** Each concept carries `term`,
`naive_question`, and `owning_community`. The load-bearing measurement ranks the
owning community's documents under three query forms to show that a constrained
definition routes to the owner that the naive question misses. `owning_community`
is what that is scored against. The code says so itself: without it a run prints
a banner declaring there is no answer key and the ranking is a demonstration
rather than a measurement.

**The convergence is looser than it was first reported.** An earlier reading of
this survey claimed that the probe's payload finding and astrakhantsev's text
requirement were two independent lines of evidence landing on the same gate. They
are not the same gate. The probe's problem is acquisition, whether bytes can be
got at all. astrakhantsev's requirement is curated passages, partitioned by
discourse community, with a hand-authored concept answer key. The two share one
necessary condition and are not the same condition. Payload is a gate on the
road, not the gate at the end of it.

## A conjecture about foreign methods generally

The method this repository could host most cleanly is the one whose input it can
least supply, and the method whose input it comes closest to supplying cannot be
hosted at all under the standard-library rule.

Only ReticleWorks would satisfy that rule: `crux_extractor.py` imports `re` and
`typing` and nothing else, and it is the one wanting reviewer-panel output.
laihsienhao needs pydantic and yaml. astrakhantsev needs numpy, scikit-learn,
and sentence-transformers pulling torch at roughly 2.5 GB, and it is the one
closest to the journal. SimonSkade1's runner is standard library but its graph
exists only because agents wrote it.

**Conjecture.** A method that operates on text carries heavy dependencies,
because comparing text requires embedding machinery. A method that operates on a
graph carries almost none, because the hard part was done upstream by whoever
built the graph. If that holds, the dependency weight of a foreign method is a
proxy for how far upstream its input was authored, and a receiver-owned
substrate will keep finding that the methods it can host cheaply are the ones
that assume the most work has already happened.

This is a conjecture and not an observation about these five, and a single
counterexample kills it: a text-operating method with no dependencies, or a
graph-operating method that needs a heavy stack. Either would show the pattern
here is an accident of five repositories.

## What this does not establish

**Anything about the wider population.** Five of twenty-one submissions, and
they were selected by whether a license let us read and reuse them, not by input
shape. Selecting on license availability has no reason to be independent of what
a method consumes, and the direction of that bias is unknown. The survey
establishes what these five want and nothing about the other sixteen.

**That the three claim-graph methods are interchangeable.** They were read for
input shape only. Their vocabularies differ and nothing here compares what they
compute.

**That astrakhantsev would work if the three gaps closed.** It was not run. The
gaps were read out of `load()`, the corpus template, and the scoring path.

## A licensing note on SimonSkade1

Recorded as found. The only license file is `LICENSE.txt`, reading
`Copyright (c) 2021 jackyzha0`, which is the license of Quartz, the static site
generator the repository is a fork of. `package.json` declares MIT for the same
inherited reason. Nothing separately licenses `content/v1/pipeline/`, which is
the actual method. Treating that pipeline as MIT would mean relying on a license
file naming a different holder for a different work.

He stays off any list of MIT-licensed methods until he answers.
