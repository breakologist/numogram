#!/usr/bin/env python3
"""Angband Agent  -  The Hungry Borg in Middle-earth.

Uses the proven Rogue architecture: TmuxGame -> Screen parser -> Agent -> send-keys.
Angband-specific: different symbols, status bar, sidebar stats, deeper levels.
"""
import subprocess, time, os, json, random, re
from collections import deque

# State logger  -  records screen + decision every turn for freeze debugging
class TurnLogger:
    def __init__(self, path='/tmp/angband_turns.jsonl'):
        self.path = path
        self.f = open(path, 'w')
    
    def log(self, turn, screen_lines, pos, hp, depth, stuck, floors, doors, decision, reason=''):
        state = {
            't': turn,
            'x': pos[0] if pos else -1,
            'y': pos[1] if pos else -1,
            'hp': hp,
            'd': depth,
            'st': stuck,
            'fl': len(floors) if floors else 0,
            'dr': len(doors) if doors else 0,
            'act': decision,
            'why': reason,
            # Capture a 5-line window around the player
            'nearby': screen_lines
        }
        self.f.write(json.dumps(state) + '\n')
        self.f.flush()
    
    def close(self):
        self.f.close()
from datetime import datetime

# ANSI color code mapping
ANSI_RESET = '\033[0m'
ANSI_COLORS = {
    0: '\033[0m',    # reset
    1: '\033[1m',    # bold/bright
    30: '\033[30m',  # black
    31: '\033[31m',  # red
    32: '\033[32m',  # green
    33: '\033[33m',  # yellow
    34: '\033[34m',  # blue
    35: '\033[35m',  # magenta
    36: '\033[36m',  # cyan
    37: '\033[37m',  # white
    90: '\033[90m',  # bright black (dark gray)
    91: '\033[91m',  # bright red
    92: '\033[92m',  # bright green
    93: '\033[93m',  # bright yellow
    94: '\033[94m',  # bright blue
    95: '\033[95m',  # bright magenta
    96: '\033[96m',  # bright cyan
    97: '\033[97m',  # bright white
}

# Angband color names for display
ANGBAND_COLOR_NAMES = {
    0: 'd', 1: 'w', 2: 's', 3: 'o', 4: 'r', 5: 'g', 6: 'b', 7: 'u',
    8: 'D', 9: 'W', 10: 'v', 11: 'y', 12: 'R', 13: 'G', 14: 'B', 15: 'U',
}

def parse_ansi(text):
    """Parse ANSI escape codes from text. Returns list of (color_codes, char) tuples."""
    result = []
    i = 0
    current_codes = []
    while i < len(text):
        if text[i] == '\033' and i + 1 < len(text) and text[i + 1] == '[':
            # Parse ANSI sequence
            j = i + 2
            codes = []
            while j < len(text) and text[j] != 'm':
                k = j
                while k < len(text) and text[k] not in ';m':
                    k += 1
                if k < len(text) and text[k] == 'm':
                    codes.append(int(text[j:k]) if text[j:k].isdigit() else 0)
                    j = k + 1
                    break
                codes.append(int(text[j:k]) if text[j:k].isdigit() else 0)
                j = k + 1
            current_codes = codes
            i = j
        else:
            result.append((list(current_codes), text[i]))
            i += 1
    return result


class TmuxGame:
    def __init__(self, session, command, w=80, h=30):
        self.session = session
        subprocess.run(['tmux','kill-session','-t',session], capture_output=True)
        env = os.environ.copy(); env['TERM'] = 'xterm-256color'
        subprocess.run(['tmux','new-session','-d','-s',session,'-x',str(w),'-y',str(h),command], env=env)
        time.sleep(8)  # Angband needs more init time
    def capture(self):
        return subprocess.run(['tmux','capture-pane','-t',self.session,'-p'], capture_output=True, text=True).stdout
    def capture_ansi(self):
        """Capture with ANSI color codes preserved."""
        return subprocess.run(['tmux','capture-pane','-t',self.session,'-p','-e'], capture_output=True, text=True).stdout
    def send(self, k):
        subprocess.run(['tmux','send-keys','-t',self.session,k], capture_output=True)
    def quit(self):
        self.send('Q'); time.sleep(0.3); self.send('y'); time.sleep(0.5)
        subprocess.run(['tmux','kill-session','-t',self.session], capture_output=True)

