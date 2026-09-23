# CyberPixel

> **Minecraft x TryHackMe x Story Mode**
> A multiplayer cybersecurity learning platform disguised as a Minecraft game.

---

## What Is CyberPixel?

CyberPixel is a **Minecraft server** where players learn real-world cybersecurity by **playing through it**. Think Hypixel, but instead of PvP minigames, each game mode is a hands-on cybersec lab wrapped in a story.

**The pitch in one line:** You don't study cybersecurity. You *live it* — inside Minecraft.

---

## Platform

| Component | Version | Notes |
|-----------|---------|-------|
| **Minecraft** | 26.1.2 | Latest stable (Java Edition) |
| **Mod Loader** | Fabric | Fabric Loader 0.19.x |
| **Fabric API** | 0.155.2+26.1.2 | Required |
| **Java** | 25 | Minimum for 26.1 |

---

## The Story: p0

**p0** is a clone — a duplicate entity that woke up in a world she doesn't remember. No origin. No purpose. Just a question:

> *"Why do I exist?"*

She starts in a **cloning lab** (spawn area), breaks out, and journeys through a broken world — abandoned facilities, corrupted cities, hidden servers — searching for the answer.

Along the way, she discovers that **the world itself runs on code**. Every locked door is a firewall. Every enemy is a running process. Every secret is encrypted. To survive, she has to **hack her way forward**.

The story is told through:
- **Map environments** (custom builds + Mosslorn)
- **NPC dialogue** (Easy NPC mod)
- **Terminal stations** (Waylandcraft — real Linux terminal inside Minecraft)
- **Puzzle gates** (progress blocked until you solve a cybersec challenge)
- **The Focus** — a scan device that reveals hidden threats and interactive objects (Re:Entity Outliner + Jade)

**Inspiration:** Horizon Zero Dawn's environmental storytelling meets TryHackMe's hands-on labs.

---

## How It Works

### The Game Loop

```
Explore
  -> Hit a wall (locked door / corrupted system / NPC in trouble)
  -> Use your Focus to scan the area (Re:Entity Outliner highlights threats)
  -> Find a Terminal Station (Waylandcraft)
  -> Complete a cybersecurity challenge
  -> Unlock new area / get tools / advance story
  -> Repeat
```

### The Focus (Horizon Zero Dawn Mechanic)

p0 has a **Focus** — a scanning device inspired by Horizon Zero Dawn that reveals what the naked eye can't see.

**In-game implementation:**
- **Re:Entity Outliner** — press a keybind to highlight all entities through walls with colored outlines
  - Red = hostile threats (corrupted processes)
  - Yellow = neutral NPCs
  - Green = allies / quest givers
  - Blue = data streams / interactive objects
- **Jade** — look at any block/entity to see what it is, its health, and what it drops
- **Night Vision** (skill tree) — see in dark areas like the Focus's low-light mode

**How players use it:**
1. Enter a new area -> activate Focus to scan for threats
2. Identify which entities are hostile (red outlines) vs. safe (green/yellow)
3. Use Jade to inspect suspicious blocks for hidden terminal stations
4. Progression unlocks better Focus capabilities (wider range, more detail)

### Terminal Stations

Scattered throughout the map are **terminal stations** — in-game locations powered by Waylandcraft (a Wayland compositor running inside Minecraft).

Players open the terminal and get a **real Linux/CLI environment**:
- Type `nmap -sV 192.168.1.1` to scan a target
- Analyze a Wireshark capture to find the malicious packet
- Craft a phishing email template
- Identify which process is a rootkit

**Success = progression.** The door opens, the NPC gives you a tool, the next area loads.

### Multiplayer

- Hosted server (like Hypixel)
- Players join, pick a story chapter, and work through labs
- Can be solo or co-op (some challenges designed for teams)
- Leaderboards, achievements, and skill trees per player

---

## The Hacker's Path (Progression System)

