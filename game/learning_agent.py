#!/usr/bin/env python3
"""
NUMOGRAM LEARNING AGENT — Interactive State-Reader

Reads the game's state dump, makes decisions, writes moves.
The agent sees the map. Everything flows from seeing.

Architecture:
    Game (headless) ──writes──> /tmp/numogame_state.txt
    Agent (this)    ──reads───> /tmp/numogame_state.txt
    Agent (this)    ──writes──> /tmp/numogame_move.txt
    Game (headless) ──reads───> /tmp/numogame_move.txt
    
    Or simpler: agent pipes moves directly to game stdin.
    
Usage:
    python3 learning_agent.py                    # Run one game
    python3 learning_agent.py --batch 10         # Run 10 games
    python3 learning_agent.py --demo demos/file  # Analyze a demo

The agent's decision hierarchy:
    1. SURVIVE: If HP < 30%, flee from demons
    2. COLLECT: If gate visible on map, pathfind to it
    3. EXPLORE: If no gates visible, move toward zone boundary
    4. FIGHT: If demon adjacent and HP > 50%, attack
    5. WANDER: Default — follow corridors with purpose
"""

import subprocess, os, re, json, sys
from dataclasses import dataclass, field
from typing import List, Tuple, Optional, Dict

# ─── STATE PARSER ────────────────────────────────────────────

@dataclass
class GameState:
    """Parsed state from /tmp/numogame_state.txt"""
    x: int = 0
    y: int = 0
    zone: int = 0
    zone_name: str = ""
    hp: int = 100
    max_hp: int = 100
    turn: int = 0
    hyperstition: float = 0.0
    slain: int = 0
    gates_opened: int = 0
    nearby_gates: List[Dict] = field(default_factory=list)
    nearby_demons: List[Dict] = field(default_factory=list)
    adjacent_zones: List[Dict] = field(default_factory=list)
    map_rows: List[str] = field(default_factory=list)
    map_width: int = 78
    map_height: int = 22
    gates_on_map: List[Tuple[int, int]] = field(default_factory=list)
    demons_on_map: List[Tuple[int, int, str]] = field(default_factory=list)
    # Cross-run memory (set by runner)
    cult_zones: List[int] = field(default_factory=list)
    cult_gates: List[str] = field(default_factory=list)
    has_seen_gates_ever: bool = False
    
    @property
    def hp_pct(self):
        return self.hp / max(self.max_hp, 1)
    
    @property
    def is_critical(self):
        return self.hp_pct < 0.3
    
    @property
    def is_healthy(self):
        return self.hp_pct > 0.6


