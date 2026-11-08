# Explicit generalization-set policy candidate

Date: 2026-11-08. Status: isolated candidate **B0-2**, related to [#93](https://github.com/ArazSaieArasi3/riskium/issues/93). This packet builds on the [EvidenceItem dependency candidate](../issue93-evidence-use/README.md) at commit `b81549f2a9b139fef5feae57f3a2e2f8008b32a8`.

## Decisions and resulting behavior

| Focal set | Decision | Result |
|---|---|---|
| GS-RKM-C014, InformationArtifact | Omit the blanket set that groups documentary subkinds and contextual evidential participation. | Every original subtype edge remains. A register entry can also play an evidential role. No replacement set over all documentary subkinds is invented without a shared criterion. |
| GS-RKM-C047, Agent | Omit the blanket set that groups bearer kinds and mandate participation. | Person/Organization remain distinct under the separate AgentKinds set. A person can be responsible and authorizing under their respective mandates. |
| GS-AgentKinds | Retain the explicit bearer-kind criterion, disjoint and incomplete. | The same individual is not both a human and an organization, while Agent is not closed to only these two kinds. |
| Other seven retained sets | Carry forward their existing policy unchanged. | Their broader semantic acceptance is outside this two-set repair; carrying them forward is not a new independent review. |

The candidate source contains an explicit `generalization_set_policy`. The native emitter reconstructs only its listed sets. It reuses the existing class/relation serializer, but does not accept automatically generated common-parent groups as the set policy. All classes, associations, constraints and 67 generalization edges from B0-1 are retained. Native packaging contains eight sets instead of ten.

This is a change to classification grouping, not a retyping of Person, Organization, documentary subkinds or roles. No global role disjointness or new covering constraint is added. The two omitted sets had both `isDisjoint=false` and `isComplete=false`; they introduced no OWL exclusion or covering axioms in the previous exporter. Accordingly, the logical OWL graph is preserved, apart from version/provenance metadata. The repair matters to the conceptual and native set policy even though it does not change the exported logical consequences. OWL consistency alone could not have diagnosed the mixed specialization criteria.

## Positive and negative checks

The [execution receipt](candidate-report.json) records:

- Exact preservation of source subtype edges, concepts, relations, constraints and the three retained disjointness decisions.
- Native fidelity to the explicit eight-set policy, including package references and the pinned OntoUML 1.0.2 schema.
- The selected GSRig trigger disappearing for the two repaired sets, with restoration mutants that recover each original trigger.
- HermiT checks for Person/Organization exclusion, legitimate responsible/authorizing overlap, documentary-subkind/evidence-role overlap, every declared subtype edge and the absence of an Agent covering axiom.
- Mutation controls for deleting a valid subtype edge, dropping bearer-kind exclusion and imposing unjustified global role exclusion.
- ROBOT OWL 2 DL profile conformance on this candidate output.

Example: one human participant can be a ResponsiblePerson and AuthorizingPerson under distinct grounded assignments. This does not turn that person into an Organization or make every Agent one of the two currently named bearer kinds. Likewise, a RiskRegisterEntry retains its documentary specialization when it is used as an EvidenceItem.

Counterexample: avoiding the GSRig trigger by deleting the EvidenceItem subtype edge would lose inherited identity. Avoiding it by making responsible and authorizing roles mutually exclusive would reject legitimate participation. Both changes are tested as unacceptable; a zero trigger count alone is not the acceptance criterion.

Other selected catalogue triggers, repeated-relator identity, independent conceptual acceptance, database mapping and full combined-candidate integration remain distinct work. No global semantic-correctness percentage or optimal modularization is inferred. HermiT 1.4.5.456 in this packet is a new candidate execution; manuscript 7.2.21 retains its original version-bound engine totals.

## Replay

Use the [B0-1 dependency versions and pinned schema/ROBOT hashes](../issue93-evidence-use/README.md#replay), then run from the repository root:

```sh
python evaluation/manuscript-review/v7.2.3/issue93-generalization-sets/verify_candidate.py --schema /tmp/ontouml-schema.json --robot /path/to/robot-1.9.11.jar
```

The builder writes generated model/native/OWL outputs in this packet and reconstructs the earlier isolated evidence-use projection as an input. It does not overwrite the B0-1 receipt. Generated RDF blank-node serializations can have different byte hashes on replay; the new receipt identifies its actual executed inputs.

## Promotion boundary and next step

The production model, current native/OWL/SHACL artifacts, database, published readers, historical receipts and article are unchanged. These two grouping repairs and the preceding EvidenceItem repair are implemented only in candidate packets. **B0-3 remains open:** review the combined candidate, rerun the affected integration checks, reconcile definitions and downstream mappings/readers, and report whether promotion is ready or identify its specific blocker. This packet does not close #93 or create a stable release.

The [OntoUML GSRig description and refactoring guidance](https://ontouml.readthedocs.io/en/latest/anti-patterns/GSRig/index.html), accessed 2026-11-08, inform the distinction between one specialization criterion and mere shared parenthood. The guidance does not independently validate the retained Riskium classification criteria.
