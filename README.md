# Horizon OS

Horizon OS is an installable Debian-based gaming system for VirtualBox and x86-64 PCs. It boots directly into a controller-style shell, includes first-run device setup, real Supabase accounts, profiles, a Store, and playable bundled games.

## 1. Create the repositories

Create a public GitHub repository named `horizon-os` under **osnide042** and upload this entire project to it. The account site will deploy to:

`https://osnide042.github.io/horizon-os/`

## 2. Create Supabase (about five minutes)

1. Create a free project at Supabase.
2. Open **Project Settings → API**.
3. Copy the Project URL and publishable/anon key.
4. In the GitHub repository, open **Settings → Secrets and variables → Actions**.
5. Add `SUPABASE_URL` and `SUPABASE_ANON_KEY`.
6. In Supabase **Authentication → URL Configuration**, set Site URL to `https://osnide042.github.io/horizon-os/` and add the same URL as a redirect URL.

The anon/publishable key is designed for client applications. Never put the Supabase service-role key in this repository.

## 3. Publish the account page

Open **Settings → Pages**, set Source to **GitHub Actions**, then run the `Deploy account site` workflow. The page supports real email/password signup and login.

## 4. Build the ISO

Open **Actions → Build Horizon OS ISO → Run workflow**. When it finishes, download `Horizon-OS-amd64` from the workflow Artifacts section and extract `Horizon-OS-amd64.iso`.

## 5. VirtualBox

1. Create a Linux/Debian 64-bit VM with 4 GB RAM, 2 CPUs, 32 GB disk, EFI disabled initially, and 128 MB video memory.
2. Attach `Horizon-OS-amd64.iso` to the virtual optical drive.
3. Boot and choose **Horizon OS Live** to test it or **Graphical Install** to install it.
4. Complete the Debian disk step, restart, remove the ISO, and follow Horizon Setup.

VirtualBox is suitable for setup and lightweight games. Modern 3D games need installation on physical hardware because VirtualBox does not provide normal gaming-class GPU acceleration.

## Architecture

- Debian Live Build creates a real hybrid boot/install image.
- LightDM automatically opens the Horizon session.
- Chromium runs the local Horizon shell in kiosk mode.
- A localhost-only Python service manages game packages and device state.
- Supabase provides real account authentication.
- GitHub Pages hosts the account-creation page.

## Security notes

- Game packages must use HTTPS and should include a SHA-256 hash before production release.
- The local service listens only on `127.0.0.1`.
- Supabase Row Level Security should be enabled before adding cloud profiles, friends, purchases, or saves.
