# Password manager: 1Password

Decided by Garrett in chat, Nov 24, 2026. Replaces the Bitwarden pick in the S1 setup guide (Project doc `lab-setup/2026-11-21-s1-setup-guide.md`, Nov 21).

| Decision | Reason |
| --- | --- |
| The lab uses 1Password, with lab logins, keys and recovery codes in a separate vault named "Uncle Buck's Laboratory" | Garrett already uses 1Password personally. One password manager is simpler than two |
| When the LLC exists, the lab vault moves to 1Password Business or the Teams Starter Pack, billed to the LLC | Same hand-off the Bitwarden plan had: the lab's vault becomes the LLC's |
| The `lab-hq squad evals` Anthropic API key is stored in the lab vault and in lab-hq's `ANTHROPIC_API_KEY` Actions secret, and nowhere else | GOVERNANCE.md: secrets live in Actions secrets and the lab vault, never in files or chat |

Done Nov 24: account, lab vault, browser passwords imported, API key stored. Two-step login and the Emergency Kit were confirmed the same night. Still open in S1: setup-guide steps 2-8.
