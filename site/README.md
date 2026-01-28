# AFGC Registry Site

This is the public-facing website for the AI Fiduciary Governance Certification Registry, built with [Astro](https://astro.build/).

## Development

### Prerequisites

- Node.js 20 or higher (see `.nvmrc`)
- pnpm package manager

### Local Development

```bash
# Install dependencies
pnpm install

# Start development server
pnpm dev

# Build for production
pnpm build

# Preview production build
pnpm preview
```

## Deployment

This site is configured for deployment on Cloudflare Pages with the following settings:

- **Root directory:** `site`
- **Build command:** `pnpm install --frozen-lockfile && pnpm build && cp -r ../registry ./dist/registry`
- **Output directory:** `dist`
- **Node version:** 20 (from `.nvmrc`)

The build process:
1. Installs dependencies with pnpm using the frozen lockfile
2. Builds the Astro static site
3. Copies the registry data from the parent directory into the output

## Project Structure

```
site/
├── src/
│   └── pages/
│       └── index.astro      # Homepage
├── functions/               # Cloudflare Pages Functions
│   └── api/
│       └── lead.ts          # Lead capture API endpoint
├── astro.config.mjs         # Astro configuration
├── package.json             # Dependencies and scripts
├── pnpm-lock.yaml           # Locked dependency versions
└── tsconfig.json            # TypeScript configuration
```

## Registry Data

The registry data (JSON files and documentation) is copied from the parent `registry/` directory during the build process and served at `/registry/` on the deployed site.