class AngbandScreen:
    """Parse Angband's terminal display."""
    
    MONSTERS = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ~&;,;\'\"!?)]/\\=+|')
    ITEMS = set('!?)\]/\\=|')  # $ removed  -  handled as TREASURE_WALLS; + removed  -  it's a closed door, not an item
    WALLS = set('#')
    RUBBLE = set(':')  # rubble  -  diggable with '+'
    FLOOR = set('.·§')  # Angband uses section sign for floors
    DOORS = set("+''")  # closed door (+), open door (')
    CLOSED_DOORS = set('+')  # must be opened before walking through
    STAIRS = set('<>')
    STORES = set('12345678')  # Town store numbers
    DIGGABLE = set('#:')  # tiles we can mine through with '+'
    TREASURE_WALLS = set('$')  # gems/ore in walls  -  diggable
    
    # Dialog prompts that intercept input
    DIALOG_PATTERNS = [
        'Ignore which item?', 'Buy which item?', 'Sell which item?',
        'Drop which item?', 'Wear/Wield which item?', 'Use which item?',
        'Read which item?', 'Quaff which item?', 'Aim which item?',
        'Zap which item?', 'Fire which item?', 'Throw which item?',
        'Take off which item?', 'Examine which item?', 'Eat which item?',
        'Activate which item?', '(Inven:', '(Equip:', '(Floor:',
        'Really drop', 'Really sell', '--More--', '-more-',
        'Direction or', 'Direction:', 'which direction',
        'Inscribe with what?', 'Inscribe which item?',
        'Store Inventory', 'Command for', '(Enter to select',
    ]
    
    STAIRS_UP = set('<')
    STAIRS_DOWN = set('>')
    STAIRS = set('<>')
    
    @staticmethod
    def _check_dialog(raw):
        """Check if screen has an active dialog/prompt."""
        # Skip wall collision and movement messages (these are game messages, not dialogs)
        if 'wall in the way' in raw:
            return False
        if any(p in raw for p in AngbandScreen.DIALOG_PATTERNS):
            return True
        # Store menu: has the bordered menu frame with store options
        if '+--' in raw and ('Items' in raw) and ('Action commands' in raw):
            return True
        # Store item listing (after pressing 'l' or 'p')
        if 'Store Inventory' in raw or 'Buy which item' in raw or 'Sell which item' in raw:
            return True
        return False
    
    def _is_building(self, y, x):
        """Check if position is adjacent to # walls (building, not sidebar)."""
        for dy in range(-1, 2):
            line = self.lines[y + dy] if 0 <= y + dy < len(self.lines) else ''
            for dx in range(-1, 2):
                if dy == 0 and dx == 0: continue
                cx = x + dx
                if 0 <= cx < len(line) and line[cx] == '#':
                    return True
        return False

    def _adj_floor(self, y, x):
        """Check if position is adjacent to a floor tile (.). Real monsters live next to floors."""
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                if dy == 0 and dx == 0: continue
                ny, nx = y + dy, x + dx
                if 0 <= ny < len(self.lines) and 0 <= nx < len(self.lines[ny]):
                    if self.lines[ny][nx] == '.':
                        return True
        return False

    def __init__(self, raw):
        self.raw = raw; self.lines = raw.split('\n')
        self.pos = None; self.monsters = []; self.items = []
        self.walls = set(); self.floors = set(); self.stairs = None
        self.stairs_up = None; self.stairs_down = None
        self.stores = []  # town buildings: [(x, y, number)]
        self.status = {}; self.game_over = False
        self.has_dialog = AngbandScreen._check_dialog(raw)
        self.messages = []  # game messages from message area
        self.kills = []  # monsters killed this turn
        self.items_found = []  # items picked up this turn
        self.in_store = False  # inside a store menu
        self.store_items = []  # items visible in store menu
        self.closed_doors = []  # closed door positions [(x, y)]  -  need 'o' to open
        self.doors = []  # door positions [(x, y)]
        self.rubble = []  # rubble positions [(x, y)]  -  diggable with '+'
        self.treasure_walls = []  # $ positions in walls  -  gems/ore
        if any(p in raw for p in ['R.I.P.', 'RIP', 'killed by', 'Score:', 'Rest In Peace', 'the Rookie']):
            self.game_over = True
        else:
            self._parse()
    
    def _parse(self):
        # Find map region  -  Angband uses the left side for map, right for stats
        # Map is typically columns 0-66
        map_start = None; map_end = None
        for i, line in enumerate(self.lines):
            if '@' in line or any(c in line for c in '#.><'):
                if map_start is None: map_start = i
                map_end = i
        
        if map_start is None: return
        
        for y in range(map_start, (map_end or map_start) + 1):
            line = self.lines[y] if y < len(self.lines) else ''
            for x, ch in enumerate(line[:66]):  # Map is left 66 columns
                if ch == '@':
                    self.pos = (x, y)
                elif ch in self.ITEMS:
                    self.items.append((x, y, ch))
                elif ch in self.FLOOR or ch == '§':
                    self.floors.add((x, y))
                elif ch in self.DOORS:
                    self.doors.append((x, y))
                    if ch in self.CLOSED_DOORS:
                        self.closed_doors.append((x, y))  # track for interest scoring
                    self.floors.add((x, y))  # treat all doors as walkable  -  bump to open
                elif ch in self.WALLS:
                    self.walls.add((x, y))
                elif ch in self.RUBBLE:
                    self.rubble.append((x, y))
                    self.walls.add((x, y))  # rubble blocks movement
                elif ch in self.TREASURE_WALLS:
                    # $ could be gold on floor OR gems in wall  -  check adjacency
                    wall_count = 0
                    for ddy in range(-1, 2):
                        for ddx in range(-1, 2):
                            if ddy == 0 and ddx == 0: continue
                            nx, ny = x + ddx, y + ddy
                            if 0 <= ny < len(self.lines) and 0 <= nx < len(self.lines[ny]) and self.lines[ny][nx] in '#:$':
                                wall_count += 1
                    if wall_count >= 3:  # surrounded by walls = treasure in wall
                        self.treasure_walls.append((x, y))
                        self.walls.add((x, y))
                    else:
                        self.items.append((x, y, ch))  # floor gold
                elif ch in self.STAIRS and x >= 13 and 1 <= y < 25:
                    # Stairs must be in map area (skip sidebar cols 0-12 and status rows)
                    if ch == '<':
                        self.stairs_up = (x, y)
                    else:
                        self.stairs_down = (x, y)
                    self.stairs = (x, y)  # backward compat
                    self.floors.add((x, y))
                elif ch in self.STORES:
                    if x < 66 and self._is_building(y, x):
                        self.stores.append((x, y, int(ch)))
                    self.floors.add((x, y))
                elif ch.islower() and ch not in '@' and x >= 13 and 1 <= y < 25:
                    # Lowercase letters = Angband monsters (a-z)
                    # Columns 0-12 = left sidebar  -  skip. Row 0 = status bar.
                    # Map area is rows 1-24, columns 13-79
                    # Real monsters are adjacent to floor tiles ('.')
                    if self.pos:
                        dist = max(abs(x - self.pos[0]), abs(y - self.pos[1]))
                        if dist <= 15 and self._adj_floor(y, x):
                            self.monsters.append((x, y, ch))
                    elif self._adj_floor(y, x):
                        self.monsters.append((x, y, ch))
                elif ch.isupper() and x >= 13 and 1 <= y < 25:
                    # Uppercase letters = strong/special Angband monsters (A-Z)
                    # Same zone restrictions as lowercase  -  must be adjacent to floor
                    if self.pos:
                        dist = max(abs(x - self.pos[0]), abs(y - self.pos[1]))
                        if dist <= 15 and self._adj_floor(y, x):
                            self.monsters.append((x, y, ch))
                    elif self._adj_floor(y, x):
                        self.monsters.append((x, y, ch))
        
        # Parse messages (top of screen, before map)
        for i in range(min(3, len(self.lines))):
            line = self.lines[i].strip()
            if not line or '@' in line or '#' in line:
                continue
            # Kill messages
            for m in re.findall(r'(?:slain|destroyed|killed)\s+(?:the\s+)?([A-Z][a-z]+(?:\s+[a-z]+)*)', line):
                self.kills.append(m)
            for m in re.findall(r'You have (?:slain|destroyed) (?:the\s+)?([A-Z][a-z]+(?:\s+[a-z]+)*)', line):
                self.kills.append(m)
            # Item pickup messages  -  skip secret doors (they're terrain, not items)
            for m in re.findall(r'You have.*?(?:found|picked up|identified)\s+(?:a|an|some|\\d+)\\s+(.+?)(?:\\.|$)', line):
                item = m.strip()
                if 'secret door' not in item.lower():
                    self.items_found.append(item)
            # Artifact names (shown in brackets)
            for m in re.findall(r'\{([^}]+)\}', line):
                self.items_found.append(f'ARTIFACT: {m}')
            if line and not line.startswith(' '):
                self.messages.append(line)
        
        # Parse status  -  look for HP line
        for line in self.lines:
            m = re.search(r'HP\s+(\d+)\s*/\s*(\d+)', line)
            if m:
                self.status['hp'] = int(m.group(1))
                self.status['max_hp'] = int(m.group(2))
            m = re.search(r'AU\s+(\d+)', line)
            if m: self.status['gold'] = int(m.group(1))
            m = re.search(r'LEVEL\s+(\d+)', line)
            if m: self.status['level'] = int(m.group(1))
            m = re.search(r'Depth:\s*(\d+)', line)
            if m: self.status['depth'] = int(m.group(1))
            m = re.search(r'(\d+)\'\s*\((\w+)\)', line)
            if m:
                self.status['depth_ft'] = int(m.group(1))
                self.status['depth_label'] = m.group(2)
            # Food status  -  Angband sidebar shows "Fed XX%" or "Fed XX"
            m = re.search(r'Fed\s+(\d+)', line)
            if m: self.status['fed'] = int(m.group(1))
        
        # Detect stairs from status bar text (when < > not visible on map)
        for line in self.lines:
                        if 'Up staircase' in line or 'up staircase' in line:
                            if not self.stairs_up:
                                self.stairs_up = self.pos
                        if 'Down staircase' in line or 'down staircase' in line:
                            if not self.stairs_down:
                                self.stairs_down = self.pos
                                
        # Detect store menu
        self.in_store = (
            ('+--' in self.raw and 'Items' in self.raw and 'Action commands' in self.raw) or
            ('Store Inventory' in self.raw) or
            ('Buy which item' in self.raw) or
            ('Sell which item' in self.raw)
        )
    
    def adj(self, a, b): return max(abs(a[0]-b[0]), abs(a[1]-b[1])) <= 1
    def passable(self): return self.floors | ({self.stairs} if self.stairs else set())
    
    def summary(self):
        hp = self.status.get('hp', '?')
        mx = self.status.get('max_hp', '?')
        gold = self.status.get('gold', 0)
        depth = self.status.get('depth_label', '?')
        return (f"@({self.pos}) HP:{hp}/{mx} AU:{gold} Depth:{depth} "
                f"F:{len(self.floors)} M:{len(self.monsters)} I:{len(self.items)}")

# Reuse the Agent from Rogue agent  -  same architecture
# Import or copy the Agent class here
# For now, we'll define a simplified version

