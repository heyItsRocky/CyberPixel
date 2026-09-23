# CyberPixel

> **Minecraft x TryHackMe x Story Mode**
> A multiplayer cybersecurity learning platform disguised as a Minecraft game.

You don't study cybersecurity. You *live it* — inside Minecraft.

## What is this?

CyberPixel is a Minecraft server where players learn real-world cybersecurity by playing through it. Players control **p0**, a clone who wakes up in a broken world with one question: *"Why do I exist?"* Every locked door is a firewall, every enemy is a running process, and every secret is encrypted — to progress, you hack your way forward.

## Platform

| Component | Version |
|-----------|---------|
| Minecraft (Java) | 26.1.2 |
| Mod Loader | Fabric 0.19.x |
| Fabric API | 0.155.2+26.1.2 |
| Java | 25 |

## Core loop

```
Explore → Scan (Focus) → Find Terminal → Complete cybersec challenge → Unlock next area → Repeat
```

- **Terminal Stations** (Waylandcraft): a real Linux shell inside Minecraft — run `nmap`, analyze captures, write rules
- **The Focus** (Re:Entity Outliner + Jade): scan device that highlights threats and interactive objects through walls
- **NPCs** (Easy NPC): story, quests, traders, and technical mentors
- **The Hacker's Path**: milestone-based progression with branching nodes, skill mastery, and a reforge loop (inspired by Dauntless's Slayer's Path)
- **CyberSkill Tree**: spend Skill Points across Offensive / Defensive / Recon branches for potion-effect abilities

## Curriculum (9 levels)

| # | Topic | Zone |
|---|-------|------|
| 1 | Linux Basics | Cloning Lab |
| 2 | Nmap & Scanning | Network Corridor |
| 3 | Phishing & Social Engineering | Phishing Tower |
| 4 | Wireshark & Packet Analysis | Packet Swamp |
| 5 | Ransomware & Insider Threat | Ransomware Bunker |
| 6 | SQL Injection | SQL Ruins |
| 7 | Rootkits | Rootkit Depths |
| 8 | ARP Poisoning & MITM | ARP Poisoning Arena |
| 9 | Snort IDS | Snort Fortress |

Post-launch plans cover IoT, blockchain, cryptography, web, mobile, and cloud security (levels 10–15).

## Mod stack

**Core:** Fabric API, Waylandcraft, Easy NPC, FTB Quests, FTB Ranks  
**Performance:** Sodium, Lithium, FerriteCore, Entity Culling  
**Exploration:** JourneyMap, Re:Entity Outliner, Jade  
**Infra:** LuckPerms, KubeJS

See [CyberPixel.md](CyberPixel.md) for the full design document — story, progression system, skill trees, NPCs, control room, curriculum details, directory structure, and open questions.

## Project structure

```
CyberPixel/
├── server/        # Fabric server, mods, configs, scripts, datapacks
├── maps/          # Pre-built worlds (lobby + 9 levels + control room)
├── assets/        # Textures, models, sounds, lang
├── docs/          # Setup, player/admin guides, curriculum, API docs
├── tools/         # Challenge tester, map validator, debug tools
└── .github/       # CI workflows
```

## Docs

- [Full design document](CyberPixel.md)
- `docs/setup.md` — server setup guide *(coming soon)*
- `docs/player-guide.md` — player onboarding *(coming soon)*
- `docs/admin-guide.md` — control room manual *(coming soon)*