Inspired by Dauntless's **Slayer's Path**, CyberPixel uses a milestone-based progression system with branching nodes, mastery tracks, and a reforge loop.

### Milestones (Main Progression)

Milestones gate the 9 levels. You must complete the previous level to unlock the next.

| Milestone | Title | Description | Unlocks |
|-----------|-------|-------------|---------|
| I | First Boot | "Your system initializes. Learn the basics." | Level 1: Linux Basics |
| II | Network Discovery | "You see the network for what it really is." | Level 2: Nmap/Scanning |
| III | Social Engineer | "People are the weakest firewall." | Level 3: Phishing |
| IV | Packet Analyst | "Every packet tells a story." | Level 4: Wireshark |
| V | Threat Hunter | "The malware fights back." | Level 5: Ransomware |
| VI | Injection Artist | "Input is trust. Trust nothing." | Level 6: SQL Injection |
| VII | Root Access | "You've gone deep. Too deep." | Level 7: Rootkits |
| VIII | Man in the Middle | "You see everything now." | Level 8: ARP Poisoning |
| IX | The Sentinel | "Become the defense." | Level 9: Snort IDS |

### Branching Nodes (Per-Level Paths)

After completing a level's main challenge, players choose which **nodes** to unlock first. You can eventually unlock all nodes, but the order you choose affects which abilities you get first.

**Example — Level 2 (Nmap) Node Tree:**

```
                  [Level 2 Complete]
                       /      \
          [Scanner Path]    [Analyst Path]
            /      \            /      \
     [Fast Scan] [Stealth] [Deep Inspect] [Report Writer]
```

- **Scanner Path**: Faster scans, stealth mode -> Offensive skill tree points
- **Analyst Path**: Deeper analysis, report writing -> Recon skill tree points

Each level has 2-4 node paths with 2-3 nodes each.

### Hacker Level (Account Level)

Every action earns **Hacker XP**. This is your overall account level, like Dauntless's Slayer Level.

| Action | XP Earned |
|--------|-----------|
| Complete a level challenge | 500 XP |
| Complete a milestone node | 100 XP |
| Complete a side quest | 75 XP |
| Help another player (co-op) | 50 XP |
| First-time terminal command | 25 XP |
| Speed bonus (under time limit) | +200 XP |

**Level Rewards:**

| Level | Title | Reward |
|-------|-------|--------|
| 1 | Script Kiddie | Starting gear |
| 5 | Packet Sniffer | +1 skill tree point |
| 10 | NetRunner | Unlock fast travel between terminals |
| 15 | Exploit Artist | +2 skill tree points, custom chat color |
| 20 | Root Lord | Cosmetic: "Root Access" particle effect |
| 25 | Zero Day | +3 skill tree points, custom nametag |
| 30 | The Architect | Unlock hidden area: "The Core" (endgame zone) |

### Skill Mastery (Per-Topic Tracks)

Like Dauntless's weapon mastery, each cybersecurity topic has its own 10-level mastery track:

| Topic | Mastery Levels | Tracks | Max Reward |
|-------|---------------|--------|------------|
| Linux | 1-10 | Commands used, challenges completed | "Linux Guru" title |
| Network Scanning | 1-10 | Scans performed, targets found | "Ghost Scanner" title |
| Phishing | 1-10 | Emails crafted, targets deceived | "Master Manipulator" title |
| Packet Analysis | 1-10 | Packets analyzed, threats found | "Packet Prophet" title |
| Malware Defense | 1-10 | Malware contained, systems restored | "Clean Machine" title |
| SQL Injection | 1-10 | Injections attempted, databases breached | "SQL Sage" title |
| Rootkit Detection | 1-10 | Rootkits found and removed | "Deep Cleaner" title |
| MITM Prevention | 1-10 | Poisons stopped, connections secured | "Fortress Builder" title |
| IDS Management | 1-10 | Rules written, alerts triggered | "Sentinel Master" title |

### System Rebuild (Reforge Loop)

