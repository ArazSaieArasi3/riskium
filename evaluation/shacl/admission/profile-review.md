# Catalog metadata admission profile 0.3.0

## Decision and scope

This is an author implementation policy for child #17 of #5, not an independent semantic review. It resolves the scalar metadata vocabulary for the bounded catalog-inspection use of the 80 baseline admission rows. The unchanged source model is conceptual version 0.3.1. The exact policy, source and contract digests are in [profile-policy.json](profile-policy.json) and the generated profile receipt.

The profile describes an **information record about a candidate**, rather than imposing documentary fields on the candidate agent, object, event or other referent. The record and candidate are separate RDF resources, linked by `ap:candidate`. No class, scalar property or axiom is added to the conceptual model or OWL.

`ap:` denotes `https://github.com/ArazSaieArasi3/riskium/profiles/catalog/0.3.0#`. It is an application envelope namespace. `dct:` denotes `http://purl.org/dc/terms/`. These record locators are neither identity keys for domain objects nor evidence of source truth.

## Admission fields

| Record field | Managed catalog requirement | Interpretation |
| --- | --- | --- |
| Record identity | Named IRI | Operational record identity; not a proof of real-world identity. |
| `ap:candidate` | Exactly one named IRI | Resource represented by this record. Its explicit class or source subtype must match the external expected class. |
| `ap:declaredClass` | Exactly one of the 77 core class IRIs; equal to the external request | A data declaration cannot choose a weaker validation class. |
| `dct:title` | At least one nonblank string or language-tagged literal | Human-readable record title. Equal titles do not merge records. Multiple language labels are allowed. |
| `dct:subject` | At least one IRI | Explicit record subject/context locator; it does not substitute for required domain relations. |
| `dct:source` | At least one IRI | Source locator; existence, accuracy, authority and endorsement are separate review questions. |
| `ap:requestedTask` | Optional in managed catalog; exactly one supported task when task readiness is requested | Only `ap:CatalogInspection` is supported. Risk assessment, scoring and other tasks are rejected rather than silently accepted. |

## Profiles and external focus

- `raw` preserves incomplete and conflicting input with no identity normalization or admission constraints. Its conformance means staging only.
- `managed-catalog` validates the envelope and candidate type, not all domain relations or business rules.
- `task-catalog-inspection` adds an explicit CatalogInspection request. Its readiness means only that managed metadata can be inspected; it never means risk-assessment readiness.

Every call requires a nonempty external list of `(record, expected class)` pairs and a supported profile. A missing record in the input still receives targets and fails its required fields. Unknown requested classes, empty focus lists, unsupported profiles and incompatible expected classes for aliased records are configuration rejections before SHACL; they are not counted as engine passes. Records outside the declared external list are not claimed validated.

Effective shapes retain only the reachable requested class profiles. Their redundant class allowlist is restricted to the externally requested core classes, while each record also retains its exact expected-class `hasValue` rule. No rule is selected from the input's declared class. Three optional boundary declarations have no class-specific core profiles and fail the generic core allowlist under managed admission. They remain preservable in raw staging. Imported foundational anchors are not added to the catalog; relation integration checks their type separately.

Blank record resources cannot be SHACL `targetNode` values under the pinned meta-schema. A caller-added reserved `ap:focus-*` predicate therefore selects such a resource through `targetSubjectsOf`; the managed record IRI constraint then rejects it. Input-supplied focus-selector predicates are rejected, and the effective data snapshot records these caller additions.

## Identity, schema and inference

Managed profiles normalize only asserted named `owl:sameAs` closures and symmetrize `owl:differentFrom`, using the existing normalization policy. SameAs/differentFrom conflicts reject before SHACL. Equal labels are never identity evidence. Blank candidates and records remain visible and fail the managed IRI rule; they are retained raw. Independent real-world identity and provenance adequacy remain #7/#8.

Managed instance input cannot supply RDFS schema, OWL equivalence or import axioms. Identity assertions involving reserved model, application or RDF vocabulary IRIs also reject before normalization, so instance alias handling cannot rewrite a declared class or property. Append only the 66 subclass statements from the pinned source model. SHACL inference is `none`; no imported ontologies, domain/range type completion, anonymous OWL fillers or unique-name assumption supplies missing evidence. The three optional boundaries remain absent from typed core classes and their class-specific shapes.

## Fixtures, exact oracles and receipts

Every admitted core concept has positive managed and catalog-task examples, incomplete raw staging, missing identity/title/subject/source/type and unsupported readiness examples, datatype and blank-node cases, alias and equal-label controls, and omitted-rule mutation controls. Every supported source subtype is tested against its ancestor and reverse inheritance is rejected. All 127 typed relations combine both original endpoint shapes with participant admission metadata. Their imported foundational participants receive only separate type checks, never invented catalog profiles.

Every negative requires the exact `(source shape, constraint component, focus node)` set. Graph snapshots preserve blank-node labels within the receipt. Reconstruct data and shapes with the shared blank-node context in `reconstruct_pair()`; independent graph canonicalization could change shared target identity. Hashes identify serialized snapshots, not canonical RDF graph identity. Builder, engine, regression and pre-validation rejection counts are reported separately.

## What this batch closes

A PASS admission row establishes managed catalog metadata acceptance or explicit optional-boundary exclusion under this policy. It does not close the remaining 21 constraint rows, C-08 unit/scale compatibility, arbitrary risk-record admission, full multi-relation/conditional integration, scientific source adequacy, independent meaning review or CQ execution. Those retain their existing obligations in #5/#6/#7/#8/#12/#13. The 359-row baseline and prior frozen receipts remain unchanged.
