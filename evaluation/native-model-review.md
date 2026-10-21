# Native OntoUML model review

Riskium now has an [OntoUML exchange representation](../ontology/native/riskium.ontouml.json) conforming to schema 1.0.2. It preserves the current source design's identifiers, definitions, stereotypes, identity suppliers, relation ends, multiplicities and generalizations. The structured source model remains unchanged.

This stage establishes exchange compatibility, source fidelity and a bounded review of the listed design questions. It does not establish independent domain adequacy, complete language-rule verification, a GUI editor import, or HermiT/SHACL results.

## What the representation contains

| Source content | Exchange representation |
| --- | --- |
| 77 typed core concepts | 77 classes with their original IDs |
| One foundational anchor | One additional class, separately identified |
| Three optional catalog boundaries | Three notes, never core classes |
| 127 typed associations | 127 binary relations with 254 ordered end properties |
| Seven optional external bridges | Seven notes preserving endpoints and multiplicities |
| 66 generalizations | 66 directed generalization elements |
| 25 interpretation constraints | 25 notes explicitly identified as non-executable |
| 11 domains | 11 domain packages, plus the root and three supporting packages |

The exchange has 585 elements, including packaging, relation ends and notes. That serialization count is not a concept count or a test count. There are 78 class elements: 77 local typed classes plus the anchor.

## Design dispositions

The [decision register](native-review-decisions.json) contains examples, counterexamples and remaining evidence obligations for ten topics.

| Question | Disposition |
| --- | --- |
| Case versus documentary identity | Preserve the case kind and separate entry, scenario and result identities. Equal labels or scores create no equality rule. |
| InformationContent | Preserve the `abstract` stereotype. It classifies abstract informational entities; it is distinct from the `isAbstract` classifier flag. |
| Responsible and authorizing roles | Preserve both role hierarchies and their mediation context. The same agent can play these roles in different mandates. |
| Mandate identity | Preserve grounding, scope and validity distinctions. Neither participant equality nor assignment documentation alone creates a real mandate. |
| EvidenceItem | Preserve the contextual role of an information artifact and its incoming evidential-use relation. Source linkage does not establish truth or endorsement. |
| Vulnerability | Preserve intrinsic-mode typing and the exactly-one substantial-object bearer. The anchor remains a modeling anchor; a resolved OWL import is not asserted. |
| Broad artifact/version endpoints | Preserve them. Constraint-specific target coherence is implemented later, rather than globally narrowing ArtifactVersion. |
| Heterogeneous boundaries | Keep the three catalog notions and seven bridges outside the typed native model. |
| Actual events | Preserve Trigger as a RiskOccurrence specialization. Hypothetical scenario content does not establish an actual occurrence. |
| Generalization sets | Make the policy explicit, as described below. |

The native review profile adds ten generalization-set declarations that were not explicit in the source JSON. All ten are incomplete: no listed group is declared to exhaust its parent. Three identity-based sets are disjoint: Person/Organization, ResponsiblePerson/ResponsibleOrganization and AuthorizingPerson/AuthorizingOrganization. The other seven sets impose no blanket disjointness. A non-disjoint group does not assert that every sibling pair overlaps.

These declarations are a visible review-profile addition. The counts and field-preservation checks do not establish formal logical equivalence between the two representations. No concept, original association or generalization was renamed, removed or retyped to improve a check result.

## Checks actually performed

1. Python `jsonschema` 4.25.1 validated the exchange against the pinned official schema, including date, date-time and URI format checks. Schema errors: zero.
2. Source-fidelity checks compared the typed-class allocation, definitions, stereotypes, identity suppliers, ordered relation ends, cardinalities, inheritance, domain membership, boundary notes and declared set policy. Fidelity errors: zero.
3. The official `ontouml-js` 1.0.0 SDK directly parsed and serialized the exchange. All 585 elements and the checked source invariants survived the roundtrip. The SDK normalizes dates, empty metadata and nullable defaults; its output was not substituted for the canonical file.
4. Eleven native-export regression tests exercised lost bearer cardinality, reversed reading ends, changed identity supplier, abstract-stereotype/flag confusion, boundary promotion, reversed inheritance, unsupported covering, lost constraints, changed bridges and lost domain membership. Together with the previous suites, 32 engineering regression tests passed.

The [exchange receipt](native-exchange-checks.json) and [SDK roundtrip receipt](native-roundtrip-checks.json) retain the exact digests and boundaries of these checks.

## The legacy verifier result

An additional run used `ontouml-js` 0.4.1 through a separately documented object adapter. It produced 68 `class_missing_is_extensional` errors because legacy-only extensionality was deliberately left unknown. Schema 1.0.2 does not require that field. The current SDK roundtrip succeeded without it. These are retained as legacy compatibility findings in the [legacy report](native-sdk-checks.json); the model was not changed merely to remove them.

Inspection also showed that the legacy SDK's relation, property and generalization-set verification functions contain no implemented rules. A successful invocation of that verifier would therefore not prove full language conformance. The current schema, source-fidelity checks and SDK interoperability are reported separately from semantic and instance-level validation. Independent semantic review remains in issue #7; formal encoding and executable constraint tests remain in #3–#6.

Both SDK commands temporarily return an empty network-interface list for their generated-ID seed in this environment. All model IDs are supplied explicitly, and no serialization or verification rule is patched.

## Reproduce

Use Python 3.12 and Node 24, or record and evaluate a different runtime explicitly.

```sh
python3 -m venv .venv-native
.venv-native/bin/pip install -r tools/requirements-native.txt
curl -L https://raw.githubusercontent.com/OntoUML/ontouml-schema/7a0fe7ef7d4caea8d62f2782fb3681261a75f452/dist/ontouml-schema.json -o /tmp/riskium-ontouml-schema.json
python3 tools/build_native.py --check
.venv-native/bin/python tools/validate_native.py --schema /tmp/riskium-ontouml-schema.json
npm ci --prefix tools/native-sdk --ignore-scripts
node tools/check_native_roundtrip.cjs tools/native-sdk/node_modules/ontouml-js-current
node tools/check_native_sdk.cjs tools/native-sdk/node_modules/ontouml-js-legacy
python3 -m unittest discover -s tests -v
```

The schema checker rejects a digest different from the reviewed upstream file. The Python requirements and npm lockfile pin the environments used for these optional checks. No remote validation service receives the model.

The technical sources are the [official schema](https://github.com/OntoUML/ontouml-schema/tree/7a0fe7ef7d4caea8d62f2782fb3681261a75f452) and [official SDK serialization implementation](https://github.com/OntoUML/ontouml-js/blob/a0e44530564331cf17c850d659fae4b6adad4415/src/serialization.ts). The former defines exchange syntax; neither source makes the current Riskium model independently valid.