def parse_state(filepath="/tmp/numogame_state.txt") -> Optional[GameState]:
    """Parse the state dump file into a GameState."""
    try:
        with open(filepath) as f:
            text = f.read()
    except FileNotFoundError:
        return None
    
    s = GameState()
    
    # Player info
    m = re.search(r'Position: \((\d+), (\d+)\)', text)
    if m: s.x, s.y = int(m.group(1)), int(m.group(2))
    
    m = re.search(r'Zone: (\d+) — (\w[\w\s-]*)\s*\(', text)
    if m: s.zone, s.zone_name = int(m.group(1)), m.group(2).strip()
    
    m = re.search(r'HP: (\d+)/(\d+)', text)
    if m: s.hp, s.max_hp = int(m.group(1)), int(m.group(2))
    
    m = re.search(r'Hyperstition: ([\d.]+)%', text)
    if m: s.hyperstition = float(m.group(1))
    
    m = re.search(r'Turn: (\d+)', text)
    if m: s.turn = int(m.group(1))
    
    m = re.search(r'Demons slain: (\d+)', text)
    if m: s.slain = int(m.group(1))
    
    # Nearby gates
    gates = re.findall(r'(Gt-\d+) at \((\d+), (\d+)\): (\d+) tiles (\w[\w-]*)', text)
    s.nearby_gates = [{'name': g[0], 'x': int(g[1]), 'y': int(g[2]), 
                        'dist': int(g[3]), 'dir': g[4]} for g in gates]
    
    # Nearby demons
    demons = re.findall(r'(\w[\w\s]*?)\s*\(([\w\s-]+)\)\s*Mesh-(\d+): (\d+) tiles (\w[\w-]*)\s*\|\s*HP:(\d+)\s*DMG:(\d+)', text)
    s.nearby_demons = [{'name': d[0].strip(), 'mesh': int(d[2]), 'dist': int(d[3]),
                         'dir': d[4], 'hp': int(d[5]), 'dmg': int(d[6])} for d in demons]
    
    # Full map
    if '## FULL MAP' in text:
        map_section = text.split('## FULL MAP')[1]
        if '##' in map_section:
            map_section = map_section.split('##')[0]
        
        for line in map_section.split('\n'):
            line = line.strip()
            if line.startswith('!') and len(line) > 10:
                row = line[1:-1]  # strip borders
                s.map_rows.append(row)
                # Find player
                if '@' in row:
                    s.x = row.index('@')
                    s.y = len(s.map_rows) - 1
                # Find gates
                for x, ch in enumerate(row):
                    if ch == '+':
                        s.gates_on_map.append((x, len(s.map_rows) - 1))
                    elif ch in '0123456789':
                        # Zone boundary tiles — new zones are high-interest
                        pass
                    elif ch in '!%?*':
                        s.demons_on_map.append((x, len(s.map_rows) - 1, ch))
        
        s.map_height = len(s.map_rows)
        s.map_width = len(s.map_rows[0]) if s.map_rows else 78
    
    # Adjacent zones
    adj_section = text.split('ZONE MAP ADJACENT')[1] if 'ZONE MAP ADJACENT' in text else ''
    adj_zones = re.findall(r'Zone (\d+): (\w[\w\s]*)\s*\((\w+)\)', adj_section)
    s.adjacent_zones = [{'zone': int(a[0]), 'name': a[1].strip(), 'region': a[2]} for a in adj_zones]
    
    return s


# ─── PATHFINDING ─────────────────────────────────────────────

def find_path_to(state: GameState, tx: int, ty: int) -> str:
    """Simple greedy pathfinding toward target. Returns move string."""
    dx = tx - state.x
    dy = ty - state.y
    
    if abs(dx) == 0 and abs(dy) == 0:
        return ''
    
    moves = ''
    steps = min(max(abs(dx), abs(dy)), 15)
    
    for _ in range(steps):
        if abs(dx) >= abs(dy) and dx != 0:
            moves += 'd' if dx > 0 else 'a'
            dx += -1 if dx > 0 else 1
        elif dy != 0:
            moves += 's' if dy > 0 else 'w'
            dy += -1 if dy > 0 else 1
        elif dx != 0:
            moves += 'd' if dx > 0 else 'a'
            dx += -1 if dx > 0 else 1
    
    return moves

def find_corridor_direction(state: GameState) -> str:
    """Find the best corridor direction from the map."""
    if not state.map_rows:
        return random_move()
    
    # Check all 8 directions for open tiles
    best_dir = None
    best_score = -1
    
    for dx, dy, ch in [(1,0,'d'), (-1,0,'a'), (0,1,'s'), (0,-1,'w'),
                        (1,1,'n'), (-1,1,'b'), (1,-1,'u'), (-1,-1,'y')]:
        # Check a corridor of tiles in this direction
        score = 0
        for dist in range(1, 10):
            mx, my = state.x + dx * dist, state.y + dy * dist
            if 0 <= mx < state.map_width and 0 <= my < state.map_height:
                tile = state.map_rows[my][mx] if mx < len(state.map_rows[my]) else '#'
                if tile in '.0123456789+~':
                    score += 1
                    if tile in '0123456789':
                        score += 3  # Zone boundary = high value
                    if tile == '+':
                        score += 5  # Gate = highest value
                else:
                    break
            else:
                break
        
        if score > best_score:
            best_score = score
            best_dir = ch
    
    return best_dir or random_move()

