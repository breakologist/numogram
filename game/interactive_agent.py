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
        ['python3', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'numogram_roguelike.py'), '--headless', '--hw-entropy'],
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
        with open(os.path.expanduser('~/numogame/cult.json')) as f:
            cult = json.load(f)
        _cult_gates = cult.get('gates_ever_opened', [])
        _cult_zones = cult.get('zones_ever_visited', [])
    except:
        _cult_gates, _cult_zones = [], []
    _has_seen_gates_ever = len(_cult_gates) > 0
    _has_visited_all_zones = len(_cult_zones) >= 10
    
    def parse_state():
        """Read /tmp/numogame_state.txt."""
        import re
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
            # Stop at next section header
            next_header = re.search(r'\n## [A-Z]', map_source)
            if next_header:
                map_source = map_source[:next_header.start()]
            s['map_rows'] = []
            for line in map_source.split('\n'):
                line = line.strip()
                if line.startswith('!') and len(line) > 10:
                    inner = line[1:-1]
                    if set(inner) == {'-'}:
                        continue
                    s['map_rows'].append(inner)
        
        # Parse FULL MAP for perfect pathfinding when stuck
        if '## FULL MAP' in text:
            map_section = text.split('## FULL MAP')[1]
            # Stop at next section header (## followed by space and uppercase)
            next_header = re.search(r'\n## [A-Z]', map_section)
            if next_header:
                map_section = map_section[:next_header.start()]
            full_rows = []
            map_y = 0
            for y, line in enumerate(map_section.split('\n')):
                line = line.strip()
                if line.startswith('!') and len(line) > 10:
                    # Skip top and bottom border rows (dashes only)
                    inner = line[1:-1]
                    if set(inner) == {'-'}:
                        continue
                    full_rows.append(inner)
                    for x, ch in enumerate(line):
                        if ch == '+':
                            known_gates.add((x-1, map_y))
                        elif ch in '0123456789':
                            known_zones.add((x-1, map_y))
                    map_y += 1
            s['full_map_rows'] = full_rows
        
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
            # Heuristic: if surrounded by 3+ walls, it's probably a wall tile
            wall_count = 0
            for ddx, ddy in [(1,0), (-1,0), (0,1), (0,-1)]:
                nx, ny = tx + ddx, ty + ddy
                if 0 <= nx < len(rows[0]) and 0 <= ny < len(rows):
                    if rows[ny][nx] == '#':
                        wall_count += 1
            if wall_count >= 3:
                return -999  # Almost certainly a wall
            
            # Favor tiles farther from center (push toward map edges / stairs)
            dist_from_start = abs(tx - 39) + abs(ty - 11)
            base += min(dist_from_start * 0.2, 10.0)
            
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
        """Find next exploration target using FULL MAP BFS.
        
        The explored map tells us what's unknown ('?').
        The full map tells us what's actually passable.
        Together they give perfect pathfinding to nearest unexplored."""
        explored_rows = state.get('map_rows', [])
        full_rows = state.get('full_map_rows', [])
        if not explored_rows or not full_rows or 'x' not in state:
            return None
        
        px, py = state['x'], state['y']
        
        # First: check adjacent unexplored on explored map
        for dx, dy, ch in [(1,0,'d'), (-1,0,'a'), (0,1,'s'), (0,-1,'w')]:
            nx, ny = px + dx, py + dy
            if 0 <= ny < len(explored_rows) and 0 <= nx < len(explored_rows[ny]):
                if explored_rows[ny][nx] == '?' and ch not in failed_dirs.get((px,py), set()):
                    # Verify it's actually passable on full map
                    if 0 <= ny < len(full_rows) and 0 <= nx < len(full_rows[ny]):
                        if full_rows[ny][nx] in '.>+0123456789':
                            return ch
        
        # BFS on full map to nearest '?' in explored map
        queue = deque([(px, py)])
        visited = {(px, py)}
        parent = {}
        
        while queue:
            cx, cy = queue.popleft()
            for dx, dy, ch in [(1,0,'d'), (-1,0,'a'), (0,1,'s'), (0,-1,'w')]:
                nx, ny = cx + dx, cy + dy
                if (nx, ny) in visited:
                    continue
                if not (0 <= nx < len(full_rows[0]) and 0 <= ny < len(full_rows)):
                    continue
                
                ftile = full_rows[ny][nx] if nx < len(full_rows[ny]) else '#'
                if ftile not in '.>+0123456789':
                    continue
                
                visited.add((nx, ny))
                parent[(nx, ny)] = (cx, cy, ch)
                
                # Check if this tile is unexplored OR stairs
                if 0 <= ny < len(explored_rows) and 0 <= nx < len(explored_rows[ny]):
                    etile = explored_rows[ny][nx]
                    if etile == '?' or etile == '>':
                        # Backtrace to first step from player
                        current = (nx, ny)
                        first_step = None
                        while current in parent:
                            px2, py2, step = parent[current]
                            if px2 == px and py2 == py:
                                first_step = step
                                break
                            current = (px2, py2)
                        if first_step and first_step not in failed_dirs.get((px,py), set()):
                            return first_step
                
                queue.append((nx, ny))
        
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
        """Walk one step toward stairs '>' visible on the explored map."""
        rows = state.get('map_rows', [])
        if not rows or 'x' not in state:
            return None
        px, py = state['x'], state['y']
        stairs = []
        for ry, row in enumerate(rows):
            for rx, ch in enumerate(row):
                if ch == '>':
                    stairs.append((rx, ry))
        if not stairs:
            return None
        # Nearest stairs by Manhattan distance
        sx, sy = min(stairs, key=lambda s: abs(s[0]-px) + abs(s[1]-py))
        dx, dy = sx - px, sy - py
        # Return single keypress toward stairs (re-evaluate next turn)
        if abs(dx) >= abs(dy):
            return 'd' if dx > 0 else 'a'
        else:
            return 's' if dy > 0 else 'w'
    
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
    def _nuclear_bfs_to_unexplored(state, full_rows, px, py):
        """BFS on full map to find nearest tile that is unexplored in explored map.
        Returns single keypress direction toward it, or None."""
        explored_rows = state.get('map_rows', [])
        if not explored_rows or not full_rows:
            return None
        
        # Get directions already proven to fail from current position
        current_pos = (px, py)
        local_fails = failed_dirs.get(current_pos, set())
        
        queue = deque([(px, py)])
        visited = {(px, py)}
        parent = {}
        
        while queue:
            cx, cy = queue.popleft()
            for dx, dy, ch in [(1,0,'d'), (-1,0,'a'), (0,1,'s'), (0,-1,'w')]:
                nx, ny = cx + dx, cy + dy
                if (nx, ny) in visited:
                    continue
                if not (0 <= nx < len(full_rows[0]) and 0 <= ny < len(full_rows)):
                    continue
                
                # Full map tells us what's passable
                ftile = full_rows[ny][nx] if nx < len(full_rows[ny]) else '#'
                if ftile not in '.>+0123456789':
                    continue
                
                visited.add((nx, ny))
                parent[(nx, ny)] = (cx, cy, ch)
                
                # Check if this tile is unexplored in the explored map
                if 0 <= ny < len(explored_rows) and 0 <= nx < len(explored_rows[ny]):
                    etile = explored_rows[ny][nx]
                    if etile == '?':
                        # Found unexplored! Backtrace to first step
                        current = (nx, ny)
                        first_step = None
                        while current in parent:
                            px2, py2, step = parent[current]
                            if px2 == px and py2 == py:
                                first_step = step
                                break
                            current = (px2, py2)
                        # Don't return a first step we know fails
                        if first_step and first_step not in local_fails:
                            return first_step
                        # If first step fails, keep searching for another path
                
                queue.append((nx, ny))
        
        return None
    
    def _corridor_fallback(state, avoid_dir=None):
        """Find best corridor direction from explored map. Optionally avoid one direction."""
        rows = state.get('map_rows', [])
        if not rows or 'x' not in state:
            return random.choice(['d', 'a', 's', 'w'])
        px, py = state['x'], state['y']
        best_dir = None
        best_score = -1
        dirs = [(1,0,'d'), (-1,0,'a'), (0,1,'s'), (0,-1,'w')]
        for dx, dy, ch in dirs:
            if avoid_dir and ch == avoid_dir:
                continue
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
                                score += 10
                        elif tile == '?':
                            score += 2
                            unknown_count += 1
                        else:
                            break
                    else:
                        break
                else:
                    break
            score += unknown_count * 2
            if score > best_score:
                best_score = score
                best_dir = ch
        return best_dir or random.choice(['d', 'a', 's', 'w'])
    # Track stuck state and failed directions
    last_pos = None
    stuck_count = 0
    last_move_dir = None
    failed_dirs = {}  # (x,y) -> set of directions that failed from this position
    wall_map = set()  # (x,y) tiles we've proven are walls by failed movement
    escape_mode = 0   # turns remaining in escape mode (random walk after being stuck)
    recent_positions = deque(maxlen=20)  # For oscillation detection
    
    proc.stdin.write('p\n')
    proc.stdin.flush()
    time.sleep(0.1)
    state = parse_state()
    
    while turn_count < max_turns and state:
        hp_pct = state.get('hp', 0) / max(state.get('max_hp', 1), 1)
        
        # Detect if we're stuck (same position as last turn)
        current_pos = (state.get('x', 0), state.get('y', 0))
        recent_positions.append(current_pos)
        
        # Oscillation detection: check if we're bouncing between same positions
        oscillating = False
        if len(recent_positions) >= 10:
            # Check if the last 10 positions form a short cycle (2-4 unique positions)
            unique_recent = set(list(recent_positions)[-10:])
            if len(unique_recent) <= 3:
                oscillating = True
        
        if last_pos == current_pos or oscillating:
            if oscillating and last_pos != current_pos:
                stuck_count += 1  # Treat oscillation as being stuck
            elif last_pos == current_pos:
                stuck_count += 1
            if last_move_dir:
                failed_dirs.setdefault(current_pos, set()).add(last_move_dir)
                dir_map = {'d': (1,0), 'a': (-1,0), 's': (0,1), 'w': (0,-1)}
                if last_move_dir in dir_map:
                    dx, dy = dir_map[last_move_dir]
                    wall_map.add((current_pos[0] + dx, current_pos[1] + dy))
        else:
            stuck_count = 0
            last_move_dir = None
        last_pos = current_pos
        
        # Decrement escape mode
        if escape_mode > 0:
            escape_mode -= 1
        
        # === DECISION HIERARCHY ===
        move = ''
        
        # 0. ESCAPE MODE: if stuck for 3+ turns, break out using least-visited gradient
        if escape_mode > 0 or stuck_count >= 3:
            if stuck_count >= 3:
                escape_mode = 10
            local_fails = failed_dirs.get(current_pos, set())
            options = [d for d in ['d', 'a', 's', 'w'] if d not in local_fails]
            
            # DEAD END ESCAPE: if oscillating in a tiny loop or fully blocked,
            # use the FULL MAP to BFS toward the nearest unexplored tile.
            # The full map has complete wall/floor info — no more guessing.
            if stuck_count >= 5 or len(options) <= 1:
                full_rows = state.get('full_map_rows', [])
                px, py = state.get('x', 0), state.get('y', 0)
                
                # If oscillating (stuck building up while moving), skip local
                # adjacent check — it just finds the other end of the oscillation.
                # Go straight to nuclear BFS for global path to unexplored.
                if stuck_count >= 10:
                    move = _nuclear_bfs_to_unexplored(state, full_rows, px, py)
                    if move:
                        last_move_dir = move
                    else:
                        move = random.choice(['d', 'a', 's', 'w'])
                        last_move_dir = move
                else:
                    best_dir = None
                    best_dist = float('inf')
                    
                    # Try each direction: use full map to see if it's floor
                    for dx, dy, ch in [(1,0,'d'), (-1,0,'a'), (0,1,'s'), (0,-1,'w')]:
                        if ch in local_fails:
                            continue  # Skip proven-failed directions
                        nx, ny = px + dx, py + dy
                        if 0 <= ny < len(full_rows) and 0 <= nx < len(full_rows[ny]):
                            tile = full_rows[ny][nx]
                            # On full map: . = floor, > = stairs, + = gate, 0-9 = zone
                            if tile in '.>+0123456789':
                                v = visit_count.get((nx, ny), 0)
                                dist = v  # least visited = best
                                if dist < best_dist:
                                    best_dist = dist
                                    best_dir = ch
                    
                    if best_dir:
                        move = best_dir
                        last_move_dir = best_dir
                    else:
                        # True nuclear option: BFS on full map to nearest unexplored
                        # tile in the explored map, then take first step
                        move = _nuclear_bfs_to_unexplored(state, full_rows, px, py)
                        if move:
                            last_move_dir = move
                        else:
                            move = random.choice(['d', 'a', 's', 'w'])
                            last_move_dir = move
            elif options:
                move = random.choice(options)
                last_move_dir = move
            else:
                move = random.choice(['d', 'a', 's', 'w'])
                last_move_dir = move
        # 1. SURVIVE: flee from demons at low HP
        elif hp_pct < 0.25 and state.get('nearby_demons'):
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
                    # Avoid directions known to fail from this position
                    local_fails = failed_dirs.get(current_pos, set())
                    if step in local_fails:
                        # Try corridor fallback avoiding failed directions
                        cf = _corridor_fallback(state, avoid_dir=step)
                        if cf and cf not in local_fails:
                            move = cf
                            last_move_dir = cf
                        else:
                            # Try any direction not failed
                            for d in ['d', 'a', 's', 'w']:
                                if d not in local_fails:
                                    move = d
                                    last_move_dir = d
                                    break
                            if not move:
                                # ALL directions failed — use nuclear BFS
                                full_rows = state.get('full_map_rows', [])
                                px, py = state.get('x', 0), state.get('y', 0)
                                move = _nuclear_bfs_to_unexplored(state, full_rows, px, py)
                                if move:
                                    last_move_dir = move
                                else:
                                    # Truly trapped — random
                                    move = random.choice(['d', 'a', 's', 'w'])
                                    last_move_dir = move
                    else:
                        move = step
                        last_move_dir = step
                else:
                    # No local targets — use nuclear BFS on full map to find
                    # nearest unexplored territory. This is the key to traversing
                    # large tree dungeons where unexplored areas are far away.
                    full_rows = state.get('full_map_rows', [])
                    px, py = state.get('x', 0), state.get('y', 0)
                    move = _nuclear_bfs_to_unexplored(state, full_rows, px, py)
                    if move:
                        last_move_dir = move
                    else:
                        # Truly everything explored — random walk
                        escape_mode = 20
                        local_fails = failed_dirs.get(current_pos, set())
                        options = [d for d in ['d', 'a', 's', 'w'] if d not in local_fails]
                        if not options:
                            options = ['d', 'a', 's', 'w']
                        move = random.choice(options)
                        last_move_dir = move
        
        # Send move (headless reads one command per line, takes first char)
        if move:
            if turn_count % 20 == 0 or stuck_count > 0:
                local_fails = failed_dirs.get(current_pos, set())
                print(f"  [DEBUG T:{turn_count}] move='{move[0]}' pos={current_pos} "
                      f"stuck={stuck_count} fails={local_fails} "
                      f"blacklist={len(_blacklist)}", file=sys.stderr)
            proc.stdin.write(move[0] + '\n')
            proc.stdin.flush()
            time.sleep(0.1)
            turn_count += 1
        else:
            # Debug: log when move is empty
            local_fails = failed_dirs.get(current_pos, set())
            print(f"  [DEBUG T:{turn_count}] EMPTY MOVE — pos={current_pos} "
                  f"stuck={stuck_count} fails={local_fails} "
                  f"blacklist={len(_blacklist)}", file=sys.stderr)

        # Dump state
        proc.stdin.write('p\n')
        proc.stdin.flush()
        time.sleep(0.15)
        
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