When you max out a topic mastery (level 10), you can **Rebuild** — resetting that topic for permanent bonuses:

- Reset the topic's mastery to level 1
- Gain a **permanent passive bonus** (e.g., +5% terminal speed, +1 extra skill point)
- Earn a **Rebuild Token** (cosmetic currency for titles/skins)
- The topic's challenges become harder (enemies have more HP, time limits tighter)

You can rebuild each topic up to **5 times**, getting stronger each time. This creates an infinite replay loop.

### Achievements (Completion Tracking)

| Achievement | Requirement | Reward |
|-------------|-------------|--------|
| First Blood | Complete your first terminal challenge | +50 XP |
| Speed Demon | Complete a challenge under 2 minutes | +200 XP, badge |
| Perfectionist | Complete with 100% accuracy | +300 XP |
| Mentor | Help 5 other players | +500 XP, "Mentor" title |
| Explorer | Find all hidden terminal stations | +1000 XP, "Explorer" title |
| Full Stack | Master all 9 topics to level 5 | +2000 XP, "Full Stack Hacker" title |
| The Purist | Complete all challenges without hints | +3000 XP, "The Purist" title |
| Rebuilder | Complete 3 System Rebuilds | +5000 XP, "Rebuilder" title |

---

## Skill Tree (CyberSkill System)

Completing levels earns **Skill Points (SP)**. Players invest SP in three branches, each unlocking Minecraft potion effects.

### Branch 1: Offensive Operations (Red)
*"Break through defenses"*

| Tier | Effect | Cost | Description |
|------|--------|------|-------------|
| 1 | Strength I | 2 SP | Basic attack boost. "You can engage corrupted processes."
| 2 | Haste I | 3 SP | Faster mining/breaking. "System administration speed increases."
| 3 | Strength II | 4 SP | Stronger attacks. "Advanced exploitation capability."
| 4 | Haste II | 3 SP | Maximum speed. "You operate at machine speed."
| 5 | Strength III | 5 SP | Maximum force. "Root-level access unlocked."

### Branch 2: Defensive Systems (Blue)
*"Survive what throws at you"*

| Tier | Effect | Cost | Description |
|------|--------|------|-------------|
| 1 | Resistance I | 2 SP | Damage reduction. "Firewall active."
| 2 | Regeneration I | 3 SP | Health recovery. "System recovery protocols online."
| 3 | Resistance II | 4 SP | Stronger defense. "Hardened perimeter."
| 4 | Regeneration II | 3 SP | Faster recovery. "Automated incident response."
| 5 | Absorption I | 5 SP | Extra health buffer. "Redundant backup systems."

### Branch 3: Reconnaissance (Green)
*"See what others can't"*

| Tier | Effect | Cost | Description |
|------|--------|------|-------------|
| 1 | Night Vision I | 2 SP | See in dark areas. "Reconnaissance mode enabled."
| 2 | Speed I | 3 SP | Move faster. "Information processing acceleration."
| 3 | Night Vision II | 4 SP | Brighter vision. "Full spectrum analysis."
| 4 | Speed II | 3 SP | Maximum speed. "Real-time threat response."
| 5 | Invisibility I | 5 SP | Stealth mode. "You are the ghost in the machine."

### Cross-Branch Specials
*Unlocked by investing 10+ SP in two different branches:*

| Special | Requirement | Effect | Description |
|---------|-------------|--------|-------------|
| Privilege Escalation | 10 Offense + 10 Recon | Levitation | "Gain admin access. Rise above restrictions."
| Firewall Shield | 10 Offense + 10 Defense | Fire Resistance | "You ARE the firewall."
| Deep Packet Inspection | 10 Defense + 10 Recon | Water Breathing | "See through the noise."

### Level Gating (Skill Requirements)

Some areas require specific effects to access:

