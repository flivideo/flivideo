---
created: 2026-11-02
timestamp: 2026-11-02T14:00+07:00
---
# Brief: self-signed code-signing identity for Snappy on the M4 (2026-11-02)

**From:** `flivideo-orch` (Swagger). **To:** `snappy-signing-work`. Report to `flivideo-orch` by name.
**Go:** David, 2026-11-02: "And I want self-signed." / "GO".

## Why
macOS ties Snappy's Screen Recording permission to the app's code signature. Ad-hoc signing gives a new identity
(cdhash) on every build, so the grant is lost every rebuild. A self-signed certificate gives a stable identity.
Background: `/Users/davidcruwys/dev/ad/brains/swift-macos/toolchain-and-signing.md`.

## Do (on this machine, mac-mini-m4, in David's login keychain)
1. Check first: `security find-identity -v -p codesigning` and `security find-certificate -a -c "AppyDave Local Code Signing"`
   — if one already exists, STOP and report; do not create a duplicate.
2. Create a self-signed certificate named **"AppyDave Local Code Signing"** with the Code Signing extended key usage
   (`openssl` with `extendedKeyUsage=codeSigning`, `keyUsage=digitalSignature`, 10-year validity), import the key + cert
   into the login keychain, allow `/usr/bin/codesign` to use the key.
3. If macOS needs the cert trusted for code signing, use `security add-trusted-cert -p codeSign` for that cert only.
   **Any password / Touch ID prompt is David's** — say plainly in this window what is prompting and why, and wait.
4. Prove it works: build a tiny throwaway Swift command-line binary in a temp dir, sign it with the identity, rebuild with
   one changed line, sign again, and show that `codesign -d -r- <binary>` gives the **same designated requirement** both
   times (certificate-based, not cdhash). Delete the throwaway.
5. Never write the private key or any p12/password into a repo or a brain. Temp files go under `$TMPDIR` and are deleted.
6. Record the identity name, how it was made and the proof (no secrets) in
   `/Users/davidcruwys/dev/ad/brains/swift-macos/toolchain-and-signing.md`, commit only that file, push.

## Limits
- This machine only. Do not touch the M2 or Roamy. Do not install Xcode (David is doing it from the App Store).
- Do not change any other keychain item, trust setting or system setting. Do not run the Snappy spikes.
- STOP after step 6 and report the identity name + the two identical designated requirements.