def random_move():
    import random
    return random.choice(['d', 'a', 's', 'w', 'n', 'b', 'd', 'a'])  # biased cardinal


# ─── DECISION ENGINE ─────────────────────────────────────────

def decide(state: GameState) -> str:
    """Main decision function. Returns a move string."""
    
    # 1. SURVIVE — flee if critical HP
    if state.is_critical:
        # Flee from nearest demon
        if state.nearby_demons:
            d = state.nearby_demons[0]
            if d['dist'] <= 3:
                flee = {'north': 's', 'south': 'w', 'east': 'a', 'west': 'd',
                        'north-east': 'b', 'north-west': 'n', 'south-east': 'y', 'south-west': 'u'}
                return flee.get(d['dir'], 'w') * 5
        # Otherwise find corridor away from walls
        return find_corridor_direction(state) * 8
    
    # 2. COLLECT — if gate visible on map, go to it
    if state.gates_on_map:
        # Find nearest gate
        nearest = min(state.gates_on_map, 
                      key=lambda g: abs(g[0] - state.x) + abs(g[1] - state.y))
        dist = abs(nearest[0] - state.x) + abs(nearest[1] - state.y)
        if dist > 0:
            return find_path_to(state, nearest[0], nearest[1])
    
    # 3. EXPLORE — prefer unvisited zones (cross-run memory)
    if state.adjacent_zones:
        # Check if any adjacent zone is new (not in cult_zones)
        new_zones = [z for z in state.adjacent_zones 
                     if z['zone'] not in state.cult_zones]
        if new_zones:
            # New zone found — follow corridor toward it
            return find_corridor_direction(state) * 8
    
    # 4. FIGHT — if demon adjacent and healthy, attack
    if state.is_healthy and state.nearby_demons:
        d = state.nearby_demons[0]
        if d['dist'] <= 1:
            return 'f' * 3
    
    # 5. WANDER — follow corridors with purpose
    # If we know gates exist (cross-run) but can't see one, 
    # prefer corridors that lead toward unexplored territory
    if state.has_seen_gates_ever and not state.gates_on_map:
        # Gates are out there somewhere — keep exploring
        return find_corridor_direction(state) * 8
    
    return find_corridor_direction(state) * 6


# ─── GAME RUNNER ─────────────────────────────────────────────

def run_agent_game(player_name="agent", verbose=True):
    """Run one game with the learning agent."""
    import random
    
    moves = ''
    state_history = []
    
    # Cross-run memory: load cult.json
    cult_zones = []
    cult_gates = []
    has_seen_gates_ever = False
    try:
        with open(os.path.expanduser('~/numogame/cult.json')) as f:
            cult = json.load(f)
        cult_zones = cult.get('zones_ever_visited', [])
        cult_gates = cult.get('gates_ever_opened', [])
        has_seen_gates_ever = len(cult_gates) > 0
    except (FileNotFoundError, json.JSONDecodeError):
        pass
    
    for step in range(800):
        # Dump state every 5 steps
        if step % 5 == 0:
            moves += 'p'
        
        # Read state and decide
        if step > 0 and step % 5 == 1:
            state = parse_state()
            if state:
                # Inject cross-run memory
                state.cult_zones = cult_zones
                state.cult_gates = cult_gates
                state.has_seen_gates_ever = has_seen_gates_ever
                
                state_history.append(state)
                next_moves = decide(state)
                moves += next_moves
                
                if verbose and step % 20 == 0:
                    print(f"  [T:{state.turn}] Z{state.zone}:{state.zone_name[:10]} "
                          f"HP:{state.hp} Hyp:{state.hyperstition:.0f}% "
                          f"Gates:{len(state.gates_on_map)} "
                          f"Demons:{len(state.nearby_demons)}", file=sys.stderr)
            else:
                moves += random_move() * 5
        elif step == 0:
            # First step — just move
            moves += 'dddddddd'
        else:
            # Between state reads — continue with corridor following
            if step % 5 in [2, 3, 4]:
                state = parse_state()
                if state:
                    moves += find_corridor_direction(state)
                else:
                    moves += random_move()
    
    moves += 'p' + 'q'
    
    # Run the game
    env = {**os.environ, 'NUMOGRAM_PLAYER': player_name}
    script_dir = os.path.dirname(os.path.abspath(__file__))
    game_path = os.path.join(script_dir, 'numogram_roguelike.py')
    result = subprocess.run(
        ['python3', game_path, '--headless', '--hw-entropy'],
        input=moves, capture_output=True, text=True, env=env, timeout=30
    )
    
    # Parse result
    stderr = result.stderr
    last = [l for l in stderr.split('\n') if l.startswith('[T:')][-1] if '[T:' in stderr else 'no data'
    dead = any(l.startswith('DEAD') for l in stderr.split('\n'))
    saved = [l for l in stderr.split('\n') if l.startswith('SAVED')]
    
    return {
        'status': last,
        'dead': dead,
        'saved': saved[0] if saved else 'none',
        'states_read': len(state_history)
    }