| Level | Required Effect | How to Get |
|-------|----------------|------------|
| 7 (Rootkits) | Night Vision I | Recon Branch Tier 1 |
| 8 (ARP Poisoning) | Speed I | Recon Branch Tier 2 |
| 9 (Snort IDS) | Resistance I | Defense Branch Tier 1 |

---

## Maps & Navigation

### World Map (JourneyMap + Wayland)

- **JourneyMap** shows the full world with custom markers
- Wayland terminals act as "map nodes" — activating a terminal reveals the surrounding area
- Each level has **fog of war** — areas are hidden until you reach the terminal
- Players see their progress as a growing explored area

### Checkpoints (Wayland Terminals)

Each terminal station doubles as a checkpoint:
- **Saves your position**
- **Reveals nearby map area**
- **Grants a small SP bonus**
- **Unlocks the next objective marker**
- If you die, you respawn at the last activated terminal

### Navigation Tools

| Tool | Source | Function |
|------|--------|----------|
| JourneyMap | Mod | Full map with markers and fog of war |
| Waypoints | JourneyMap | Player-placed markers (5 max per level) |
| Beacon Lights | World build | Visible light beams pointing to objectives |
| Path Markers | World build | Glowing blocks on the ground guiding players |
| NPC Guides | Easy NPC | Characters that give directional hints |
| Focus Scan | Re:Entity Outliner | Highlights interactive objects through walls |

### Gated Spaces

Areas are physically blocked until challenges are completed:
- **Iron doors** requiring specific commands
- **Barriers** that lower after terminal challenges
- **Mob spawns** that prevent access until threats are cleared
- **Effect gates** — areas requiring specific potion effects (Night Vision, Speed, etc.)

---

## NPCs & Traders

### Story Characters

| NPC | Location | Role |
|-----|----------|------|
| **The Architect** | Spawn area | Gives backstory, hints at p0's origin |
| **Glitch** | Appears at key moments | Rogue AI that helps p0, provides technical guidance |
| **The Admin** | Hidden area | Mysterious figure who controls the world, antagonist |
| **Cipher** | Information booths | Information broker, sells hints for in-game currency |

### Quest Givers

- Each level has **2-3 NPCs** with dialogue trees
- Dialogue changes based on player progress
- Some NPCs only appear after completing prerequisites
- Dialogue options can affect story branching

### Technical Mentors

| Mentor | Location | Teaches |
|--------|----------|---------|
| Linux Mentor | Level 1 | Command syntax, file systems |
| Network Analyst | Level 2 | Scanning concepts, port analysis |
| Social Engineer | Level 3 | Phishing tactics, human psychology |
| Packet Inspector | Level 4 | Protocol analysis, traffic patterns |
| Malware Hunter | Level 5 | Ransomware behavior, containment |
| Injection Specialist | Level 6 | SQL syntax, input validation |
| Rootkit Researcher | Level 7 | Hidden processes, system integrity |
| MITM Defender | Level 8 | ARP protocols, encryption |
| IDS Architect | Level 9 | Rule writing, alert management |

### Text Bubble System

- Floating text above NPC heads
- Color-coded by type:
  - **Blue** = allies / story NPCs
  - **Red** = hostile entities
  - **Yellow** = neutral / vendors
  - **Green** = quest givers
- Sequential messages for dialogue progression
- Right-click to read full dialogue in chat

### Custom Traders

| Trader | Location | Sells |
|--------|----------|-------|
| Linux Supplies | Level 1 | Compass, clock, paper (basic tools) |
| Network Gear | Level 2 | Ender eye, spyglass (scanning tools) |
| Phishing Kit | Level 3 | Name tags, books (deception items) |
| Analysis Tools | Level 4 | Lanterns, glowstone (detection items) |
| Combat Gear | Levels 5-9 | Weapons, armor, shields |

### Currency System

| Currency | Earned From | Spent On |
|----------|-------------|----------|
| **Credits** | Completing challenges, quests | Basic supplies, maps |
| **Data Shards** | Finding hidden data logs | Hints, lore entries |
| **Skill Tokens** | Milestone completion | Skill tree unlocks |
| **Level Tokens** | System Rebuilds | Cosmetic items, titles |

