# Smart Thermostat v2 (test project for CRA Sentinel)

A made-up product for trying CRA Sentinel. The code is a stub; what matters are the dependency files,
which pin old versions with publicly known vulnerabilities, and how the code uses (or doesn't use) them.
Never install or deploy these dependencies.

| Part | File | Ecosystem | Examples |
|---|---|---|---|
| Web UI | `web/package-lock.json` | npm | jQuery 3.4.1 (CVE-2020-11023, CISA KEV), lodash 4.17.15, minimist 1.2.0, axios 0.21.0 |
| Cloud backend | `backend/requirements.txt` | PyPI | PyYAML 5.3, Pillow 8.0.0 (libwebp CVE-2023-4863, KEV), Django 3.2, requests 2.19.0 |
| Device bridge | `firmware-bridge/pom.xml` | Maven | log4j-core 2.14.1 (Log4Shell, KEV), commons-collections 3.2.1 (KEV) |
| Device firmware | `../thermostat-fw-1.0.0.bin` (next to this folder) | binary | Linux 4.19.94, BusyBox 1.31.1, OpenSSL 1.1.1k, curl 7.68.0, Dropbear 2019.78, dnsmasq 2.80, lighttpd 1.4.55, zlib 1.2.11 |

The folder is a git repository with one commit, so Sentinel can make fix branches in it.

## 1. Scan the folder → reachability

Get started → product "Smart Thermostat", version "1.0.0" → Scan a project folder → pick this folder.
After matching, Sentinel checks which vulnerable code the product really uses. Expect roughly:

- **called**: PyYAML (`yaml.load` in `backend/app/main.py`)
- **used**: axios, lodash (imported in `web/src/index.js`), follow-redirects (pulled in by axios),
  log4j-api/log4j-core (imported in `Bridge.java`; core is log4j-api's runtime)
- **not called**: lodash advisories naming functions the code never calls (e.g. `template`)
- **not used**: jQuery, minimist, moment, Django, requests, Pillow, urllib3, Jinja2, cryptography,
  jackson-databind, commons-collections

As an approver, accept the high-confidence proposals: those findings become VEX not_affected
(code_not_reachable) with the evidence in the note.

## 2. Fix plan → fix branch

Version page → Fix plan → tick upgrades → Create fix branch. Sentinel edits requirements.txt,
package.json (+ package-lock via npm) and pom.xml in a separate worktree, commits to
`sentinel/fix-…` and leaves your checkout alone. There is no remote, so the branch stays local.
To simulate the merge:

    git merge sentinel/fix-<name>-<timestamp>

Then "Check for merges now": Sentinel scans the merged code as the release version you entered and
proposes the fix-available date on the incidents it fixes.

## 3. Firmware image

New product (e.g. "Thermostat firmware", version "1.0.0") → Analyse a firmware image →
`thermostat-fw-1.0.0.bin`. Sentinel unpacks the gzip kernel and the SquashFS root filesystem, finds the
components above with confidence levels, and matches them against NVD (a minute or two: NVD's free API
allows 5 lookups per 30 s). The binaries in the image are fake stubs that only carry real version strings.
