#!/usr/bin/env python3
"""Rogue Agent v9 — The Hungry Borg: wall-aware, corridor-following.

Fixes from v8:
- Wall oscillation: detect no-movement, blacklist direction, try next
- Corridor following: walk toward corridor endpoints (room entrances)
- Dijkstra threat avoidance: compute distance from walls, prefer high-distance tiles
- Running: only run in open areas (8+ adjacent passable), walk near walls
"""
import subprocess, time, re, os, json
from collections import deque

class TmuxGame:
    def __init__(self, session, command, w=80, h=24):
        self.session = session
        subprocess.run(['tmux','kill-session','-t',session], capture_output=True)
        env = os.environ.copy(); env['TERM'] = 'xterm-256color'
        subprocess.run(['tmux','new-session','-d','-s',session,'-x',str(w),'-y',str(h),command], env=env)
        time.sleep(3)
    def capture(self):
        return subprocess.run(['tmux','capture-pane','-t',self.session,'-p'], capture_output=True, text=True).stdout
    def send(self, k):
        subprocess.run(['tmux','send-keys','-t',self.session,k], capture_output=True)
    def quit(self):
        self.send('Q'); time.sleep(0.3); self.send('y'); time.sleep(0.5)
        subprocess.run(['tmux','kill-session','-t',self.session], capture_output=True)

class Screen:
    WALLS = set('|-'); DOOR = '+'; FLOOR = '.'; CORRIDOR = '#'
    STAIRS_DOWN = '>'; MONSTERS = set('HSEBIAROTLNFMDGCWXYjZJKU'); ITEMS = set('!?)]/=*:^')
    
    def __init__(self, raw):
        self.raw = raw; self.lines = raw.split('\n')
        self.pos = None; self.monsters = []; self.items = []
        self.walls = set(); self.floors = set(); self.doors = set()
        self.corridors = set(); self.stairs = None; self.status = {}
        self.game_over = any(p in raw for p in ['R.I.P.','killed by','IN PEACE','Score:'])
        if not self.game_over: self._parse()
    
    def _parse(self):
        ms = me = None
        for i, line in enumerate(self.lines):
            s = line.rstrip()
            if any(c in s for c in '|-@#>+'):
                if ms is None: ms = i
                me = i
        if ms is None: return
        for y in range(ms, (me or ms)+1):
            line = self.lines[y] if y < len(self.lines) else ''
            for x, ch in enumerate(line):
                if ch == '@': self.pos = (x,y)
                elif ch in self.ITEMS: self.items.append((x,y,ch))
                elif ch == self.CORRIDOR: self.corridors.add((x,y))
                elif ch == self.FLOOR: self.floors.add((x,y))
                elif ch in self.WALLS: self.walls.add((x,y))
                elif ch == self.DOOR: self.doors.add((x,y))
                elif ch == self.STAIRS_DOWN: self.stairs = (x,y); self.floors.add((x,y))
                elif ch in self.MONSTERS: self.monsters.append((x,y,ch))
        for line in reversed(self.lines):
            if 'Level:' in line: self._status(line.strip()); break
    
    def _status(self, line):
        for k,p in [('level',r'Level:\s*(\d+)'),('gold',r'Gold:\s*(\d+)'),
                    ('hp',r'Hp:\s*(\d+)\((\d+)\)'),('armor',r'Arm:\s*(\d+)'),
                    ('exp',r'Exp:\s*(\d+)/(\d+)')]:
            m = re.search(p, line)
            if m:
                if k=='hp': self.status['hp']=int(m.group(1)); self.status['max_hp']=int(m.group(2))
                elif k=='exp': self.status['el']=int(m.group(1)); self.status['ep']=int(m.group(2))
                else: self.status[k]=int(m.group(1))
    
    def adj(self, a, b): return max(abs(a[0]-b[0]),abs(a[1]-b[1]))<=1
    def passable(self): return self.floors|self.corridors|self.doors|({self.stairs} if self.stairs else set())

