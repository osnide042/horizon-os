# Horizon OS

Horizon OS is an installable Debian-based gaming system for VirtualBox and x86-64 PCs. It boots directly into a controller-style shell and includes first-run setup, Supabase accounts, local profiles, and a Steam-powered Horizon Store. No games are preinstalled.

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

The workflow installs the current official Debian Live Build source over Ubuntu's older packaged copy so current Trixie repository metadata is understood. The prototype also disables the obsolete security-mirror entry generated during host bootstrapping; before production, move the entire workflow into a current Debian build container and explicitly enable `trixie-security`.

## 5. VirtualBox

1. Create a Linux/Debian 64-bit VM with 4 GB RAM, 2 CPUs, at least a 64 GB disk, EFI enabled, and 128 MB video memory.
2. Attach `Horizon-OS-amd64.iso` to the virtual optical drive.
3. Boot and choose **Live system** only for a quick test. Choose **Start installer** before installing Steam, Minecraft, Netflix or games—the temporary Live filesystem is too small and is erased at shutdown.
4. Horizon now fills in the repetitive language, network, domain, mirror, proxy, root-account and layout questions. Choose the target disk, create the local administrator password, confirm formatting, then restart and remove the ISO.
5. Installed launches hide the GRUB menu and show the animated blue-purple Horizon startup screen. VirtualBox's own firmware logo appears before the guest starts and cannot be replaced by an ISO.

VirtualBox is suitable for setup and lightweight games. Modern 3D games need installation on physical hardware because VirtualBox does not provide normal gaming-class GPU acceleration.

### Increase VirtualBox storage before installation

Power off the VM. In VirtualBox open **Tools → Media**, select `Horizon OS.vdi`, increase its virtual size (80–100 GB is recommended for games), and apply. Then start the ISO installer and let Debian use the whole virtual disk. If Horizon has already been installed, the partition and filesystem must also be expanded inside the guest.

## Architecture

- Debian Live Build creates a real hybrid boot/install image.
- LightDM automatically opens the Horizon session.
- Chromium runs the local Horizon shell in kiosk mode. Netflix uses a dedicated full-screen Google Chrome app window for supported protected playback.
- Horizon Store contains real free-to-play Steam games rather than Horizon-made demo games. Install, ownership, downloads and updates are handed to the official Steam client using each title's Steam App ID.
- A localhost-only Python service manages Steam launching, Flatpak apps and device state.
- Netflix and YouTube open as dedicated full-screen app windows rather than ordinary browser tabs. Netflix still uses Chrome internally because its protected video playback requires a supported browser engine.
- The app guard closes Netflix and YouTube with Escape. The PlayStation PS button or Xbox Guide button closes the active external app when Linux exposes it as `BTN_MODE`.
- Debian's `steam-devices` rules are built into Horizon for Steam, Xbox, PlayStation, Nintendo and compatible controller access.
- Supabase provides real account authentication.
- GitHub Pages hosts the account-creation page.

## Security notes

- Game packages must use HTTPS and should include a SHA-256 hash before production release.
- The local service listens only on `127.0.0.1`.
- Supabase Row Level Security should be enabled before adding cloud profiles, friends, purchases, or saves.
