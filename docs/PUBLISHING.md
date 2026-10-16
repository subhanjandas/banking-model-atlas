# Publishing this checkpoint

Suggested repository: `subhanjandas/banking-model-atlas`.

The current GitHub connection can edit repositories but does not expose repository creation. No GitHub CLI authentication is available in the build environment. This package is ready to upload; no repository or website has been claimed as published.

## Smallest handoff

Create a public repository named `banking-model-atlas` on GitHub and initialize it with a README. If the GitHub connection only has access to selected repositories, include the new repository. Share its URL so the prepared checkpoint can be uploaded as a coherent commit.

Initializing the README gives the connector an existing branch and commit to build on. The prepared README will replace that initial placeholder.

## Upload from your Mac instead

If uploading yourself, create an empty repository without an initial README. Unzip the package, open a terminal in `banking-model-atlas`, run the checks in the README, then run:

```bash
git init -b main
git add .
git commit -m "docs: establish Banking Model Atlas foundation"
git remote add origin https://github.com/subhanjandas/banking-model-atlas.git
git push -u origin main
```

These commands assume a fresh extracted folder and an empty remote. Authenticate through your usual GitHub setup. Do not put tokens in repository files.

## Website publication comes later

The foundation does not contain a built website. A future GitHub Pages workflow should build the viewer, use the correct `/banking-model-atlas/` base path, run checks, and publish the static assets. Repository upload and website deployment are separate milestones.