class Agent:
    """Wall-aware, corridor-following agent with Dijkstra threat avoidance."""
    def __init__(self, game):
        self.game = game; self.turn = 0; self.visited = set()
        self.vcount = {}; self.stuck = 0; self.last = None; self.depth = 1
        self.known_floors = set(); self.known_doors = set()
        self.known_corridors = set(); self.known_walls = set(); self.known_stairs = None
        self.unreachable = set(); self.last_action = ''; self.corridors = []
        self.tried_directions = set()
        self.action_history = []
        self.plex_goal = None
        self.plex_turns = 0
        self.committed_target = None  # DFS: committed destination
        self.committed_steps = 0  # steps taken toward committed target
        self._load_memory()
    
    def _load_memory(self):
        self.memory = {
            'runs':0, 'max_depth':0, 'total_gold':0, 'deaths':[],
            'doors_walked':0, 'knows_doors':True, 'knows_running':True,
            'knows_stairs': True,  # stairs always exist — learn from any run
            'knows_autopickup': True,  # Rogue has autopickup
            'items_found': 0,  # items picked up across runs
        }
        try:
            with open(os.path.expanduser('~/.rogue_memory.json')) as f:
                self.memory = json.load(f)
        except: pass
    
    def _save_memory(self):
        self.memory['runs'] += 1
        self.memory['max_depth'] = max(self.memory['max_depth'], self.depth)
        self.memory['knows_stairs'] = True  # always remember stairs exist
        try:
            with open(os.path.expanduser('~/.rogue_memory.json'), 'w') as f:
                json.dump(self.memory, f, indent=2)
        except: pass
    
    def run(self, max_turns=500):
        for t in range(max_turns):
            self.turn = t
            raw = self.game.capture(); s = Screen(raw)
            if not s.pos and not s.game_over:
                time.sleep(0.2); raw = self.game.capture(); s = Screen(raw)
            if '--More--' in raw: self.game.send(' '); time.sleep(0.1); continue
            if s.game_over or (s.status.get('hp',1)<=0 and s.pos):
                print(f'DEAD turn {t} depth {self.depth}'); break
            if not s.pos: self.game.send('s'); time.sleep(0.1); continue
            
            px,py = s.pos; self.visited.add(s.pos)
            self.vcount[s.pos] = self.vcount.get(s.pos,0)+1
            self.known_floors |= s.floors; self.known_corridors |= s.corridors
            self.known_doors |= s.doors; self.known_walls |= s.walls
            if s.stairs: self.known_stairs = s.stairs
            self._detect_corridors(s)
            
            # Stuck detection — position unchanged (not resting)
            if s.pos == self.last and self.last_action != '.':
                self.stuck += 1
            elif s.pos != self.last:
                self.stuck = 0
                self.tried_directions.clear()
                self.recent_positions.clear() if hasattr(self, 'recent_positions') else None
            self.last = s.pos
            
            # PLEX DETECTION: position oscillation folds into exit-seeking
            self.action_history.append(s.pos)
            if len(self.action_history) > 20:
                self.action_history.pop(0)
            if self.plex_turns > 0:
                self.plex_turns -= 1
            elif len(self.action_history) >= 12:
                from collections import Counter
                counts = Counter(self.action_history[-12:])
                if len(counts) <= 3:
                    # SYZYGy: oscillation detected. Don't break it — ride it.
                    # Follow the syzygy current outward. Pick one direction and COMMIT.
                    self.plex_turns = 20
                    # Determine which direction the syzygy extends
                    xs = [p[0] for p in counts.keys()]
                    ys = [p[1] for p in counts.keys()]
                    # Run along the dominant axis
                    if max(xs)-min(xs) > max(ys)-min(ys):
                        # Horizontal syzygy — ride it left or right
                        self.plex_goal = 'ride_h'
                    else:
                        # Vertical syzygy — ride it up or down
                        self.plex_goal = 'ride_v'
                    self.action_history.clear()
            
            # Stagnation/oscillation detection — triggers plex (syzygy riding)
            if not hasattr(self, 'recent_positions'):
                self.recent_positions = []
            self.recent_positions.append(s.pos)
            if len(self.recent_positions) > 20:
                self.recent_positions.pop(0)
            
            if len(self.recent_positions) >= 12:
                from collections import Counter
                pos_counts = Counter(self.recent_positions[-12:])
                unique_positions = len(pos_counts)
                
                # STAGNATION: same position for 8+ of last 12 turns
                most_common_pos, count = pos_counts.most_common(1)[0]
                if count >= 8:
                    self.plex_turns = 15
                    self.plex_goal = 'oblique'  # oblique strategy — try something different
                    self.recent_positions.clear()
                
                # OSCILLATION: 2-3 unique positions in 12 turns
                elif unique_positions <= 3 and self.plex_turns <= 0:
                    xs = [p[0] for p in pos_counts.keys()]
                    ys = [p[1] for p in pos_counts.keys()]
                    self.plex_turns = 20
                    if max(xs)-min(xs) > max(ys)-min(ys):
                        self.plex_goal = 'ride_h'
                    else:
                        self.plex_goal = 'ride_v'
                    self.recent_positions.clear()
            
            if t % 25 == 0:
                hp = s.status.get('hp','?')
                print(f'T:{t:3d} D:{self.depth} @({px:2d},{py:2d}) HP:{hp} F:{len(s.floors)} C:{len(s.corridors)} D:{len(s.doors)} S:{"Y" if s.stairs else "n"} stuck:{self.stuck}')
            
            act = self._decide(s)
            self.last_action = act
            self.game.send(act); time.sleep(0.12)
        self._save_memory()
        print(f'Finished depth {self.depth}')
    
    def _detect_corridors(self, s):
        all_corridors = self.known_corridors | (s.corridors if s else set())
        all_floors = self.known_floors | (s.floors if s else set())
        all_doors = self.known_doors | (s.doors if s else set())
        visited = set(); self.corridors = []
        for tile in all_corridors:
            if tile in visited: continue
            corr_tiles = set(); queue = [tile]
            while queue:
                cx, cy = queue.pop()
                if (cx,cy) in visited or (cx,cy) not in all_corridors: continue
                visited.add((cx,cy)); corr_tiles.add((cx,cy))
                for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
                    if (cx+dx,cy+dy) in all_corridors and (cx+dx,cy+dy) not in visited:
                        queue.append((cx+dx,cy+dy))
            if len(corr_tiles) < 2: continue
            endpoints = set()
            for (cx,cy) in corr_tiles:
                for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
                    nx,ny = cx+dx,cy+dy
                    if (nx,ny) in all_floors or (nx,ny) in all_doors:
                        endpoints.add((nx,ny))
            self.corridors.append({'tiles':corr_tiles,'endpoints':endpoints,'length':len(corr_tiles)})
    
    def _decide(self, s):
        px,py = s.pos; hp = s.status.get('hp',100); mx = s.status.get('max_hp',100)
        pct = hp/max(mx,1); passable = s.passable()
        DANGER = set('DHMTAGICFRXYZNU')
        
        # 0. COMMITTED PATH — follow DFS target (override everything except critical HP)
        if self.committed_target and pct > 0.2:
            tx, ty = self.committed_target
            dist = abs(tx-px) + abs(ty-py)
            if dist == 0:
                self.committed_target = None
                self.committed_steps = 0
            elif self.committed_steps > 60:
                self.committed_target = None
                self.committed_steps = 0
            else:
                self.committed_steps += 1
                self._last_target_dist = dist
                return self._move(tx-px, ty-py, s, run=True)
        
        # 0b. PLEX MODE — syzygy riding and oblique strategies
        if self.plex_turns > 0:
            if self.plex_goal == 'exit':
                exits = list(s.doors | self.known_doors | s.corridors | self.known_corridors)
                if s.stairs: exits.append(s.stairs)
                if self.known_stairs: exits.append(self.known_stairs)
                if exits:
                    nearest = min(exits, key=lambda e: abs(e[0]-px)+abs(e[1]-py))
                    return self._move(nearest[0]-px, nearest[1]-py, s, run=True)
            elif self.plex_goal in ('ride_h', 'ride_v'):
                # SYZYGy RIDING: commit to one direction along the syzygy axis
                import random
                if self.plex_goal == 'ride_h':
                    return random.choice(['L','H'])  # run horizontally
                else:
                    return random.choice(['J','K'])  # run vertically
            elif self.plex_goal == 'oblique':
                # OBLIQUE STRATEGY: creative intervention
                strategies = [
                    's',  # search (look for secret doors)
                    'v',  # check AQ (if implemented)
                    '.',  # rest (do nothing — let the world come to you)
                    random.choice(['L','H','J','K']),  # run in a random direction
                ]
                return random.choice(strategies)
        
        # 1. FLEE — always flee from dangerous monsters below 50%, any monster below 40%
        for mpx,mpy,ch in s.monsters:
            if s.adj(s.pos,(mpx,mpy)):
                threshold = 0.55 if ch in DANGER else 0.4
                if pct < threshold:
                    # Flee toward the nearest exit, not just away from monster
                    flee_dx, flee_dy = px-mpx, py-mpy
                    # Check if fleeing toward an exit
                    exits = list(s.doors | self.known_doors | s.corridors | self.known_corridors)
                    if exits:
                        nearest_exit = min(exits, key=lambda e: abs(e[0]-px)+abs(e[1]-py))
                        exit_dx, exit_dy = nearest_exit[0]-px, nearest_exit[1]-py
                        # If exit is roughly in flee direction, go to exit
                        if flee_dx*exit_dx >= 0 and flee_dy*exit_dy >= 0:
                            return self._move(exit_dx, exit_dy, s, run=True)
                    # Otherwise flee away from monster
                    return self._move(flee_dx, flee_dy, s, run=False)
        
        # 2. FIGHT — only fight when healthy (>60% HP)
        if pct > 0.6:
            for mpx,mpy,ch in s.monsters:
                if s.adj(s.pos,(mpx,mpy)):
                    return self._move(mpx-px, mpy-py, s, run=False)
        
        # 3. HEAL
        if pct < 0.4 and not s.monsters: return '.'
        
        # 4. STAIRS
        if s.stairs:
            if s.pos == s.stairs: self.depth += 1; return '>'
            if s.adj(s.pos, s.stairs): return self._move(s.stairs[0]-px, s.stairs[1]-py, s, run=False)
        
        # 4b. COMMITTED PATH — follow branch to its end (DFS tree traversal)
        if self.committed_target:
            tx, ty = self.committed_target
            dist = abs(tx-px) + abs(ty-py)
            
            # Reached target — run AWAY from it (prevent oscillation)
            if dist == 0:
                # Find the farthest unvisited endpoint and commit to it
                self.committed_target = None
                self.committed_steps = 0
                # Don't re-evaluate immediately — keep running in same direction for 3 turns
                if self.last_action and self.last_action.upper() in ('L','H','J','K'):
                    return self.last_action
            # Too many steps — branch exhausted, backtrack
            elif self.committed_steps > 50:
                self.committed_target = None
                self.committed_steps = 0
            # Blocked — try to get around
            elif dist < abs(self._last_target_dist or 999):
                # Getting closer — keep going
                self.committed_steps += 1
                self._last_target_dist = dist
                return self._move(tx-px, ty-py, s, run=True)
            else:
                # Not getting closer — branch might be blocked
                self.committed_target = None
                self.committed_steps = 0
        
        # 5. ON A DOOR — keep walking to pass through
        if (px,py) in s.doors or (px,py) in self.known_doors:
            for test_dx, test_dy in [(1,0),(-1,0),(0,1),(0,-1)]:
                tx, ty = px+test_dx, py+test_dy
                if (tx,ty) in s.corridors or (tx,ty) in self.known_corridors:
                    return self._move(test_dx, test_dy, s, run=True)
                if (tx,ty) in s.floors and (tx,ty) not in self.visited:
                    return self._move(test_dx, test_dy, s, run=True)
            import random
            return random.choice(['L','H','J','K'])
        
        # 6. IN A CORRIDOR — RUN toward endpoint (tree traversal: follow the branch)
        in_corr = (px,py) in s.corridors or (px,py) in self.known_corridors
        if in_corr:
            # Find the corridor we're in
            for corr in self.corridors:
                if (px,py) in corr['tiles']:
                    # Prefer unvisited endpoints (rooms we haven't explored)
                    targets = [e for e in corr['endpoints'] if e not in self.visited]
                    if not targets:
                        targets = corr['endpoints']
                    if targets:
                        target = min(targets, key=lambda e: abs(e[0]-px)+abs(e[1]-py))
                        # COMMIT to this endpoint — DFS tree traversal
                        self.committed_target = target
                        self.committed_steps = 0
                        self._last_target_dist = abs(target[0]-px) + abs(target[1]-py)
                        return self._move(target[0]-px, target[1]-py, s, run=True)
                    break
            # In a corridor but no corridor entity — just run forward
            # The corridor leads somewhere — keep going
            if self.last_action and self.last_action.upper() in ('L','H','J','K'):
                return self.last_action  # keep running in same direction
        
        # 7. STUCK — at dead end, backtrack toward nearest fork (door/corridor)
        if self.last == s.pos and self.last_action not in ('.', 's'):
            self.stuck += 1
        
        if self.stuck > 1:
            # Find the nearest door or corridor tile we HAVEN'T fully explored
            backtrack_targets = []
            for door in s.doors | self.known_doors:
                if door not in self.visited:
                    backtrack_targets.append(door)
            for corr in s.corridors | self.known_corridors:
                if corr not in self.visited:
                    backtrack_targets.append(corr)
            # Also try doors we've visited but might lead to unexplored branches
            for door in s.doors | self.known_doors:
                if door in self.visited and door not in backtrack_targets:
                    backtrack_targets.append(door)
            
            if backtrack_targets:
                target = min(backtrack_targets, key=lambda t: abs(t[0]-px)+abs(t[1]-py))
                self.committed_target = target
                self.committed_steps = 0
                self._last_target_dist = abs(target[0]-px) + abs(target[1]-py)
                return self._move(target[0]-px, target[1]-py, s, run=True)
            
            import random
            return random.choice(['L','H','J','K'])
            import random
            # Try RUNNING (capital) — covers more ground, passes through doors
            candidates = ['L','H','J','K']
            # Filter to directions with adjacent passable tiles
            valid = []
            for key, (ddx,ddy) in [('L',(1,0)),('H',(-1,0)),('J',(0,1)),('K',(0,-1))]:
                tx,ty = px+ddx,py+ddy
                if (tx,ty) in s.floors or (tx,ty) in s.corridors or (tx,ty) in s.doors:
                    valid.append(key)
            if valid:
                return random.choice(valid)
            return 's'
        
        # 7. ITEMS — walk toward visible items (autopickup)
        if s.items:
            nearest = min(s.items, key=lambda i: abs(i[0]-px)+abs(i[1]-py))
            dist = abs(nearest[0]-px) + abs(nearest[1]-py)
            if dist <= 5:
                return self._move(nearest[0]-px, nearest[1]-py, s, run=False)
        
        # 7a. LOW HP + been resting → try quaffing a potion
        if pct < 0.5 and self.last_action == '.' and self.stuck > 3:
            # Been resting for a while — try quaffing
            return 'q'
        
        # 7b. CORRIDORS visible — run toward them (they're tree branches)
        if s.corridors:
            corr = min(s.corridors, key=lambda c: abs(c[0]-px)+abs(c[1]-py))
            if s.adj(s.pos, corr):
                # Adjacent to corridor — walk into it
                return self._move(corr[0]-px, corr[1]-py, s, run=False)
            dist = abs(corr[0]-px) + abs(corr[1]-py)
            if dist <= 5:
                return self._move(corr[0]-px, corr[1]-py, s, run=True)
        
        # 8. DOORS — RUN toward nearest door (running passes through doors)
        all_doors = s.doors | self.known_doors
        if all_doors:
            reachable_doors = [d for d in all_doors if d not in self.unreachable]
            if reachable_doors:
                door = min(reachable_doors, key=lambda d: abs(d[0]-px)+abs(d[1]-py))
                # COMMIT to this door — don't change targets
                self.committed_target = door
                self.committed_steps = 0
                self._last_target_dist = abs(door[0]-px) + abs(door[1]-py)
                return self._move(door[0]-px, door[1]-py, s, run=True)
        
        # 9. STAIRS — pursue if known
        if self.known_stairs:
            return self._move(self.known_stairs[0]-px, self.known_stairs[1]-py, s, run=True)
        
        # 9b. LEVEL MOSTLY EXPLORED — seek unvisited corridor endpoints (where stairs hide)
        total_floor = len(s.floors | self.known_floors)
        if total_floor > 0:
            explored_pct = len((s.floors | self.known_floors) & self.visited) / total_floor
            if explored_pct > 0.6:
                all_ends = []
                for c in self.corridors:
                    for e in c.get('endpoints', set()):
                        if e not in self.visited:
                            all_ends.append(e)
                if all_ends:
                    target = max(all_ends, key=lambda e: abs(e[0]-px)+abs(e[1]-py))
                    self.committed_target = target
                    self.committed_steps = 0
                    self._last_target_dist = abs(target[0]-px) + abs(target[1]-py)
                    return self._move(target[0]-px, target[1]-py, s, run=True)
        
        # 9b. CURRENT TILE VERY VISITED — force toward exits
        current_visits = self.vcount.get((px,py), 0)
        if current_visits > 4:
            # Run toward nearest door or corridor
            all_exits = list(s.doors | self.known_doors | s.corridors | self.known_corridors)
            if all_exits:
                nearest = min(all_exits, key=lambda e: abs(e[0]-px)+abs(e[1]-py))
                return self._move(nearest[0]-px, nearest[1]-py, s, run=True)
        
        # 10. GOAL: stairs exist but not found — seek unvisited territory
        # The agent KNOWS stairs exist (from memory). Unvisited areas might contain them.
        # Boost interest of unvisited tiles near corridor endpoints (dead ends = stairs)
        if self.memory.get('knows_stairs') and not self.known_stairs:
            # Corridor endpoints are likely stair locations (dead ends)
            for corr in self.corridors:
                for ep in corr.get('endpoints', []):
                    if ep not in self.visited:
                        # This endpoint might lead to stairs — prioritize it
                        return self._move(ep[0]-px, ep[1]-py, s, run=True)
        
        # 10. BFS EXPLORE — find most interesting tile
        step = self._bfs(s, passable)
        if step: return step
        
        # 11. Search
        return 's'
    
    def _bfs(self, s, passable):
        px,py = s.pos
        all_pass = passable | self.known_floors | self.known_corridors | self.known_doors
        if self.known_stairs: all_pass.add(self.known_stairs)
        
        q = deque([(px,py)]); came = {(px,py):None}
        best = None; best_s = -999
        
        while q and len(came) < 5000:
            cx,cy = q.popleft()
            sc = self._interest(cx,cy,s)
            if sc > best_s: best = (cx,cy); best_s = sc
            
            for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
                nx,ny = cx+dx,cy+dy
                if (nx,ny) in came: continue
                if (nx,ny) in self.known_walls and (nx,ny) not in self.known_doors: continue
                if s and (nx,ny) in s.walls and (nx,ny) not in s.doors: continue
                if (nx,ny) in all_pass or (nx,ny) in self.known_doors:
                    came[(nx,ny)] = (cx,cy)
                    q.append((nx,ny))
        
        if not best or best == (px,py): return None
        cur = best
        while cur != (px,py) and cur in came:
            prev = came[cur]
            if prev == (px,py):
                dx,dy = cur[0]-px, cur[1]-py
                return self._move(dx, dy, s, run=False)
            cur = prev
        return None
    
    def _interest(self, x, y, s):
        if (x,y) in self.known_walls: return -999
        if s and (x,y) in s.walls: return -999
        
        is_door = (x,y) in (s.doors if s else set()) or (x,y) in self.known_doors
        is_corridor = (x,y) in (s.corridors if s else set()) or (x,y) in self.known_corridors
        is_stairs = ((s.stairs and (x,y) == s.stairs) if s else False) or (self.known_stairs and (x,y) == self.known_stairs)
        is_item = any(ix==x and iy==y for ix,iy,_ in (s.items if s else []))
        is_endpoint = any((x,y) in c.get('endpoints',set()) for c in self.corridors)
        
        if (x,y) not in self.visited:
            sc = 8.0
            if is_stairs: sc += 20.0
            if is_door: sc += 10.0
            if is_corridor: sc += 8.0
            if is_item: sc += 6.0
            if is_endpoint: sc += 12.0
            return sc
        
        v = self.vcount.get((x,y),1)
        # Exponential decay: 1 visit=-2.5, 2=-4, 3=-6, 4=-9, 5=-13
        sc = -2.0 - v*v*0.5
        if is_stairs: sc += 15.0
        if is_door: sc += 8.0
        if is_corridor: sc += 6.0
        if is_endpoint: sc += 10.0
        if is_item: sc += 5.0
        return sc
    
    def _move(self, dx, dy, s=None, run=True):
        dx = max(-1,min(1,dx)); dy = max(-1,min(1,dy))
        if abs(dx) >= abs(dy):
            ch = {(1,0):'L',(-1,0):'H'}.get((dx,0), 'J')
        else:
            ch = {(0,1):'J',(0,-1):'K'}.get((0,dy), 'L')
        # In open areas: use diagonal if needed
        if s and dx != 0 and dy != 0:
            px,py = s.pos
            adj_open = sum(1 for ddx,ddy in [(1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,1),(1,-1),(-1,-1)]
                          if (px+ddx,py+ddy) in (s.floors | s.corridors | s.doors))
            if adj_open >= 6:
                ch = {(1,1):'N',(-1,1):'B',(1,-1):'U',(-1,-1):'Y'}.get((dx,dy), ch)
        return ch if run else ch.lower()

if __name__ == '__main__':
    print("=== HUNGRY BORG v9 — WALL-AWARE ===")
    g = TmuxGame('borg-v9', 'rogue')
    a = Agent(g)
    try: a.run(500)
    except KeyboardInterrupt: print("\nStopped.")
    raw = g.capture(); s = Screen(raw)
    print(f"Final: @{s.pos} HP:{s.status.get('hp','?')} Gold:{s.status.get('gold','?')} depth:{a.depth}")
    g.quit()