class AngbandAgent:
    """Angband agent  -  tree-traversal with DFS commitment."""
    def __init__(self, game):
        self.game = game; self.turn = 0; self.visited = set()
        self.vcount = {}; self.stuck = 0; self.last = None
        self.known_floors = set(); self.known_walls = set()
        self.known_stairs = None  # down stairs
        self.known_stairs_up = None  # up stairs
        self.committed_target = None; self.committed_steps = 0
        self._last_target_dist = None; self.last_action = ''
        self.action_history = []; self.plex_turns = 0; self.plex_goal = None
        self.corridors = []
        self._load_memory()
        self.level_turns = 0  # turns spent on current level
        self.last_depth = None
        self.level_visits = {}  # depth_label -> visit count
        self.known_stores = {}  # store_number -> (x, y)
        self.visited_stores = set()  # store_numbers we've entered and browsed
        self.recent_positions = deque(maxlen=12)  # last 12 positions  -  detect oscillation
        self.run_data = None  # populated at run start
        self.turn_log = TurnLogger()  # freeze debugging
        self.events = []  # per-run event log
        
        # Class knowledge (Human Warrior by default with -n)
        self.char_class = 'Warrior'
        self.useful_stats = {'STR', 'DEX', 'CON'}  # warrior stats
        self.useless_stats = {'INT', 'WIS'}          # mage/priest stats
        self.can_cast = False  # warriors can't use spellbooks
    
    def _load_memory(self):
        self.memory = {'runs': 0, 'max_depth': 0, 'total_gold': 0, 'knows_stairs': True}
        try:
            with open(os.path.expanduser('~/.angband_memory.json')) as f:
                self.memory = json.load(f)
        except: pass
    
    def _go_up_stairs(self, s):
        """Navigate to up stairs and go up  -  regenerates the level when we come back down.
        On DL1 (town), going up does nothing  -  find > instead."""
        px, py = s.pos
        
        # DL1 SPECIAL: pocket rooms have no >  -  go UP to reach town, then find >
        if self._is_town(s):
            if s.stairs_down:
                # Down stairs visible  -  go there
                if s.pos == s.stairs_down:
                    print(f'  GO DOWN at {self.turn}  -  entering dungeon', flush=True)
                    return '>'
                step = self._bfs_to(s.stairs_down, s)
                if step:
                    return step
                return self._move(s.stairs_down[0] - px, s.stairs_down[1] - py, s)
            # No down stairs  -  go UP to town (pockets connect to town via <)
            if s.stairs_up:
                if s.pos == s.stairs_up:
                    print(f'  GO UP to town at {self.turn}  -  pocket has no >', flush=True)
                    return '<'
                step = self._bfs_to(s.stairs_up, s)
                if step:
                    return step
                return self._move(s.stairs_up[0] - px, s.stairs_up[1] - py, s)
            # No stairs at all  -  search for hidden doors
            print(f'  DL1 no stairs at {self.turn}  -  searching', flush=True)
            return self._search_wall(s)
        
        # NORMAL LEVELS: go up to regenerate
        target = s.stairs_up or self.known_stairs_up
        if target:
            if s.pos == target:
                print(f'  GO UP at {self.turn}  -  regenerating level', flush=True)
                # Clear any pending messages before going up
                self.game.send(' ')
                time.sleep(0.1)
                return '<'
            step = self._bfs_to(target, s)
            if step:
                return step
            # Can't BFS to stairs  -  walk toward stairs direction instead
            print(f'  CANT BFS to stairs at {self.turn}  -  walking toward {target}', flush=True)
            return self._move(target[0] - px, target[1] - py, s)
        # No known up stairs  -  save and quit (rare)
        print(f'  NO UP STAIRS at {self.turn}  -  saving character', flush=True)
        self.game.send('Q')
        time.sleep(0.5)
        self.game.send('y')
        time.sleep(0.5)
        self.game.send('@')
        time.sleep(2)
        return None  # signal to stop
    
    def _search_wall(self, s):
        """Search for hidden doors  -  vanilla Angband original keyset: 's' searches ALL adjacent tiles.
        No direction needed. This is the correct way to find hidden doors.
        '+' + direction is Alter (tunnel/trap/disarm)  -  NOT search."""
        return 's'
    
    def _scan_nearby_monsters(self):
        """Use Angband's 'C' command to list visible monsters.
        Returns list of dicts with char, name, distance, direction.
        More reliable than screen parsing for monster detection."""
        self.game.send('C')
        time.sleep(0.15)
        raw = self.game.capture()
        self.game.send('Escape')  # dismiss monster list
        time.sleep(0.1)
        
        monsters = []
        for line in raw.split('\n'):
            line = line.strip()
            # "a Kobold (3 north)" or "r Giant white mouse (adjacent)"
            m = re.match(r'([a-zA-Z])\)\s+(?:the\s+)?(.+?)\s+\((\d+)\s+(north|south|east|west|NE|NW|SE|SW)\)', line)
            if m:
                monsters.append({'char': m.group(1), 'name': m.group(2).strip(),
                                'distance': int(m.group(3)), 'direction': m.group(4)})
            m2 = re.match(r'([a-zA-Z])\)\s+(?:the\s+)?(.+?)\s+\(adjacent\)', line)
            if m2:
                monsters.append({'char': m2.group(1), 'name': m2.group(2).strip(),
                                'distance': 0, 'direction': 'adjacent'})
        return monsters
    
    def _save_memory(self):
        self.memory['runs'] += 1
        try:
            with open(os.path.expanduser('~/.angband_memory.json'), 'w') as f:
                json.dump(self.memory, f, indent=2)
        except: pass
    
    def _log_event(self, event_type, data=None):
        """Log an event during the current run."""
        self.events.append({
            'turn': self.turn,
            'type': event_type,
            'data': data or {},
        })
    
    def _start_run(self):
        """Initialize run data for logging."""
        self.run_data = {
            'run': self.memory.get('runs', 0) + 1,
            'timestamp': datetime.now().isoformat(),
            'class': 'Warrior',
            'events': [],
            'depth_log': [],
            'bugs': [],
            'elements_exercised': [],
            'stores_visited': [],
            'max_stuck': 0,
        }
        self.events = []
        self.max_depth_ft = 0
        self.max_stuck_turns = 0
    
    def _end_run(self, death_cause=None):
        """Finalize run and write to JSONL."""
        if not self.run_data:
            return
        
        self.run_data['total_turns'] = self.turn
        self.run_data['max_depth'] = self.last_depth or '?'
        self.run_data['max_depth_ft'] = self.max_depth_ft
        self.run_data['death_cause'] = death_cause or 'timeout'
        self.run_data['max_stuck'] = self.max_stuck_turns
        self.run_data['stores_visited'] = list(self.known_stores.keys())
        self.run_data['events'] = self.events[-50:]
        
        path = os.path.expanduser('~/.angband_runs.jsonl')
        try:
            os.makedirs(os.path.dirname(path) or '.', exist_ok=True)
            with open(path, 'a') as f:
                f.write(json.dumps(self.run_data) + '\n')
            print(f"Run #{self.run_data['run']} logged -> {path}", flush=True)
        except Exception as e:
            print(f"Run log error: {e}", flush=True)
    
    def _turn_budget(self, depth):
        """Progressive turn allowance: more visits = more turns (player gets stronger)."""
        visits = self.level_visits.get(depth, 1)
        return 200 + (visits - 1) * 75  # 200, 275, 350, 425, ...
    
    def _is_town(self, s):
        """Check if we're in town (DL1)  -  surface level, no up stairs exist."""
        depth = s.status.get('depth_label', '')
        depth_ft = s.status.get('depth_ft', 0)
        # Town pocket rooms say "L1" not "Town"  -  match both
        return depth in ('Town', 'L1') or depth_ft == 50 or len(s.stores) > 0 or len(s.floors) > 300
    
    def _room_type(self, s):
        """Classify room: 'town', 'corridor', 'room', or 'pocket'.
        
        Pocket: <=12 floors, no doors, no stairs down  -  dead end, go up.
        Corridor: narrow passage (height >> width or vice versa), might connect.
        Room: normal room with doors/corridors.
        Town: town level (has stores or large floor count).
        """
        if self._is_town(s):
            return 'town'
        
        n = len(s.floors)
        doors = len(s.doors) + len(s.closed_doors)
        has_down = bool(s.stairs_down)
        has_up = bool(s.stairs_up)
        
        # Check if room is narrow (corridor-like)
        if s.floors:
            xs = [x for x, y in s.floors]
            ys = [y for x, y in s.floors]
            width = max(xs) - min(xs) + 1
            height = max(ys) - min(ys) + 1
            aspect = max(width, height) / max(min(width, height), 1)
        else:
            aspect = 1
        
        # Pocket detection
        if n <= 12 and doors == 0 and not has_down:
            return 'pocket'
        if n <= 8 and not has_down:
            return 'pocket'
        
        # Corridor detection  -  long and narrow
        if aspect > 4 and n <= 30:
            return 'corridor'
        
        # Normal room
        return 'room'
    
    def _pocket_is_new(self, s):
        """Check if this pocket is new (different from last pocket we escaped).
        Prevents going up and landing in the same pocket repeatedly."""
        if not s.stairs_up:
            return True
        # If stairs position is same as last known stairs, same pocket
        if s.stairs_up == self.last_pocket_stairs:
            return False
        return True

    def _can_dig(self, s):
        """Check if digging is possible  -  town walls are permanent, dungeon walls are diggable."""
        return not self._is_town(s)
    
    def _town_stores_visited(self, s):
        """Have we browsed enough stores in town?"""
        if not s.stores:
            return True
        for sx, sy, sn in s.stores:
            if sn not in self.visited_stores:
                return False
        return True
    
    def _next_unvisited_store(self, s):
        """Find the nearest store we haven't browsed yet."""
        px, py = s.pos
        best = None; best_dist = 999
        for sx, sy, sn in s.stores:
            if sn not in self.visited_stores:
                d = abs(sx - px) + abs(sy - py)
                if d < best_dist:
                    best_dist = d; best = (sx, sy, sn)
        return best
    
    def _shop(self, s):
        """Handle store interaction. Class-aware: buy useful, sell junk, skip useless."""
        raw = s.raw
        
        # Store menu (main options)  -  mark as browsing
        if '+--' in raw and 'Items' in raw and 'Action commands' in raw:
            for sn, pos in self.known_stores.items():
                if sn not in self.visited_stores:
                    self.visited_stores.add(sn)
                    self._log_event('store_browse', {'store': sn})
                    break
            return 'l'  # Browse items first
        
        # Store inventory listing (after 'l')
        if 'Store Inventory' in raw or ('Weight' in raw and 'Price' in raw):
            gold = s.status.get('gold', 0)
            
            # Class-aware buying priorities
            # All classes: potions, scrolls, food, light, escape, detection
            buy_patterns = [
                ('Cure Light Wounds', 25, 'healing'),
                ('Cure Serious Wounds', 75, 'healing'),
                ('Cure Critical Wounds', 200, 'healing'),
                ('Healing', 500, 'healing'),
                ('Word of Recall', 150, 'recall'),
                ('Ration', 5, 'food'),
                ('Torch', 2, 'light'),
                ('Lantern', 35, 'light'),
                ('Flask of oil', 3, 'light_fuel'),
                ('Phase Door', 15, 'escape'),
                ('Treasure Detection', 50, 'detection'),
                ('Object Detection', 50, 'detection'),
                ('Door/Stair Location', 50, 'detection'),
                ('Identify', 200, 'identification'),
                ('Remove Curse', 100, 'utility'),
                # Warriors: STR/DEX/CON potions
                ('Strength', 800, 'stat_up'),
                ('Dexterity', 800, 'stat_up'),
                ('Constitution', 800, 'stat_up'),
                ('Restore Strength', 1000, 'stat_restore'),
                ('Restore Dexterity', 1000, 'stat_restore'),
                ('Restore Constitution', 1000, 'stat_restore'),
            ]
            
            # Skip patterns (useless for Warriors)
            skip_patterns = [
                'Book of', 'Spellbook', 'Magic Missile', 'Lightning Bolt',
                'Fireball', 'Frost Bolt', 'Confuse Monster',
                'Intelligence', 'Wisdom',  # INT/WIS potions
                'Staff', 'Wand', 'Rod',  # magical devices
            ]
            
            for line in s.lines:
                # Skip useless items
                if any(skip.lower() in line.lower() for skip in skip_patterns):
                    continue
                
                for pattern, max_price, reason in buy_patterns:
                    if pattern.lower() in line.lower() and max_price <= gold:
                        self._log_event('store_buy_attempt', {'item': line.strip()[:60], 'reason': reason})
                        return 'p'  # Go to buy mode
            
            # Nothing to buy  -  try selling spellbooks if we have them
            self._log_event('store_leave', {'reason': 'nothing useful to buy'})
            return '\033'  # ESC to leave
        
        # Buy prompt
        if 'Buy which item' in raw or '(Letter' in raw:
            # Find first useful item letter
            skip_patterns_lower = ['book of', 'spellbook', 'intelligence', 'wisdom', 'staff', 'wand', 'rod']
            for line in s.lines:
                if any(skip.lower() in line.lower() for skip in skip_patterns_lower):
                    continue
                # Prefer useful items
                if any(useful in line.lower() for useful in ['cure', 'recall', 'ration', 'torch', 'lantern', 'oil', 'phase']):
                    m = re.match(r'\s*([a-z])\)', line)
                    if m:
                        self._log_event('store_select', {'letter': m.group(1), 'item': line.strip()[:40]})
                        return m.group(1)
                m = re.match(r'\s*([a-z])\)', line)
                if m:
                    self._log_event('store_select', {'letter': m.group(1), 'item': line.strip()[:40]})
                    return m.group(1)  # Select item
            return '\033'  # Nothing to buy, cancel
        
        # Confirm purchase
        if ('Buy' in raw or 'buy' in raw) and ('y/n' in raw.lower() or 'yes' in raw.lower()):
            self._log_event('store_confirm', {})
            return 'y'
        
        # Default: try to leave
        return '\033'  # ESC
    
    def run(self, max_turns=500):
        # With -n flag, Angband auto-creates character with defaults
        # Just dismiss any -more- prompts and inscription dialogs
        time.sleep(3)  # Let the game fully init
        for i in range(60):
            raw = self.game.capture()
            if '-more-' in raw.lower():
                self.game.send('space')
            elif any(p in raw for p in ['Inscribe', 'which item?', '(Inven:', 'Equip']):
                self.game.send('Escape')
            elif 'use as is' in raw or 'redo' in raw:
                self.game.send('y')  # Accept character
                time.sleep(0.5)
                self.game.send('Enter')  # Confirm past stat screen
            elif '@' in raw and ('floor' in raw.lower() or 'town' in raw.lower() or 'Open floor' in raw):
                break  # Game ready
            else:
                self.game.send('space')
            time.sleep(0.25)
        
        self._start_run()
        self._log_event('game_start', {'depth': '?'})
        
        try:
            for t in range(max_turns):
                self.turn = t
                raw = self.game.capture(); s = AngbandScreen(raw)
                # Validate monster count  -  screen parser inflates from sidebar/status
                if len(s.monsters) > 3 and t % 5 == 0:
                    real = self._scan_nearby_monsters()
                    if len(real) < len(s.monsters) and s.pos:
                        # Convert C command direction/distance to approximate positions
                        dir_to_delta = {'north':(0,-1), 'south':(0,1), 'east':(1,0), 'west':(-1,0),
                                        'NE':(1,-1), 'NW':(-1,-1), 'SE':(1,1), 'SW':(-1,1)}
                        px, py = s.pos
                        s.monsters = []
                        for m in real:
                            d = dir_to_delta.get(m['direction'], (0,0))
                            mx = px + d[0] * m['distance']
                            my = py + d[1] * m['distance']
                            s.monsters.append((mx, my, m['char']))
                if s.game_over:
                    print(f'DEAD turn {t}', flush=True)
                    self._log_event('death', {'pos': str(s.pos), 'depth': depth})
                    self._end_run(death_cause='killed')
                    break
                # Dismiss dialogs first  -  they intercept all input
                if s.has_dialog:
                    if '-more-' in raw.lower() or '--More--' in raw:
                        self.game.send('space')
                    else:
                        self.game.send('Escape')
                    time.sleep(0.15)
                    continue
                
                if not s.pos:
                    self.game.send('Escape')
                    time.sleep(0.1)
                    self.game.send('Enter')
                    time.sleep(0.1)
                    continue
                
                px, py = s.pos
                self.visited.add(s.pos)
                self.vcount[s.pos] = self.vcount.get(s.pos, 0) + 1
                self.recent_positions.append(s.pos)  # track for oscillation detection
                self.known_floors |= s.floors; self.known_walls |= s.walls
                if s.stairs_down: self.known_stairs = s.stairs_down
                if s.stairs_up: self.known_stairs_up = s.stairs_up
                
                depth = s.status.get('depth_label', '?')
                if depth != self.last_depth:
                    self.level_turns = 0
                    self.last_depth = depth
                    # Reset exploration state  -  new level, fresh start
                    self.visited = {s.pos}
                    self.vcount = {}
                    self.recent_positions = deque(maxlen=20)
                    self.level_visits[depth] = self.level_visits.get(depth, 0) + 1
                    # Agent always lands on < when descending  -  record it
                    if depth != '?' and not self._is_town(s):
                        self.known_stairs_up = s.pos  # standing on < right now
                    # Reset store visits when returning to town (fresh stock)
                    if self._is_town(s):
                        self.visited_stores = set()
                    depth_ft = s.status.get('depth_ft', 0)
                    if depth_ft > self.max_depth_ft:
                        self.max_depth_ft = depth_ft
                    self._log_event('depth_change', {'depth': depth, 'depth_ft': depth_ft, 'visits': self.level_visits[depth]})
                self.level_turns += 1
                # Track stores and mark as visited when walking on them
                for sx, sy, sn in s.stores:
                    self.known_stores[sn] = (sx, sy)
                    if abs(s.pos[0] - sx) <= 1 and abs(s.pos[1] - sy) <= 1:
                        if sn not in self.visited_stores:
                            self.visited_stores.add(sn)
                            self._log_event('store_visited', {'store': sn})
                
                # Track kills and items
                for kill in s.kills:
                    self._log_event('kill', {'monster': kill})
                for item in s.items_found:
                    self._log_event('item_found', {'item': item})
                    # Equip immediately after pickup
                    # Angband's 'w' command handles ALL equipment: weapons, armor,
                    # cloaks, shields, boots, rings, amulets  -  everything.
                    # If nothing to equip, prompt says "You have nothing to..."
                    # which we dismiss with Escape.
                    self._log_event('auto_equip_on_pickup', {'item': item})
                    self.game.send('w')  # wield/wear any equippable item
                    time.sleep(0.15)
                    raw2 = self.game.capture()
                    if 'nothing' in raw2.lower() or 'which' in raw2.lower():
                        self.game.send('Escape')
                    else:
                        time.sleep(0.15)
                        self.game.send('Escape')
                    time.sleep(0.1)
                
                # Fallback equip: every 100 turns if in dungeon, in case message parsing
                # missed a pickup. This catches items found by walking over them
                # without a visible pickup message.
                if t > 0 and t % 100 == 0 and not self._is_town(s) and depth != '?':
                    self.game.send('w')  # wield/wear anything equippable
                    time.sleep(0.15)
                    raw2 = self.game.capture()
                    if 'nothing' in raw2.lower() or 'which' in raw2.lower():
                        self.game.send('Escape')
                    else:
                        time.sleep(0.15)
                        self.game.send('Escape')
                    time.sleep(0.1)
                
                if s.pos == self.last and self.last_action not in ('.', ','):
                    self.stuck += 1
                    if self.stuck > self.max_stuck_turns:
                        self.max_stuck_turns = self.stuck
                    # Debug: print decision when stuck
                    if self.stuck == 5 or self.stuck % 100 == 0:
                        depth_label = s.status.get('depth_label', '?')
                        print(f'  STUCK {self.stuck} @{s.pos} D:{depth_label} stores:{len(s.stores)} floors:{len(s.floors)} doors:{len(s.doors)} closed:{len(s.closed_doors)} stairs_up:{s.stairs_up} stairs_down:{s.stairs_down} known_up:{self.known_stairs_up}', flush=True)
                        # Dump adjacent tiles
                        for dy in range(-2, 3):
                            row = ''
                            for dx in range(-3, 4):
                                tx, ty = px+dx, py+dy
                                ch = '?'
                                if (tx, ty) == s.pos: ch = '@'
                                elif (tx, ty) in s.walls: ch = '#'
                                elif (tx, ty) in s.floors: ch = '.'
                                elif (tx, ty) in s.closed_doors: ch = '+'
                                elif (tx, ty) in [d for d in s.doors]: ch = "'"
                                elif s.stairs_up and (tx, ty) == s.stairs_up: ch = '<'
                                elif s.stairs_down and (tx, ty) == s.stairs_down: ch = '>'
                                row += ch
                            print(f'    {row}', flush=True)
                    # HARD LIMIT  -  if stuck 500+ turns, this level is hopeless
                    if self.stuck >= 500:
                        depth_label = s.status.get('depth_label', '?')
                        print(f'  HARD STUCK LIMIT at {self.stuck} turns  -  dead end on {depth_label}. Ending run.', flush=True)
                        self._log_event('stuck_death', {'turn': t, 'pos': str(s.pos), 'stuck': self.stuck})
                        return  # exit run loop
                elif s.pos != self.last:
                    self.stuck = 0
                self.last = s.pos
                
                if t % 25 == 0:
                    hp = s.status.get('hp', '?')
                    depth = s.status.get('depth_label', '?')
                    sd = 'D' if s.stairs_down else '-'
                    su = 'U' if s.stairs_up else '-'
                    visits = self.level_visits.get(depth, 1)
                    budget = self._turn_budget(depth)
                    stores = len(s.stores)
                    store_str = f' St:{stores}' if stores else ''
                    print(f'T:{t:3d} @{s.pos} HP:{hp} Fed:{s.status.get("fed","?")} D:{depth} F:{len(s.floors)} M:{len(s.monsters)} [{su}{sd}] L{self.level_turns}/{budget} V{visits}{store_str} stuck:{self.stuck}', flush=True)
                    # Periodic checkpoint
                    if t > 0 and t % 100 == 0:
                        self.run_data['total_turns'] = t
                        self.run_data['max_depth'] = depth
                        self.run_data['max_depth_ft'] = self.max_depth_ft
                        self.run_data['max_stuck'] = self.max_stuck_turns
                        self.run_data['stores_visited'] = list(self.known_stores.keys())
                        self.run_data['events'] = self.events[-30:]
                        path = os.path.expanduser('~/.angband_runs_checkpoint.json')
                        try:
                            with open(path, 'w') as f:
                                json.dump(self.run_data, f)
                        except: pass
                
                act = self._decide(s)
                if act is None:
                    break  # save-and-quit signal
                # Log screen state + decision for freeze debugging
                self.turn_log.log(
                    turn=self.turn,
                    screen_lines=self._get_nearby_screen(s),
                    pos=s.pos,
                    hp=s.status.get('hp', 0),
                    depth=s.status.get('depth_label', '?'),
                    stuck=self.stuck,
                    floors=s.floors,
                    doors=s.doors,
                    decision=act
                )
                self.last_action = act
                # Send each character as a separate key (for 'o'+direction combos)
                for i, ch in enumerate(act):
                    self.game.send(ch)
                    # Extra delay after '+' or 'o' for dialog mode to activate
                    if ch in ('+', 'o') and i + 1 < len(act):
                        time.sleep(0.2)
                    else:
                        time.sleep(0.08)
                time.sleep(0.04)
        except KeyboardInterrupt:
            self._log_event('interrupted', {'turn': self.turn})
        finally:
            self.turn_log.close()
            self._log_event('game_end', {'max_depth_ft': self.max_depth_ft})
            self._end_run()  # survived, timeout, or killed
            self._save_memory()
            if self.run_data:
                print(f'Finished  -  Run #{self.run_data["run"]} logged', flush=True)
    
    def _get_nearby_screen(self, s):
        """Get a compact view of the map around the player for debugging."""
        if not s.pos:
            return []
        px, py = s.pos
        lines = []
        for dy in range(-5, 6):
            row = ''
            for dx in range(-8, 9):
                nx, ny = px + dx, py + dy
                if 0 <= ny < len(s.lines) and 0 <= nx < len(s.lines[ny]):
                    row += s.lines[ny][nx]
                else:
                    row += ' '
            lines.append(row)
        return lines
    
    # ═══════════════════════════════════════════════════════
    # DECISION SUB-METHODS (extracted from monolithic _decide)
    # Each returns: action string, or None if it doesn't handle this situation
    # ═══════════════════════════════════════════════════════

    def _handle_town(self, s, pct):
        """Town behavior: head for > stairs, skip shopping."""
        if not self._is_town(s):
            return None
        if s.in_store:
            return self._shop(s)
        if s.stairs_down:
            if s.pos == s.stairs_down:
                return '>'
            step = self._bfs_to(s.stairs_down, s)
            if step:
                self.committed_target = s.stairs_down
                return step
        return None

    def _handle_pocket_room(self, s, pct):
        """Handle pocket rooms - tiny dead ends with no doors or > stairs.
        Go up immediately to reach town. Track pocket escapes to avoid loops."""
        rt = self._room_type(s)
        # Only act on actual pockets, not corridors or rooms
        if rt == 'corridor' or rt == 'room' or rt == 'town':
            return None
        if rt != 'pocket':
            return None
        
        # Check if we've been here before (same pocket)
        if not self._pocket_is_new(s):
            if self.stuck < 5:
                return None
            dirs = [(0,-1,'8'),(0,1,'2'),(-1,0,'4'),(1,0,'6')]
            random.shuffle(dirs)
            for dx, dy, ch in dirs:
                nx, ny = s.pos[0]+dx, s.pos[1]+dy
                if (nx, ny) in s.floors:
                    return ch
            self.last_pocket_stairs = s.stairs_up
            return self._go_up_stairs(s) or 's'
        
        # New pocket - search briefly, then go up
        if self.stuck < 5:
            step = self._bfs(s)
            if step:
                return step
            return self._search_wall(s)
        
        print(f'  POCKET ESCAPE at {self.turn} - {len(s.floors)} floors, stuck:{self.stuck}', flush=True)
        self.last_pocket_stairs = s.stairs_up
        self._log_event('pocket_escape', {'turn': self.turn, 'floors': len(s.floors), 'stuck': self.stuck})
        return self._go_up_stairs(s) or 's'

    def _handle_town_explore(self, s, pct):
        """Town exploration: walk toward nearest unvisited floor or unexplored wall.
        In town, the viewport is small but the level is huge. We need to push
        into unexplored territory by walking toward wall-adjacent unvisited floors."""
        if not self._is_town(s):
        return None
        
        visible_unvisited = s.floors - self.visited
        if visible_unvisited:
        # BFS should handle this — let it explore
        return None
        
        # All visible floors visited. Walk toward nearest wall to expand viewport.
        # Pick a direction that maximizes distance from recent positions.
        px, py = s.pos
        if not self.recent_positions:
        return None
        
        # Find wall-adjacent floors we could search
        wall_adjacent = set()
        for fx, fy in s.floors:
        for dx, dy in [(0,-1),(0,1),(-1,0),(1,0)]:
        if (fx+dx, fy+dy) in s.walls:
        wall_adjacent.add((fx, fy))
                    break
        
        unsearched = wall_adjacent - self.visited
        if unsearched:
        best = min(unsearched, key=lambda w: abs(w[0]-px) + abs(w[1]-py))
        d = abs(best[0]-px) + abs(best[1]-py)
        if d <= 2:
        return 's'  # search adjacent walls for hidden doors
        return self._move(best[0] - px, best[1] - py, s)
        
        # Everything searched. Walk in a direction away from recent positions.
        # This pushes the viewport into new territory.
        from collections import Counter
        pos_counts = Counter(self.recent_positions)
        # Find least-visited direction
        dirs = [(0,-1,'8'),(0,1,'2'),(-1,0,'4'),(1,0,'6'),
                (-1,-1,'7'),(1,-1,'9'),(-1,1,'1'),(1,1,'3')]
        best_dir = None
        best_score = -999
        for dx, dy, ch in dirs:
        nx, ny = px+dx, py+dy
        if (nx, ny) not in s.floors:
                continue
        score = -pos_counts.get((nx, ny), 0)
        # Prefer directions that haven't been explored
        # Check if this direction leads to unvisited area (rough heuristic)
        if (nx, ny) in self.visited:
        score -= 5
        if score > best_score:
        best_score = score
        best_dir = ch
        return best_dir or 's'

