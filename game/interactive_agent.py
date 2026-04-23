#!/usr/bin/env python3
"""Interactive learning agent — reads state between moves.

Spawns the headless game, sends one move at a time,
reads the state dump after each move, decides the next move.

Interest model: tiles have novelty scores that decay with familiarity.
Known-unknowns (gates seen once, zone boundaries glimpsed) attract most.
Empty explored tiles bore. Demons repel. Mystery attracts.
"""
import subprocess, os, sys, time, re, random
from collections import deque

def run_interactive(player_name="agent", max_turns=800, verbose=True):
    """Run one interactive game session."""
    
    # Start the headless game as a subprocess
    env = {**os.environ, 'NUMOGRAM_PLAYER': player_name}
    proc = subprocess.Popen(
        ['python3', '/home/etym/numogame/numogram_roguelike.py', '--headless', '--hw-entropy'],
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        env=env, text=True, bufsize=1
    )
    time.sleep(0.3)
    
    # === PERSISTENT AGENT MEMORY ===
    # Known-unknowns: gates and zone tiles the agent has EVER seen (persists across state reads)
    known_gates = set()       # (x,y) of gates seen on full map
    known_zones = set()       # (x,y) of zone boundary tiles seen
    demon_kills = set()       # (x,y) where demons were slain (the blood remembers)
    _blacklist = set()        # unreachable ? tiles
    visit_count = {}          # (x,y) -> number of times visited (decays interest)
    turn_count = 0
    
    # Cross-run knowledge: the agent remembers from past runs
    try:
        import json
        with open('/home/etym/numogame/cult.json') as f:
            cult = json.load(f)
        _cult_gates = cult.get('gates_ever_opened', [])
        _cult_zones = cult.get('zones_ever_visited', [])
    except:
        _cult_gates, _cult_zones = [], []
    _has_seen_gates_ever = len(_cult_gates) > 0
    _has_visited_all_zones = len(_cult_zones) >= 10
    
    def parse_state():
        """Read /tmp/numogame_state.txt."""
        try:
            with open("/tmp/numogame_state.txt") as f:
                text = f.read()
        except FileNotFoundError:
            return None
        
        s = {}
        m = re.search(r'Position: \((\d+), (\d+)\)', text)
        if m: s['x'], s['y'] = int(m.group(1)), int(m.group(2))
        m = re.search(r'Zone: (\d+)', text)
        if m: s['zone'] = int(m.group(1))
        m = re.search(r'HP: (\d+)/(\d+)', text)
        if m: s['hp'], s['max_hp'] = int(m.group(1)), int(m.group(2))
        m = re.search(r'Hyperstition: ([\d.]+)%', text)
        if m: s['hyp'] = float(m.group(1))
        m = re.search(r'Turn: (\d+)', text)
        if m: s['turn'] = int(m.group(1))
        
        # Parse EXPLORED MAP
        if '## EXPLORED MAP' in text:
            map_source = text.split('## EXPLORED MAP')[1]
            s['map_rows'] = [l.strip()[1:-1] for l in map_source.split('\n')
                            if l.strip().startswith('!') and len(l.strip()) > 10]
        
        # Parse FULL MAP for known-unknowns (gates, zone boundaries)
        if '## FULL MAP' in text:
            map_section = text.split('## FULL MAP')[1]
            for y, line in enumerate(map_section.split('\n')):
                line = line.strip()
                if line.startswith('!') and len(line) > 10:
                    for x, ch in enumerate(line):
                        if ch == '+':
                            known_gates.add((x-1, y-2))
                        elif ch in '0123456789':
                            known_zones.add((x-1, y-2))
        
        # Gates from known memory (even if not currently visible)
        s['gates'] = list(known_gates)
        
        # Adjacent zones
        adj = re.findall(r'Zone (\d+)', text.split('ZONE MAP ADJACENT')[1]) if 'ZONE MAP ADJACENT' in text else []
        s['adj_zones'] = [int(z) for z in adj]
        
        # Nearby demons
        demons_list = re.findall(r'Mesh-\d+:.*?(\d+) tiles (\w[\w-]*)', text)
        s['nearby_demons'] = [{'dist': int(d[0]), 'dir': d[1]} for d in demons_list]
        
        # Track current position visits
        if 'x' in s and 'y' in s:
            pos = (s['x'], s['y'])
            visit_count[pos] = visit_count.get(pos, 0) + 1
        
        return s
    
    def tile_interest(tx, ty, rows, state):
        """Score a tile's interest/novelty. Higher = more attractive.
        
        Within-run: visit decay, known-unknowns (glimpsed tiles).
        Cross-run: agent remembers from cult.json that gates and zones exist.
        "I know gates exist. This ? might hide one. I will find it."
        """
        if not (0 <= ty < len(rows) and 0 <= tx < len(rows[ty])):
            return -999
        
        tile = rows[ty][tx]
        visits = visit_count.get((tx, ty), 0)
        
        if tile == '#':
            return -999
        
        if tile == '?':
            base = 5.0
            # Cross-run curiosity: agent knows gates exist from past runs
            if _has_seen_gates_ever:
                base += 3.0  # "Gates are real. This mystery might hide one."
            # Within-run known-unknowns
            if (tx, ty) in known_zones:
                base += 8.0
            if (tx, ty) in known_gates:
                base += 12.0
            if (tx, ty) in demon_kills:
                base += 3.0
            if (tx, ty) in _blacklist:
                base = -999
            return base
        
        if tile in '.0123456789+~!%*>':
            base = 1.0 - min(visits * 0.5, 2.0)
            if tile == '+':
                base += 2.0
            if tile == '>':
                base += 8.0  # Stairs — highest priority target
            if tile in '0123456789':
                zone_num = int(tile)
                if zone_num in _cult_zones:
                    base += 0.5  # Already conquered in past runs
                else:
                    base += 3.0  # New zone — strong attractor
            return base
        
        return 0.0
    
    def find_most_interesting_target(state):
        """BFS through explored tiles to find the most interesting reachable ? tile.
        
        Returns (target_x, target_y) or None.
        """
        rows = state.get('map_rows', [])
        if not rows or 'x' not in state:
            return None
        
        px, py = state['x'], state['y']
        
        queue = deque([(px, py)])
        visited_bfs = {(px, py)}
        parent = {}
        
        best_target = None
        best_interest = -1
        
        while queue:
            cx, cy = queue.popleft()
            for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
                nx, ny = cx + dx, cy + dy
                if (nx, ny) in visited_bfs:
                    continue
                if not (0 <= nx < 78 and 0 <= ny < len(rows)):
                    continue
                if ny >= len(rows) or nx >= len(rows[ny]):
                    continue
                
                tile = rows[ny][nx]
                if tile == '#':
                    continue
                
                if tile == '?':
                    interest = tile_interest(nx, ny, rows, state)
                    if interest > best_interest:
                        best_target = (nx, ny)
                        best_interest = interest
                        parent[(nx, ny)] = (cx, cy)
                    elif best_target is None:
                        best_target = (nx, ny)
                        parent[(nx, ny)] = (cx, cy)
                elif tile == '>':
                    # Stairs — always target, high priority
                    interest = tile_interest(nx, ny, rows, state)
                    if interest > best_interest:
                        best_target = (nx, ny)
                        best_interest = interest
                        parent[(nx, ny)] = (cx, cy)
                elif tile in '.0123456789+~!%*':
                    visited_bfs.add((nx, ny))
                    parent[(nx, ny)] = (cx, cy)
                    queue.append((nx, ny))
        
        if not best_target:
            return None
        
        # Blacklist unreachable targets
        _blacklist.add(best_target)
        if len(_blacklist) > 200:
            _blacklist.clear()
        
        # Backtrace to first step
        current = best_target
        while current != (px, py) and current in parent:
            prev = parent[current]
            if prev == (px, py):
                dx, dy = current[0] - px, current[1] - py
                move_map = {(1,0): 'd', (-1,0): 'a', (0,1): 's', (0,-1): 'w',
                            (1,1): 'n', (-1,1): 'b', (1,-1): 'u', (-1,-1): 'y'}
                return move_map.get((dx, dy), '')
            current = prev
        return None
    
    def flee_direction(demon_info):
        """Flee from a demon."""
        d = demon_info
        flee = {'north':'s','south':'w','east':'a','west':'d',
                'north-east':'b','north-west':'n','south-east':'y','south-west':'u'}
        return flee.get(d.get('dir',''), 'w')
    
    def gate_direction(state):
        """Walk toward nearest known gate."""
        if not state.get('gates') or 'x' not in state:
            return None
        px, py = state['x'], state['y']
        # Filter to gates not at current position
        reachable_gates = [(gx,gy) for gx,gy in state['gates'] if (gx,gy) != (px,py)]
        if not reachable_gates:
            return None
        gx, gy = min(reachable_gates, key=lambda g: abs(g[0]-px) + abs(g[1]-py))
        dx, dy = gx - px, gy - py
        if abs(dx) >= abs(dy):
            return ('d' if dx > 0 else 'a')
        else:
            return ('s' if dy > 0 else 'w')
    
    def _stair_direction(state):
        """Walk toward stairs '>' visible on the map."""
        rows = state.get('map_rows', [])
        if not rows or 'x' not in state:
            return None
        px, py = state['x'], state['y']
        # Search full map for '>' tiles
        stairs = []
        for ry, row in enumerate(rows):
            for rx, ch in enumerate(row):
                if ch == '>':
                    stairs.append((rx, ry))
        if not stairs:
            return None
        # Nearest stairs
        sx, sy = min(stairs, key=lambda s: abs(s[0]-px) + abs(s[1]-py))
        dx, dy = sx - px, sy - py
        if abs(dx) >= abs(dy):
            return ('d' if dx > 0 else 'a') * min(abs(dx), 8)
        else:
            return ('s' if dy > 0 else 'w') * min(abs(dy), 8)
    
    def _adjacent_stair(state):
        """Check if stairs are adjacent — step onto them."""
        rows = state.get('map_rows', [])
        if not rows or 'x' not in state:
            return None
        px, py = state['x'], state['y']
        for dx, dy, ch in [(1,0,'d'), (-1,0,'a'), (0,1,'s'), (0,-1,'w')]:
            nx, ny = px + dx, py + dy
            if 0 <= ny < len(rows) and 0 <= nx < len(rows[ny]):
                if rows[ny][nx] == '>':
                    return ch
        return None
    def _corridor_fallback(state):
        """Find best corridor direction from explored map. From learning agent."""
        rows = state.get('map_rows', [])
        if not rows or 'x' not in state:
            return random.choice(['d', 'a', 's', 'w'])
        px, py = state['x'], state['y']
        best_dir = None
        best_score = -1
        for dx, dy, ch in [(1,0,'d'), (-1,0,'a'), (0,1,'s'), (0,-1,'w'),
                            (1,1,'n'), (-1,1,'b'), (1,-1,'u'), (-1,-1,'y')]:
            score = 0
            unknown_count = 0
            for dist in range(1, 10):
                mx, my = px + dx * dist, py + dy * dist
                if 0 <= mx < 78 and 0 <= my < len(rows):
                    if my < len(rows) and mx < len(rows[my]):
                        tile = rows[my][mx]
                        if tile in '.0123456789+~*>':
                            score += 1
                            if tile in '0123456789':
                                score += 3
                            if tile == '+':
                                score += 5
                            if tile == '>':
                                score += 10  # Stairs — highest priority
                        elif tile == '?':
                            score += 2  # Unknown tiles are attractive
                            unknown_count += 1
                        else:
                            break
                    else:
                        break
                else:
                    break
            # Bonus for directions with more unknown tiles (push toward edge)
            score += unknown_count * 2
            if score > best_score:
                best_score = score
                best_dir = ch
        return best_dir or random.choice(['d', 'a', 's', 'w'])
    proc.stdin.write('p\n')
    proc.stdin.flush()
    time.sleep(0.1)
    state = parse_state()
    
    while turn_count < max_turns and state:
        hp_pct = state.get('hp', 0) / max(state.get('max_hp', 1), 1)
        
        # === DECISION HIERARCHY ===
        move = ''
        
        # 1. SURVIVE: flee from demons at low HP
        if hp_pct < 0.25 and state.get('nearby_demons'):
            move = flee_direction(state['nearby_demons'][0]) * 3
        
        # 2. FIGHT: attack adjacent demon if healthy
        elif hp_pct > 0.5 and state.get('nearby_demons') and state['nearby_demons'][0].get('dist', 99) <= 1:
            move = 'f' * 2
        
        # 3. EXPLORE: interest-driven auto-explore
        else:
            # Check if stairs adjacent — step onto them directly
            sd = _adjacent_stair(state)
            if sd:
                move = sd
            else:
                step = find_most_interesting_target(state)
                if step:
                    # Anti-oscillation: if current tile visited many times, try corridor
                    pos = (state.get('x', 0), state.get('y', 0))
                    visits = visit_count.get(pos, 0)
                    if visits > 4:
                        cf = _corridor_fallback(state)
                        if cf:
                            move = cf
                        else:
                            move = step
                    else:
                        move = step
                else:
                    # Fully explored — check for stairs first, then gates, then corridor
                    sd = _stair_direction(state)
                    if sd:
                        move = sd
                    else:
                        gd = gate_direction(state)
                        if gd:
                            move = gd
                        else:
                            # Corridor-based fallback (from learning agent)
                            move = _corridor_fallback(state)
        
        # Send move
        for ch in move:
            proc.stdin.write(ch)
            proc.stdin.flush()
            time.sleep(0.02)
            turn_count += 1
        
        # Dump state (must include \n — headless reads line-by-line)
        proc.stdin.write('p\n')
        proc.stdin.flush()
        time.sleep(0.05)
        
        state = parse_state()
        if state and verbose and turn_count % 20 == 0:
            z = state.get('zone','?')
            print(f"  [T:{turn_count}] Z{z} ({state.get('x','?')},{state.get('y','?')}) "
                  f"HP:{state.get('hp','?')} Hyp:{state.get('hyp',0):.0f}% "
                  f"Gates:{len(known_gates)} KnownZ:{len(known_zones)}",
                  file=sys.stderr)
        
        if state and state.get('hp', 0) <= 0:
            break
    
    # Quit
    try:
        proc.stdin.write('q\n')
        proc.stdin.flush()
    except:
        pass
    
    proc.wait(timeout=300)
    
    stderr = proc.stderr.read()
    last = [l for l in stderr.split('\n') if l.startswith('[T:') or l.startswith('SAVED') or l.startswith('DEAD')]
    
    return last


if __name__ == "__main__":
    print("Starting interest-driven learning agent...", file=sys.stderr)
    result = run_interactive(verbose=True)
    for line in result:
        print(line, file=sys.stderr)
