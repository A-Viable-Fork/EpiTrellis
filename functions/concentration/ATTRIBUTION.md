# Attribution

Vendored 2026-08-14.

**Upstream.** https://github.com/kyaloeric/epistemic-stack

**Commit.** `89d6632abd0b7678b738b722547d17b984fe1014`

**Files vendored, byte for byte.**

| Path here | Path upstream | sha256 |
|---|---|---|
| `vendor/src/concentration.py` | `src/concentration.py` | `3848b8af2c77675ed6a9ba6fac9f66f47f01a6dc7dc3515cc0fe687efca1c077` |
| `vendor/src/warrant.py` | `src/warrant.py` | `c2160f3e62649336ef8b0d4ac10d18141fc7d0dbcd82926b7e9ffa461cfa1e98` |
| `vendor/src/__init__.py` | `src/__init__.py` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (empty file) |

Nothing else was taken. Both modules import only `json`, `os`, `collections`
and `math`, so the upstream `requirements.txt` describes the rest of that
repository and not what is vendored here.

**License.** MIT. `LICENSE` in this directory is the upstream root `LICENSE`
copied unchanged, Copyright (c) 2026 Eric Kyalo. Upstream carries no per-file
headers, so the root file is what covers `src/`. The wrapper `run` in this
directory is a separate work under Apache-2.0, and it links to nothing: the
vendored method is imported into the wrapper's own process, and the wrapper as a
whole is invoked by the loader as a subprocess.

**The package path is load-bearing.** `warrant.py` contains
`from src.concentration import concentration_for, circular_support_flags` at
module level. The upstream directory layout is preserved as `vendor/src/` and
the wrapper puts `vendor/` on `sys.path` so that import resolves untouched.
Flattening the files into `vendor/` and editing that import line would be the
one repair that destroys the experiment.

**What the method does.** Given a typed claim graph, it measures how much of a
conclusion's evidential support rests on a single load-bearing claim.
`concentration_for` walks support edges backward from a conclusion with a decay
factor, folds the support of any claim into the upstream claim it declares a
`depends_on` relation to so that shared roots absorb apparently independent
support, and reports both the top claim's share and a Herfindahl
numbers-equivalent it calls the effective number of independent supporting
claims. `circular_support_flags` runs Tarjan's algorithm over the support edges
to find groups of claims that prop each other up, and separates loops that also
rest on something outside themselves from loops that ground in nothing.
`warrant.assess_graph` bundles those together with a crux ranking that scores a
claim by its support share times `log2(1 + supporters)`, so that carrying all of
a one-claim conclusion cannot outrank carrying a quarter of a large one. It is
deliberately deterministic and calls no model.

**Verified to run.** Against upstream's own `eggs` case graph, 202 claims and
220 edges, the vendored copy returns 39 concentration results, 10 cruxes and 2
circular-support flags. Against `blackholes`, 157 claims and 363 edges, it
returns 21, 10 and 1. The copy here is functional, which is what makes the empty
result over our own journal a fact about the journal rather than about the
vendoring. See `GAP.md`.
