# MR.ROBOT OS

MR.ROBOT Desktop is an installable, bloat-conscious Debian 13 desktop for VirtualBox and x86-64 PCs. It combines a minimal KDE Plasma workspace with MR.ROBOT's black-and-red identity, first-run setup, optional MR.ROBOT Network accounts, a privacy-configured browser, real file management and Steam integration.

## MR.ROBOT OS source

This is a rebranded source project based on the uploaded Horizon OS source. It is **not a prebuilt ISO**; build it using the included GitHub Actions workflow or Debian live-build environment. The original Horizon repository is not configured as this project’s remote in this ZIP. Review account/backend configuration before publishing.

## Main experience

- A normal desktop with taskbar, Start/Application menu, Super-key search, system tray, notifications, right-click menus, desktop files, Recycle Bin, window snapping and Alt+Tab.
- Dolphin is presented as the main file manager, with tabs, previews, archives, removable drives and normal create/copy/move/rename/delete operations.
- KWin provides hardware-accelerated transparency, blur, overview, glide, minimise and popup animations.
- MR.ROBOT Dark colours, an original MR.ROBOT wallpaper and a generated red cursor are applied by default.
- MR.ROBOT Setup opens on the first desktop launch. A MR.ROBOT Network login is optional; local use works without an online account.

## Included essentials

- MR.ROBOT Browser: Firefox ESR with telemetry, studies, Pocket, sponsored content and health-report uploads disabled by policy. Strict tracking features and Global Privacy Control are enabled.
- MR.ROBOT Files: Dolphin.
- Settings, terminal, text editor, archive manager and screenshot tool.
- A clean MR.ROBOT desktop with a floating glass dock, a native continuously animated Plasma wallpaper and smooth KWin effects.
- A MR.ROBOT Plymouth boot sequence with a glowing, 3D-flipping red MR mark.
- MR.ROBOT Browse with telemetry, sponsored content and tracking disabled by policy.
- An on-demand official Steam Flatpak. Games themselves are never bundled into the ISO.

MR.ROBOT does not claim that websites, an ISP or a signed-in service cannot observe traffic required to provide their service. The distribution disables its own telemetry defaults, but online privacy still depends on the sites and accounts a person chooses to use.

## Build the ISO

1. Create or update the public `YOUR-GITHUB-USERNAME/mr-robot-os` GitHub repository with this project.
2. In **Settings → Secrets and variables → Actions**, retain `SUPABASE_URL` and `SUPABASE_ANON_KEY` for optional MR.ROBOT Network features.
3. Open **Actions → Build MR.ROBOT OS ISO → Run workflow**.
4. Download the `MR.ROBOT-OS-amd64` artifact and extract `MR.ROBOT-OS-amd64.iso`.

## VirtualBox

Recommended test configuration:

- Debian 64-bit VM
- EFI enabled
- 8 GB RAM recommended (4 GB minimum)
- 4 virtual CPUs
- 128 MB video memory and VMSVGA
- 3D acceleration enabled
- 100–150 GB dynamically allocated disk for Steam games
- NAT networking

Boot the ISO and choose **Start installer**. MR.ROBOT pre-fills repetitive Debian questions while leaving the target-disk choice and final erase confirmation visible. After installation, remove the ISO and reboot.

VirtualBox is appropriate for desktop testing and light games. Modern 3D Steam games generally require installation on physical hardware with supported graphics drivers.

## Architecture

- Debian Live Build produces the bootable hybrid ISO.
- SDDM starts the MR.ROBOT Desktop Plasma session.
- KDE Plasma supplies mature desktop, search and file-management behavior.
- Firefox ESR supplies a maintained browser engine under MR.ROBOT privacy policy defaults.
- The localhost-only MR.ROBOT service handles device state, optional setup integration and Steam App-ID actions.
- Flatpak supplies the official Steam client on demand.
- Plymouth supplies the MR.ROBOT startup animation.

## Privacy and security

- No MR.ROBOT advertising ID or analytics endpoint.
- MR.ROBOT Network is optional.
- Browser telemetry, experiments and sponsored home content are disabled.
- The local MR.ROBOT API listens only on `127.0.0.1`.
- Supabase Row Level Security must remain enabled for public account data.
- The Supabase service-role key must never be placed in this repository or ISO.
