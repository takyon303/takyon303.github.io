# takyon.online

Personal site for **takyon303 (Mia Takyon)**. Plain HTML + CSS, no JavaScript.

## Files

```
index.html      the page (all content lives here)
css/style.css   all styling, organised by section
favicon.svg     the little icon in the browser tab
robots.txt      crawler / scraper rules
sitemap.xml     single-page sitemap
CNAME           points GitHub Pages at takyon.online
.nojekyll       tells GitHub Pages to serve files as-is
```

## Updating content

The page is laid out as terminal output: each block is a `<section class="entry">` with a
command `<h2 class="cmd">` and the lines below it. The `$` prompt is drawn by CSS, so you only
type the command name.

- **Identity / age / study** → the `whoami` section.
- **Interests** → the `interests` section, one line per area.
- **Coding** → the `coding` section.
- **Current work** → the `work` section, one line per project.
- **Contact** → the `contact` section's `.links` line. Each platform is one `<a>` tag, all on
  a single line. The Discord link has a placeholder ID
  (`https://discord.com/users/000000000000000000`) — replace the zeros with your own Discord
  user ID.
- **Command names** → the text inside any `<h2 class="cmd">` (e.g. rename `whoami`).
- **Add a block** → copy a whole `<section class="entry">` and edit it. Nothing else to wire up.

## Updating looks

Colours and the font stack live in the `:root { ... }` block at the top of `css/style.css`.
The scheme is intentionally just two colours: `--bg` (pitch black) and `--fg` (plain white).
Links are underlined, and invert to white-on-black on hover. The `$` prompt and the blinking
cursor are added with CSS `::before` / `::after` on `.cmd` and `.prompt`.

The font is **Iosevka**, loaded from the Fontsource CDN (jsDelivr) via the two `<link>` tags in
`<head>` — one for regular (400) and one for bold (700). Google Fonts doesn't carry Iosevka, so
jsDelivr's `@fontsource/iosevka` package is the host. To change weights, add/remove a
`https://cdn.jsdelivr.net/npm/@fontsource/iosevka/<weight>.css` link. To self-host instead (no
third-party requests at all), download the `.woff2` files from
`https://cdn.jsdelivr.net/npm/@fontsource/iosevka/files/` into `fonts/`, then replace the CDN
links with your own `@font-face` rules pointing at `fonts/`.

## Deploying to GitHub Pages

1. Create a repo named for the site, e.g. `takyon303.github.io` or `takyon.online`.
2. Push these files to the default branch:
   ```sh
   cd ~/Projects/takyon.online
   git init
   git add .
   git commit -m "initial site"
   git branch -M main
   git remote add origin git@github.com:takyon303/takyon.online.git
   git push -u origin main
   ```
3. Repo → **Settings → Pages** → Source: *Deploy from a branch*, Branch: `main` / `/ (root)`.
4. Repo → **Settings → Pages → Custom domain** → enter `takyon.online`.

### DNS for the custom domain

At your domain registrar, point the apex domain `takyon.online` at GitHub:

| Type  | Host | Value                 |
|-------|------|-----------------------|
| A     | @    | 185.199.108.153       |
| A     | @    | 185.199.109.153       |
| A     | @    | 185.199.110.153       |
| A     | @    | 185.199.111.153       |
| CNAME | www  | takyon303.github.io   |

Then in Pages tick **Enforce HTTPS**.

## Local preview

```sh
cd ~/Projects/takyon.online
python3 -m http.server 8000
# open http://localhost:8000
```

---

## About the anti-scraping measures (read this)

The `robots.txt` and the `<meta name="robots">` tags ask OpenAI, Anthropic, Google,
Microsoft/Bing, the Internet Archive and friends to stay away. **They are requests, not
locks.** Compliant crawlers honour them; a scraper that feels like ignoring them can.

