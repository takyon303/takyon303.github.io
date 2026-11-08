idk

bun run dev

or bun build to deploy ig

## Deploying to GitHub Pages

The site deploys automatically to https://takyon.online via GitHub Actions
(`.github/workflows/deploy.yml`) on every push to `main`.

Setup (one time):

1. Push this repo to GitHub as `takyon303/takyon303.github.io` (user repository, custom domain takyon.online)
2. On GitHub, go to Settings → Pages → set **Source** to **GitHub Actions**

To deploy manually, run the "Deploy to GitHub Pages" workflow from the Actions tab.
