# Publishing the explorer

Repository: https://github.com/subhanjandas/banking-model-atlas

The foundation checkpoint is already on main. The explorer workflow runs Python metadata checks, TypeScript compilation, unit tests and Chromium interaction checks before uploading a static Pages artifact. Deployment depends on that successful build.

## One-time GitHub Pages setting

In the repository, open **Settings → Pages → Build and deployment → Source**, and select **GitHub Actions**. GitHub requires this setting before a custom Pages workflow can deploy. The current connector cannot modify Pages administration settings, and the workflow deliberately does not request a personal access token.

After enabling Pages, rerun the failed deployment job from the latest **Explorer checks and Pages** run, or run the workflow again from Actions. A successful deployment records the actual URL in its environment output. Do not treat an expected URL as evidence that the site is live.

The expected project path is `/banking-model-atlas/`. Vite builds relative asset paths, and browser tests serve the production bundle at that same subpath. Query-string links work without a server-side router or a 404 fallback.

## Local use

```bash
npm ci
npm run dev
```

For the production bundle, run `npm run build` and `npm run preview`. No secrets or external data are required.