More importantly, **GitHub Pages cannot enforce anything at the network level.** It only
serves static files, and it does *not* let you set custom HTTP response headers — so you
cannot block by `User-Agent`, and you cannot send an `X-Robots-Tag` header. Anything that
actually stops a bot has to run *in front of* the site. Two realistic options are below.

### What's already in place

- `robots.txt` — blocks the named AI crawlers, the Internet Archive (`ia_archiver`,
  `archive.org_bot`, `Archive-It`), Googlebot, Bingbot, Applebot, CCBot, Perplexity, etc.
- `<meta name="robots" content="noindex, nofollow, noarchive, nosnippet, noai, noimageai">`
  plus per-bot variants — a belt-and-braces "don't index, don't archive, don't train" signal
  (the `noai`/`noimageai` values are honoured by some crawlers, ignored by others).

### Option A — put Cloudflare in front (free, recommended)

This is the practical way to get real filtering without running a server.

1. Create a free Cloudflare account and add `takyon.online`.
2. Move your registrar's nameservers to the two Cloudflare gives you.
3. In Cloudflare DNS, recreate your records and set them to **Proxied** (orange cloud):
   | Type  | Name | Target              | Proxy   |
   |-------|------|---------------------|---------|
   | CNAME | @    | takyon303.github.io | Proxied |
   | CNAME | www  | takyon303.github.io | Proxied |
4. SSL/TLS mode → **Full**. (GitHub Pages has a valid cert, so Full works.)
5. Turn on **Security → Bots → Bot Fight Mode**.
6. Turn on **Security → Bots → Block AI Scrapers and Crawlers** (one toggle, blocks the big
   AI training crawlers at the edge).
7. For extra control, add a **Security → WAF → Custom rule**:

   - Field: `User Agent`  Operator: `contains`  Value (one rule, OR them):
     ```
     GPTBot OAI-SearchBot ChatGPT-User ClaudeBot Claude-Web anthropic-ai
     Google-Extended CCBot PerplexityBot Bytespider Amazonbot Applebot-Extended
     meta-externalagent ia_archiver archive.org_bot Archive-It
     ```
   - Action: **Block**.

Note: Cloudflare still lets Googlebot/Bing index you unless you block them in the rule above —
which the robots.txt already asks for, so this is where you'd actually enforce it.

### Option B — Anubis: can you use it on GitHub Pages?

**Not directly.** Anubis is a reverse proxy / HTTP middleware written in Go. It sits *in front
of* an origin server and issues a small proof-of-work challenge to suspicious clients. GitHub
Pages gives you no server to install it on and no way to run middleware, so you cannot host
Anubis *on* GitHub Pages.

You *can* run Anubis in front of the static files if you put a small box between the visitor
and the site. Roughly:

1. Stand up a VPS (e.g. a €4 Hetzner/Fly.io/Render instance) with `takyon.online` pointed at it.
2. Download the Anubis binary for your architecture from
   `https://github.com/TecharoHQ/anubis/releases`.
3. Point Anubis at your GitHub Pages URL as its *upstream*, in `/etc/anubis/anubis.conf`:
   ```json
   {
     "bind": ":8080",
     "difficulty": 4,
     "webrouter": {
       "upstreams": [
         { "host": "localhost", "port": 80, "weight": 1 }
       ]
     }
   }
   ```
   (or use the `TARGET` env var pointing at `https://takyon303.github.io`.)
4. Reverse-proxy Nginx/Caddy on ports 80/443 to Anubis on `:8080`, and let Anubis fetch GitHub
   Pages as its backend.
5. Keep Cloudflare in front for TLS and caching if you like.

This gives you the real Anubis challenge, but it means paying for and maintaining a server, and
it's honestly overkill for a one-page personal site. **Cloudflare (Option A) gets you ~90% of
the benefit for free, with nothing to run.** If your goal is specifically "no AI can read this
page," Anubis on a VPS is the strongest of these options — just know it can't live on GitHub
Pages itself.