def _handle_eat(self, s, pct):
        """Dont starve. E auto-selects food if only one type."""
        if self._is_town(s):
        return None
        fed = s.status.get('fed', 100)
        if fed < 50 and pct > 0.25:
            self._log_event('eat', {'turn': self.turn, 'fed': fed})
        return 'E'
        if self.turn > 0 and self.turn % 2000 == 0:
            self._log_event('eat_fallback', {'turn': self.turn, 'fed': fed})
        return 'E'
        return None

        
    def _handle_tiny_room_reroll(self, s, pct):
        """Tiny room with no doors and no >  -  search persistently, then reroll."""
        if self._is_town(s) or s.stairs_down or s.doors or len(s.floors) >= 30:
            return None
        if not s.stairs_up:
            return None
        px, py = s.pos

        # Check if room is truly explored  -  all floors visited and no hidden doors found
        all_visited = len(s.floors - self.visited) == 0

        if s.pos == s.stairs_up and all_visited and self.stuck > 20:
            # Room fully explored, stuck at stairs, no doors found  -  reroll
            dirs = [(0,-1,'8'),(0,1,'2'),(-1,0,'4'),(1,0,'6'),
                    (-1,-1,'7'),(1,-1,'9'),(-1,1,'1'),(1,1,'3')]
            dig_targets = [ch for dx, dy, ch in dirs
                          if (px+dx, py+dy) in s.rubble or (px+dx, py+dy) in s.treasure_walls]
            if dig_targets and self.level_turns < 40:
                return '+' + random.choice(dig_targets)
            print(f'  REROLL: tiny room ({len(s.floors)} floors), fully explored, stuck:{self.stuck}, going up', flush=True)
            self._log_event('go_up_reroll', {'turn': self.turn, 'floors': len(s.floors), 'stuck': self.stuck})
            return '<'
        elif s.stairs_up:
            if self.level_turns % 2 == 0:
                return 's'  # search every other turn  -  hidden doors need many attempts
            return self._move(s.stairs_up[0] - px, s.stairs_up[1] - py, s)
        return None

    def _handle_stairs(self, s, pct):
        """Stair navigation: descend >, walk away first if just came up."""
        px, py = s.pos
        if not s.stairs_down or pct <= 0.6:
            return None
        if s.pos == s.stairs_down:
            if self.level_turns < 30:
                dirs = [(0,-1,'8'),(0,1,'2'),(-1,0,'4'),(1,0,'6'),
                        (-1,-1,'7'),(1,-1,'9'),(-1,1,'1'),(1,1,'3')]
                random.shuffle(dirs)
                for dx, dy, ch in dirs:
                    nx, ny = s.pos[0]+dx, s.pos[1]+dy
                    if (nx, ny) in s.floors and (nx, ny) != s.pos:
                        return ch
            return '>'  # DESCEND
        elif s.adj(s.pos, s.stairs_down) and self.level_turns > 20:
            if self.level_turns % 40 == 0 and len(s.floors) < 30:
                return 's'
            self.committed_target = s.stairs_down
            self.committed_steps = 0
            return self._move(s.stairs_down[0] - px, s.stairs_down[1] - py, s)
        return None

    def _handle_committed(self, s, pct):
        """Continue toward committed target (DFS-style movement)."""
        if not self.committed_target or pct <= 0.2:
            return None
        px, py = s.pos
        tx, ty = self.committed_target
        dist = abs(tx - px) + abs(ty - py)
        if dist == 0:
            self.committed_target = None; self.committed_steps = 0
            return None  # reached  -  fall through to BFS
        elif self.committed_steps > 60:
            self.committed_target = None; self.committed_steps = 0
            return None
        else:
            self.committed_steps += 1; self._last_target_dist = dist
            return self._move(tx - px, ty - py, s)

    def _handle_stuck_recovery(self, s, pct):
        """General stuck recovery  -  explores fully before retreating."""
        if self._is_town(s):
            return None
        has_unvisited = len(s.floors - self.visited) > 0
        has_stairs = bool(s.stairs_up or self.known_stairs_up)

        if self.stuck > 100 and has_stairs and not has_unvisited:
            self._log_event('go_up_stuck_any', {'turn': self.turn, 'stuck': self.stuck, 'floors': len(s.floors)})
            return self._go_up_stairs(s) or 's'
        if self.stuck > 100 and not has_stairs:
            return self._search_wall(s)
        if self.stuck > 100 and has_stairs:
            return self._search_wall(s)
        if self.stuck > 50 and len(s.floors) <= 25 and not has_unvisited and has_stairs:
            self._log_event('go_up_stuck_tiny', {'turn': self.turn, 'stuck': self.stuck})
            return self._go_up_stairs(s) or 's'
        if self.stuck > 50 and has_stairs and not has_unvisited:
            self._log_event('go_up_stuck', {'turn': self.turn, 'stuck': self.stuck, 'floors': len(s.floors)})
            return self._go_up_stairs(s) or 's'
        return None

    def _handle_escape_pocket(self, s, pct):
        """Escape tiny pocket  -  dig rubble/treasure, search, go up.
        Defers to _handle_stuck_recovery after stuck > 50."""
        px, py = s.pos
        walkable = [(px+dx, py+dy) for dx, dy in [(0,-1),(0,1),(-1,0),(1,0),(-1,-1),(1,-1),(-1,1),(1,1)]
                    if (px+dx, py+dy) in s.floors]
        if self.stuck <= 5 or len(walkable) >= 2:
            return None
        if self.stuck > 50:
            # Stuck 50+ in tiny pocket  -  go up directly
            self._log_event('go_up_pocket', {'turn': self.turn, 'stuck': self.stuck, 'walkable': len(walkable)})
            return self._go_up_stairs(s) or self._search_wall(s)
        targets = []
        for dx, dy in [(0,-1),(0,1),(-1,0),(1,0),(-1,-1),(1,-1),(-1,1),(1,1)]:
            nx, ny = px+dx, py+dy
            if (nx, ny) in s.rubble: targets.append((2/3, (dx, dy), 'rubble'))
            elif (nx, ny) in s.treasure_walls: targets.append((1/2, (dx, dy), 'treasure'))
        if targets:
            _, (dx, dy), kind = random.choice(targets)
            ch = self._move(dx, dy, s)
            print(f'  ESCAPE: digging {kind} at ({px+dx},{py+dy}) stuck:{self.stuck}', flush=True)
            return '+' + ch
        if self.stuck % 3 == 0:
            return self._search_wall(s)
        if self.stuck > 20 and len(s.floors) <= 25:
            self._log_event('go_up_reroll', {'turn': self.turn, 'stuck': self.stuck})
            return self._go_up_stairs(s) or 's'
        return None

    def _handle_flee(self, s, pct):
        """Flee adjacent monsters  -  always in town, when HP < 50% in dungeon."""
        px, py = s.pos
        for mpx, mpy, ch in s.monsters:
            if s.adj(s.pos, (mpx, mpy)):
                if self._is_town(s) or pct < 0.5:
                    return self._move(px - mpx, py - mpy, s)
        return None

    def _handle_fight(self, s, pct):
        """Hunt monsters: weak at HP>25%, strong at HP>60%. Walk toward within range."""
        px, py = s.pos
        weak = [(mx, my, ch) for mx, my, ch in s.monsters if ch.islower()]
        strong = [(mx, my, ch) for mx, my, ch in s.monsters if ch.isupper()]
        if pct > 0.25 and weak and not self._is_town(s):
            for mpx, mpy, ch in weak:
                if s.adj(s.pos, (mpx, mpy)):
                    return self._move(mpx - px, mpy - py, s)
            closest = None; closest_dist = 999
            for mpx, mpy, ch in weak:
                d = abs(mpx - px) + abs(mpy - py)
                if d < closest_dist and d <= 5:
                    closest = (mpx, mpy); closest_dist = d
            if closest:
                return self._move(closest[0] - px, closest[1] - py, s)
        if pct > 0.6 and strong and not self._is_town(s):
            for mpx, mpy, ch in strong:
                if s.adj(s.pos, (mpx, mpy)):
                    return self._move(mpx - px, mpy - py, s)
            closest = None; closest_dist = 999
            for mpx, mpy, ch in strong:
                d = abs(mpx - px) + abs(mpy - py)
                if d < closest_dist and d <= 3:
                    closest = (mpx, mpy); closest_dist = d
            if closest:
                return self._move(closest[0] - px, closest[1] - py, s)
        return None

    def _handle_heal(self, s, pct):
        """Rest when critically low HP and no targets nearby."""
        weak = any(ch.islower() for _, _, ch in s.monsters)
        if pct < 0.25 and not weak and self.stuck < 3:
            return ','
        if pct < 0.15 and self.stuck < 3:
            return ','
        return None

    def _handle_closed_doors(self, s):
        """Open adjacent closed doors with 'o' + direction."""
        if not s.closed_doors:
            return None
        px, py = s.pos
        for dx, dy, ch in [(0,-1,'8'),(0,1,'2'),(-1,0,'4'),(1,0,'6'),
                           (-1,-1,'7'),(1,-1,'9'),(-1,1,'1'),(1,1,'3')]:
            if (px+dx, py+dy) in s.closed_doors:
                return 'o' + ch
        return None

    def _handle_stuck_dungeon(self, s, pct):
        """Stuck in dungeon  -  dig treasure, search, go up when desperate."""
        if self.stuck <= 5 or self._is_town(s):
            return None
        px, py = s.pos
        # Stuck 200+  -  head for stairs
        if self.stuck > 200:
            target = self.known_stairs_down or self.known_stairs_up
            if target:
                print(f'  STUCK 200+  -  heading for stairs at {target}', flush=True)
                if s.pos == target:
                    return '>' if target == self.known_stairs_down else '<'
                step = self._bfs_to(target, s)
                if step:
                    return step
            return self._search_wall(s)
        # Dig treasure/rubble
        dirs = [(0,-1,'8'), (0,1,'2'), (-1,0,'4'), (1,0,'6'),
                (-1,-1,'7'), (1,-1,'9'), (-1,1,'1'), (1,1,'3')]
        treasure = [ch for dx, dy, ch in dirs
                    if (px+dx, py+dy) in s.treasure_walls or (px+dx, py+dy) in s.rubble]
        if treasure:
            ch = random.choice(treasure)
            if self.stuck == 2 or self.stuck % 20 == 0:
                print(f'  DIG treasure/rubble at stuck {self.stuck}', flush=True)
            return '+' + ch
        if self.stuck % 3 == 0:
            return self._search_wall(s)
        if self.stuck > 50 and len(s.floors) < 25 and not s.doors and not s.treasure_walls:
            self._log_event('go_up_deadend', {'turn': self.turn, 'stuck': self.stuck})
            return self._go_up_stairs(s) or 's'
        return random.choice(['2', '4', '6', '8', '7', '9', '1', '3'])

    def _handle_tiny_room(self, s):
        """Small room with no stairs  -  search for hidden doors."""
        if len(s.floors) >= 20 or s.stairs_down or s.stairs_up or self._is_town(s):
            return None
        px, py = s.pos
        dirs = [(0,-1,'8'), (0,1,'2'), (-1,0,'4'), (1,0,'6'),
                (-1,-1,'7'), (1,-1,'9'), (-1,1,'1'), (1,1,'3')]
        treasure = [ch for dx, dy, ch in dirs
                    if (px+dx, py+dy) in s.treasure_walls or (px+dx, py+dy) in s.rubble]
        if treasure:
            return '+' + random.choice(treasure)
        if random.random() < 0.6:
            return self._search_wall(s)
        return None

    def _handle_oscillation(self, s):
        """Last 8 positions are <=3 unique tiles  -  break the loop."""
        if len(self.recent_positions) < 8:
            return None
        if len(set(self.recent_positions)) > 3:
            return None
        px, py = s.pos
        unvisited = s.floors - self.visited
        if not unvisited and not s.stairs_down:
            if s.stairs_up:
                if s.pos == s.stairs_up:
                    return '<'
                return self._move(s.stairs_up[0] - px, s.stairs_up[1] - py, s)
            if self.known_stairs_up:
                if s.pos == self.known_stairs_up:
                    return '<'
                step = self._bfs_to(self.known_stairs_up, s)
                if step:
                    return step
        # Still unvisited  -  search/dig
        dirs = [(0,-1,'8'), (0,1,'2'), (-1,0,'4'), (1,0,'6'),
                (-1,-1,'7'), (1,-1,'9'), (-1,1,'1'), (1,1,'3')]
        treasure = [ch for dx, dy, ch in dirs
                    if (px+dx, py+dy) in s.treasure_walls or (px+dx, py+dy) in s.rubble]
        if treasure:
            return '+' + random.choice(treasure)
        return self._search_wall(s)

    def _handle_explore(self, s, pct):
        """BFS exploration with perimeter search when level is fully explored."""
        step = self._bfs(s)
        if not step:
            return None
        px, py = s.pos
        visible_unvisited = s.floors - self.visited
        if not visible_unvisited and not s.stairs_down:
            wall_adjacent = set()
            for fx, fy in s.floors:
                for dx, dy in [(0,-1),(0,1),(-1,0),(1,0)]:
                    if (fx+dx, fy+dy) in s.walls:
                        wall_adjacent.add((fx, fy))
                        break
            unsearched = wall_adjacent - self.visited
            if unsearched:
                best = min(unsearched, key=lambda w: abs(w[0]-px) + abs(w[1]-py))
                d = abs(best[0]-px) + abs(best[1]-py)
                if d <= 2:
                    return 's'
                return self._move(best[0] - px, best[1] - py, s)
            self._log_event('go_up_perimeter_done', {'turn': self.turn, 'floors': len(s.floors)})
            return self._go_up_stairs(s) or step
        return step

    def _handle_closed_doors_bfs(self, s):
        """BFS found nothing  -  walk toward nearest closed door."""
        if not s.closed_doors:
            return None
        px, py = s.pos
        door = min(s.closed_doors, key=lambda d: abs(d[0]-px) + abs(d[1]-py))
        if s.adj(s.pos, door):
            dx, dy = door[0] - px, door[1] - py
            return 'o' + self._move(dx, dy, s)
        return self._move(door[0] - px, door[1] - py, s)

    def _handle_go_up(self, s, pct):
        """Last resort: go up stairs if budget exceeded or level explored."""
        depth = s.status.get('depth_label', '?')
        budget = self._turn_budget(depth)
        up_target = s.stairs_up or self.known_stairs_up
        go_up = (up_target and not s.stairs_down and
                 (self.level_turns > budget or not (s.floors - self.visited) or self.stuck > 100))
        if not go_up:
            return None
        px, py = s.pos
        if s.pos == up_target:
            return '<'
        if s.adj(s.pos, up_target):
            return self._move(up_target[0] - px, up_target[1] - py, s)
        self.committed_target = up_target
        return self._move(up_target[0] - px, up_target[1] - py, s)

    def _decide(self, s):
        """Main decision dispatcher  -  calls sub-methods in priority order.
        First non-None return wins. Order matters: highest priority first."""
        # NOTE: don't auto-send Escape/Space every turn  -  no prompt usually exists
        # Prompt handling is done in _handle_stuck_recovery and _run when detected
        
        px, py = s.pos
        hp = s.status.get('hp', 100); mx = s.status.get('max_hp', 100)
        pct = hp / max(mx, 1)

        # UNIVERSAL STUCK RECOVERY  -  fires before everything when stuck > 30
        if self.stuck > 30 and not self._is_town(s):
            target = s.stairs_up or self.known_stairs_up
            if target:
                if s.pos == target:
                    return '<'  # on the stairs  -  go up
                step = self._bfs_to(target, s)
                if step:
                    return step
                # Can't BFS to stairs  -  walk directionally
                return self._move(target[0] - px, target[1] - py, s)
            # No known stairs  -  search for hidden doors
            return self._search_wall(s)

        # Priority order  -  first match wins
        handlers = [
            ('town',        lambda: self._handle_town(s, pct)),
            ('eat',         lambda: self._handle_eat(s, pct)),
            ('reroll',      lambda: self._handle_tiny_room_reroll(s, pct)),
            ('pocket_room', lambda: self._handle_pocket_room(s, pct)),
            ('town_explore', lambda: self._handle_town_explore(s, pct)),
            ('stairs',      lambda: self._handle_stairs(s, pct)),
            ('committed',   lambda: self._handle_committed(s, pct)),
            ('stuck_top',   lambda: self._handle_stuck_recovery(s, pct)),
            ('pocket',      lambda: self._handle_escape_pocket(s, pct)),
            ('flee',        lambda: self._handle_flee(s, pct)),
            ('fight',       lambda: self._handle_fight(s, pct)),
            ('heal',        lambda: self._handle_heal(s, pct)),
            ('doors',       lambda: self._handle_closed_doors(s)),
            ('go_up',       lambda: self._handle_go_up(s, pct)),
            ('stuck_dung',  lambda: self._handle_stuck_dungeon(s, pct)),
            ('tiny_room',   lambda: self._handle_tiny_room(s)),
            ('oscillate',   lambda: self._handle_oscillation(s)),
            ('explore',     lambda: self._handle_explore(s, pct)),
            ('doors_bfs',   lambda: self._handle_closed_doors_bfs(s)),
        ]

        for name, handler in handlers:
            action = handler()
            if action:
                return action

        return ','  # rest  -  nothing to do
    
    def _bfs_to(self, target, s):
        """BFS pathfinding to a specific target. Returns first step or None."""
        px, py = s.pos
        tx, ty = target
        if (px, py) == (tx, ty):
            return None
        
        all_pass = s.floors | self.known_floors
        if s.stairs_up: all_pass.add(s.stairs_up)
        if s.stairs_down: all_pass.add(s.stairs_down)
        # Add store positions as passable (but not the ones we just left)
        for sx, sy, sn in s.stores:
            if sn not in self.visited_stores:
                all_pass.add((sx, sy))
        
        q = deque([(px, py)]); came = {(px, py): None}
        
        while q and len(came) < 5000:
            cx, cy = q.popleft()
            if (cx, cy) == (tx, ty):
                # Reconstruct path  -  first step
                cur = (tx, ty)
                while cur != (px, py) and cur in came:
                    prev = came[cur]
                    if prev == (px, py):
                        return self._move(cur[0] - px, cur[1] - py, s)
                    cur = prev
                return None
            
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                nx, ny = cx + dx, cy + dy
                if (nx, ny) in came: continue
                if (nx, ny) not in all_pass: continue
                if (nx, ny) in self.known_walls: continue
                if (nx, ny) in s.walls: continue
                came[(nx, ny)] = (cx, cy)
                q.append((nx, ny))
        
        return None  # no path found
    
    def _bfs(self, s):
        px, py = s.pos
        all_pass = s.passable() | self.known_floors
        if self.known_stairs: all_pass.add(self.known_stairs)
        
        # In small rooms, expand passable to include adjacent ? (unknown) tiles
        # The ? might be a corridor, door, or room  -  worth exploring through
        if len(s.floors) < 25:
            for y in range(len(s.lines)):
                for x, ch in enumerate(s.lines[y]):
                    if x < 13: continue  # skip sidebar
                    if ch == '?' and (x, y) not in s.walls and (x, y) not in self.known_walls:
                        # Check if adjacent to a known passable tile
                        for dx, dy in [(1,0),(-1,0),(0,1),(0,-1)]:
                            if (x+dx, y+dy) in all_pass:
                                all_pass.add((x, y))
                                break
        
        q = deque([(px, py)]); came = {(px, py): None}
        best = None; best_s = -999
        
        while q and len(came) < 3000:
            cx, cy = q.popleft()
            sc = self._interest(cx, cy, s)
            if sc > best_s or (sc == best_s and random.random() < 0.3):
                best = (cx, cy); best_s = sc
            
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                nx, ny = cx + dx, cy + dy
                if (nx, ny) in came: continue
                if (nx, ny) in self.known_walls: continue
                if (nx, ny) in all_pass:
                    came[(nx, ny)] = (cx, cy)
                    q.append((nx, ny))
        
        if not best or best == (px, py): return None
        cur = best
        while cur != (px, py) and cur in came:
            prev = came[cur]
            if prev == (px, py):
                return self._move(cur[0] - px, cur[1] - py, s)
            cur = prev
        return None
    
    def _interest(self, x, y, s):
        if (x, y) in self.known_walls: return -999
        if (x, y) in s.walls: return -999
        
        is_down = (s.stairs_down and (x, y) == s.stairs_down)
        is_up = (s.stairs_up and (x, y) == s.stairs_up)
        is_item = any(ix == x and iy == y for ix, iy, _ in s.items)
        is_store = any(sx == x and sy == y for sx, sy, _ in s.stores)
        is_door = any(dx == x and dy == y for dx, dy in s.doors)
        is_weak_monster = any(mx == x and my == y and ch.islower()
                              for mx, my, ch in s.monsters)
        
        if (x, y) not in self.visited:
            sc = 8.0
            if is_down: sc += 25.0  # > always hot  -  depth is everything
            if is_up: sc += 2.0     # < only mildly interesting
            if is_item: sc += 10.0
            if is_store: sc += 30.0  # stores are very interesting in town
            if is_door: sc += 15.0   # doors lead to new areas
            if is_weak_monster and not self._is_town(s):
                sc += 6.0  # weak monsters = free XP  -  worth pursuing
            return sc
        
        v = self.vcount.get((x, y), 1)
        # Strong decay: first visit -2, second -4, third -6...
        # Floors with nothing interesting become invisible quickly
        sc = -2.0 - (v - 1) * 2.0
        # Stairs stay interesting even when visited  -  always worth checking
        if is_down: sc += 20.0
        # Items stay mildly interesting
        if is_item: sc += 5.0
        return sc
    
    def _move(self, dx, dy, s=None, run=True):
        dx = max(-1, min(1, dx)); dy = max(-1, min(1, dy))
        # Angband curses mode: numpad keys, not vi keys
        # 8=Up, 2=Down, 4=Left, 6=Right, 7/9/1/3=diagonals
        # Full diagonal support
        key = (dx, dy)
        numpad = {
            (0, -1): '8', (0, 1): '2', (-1, 0): '4', (1, 0): '6',
            (-1, -1): '7', (1, -1): '9', (-1, 1): '1', (1, 1): '3',
        }
        return numpad.get(key, '5')  # 5 = rest if no direction


if __name__ == '__main__':
    import sys
    import random as _random
    _hungry_names = ['borg', 'crawler', 'maw', 'dive', 'grip', 'worm', 'drift', 'slab',
                     'hunger', 'depth', 'spoor', 'gnaw', 'rift', 'silt', 'mire', 'bone',
                     'chasm', 'flux', 'vault', 'glyph', 'spine', 'forge', 'root', 'ether']
    max_runs = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    for run_num in range(max_runs):
        name = f"hungry-{_hungry_names[run_num % len(_hungry_names)]}-{run_num + 1}"
        print(f"\n=== RUN {run_num + 1}/{max_runs} [{name}] ===", flush=True)
        g = TmuxGame('hungry-borg-angband', f'angband -mgcu -n -u{name}')
        a = AngbandAgent(g)
        try:
            a.run(4000)
        except KeyboardInterrupt:
            print("\nStopped.")
            g.quit()
            break
        g.quit()
        time.sleep(2)
    print(f"\n=== ALL {max_runs} RUNS COMPLETE ===")