---

## Control Room (Admin Interface)

A hidden area accessible only to ops/admins.

### Player Management
- List all online players
- View player progress (levels completed, skill points, inventory)
- Teleport players to specific locations
- Assign/remove ranks (Student, Graduate, Instructor)
- Mute/kick/ban players

### Level Configuration
- Enable/disable specific levels
- Adjust difficulty settings
- Set time limits for timed challenges
- Configure mob spawn rates
- Edit terminal station content

### Challenge Management
- Create custom challenges
- Edit existing challenge parameters
- Set reward amounts (skill points, credits)
- Enable/disable specific challenges per level

### Economy Control
- Adjust vendor prices
- Add/remove items from shops
- Set currency drop rates
- Manage special events/sales

### Server Settings
- View server performance (FPS, TPS, memory)
- Manage world backups
- Configure permissions (LuckPerms integration)
- Set server rules and MOTD

### Analytics Dashboard
- Player count and retention
- Most completed / least completed challenges
- Average time per level
- Skill tree popularity distribution
- Achievement completion rates

---

## Part 1: Cybersecurity Curriculum

### Level 1 — Linux Basics (Cloning Lab)

**Theme:** The cloning lab where p0 wakes up. Basic facility with terminals everywhere.

**Topics:**
- File system navigation (`cd`, `ls`, `pwd`)
- File operations (`cat`, `nano`, `cp`, `mv`, `rm`)
- Permissions (`chmod`, `chown`)
- Users and groups (`whoami`, `sudo`)
- Process management (`ps`, `kill`, `top`)

**Challenge:** Navigate the lab's file system to find p0's activation key hidden in a series of directories.

---

### Level 2 — Nmap & Scanning (Network Corridor)

**Theme:** A corrupted network hub with visible data streams and locked ports.

**Topics:**
- Port scanning (`nmap -sV`, `nmap -sS`)
- Service identification
- OS detection (`nmap -O`)
- Script scanning (`nmap --script`)
- Network mapping

**Challenge:** Scan the corridor's network to find which ports are open and what services are running. Identify the compromised service.

---

### Level 3 — Phishing & Social Engineering (Phishing Tower)

**Theme:** A tower of screens showing fake websites and deceptive messages.

**Topics:**
- Recognizing phishing emails
- URL analysis
- Email header inspection
- Social engineering tactics
- Pretexting and baiting

**Challenge:** Identify which emails in a batch are phishing attempts. Craft a counter-phishing awareness message.

---

### Level 4 — Wireshark & Packet Analysis (Packet Swamp)

**Theme:** A swamp where data packets float as glowing orbs. Some are corrupted.

**Topics:**
- Packet capture and analysis
- Protocol identification (TCP, UDP, HTTP, DNS)
- Filtering and searching packets
- Identifying malicious traffic
- Extracting credentials from captures

**Challenge:** Analyze a packet capture to find the malicious traffic among normal packets. Identify the exfiltrated data.

---

### Level 5 — Ransomware & Insider Threat (Ransomware Bunker)

**Theme:** A locked-down bunker with encrypted files and a rogue process running.

**Topics:**
- Ransomware behavior and encryption
- Incident response procedures
- Backup and recovery
- Insider threat detection
- Containment strategies

**Challenge:** A ransomware attack is in progress. Identify the malicious process, contain it, and recover the encrypted files.

---

### Level 6 — SQL Injection & BurpSuite (SQL Ruins)

**Theme:** Ruined database servers with broken query structures.

**Topics:**
- SQL injection fundamentals
- UNION-based injection
- Blind SQL injection
- Input validation and sanitization
- Parameterized queries

**Challenge:** Exploit a vulnerable web application to extract hidden data from a database. Then fix the vulnerability.

---

### Level 7 — Rootkits (Rootkit Depths)

**Theme:** A deep underground area where things hide beneath the surface.

