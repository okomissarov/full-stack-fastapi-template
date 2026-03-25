# Workshop Preparation — Please Complete Before the Session

Hi team,

Please complete the following setup steps before the workshop. This should take about 15-20 minutes.

---

## 1. Verify Access

You've been granted access to the following. Please verify you can reach each one:

- [ ] **GitLab:** https://gitlab.dataart.com/da/dalf — you should see the DALF repositories
- [ ] **GitHub:** https://github.com/okomissarov/full-stack-fastapi-template — public workshop repo
- [ ] **JIRA:** https://support.dataart.com/browse/AWSP-114 — Time Tracking epic in AWSP project

If any access is missing, let me know before the workshop.

---

## 2. Install Prerequisites

### Python 3.10+

macOS:
```bash
brew install python
```
Windows:
```bash
winget install Python.Python.3
```
Linux:
```bash
sudo apt update && sudo apt install python3 python3-pip
```
Verify: `python3 --version`

### Node.js 18+

macOS:
```bash
brew install node
```
Windows:
```bash
winget install OpenJS.NodeJS
```
Linux:
```bash
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install nodejs
```
Verify: `node --version`

### Git

Verify: `git --version`

---

## 3. Install Kiro CLI

Follow the official installation guide: https://kiro.dev/docs/cli/installation/

Quick install:
```bash
# macOS / Linux
curl -fsSL https://kiro.dev/install.sh | bash

# Windows — see https://kiro.dev/docs/cli/installation/
```

### Login to Kiro

```bash
kiro-cli login --region us-east-1 --start-url https://dataart.awsapps.com/start/#
```

This opens a browser for authentication. Log in with your DataArt credentials and authorize the access.

### Verify Kiro Works

Open your IDE (VS Code, or any terminal) and run:
```bash
kiro-cli --version
```

Or start an interactive session:
```bash
kiro-cli chat
```

Type `/quit` to exit.

---

## 4. Clone Repositories

### Workshop repo (GitHub):
```bash
git clone https://github.com/okomissarov/full-stack-fastapi-template.git
```

### AILA SDK (GitLab):
```bash
git clone git@gitlab.dataart.com:da/dalf/aila-kiro-home.git
```

If SSH doesn't work, try HTTPS:
```bash
git clone https://gitlab.dataart.com/da/dalf/aila-kiro-home.git
```

---

## 5. Quick Verification Checklist

Run through this checklist to confirm everything is ready:

- [ ] `python3 --version` → 3.10+
- [ ] `node --version` → 18+
- [ ] `git --version` → any
- [ ] `kiro-cli --version` → installed
- [ ] `kiro-cli login` → authenticated
- [ ] `cd full-stack-fastapi-template && ls workspace.py` → file exists
- [ ] `cd aila-kiro-home && ls AILA-SKILLS-BOOTSTRAP.md` → file exists
- [ ] Can access JIRA AWSP-114 in browser

---

If you run into any issues, reach out and we'll sort it out before the workshop.

**Workshop agenda:** https://github.com/okomissarov/full-stack-fastapi-template/blob/master/docs/workshop/agenda.md

See you there!