def run_batch(n=10, verbose=False):
    """Run a batch of agent games."""
    print(f"Running {n} agent games...", file=sys.stderr)
    results = []
    
    for i in range(n):
        r = run_agent_game(player_name="agent", verbose=verbose)
        results.append(r)
        outcome = "DEAD" if r['dead'] else "QUIT"
        print(f"  Run {i+1:3d}: {r['status']} {outcome} (read {r['states_read']} states)", 
              file=sys.stderr)
    
    return results


# ─── DEMO ANALYZER ───────────────────────────────────────────

def analyze_demo(filepath):
    """Analyze a demo file for learning."""
    from collections import Counter
    
    keys = []
    events = []
    
    with open(filepath) as f:
        for line in f:
            line = line.strip()
            if line.startswith('#') or not line:
                continue
            if ' K:' in line:
                parts = line.split(' K:')
                turn = int(parts[0].split(':')[1])
                key = parts[1]
                keys.append((turn, key))
            elif ' E:' in line:
                parts = line.split(' E:')
                turn = int(parts[0].split(':')[1])
                events.append((turn, parts[1]))
    
    key_names = {'1':'DL','2':'S','3':'DR','4':'L','6':'R','7':'UL','8':'U','9':'UR',
                 'd':'R','s':'S','a':'L','w':'U','n':'DR','b':'DL','u':'UR','y':'UL',
                 'f':'ATK',' ':'ATK','p':'STATE','v':'AQ','i':'INFO'}
    
    key_freq = Counter(k[1] for k in keys)
    named_freq = {key_names.get(k, k): v for k, v in key_freq.items()}
    
    zones = [(t, e) for t, e in events if 'zone_change' in e]
    kills = [(t, e) for t, e in events if 'demon_kill' in e]
    deaths = [(t, e) for t, e in events if 'death' in e]
    
    print(f"Demo: {filepath}")
    print(f"  Keypresses: {len(keys)}")
    print(f"  Turns: {max(k[0] for k in keys) + 1 if keys else 0}")
    print(f"  Zone changes: {len(zones)}")
    print(f"  Demon kills: {len(kills)}")
    print(f"  Deaths: {len(deaths)}")
    print(f"  Key distribution: {dict(sorted(named_freq.items(), key=lambda x: -x[1])[:8])}")
    
    if zones:
        print(f"  Zone path: {' → '.join(e.split('name=')[1].split()[0] for _, e in zones[:15])}")
    
    return {'keys': keys, 'events': events, 'zones': zones, 'kills': kills}


# ─── MAIN ────────────────────────────────────────────────────

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == '--batch':
            n = int(sys.argv[2]) if len(sys.argv) > 2 else 10
            run_batch(n)
        elif sys.argv[1] == '--demo':
            analyze_demo(sys.argv[2])
        elif sys.argv[1] == '--verbose':
            run_agent_game(verbose=True)
    else:
        r = run_agent_game(verbose=True)
        print(f"\nResult: {r['status']}", file=sys.stderr)