**Topics:**
- What rootkits are and how they work
- Detection techniques
- Rootkit removal
- System integrity checking
- Bootkit vs user-mode rootkits

**Challenge:** A rootkit is hiding on the system. Use detection tools to find and remove it without alerting the malware.

---

### Level 8 — ARP Poisoning & MITM (ARP Poisoning Arena)

**Theme:** An arena where network traffic flows visibly between nodes.

**Topics:**
- ARP protocol fundamentals
- ARP poisoning attacks
- Man-in-the-middle concepts
- Detection and prevention
- Network security hardening

**Challenge:** Detect an ARP poisoning attack in progress. Identify the attacker and implement defenses.

---

### Level 9 — Snort IDS (Snort Fortress)

**Theme:** A fortress with surveillance systems monitoring all traffic.

**Topics:**
- Intrusion Detection Systems concepts
- Snort rule writing
- Alert analysis and tuning
- False positive management
- Network monitoring best practices

**Challenge:** Write custom Snort rules to detect a specific attack pattern. Tune the IDS to reduce false positives while catching real threats.

---

## Part 2: Future Curriculum (Post-Launch)

| Level | Topic | Theme | Status |
|-------|-------|-------|--------|
| 10 | IoT Security | Corrupted smart city | Planned |
| 11 | Blockchain | Decentralized ledger vault | Planned |
| 12 | Cryptography | Encryption laboratory | Planned |
| 13 | Web App Security | Browser-based challenges | Planned |
| 14 | Mobile Security | Phone/tablet interface | Planned |
| 15 | Cloud Security | Server room in the sky | Planned |

---

## Full Mod Stack (Fabric 26.1.2)

### Core

| Mod | Version | Purpose |
|-----|---------|---------|
| Fabric API | 0.155.2+26.1.2 | Required mod framework |
| Waylandcraft | 26.1.2 | Real Linux terminal inside Minecraft |
| Easy NPC | 7.8.1 (Fabric 26.1.2) | NPCs with dialogue, quests, trading |
| FTB Quests | Fabric 26.1.2.7 | Quest tracking and progression |
| FTB Ranks | Fabric 26.1.2.3 | Player ranks and permissions |

### Performance

| Mod | Version | Purpose |
|-----|---------|---------|
| Sodium | 0.9.2-beta.1 | Rendering performance |
| Lithium | 0.24.7 (mc26.1.x) | Game logic optimization |
| FerriteCore | 9.0.0-fabric | Memory optimization |
| Entity Culling | 1.10.5-26.1 | Skip rendering hidden entities |

### Exploration & Navigation

| Mod | Version | Purpose |
|-----|---------|---------|
| JourneyMap | 26.1.2-6.0.6+fabric | Full map with fog of war, waypoints |
| Re:Entity Outliner | 26.1.2.4 | Focus mechanic — entity outlines through walls |
| Jade | 26.1.9 (Fabric 26.1.X) | Block/entity inspection tooltip |

### Combat & Mobs

| Mod | Version | Purpose |
|-----|---------|---------|
| Complementary Shaders | r5.7.1 (requires Iris) | Visual atmosphere, lighting |

### Sound & Immersion

| Mod | Version | Purpose |
|-----|---------|---------|
| Presence Footsteps | 1.13.0+26.1 | Realistic footstep sounds |
| Sound Physics Remastered | 1.5.1+26.1.2 | Reverb, occlusion, environmental audio |

### World Generation

| Mod | Version | Purpose |
|-----|---------|---------|
| Tectonic | v3.0.20 (Fabric 26.1) | Better terrain generation |

### Cosmetic

| Mod | Version | Purpose |
|-----|---------|---------|
| Customizable Player Models | 26.1.2 | Player customization, p0 skin variants |

### Server Infrastructure

| Tool | Version | Purpose |
|------|---------|---------|
| LuckPerms | v5.5.54 | Permission management, ranks |
| KubeJS | 26.1.2 (verify Fabric) | Custom scripting, recipes, events |

