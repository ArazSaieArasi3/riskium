# N5a: full candidate and source-pinned publication path

This stage prepares the coordinated v0.3.10 candidate. It does not create a tag/release, merge main, deploy Pages, write native Wiki or close #85.

## Candidate contract

- Preserve scientific model 0.3.2, article 7.2.21, N4 receipts and all historical experiment oracles.
- Select eight current component roles and 38 retained predecessor component records. Modified historical scheduler bytes are retained through exact aliases; the frozen v0.3.9 selection is not edited.
- Compose reader 0.4.10 and review 0.2.0 with all twenty maintained guides and the historical native Wiki References body. Preserve every prior release snapshot byte.
- Source-pin legacy read-only CI to the already verified main `3ce6f5573e2e0a698591615a7ded75c2f9451444`. Disable legacy jobs with write authority. Keep current-source qualification and six-asset packaging in their separate read-only workflow. Original oracle commands and frozen recipes are not rewritten to accept successor data.
- Reconstruct the predecessor reader and compare it to its archived actual-body receipt; distinguish this from new HTTP observations. The [native Wiki observation](wiki-observation.json) separately confirms the existing predecessor bodies and supplies its retained historical reference.
- Build the complete candidate twice, compare bytes, qualify internal links and paired source/HTML/Wiki text, then test and freeze six source-bound assets. A standalone offline verifier reconstructs the pinned Git commit/tree and checks current and historical component/evidence roles.

**N5a is DONE within its prepared-candidate scope.** [CI run 42890784207](https://github.com/ArazSaieArasi3/riskium/actions/runs/42890784207) qualified and packaged the clean exact source `073f22cbe15be32294d498eb6b300cb31a6584f0`. Both jobs and both artifact uploads passed. The 20 documentary, nine composition/history and seven package contracts passed (36 total). Two builds reproduced 1,022 files: a 908-file site and 114 native Wiki files, including twenty maintained guides and one historical reference. All 111 source/HTML/Wiki body pairs agree. The selected HTML bodies expose 16,308 verified local routes/anchors and Wiki exposes 2,803. All 406 prior snapshot files retain their exact bytes.

The actual CI ZIPs were downloaded and their archive digests matched authenticated artifact metadata. The independently invoked offline verifier then checked all six downloaded package assets, reconstructed the full 2,450-file Git source tree, and checked 1,392 selected bindings, eight active roles and 38 retained predecessor component records. The downloaded complete candidate was also rechecked. Artifact transport omits hidden files by default: the one declared empty `.nojekyll` build marker was restored under its exact empty-content digest; no documentary body was synthesized. N5b must preserve this explicit transport step when materializing the publication artifact.

Evidence: [CI qualification](ci-qualification.json), [test transcript](ci-tests.txt), [CI and artifact receipt](ci-receipt.json), [CI package verification](ci-package-verification.json), [independent downloaded-package verification](downloaded-package-verification.json), [downloaded-candidate verification](downloaded-composition-verification.json), [six asset identities/checksums](assets.json) and [progress](progress.json). The initial packaging attempt's test-runner naming error and its corrected successful source/run remain recorded in the receipt; it is not relabeled successful.

All 72 preparation files and two corrected files were fetched from Git and byte-verified. The successor receipt only adds evidence and updates status/planning documentation; all 1,392 qualified selected inputs remain unchanged. The candidate checks 31 routed schedulers and disables fifteen legacy write jobs **on the candidate branch**. This is not a claim that all legacy workflows were freshly rerun or that the routing has already been integrated into main. Main, published v0.3.9 and article 7.2.21 remain unchanged. No new ontology-engine, independent expert or operational result is asserted; #85 remains open for N5b, while #78 and #23 retain their own scopes.

## N5b handoff

Use the successful exact-source CI artifacts, their run IDs/digests and six verified asset checksums. Integrate that source through the repository's accepted merge path; create the new release/tag without replacing predecessor assets. Verify all public downloads against the pinned source/run, then qualify the finite live-status delivery adapter and publish the matching Pages/native Wiki bodies. Retain unrelated guides and historical references. Independently read back actual body bytes, navigation and maintained pointers. Only then close #85 within its own criteria. #78 exact normative adoption and #23 independent interpretation remain separately open.

The proposed later bounded database/generative pilot and pharmaceutical migration are not prerequisites for this documentation release.

## Reproduce the prepared source

Start from the pinned qualified source commit and keep generated output outside the checkout. Install `tools/releases/v0310/requirements-n5a.txt` and `tools/requirements-shacl.txt`, then run:

```sh
python -B tools/releases/v0310/selection.py --check
python -B tools/releases/v0310/routing.py --check
python -B tools/releases/v0310/qualify_n5a.py --mode LOCAL --commit FULL_CHECKOUT_COMMIT --output /tmp/riskium-n5a-new
python -B tools/releases/v0310/package/build_package.py --mode local-preflight --qualification /tmp/riskium-n5a-new/qualification.json --output /tmp/riskium-v0310-assets-new
python -I tools/releases/v0310/package/verify_package.py --assets /tmp/riskium-v0310-assets-new --expected-source-commit FULL_CHECKOUT_COMMIT
```

Use new empty output destinations and replace `FULL_CHECKOUT_COMMIT` with the independently checked complete SHA. LOCAL preparation is not CI evidence. For downloaded CI assets supply the independently observed qualifying workflow run through `--expected-run-id` as well.