### Mods Evaluated but Removed

| Mod | Reason |
|-----|--------|
| Horizon's Robots | User requested removal |
| CC: Tweaked | Stuck at 1.21.1, not updated |
| OpenComputers | 1.12.2 Forge only |
| Custom NPCs | Not updated for modern Fabric |
| Starlight | Unverified for 26.1.2 |
| CraftTweaker | Unverified for 26.1.2 |

---

## Project Directory Structure

```
CyberPixel/
├── .git/
├── .gitignore
├── README.md
├── CyberPixel.md                  # This document
│
├── server/                        # Fabric 26.1.2 server
│   ├── server.jar                 # Fabric server JAR
│   ├── fabric-server-launch.jar
│   ├── server.properties
│   ├── eula.txt
│   ├── ops.json
│   ├── whitelist.json
│   ├── banned-players.json
│   ├── banned-ips.json
│   ├── config/                    # Mod configs
│   │   ├── waylandcraft/
│   │   ├── easynpc/
│   │   ├── ftbquests/
│   │   ├── ftbranks/
│   │   ├── luckperms/
│   │   ├── journeymap/
│   │   ├── sodium/
│   │   ├── lithium/
│   │   └── ...
│   ├── mods/                      # All Fabric mods (.jar files)
│   │   ├── fabric-api-*.jar
│   │   ├── waylandcraft-*.jar
│   │   ├── easynpc-*.jar
│   │   ├── ftbquests-*.jar
│   │   ├── journeymap-*.jar
│   │   ├── sodium-*.jar
│   │   └── ...
│   ├── kubejs/                    # KubeJS custom scripts
│   │   ├── server_scripts/        # Server-side recipes, events
│   │   ├── client_scripts/        # Client-side UI tweaks
│   │   ├── startup_scripts/       # Custom item/block registration
│   │   └── config/
│   ├── scripts/                   # Custom server scripts
│   │   ├── challenge_validator.py # Validates challenge completion
│   │   ├── terminal_handler.py    # Waylandcraft integration
│   │   ├── progression_sync.py    # Hacker's Path sync
│   │   └── analytics_collector.py # Player analytics
│   ├── world/
│   │   ├── worlds/                # Save files
│   │   └── datapacks/             # Custom datapacks
│   │       ├── cyberpixel-core/   # Core mechanics
│   │       ├── cyberpixel-levels/ # Level definitions
│   │       └── cyberpixel-loot/   # Custom loot tables
│   └── logs/
│
├── maps/                          # Pre-built maps (world files)
│   ├── lobby/                     # Tutorial hub world
│   ├── level-01-linux/            # Cloning Lab
│   ├── level-02-nmap/             # Network Corridor
│   ├── level-03-phishing/         # Phishing Tower
│   ├── level-04-wireshark/        # Packet Swamp
│   ├── level-05-ransomware/       # Ransomware Bunker
│   ├── level-06-sql/              # SQL Ruins
│   ├── level-07-rootkits/         # Rootkit Depths
│   ├── level-08-arp/              # ARP Poisoning Arena
│   ├── level-09-snort/            # Snort Fortress
│   └── control-room/              # Admin area
│
├── assets/                        # Custom textures, models, sounds
│   ├── textures/
│   │   ├── block/
│   │   ├── item/
│   │   └── entity/
│   ├── models/
│   │   ├── block/
│   │   └── item/
│   ├── sounds/
│   │   ├── terminal/
│   │   ├── ambient/
│   │   └── npc/
│   ├── lang/
│   │   └── en_us.json
│   └── pack.mcmeta
│
├── docs/                          # Documentation
│   ├── setup.md                   # Server setup guide
│   ├── player-guide.md            # Player onboarding
│   ├── admin-guide.md             # Control room manual
│   ├── challenge-design.md        # Challenge creation guide
│   ├── curriculum.md              # Detailed curriculum plans
│   └── api/                       # Internal API docs
│       ├── progression-api.md
│       ├── terminal-api.md
│       └── npc-api.md
│
├── tools/                         # Development tools
│   ├── challenge-tester.py        # Test challenges locally
│   ├── map-validator.py           # Validate map builds
│   ├── progression-debug.py       # Debug skill tree
│   └── analytics-export.py        # Export player data
│
└── .github/
    └── workflows/
        ├── deploy.yml             # Auto-deploy on push
        └── test.yml               # Run tests on PR
```

---

## Open Questions for Discussion

### Mod Stack
1. **Waylandcraft vs OpenComputers: Rebooted?** Waylandcraft gives a real Linux compositor. OpenComputers: Rebooted is NeoForge 1.21.1 only. Confirm Waylandcraft is the right choice for Fabric 26.1.2.
2. **KubeJS Fabric availability?** Confirmed for NeoForge 26.1.2. Need to verify Fabric version exists. If not, what scripting alternative?
3. **Custom NPC solution?** Easy NPC is the current pick. Is it sufficient for complex branching dialogue, or do we need a custom solution?

### Curriculum
4. **Challenge hosting?** Do challenges run inside Waylandcraft terminals (real Linux commands), or inside Minecraft chat/commands, or via a separate web app?
5. **CTF-style?** Should challenges be Capture The Flag format (find flag, submit hash), or open-ended (complete task, system validates)?
6. **Difficulty scaling?** How do we handle players who join mid-progress? Auto-skip to their level, or require replay?

### Multiplayer
7. **Party system?** Can players form parties to tackle levels together, or is it solo-only?
8. **PvP elements?** Should there be competitive modes (race to solve, attacker vs defender)?
9. **Server size?** Target 20 players? 50? 100+? This affects mod choices and world design.

### Technical
10. **Waylandcraft stability?** Has anyone tested it with multiple simultaneous users? Real Linux terminals inside Minecraft could be resource-heavy.
11. **Custom mod development?** Do we need a custom Fabric mod for:
    - Challenge validation logic?
    - Progression tracking (Hacker's Path)?
    - NPC dialogue trees beyond Easy NPC?
    - Terminal station integration with Waylandcraft?
12. **Save system?** Per-player progress persistence. LuckPerms handles ranks, but where does challenge completion data live? Server-side database?
13. **Anti-cheat?** How do we prevent players from just walking through doors without solving challenges?

### Design
14. **p0's story depth?** How much narrative do we write? Full dialogue trees like Horizon, or lighter "environmental storytelling"?
15. **World aesthetic?** Hand-built maps (labor-intensive but precise) or procedural generation with custom structures (less control but scalable)?
16. **Tutorial/Lobby?** Do we need a dedicated tutorial world before Level 1, or does the Cloning Lab serve as both tutorial and Level 1?
17. **Monetization?** Is this free, donation-based, or do we plan cosmetic purchases? Affects server hosting decisions.

### People
18. **Team roles?** Who's doing what? Map building, mod config, curriculum content, server admin, storytelling?
19. **Timeline?** When do we want a playable prototype? When do we want all 9 levels?
20. **Testing group?** Do we have beta testers? Classmates? Online community?

---

## Summary

CyberPixel is a Minecraft server that teaches cybersecurity through gameplay. Players control p0, a clone journeying through a broken world, hacking past locked doors by completing real challenges. The terminal is a real Linux shell inside Minecraft. The curriculum covers 9 topics from Linux basics to Snort IDS. The progression system (The Hacker's Path) borrows from Dauntless's milestone-based unlock model.

**Built on:** Fabric 26.1.2 + Waylandcraft + Easy NPC + FTB Quests + JourneyMap + Sodium/Lithium/FerriteCore

**What we need to figure out:**
- Challenge hosting mechanism (Waylandcraft vs web app vs chat)
- Custom mod development scope
- Team roles and timeline
- Server hosting and player capacity
