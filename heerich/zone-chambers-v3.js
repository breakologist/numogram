/**
 * zone-chambers-v3.js — Canonical Numogram three-region layout
 *
 * Structure (from numogram-structure.md):
 *   Warp (upper):       zones 3, 6   — self-folding vortex
 *   Time-Circuit (mid): zones 1,8,2,7,5,4 — anticlockwise hexagon
 *   Plex (lower):       zones 0, 9   — abyssal boundary
 *
 * Current connections follow canonical paths:
 *   Time-Circuit: 1→8→2→7→5→4→(back to 1)
 *   Warp: 3↔6 (self-loop)
 *   Plex: 0↔9 (self-loop)
 *   Syzygy lanes: 4::5, 3::6, 2::7, 1::8, 0::9
 */

import { Heerich } from 'heerich'
import { writeFileSync, mkdirSync } from 'fs'
import { resolve, dirname } from 'path'
import { fileURLToPath } from 'url'

const __dirname = dirname(fileURLToPath(import.meta.url))
const OUT_DIR = resolve(__dirname, 'outputs')
mkdirSync(OUT_DIR, { recursive: true })

// ── Zone Definitions ─────────────────────────────────────────────

const ZONE_DATA = [
  { name: 'Void',    color: '#0a0a0a', stroke: '#333', region: 'Plex', size: [5, 2, 5] },
  { name: 'Gate 1',  color: '#1a3a5c', stroke: '#4a7aac', region: 'Circuit', size: [4, 2.5, 4] },
  { name: 'Gate 2',  color: '#2a5a3c', stroke: '#5a8a5c', region: 'Circuit', size: [4, 2.5, 4] },
  { name: 'Gate 3',  color: '#5a3a1c', stroke: '#8a6a3c', region: 'Warp', size: [4, 2.5, 4] },
  { name: 'Zone 4',  color: '#5a1a3c', stroke: '#8a4a6c', region: 'Circuit', size: [4, 2.5, 4] },
  { name: 'Abyss',   color: '#2a0a4c', stroke: '#5a2a8c', region: 'Circuit', size: [6, 3, 6] },
  { name: 'Zone 6',  color: '#1c3a5a', stroke: '#4c6a8a', region: 'Warp', size: [4, 2.5, 4] },
  { name: 'Gate 7',  color: '#3a5a1c', stroke: '#6a8a3c', region: 'Circuit', size: [4, 2.5, 4] },
  { name: 'Gate 8',  color: '#5a3a5a', stroke: '#8a6a8a', region: 'Circuit', size: [4, 2.5, 4] },
  { name: 'Plex',    color: '#1a1a3a', stroke: '#5a5a9a', region: 'Plex', size: [5, 2, 5] },
]

// ── Layout Geometry ─────────────────────────────────────────────
// Three Y levels:
//   Warp:    Y = 24
//   Circuit: Y = 12
//   Plex:    Y = 0

// Time-Circuit hexagon (anticlockwise order: 1→8→2→7→5→4→1)
// Center at (10, 12, 8), radius = 6 (in isometric space)
function hexPos(index, total, cx, cy, cz, radius, y) {
  const angle = (Math.PI / 2) + (2 * Math.PI * index / total)  // start from top
  return {
    x: cx + Math.sin(angle) * radius,
    y: y + cy,
    z: cz + Math.cos(angle) * radius,
  }
}

const CIRCUIT_ZONES = [1, 8, 2, 7, 5, 4]  // anticlockwise order
const CIRCUIT_CENTER = { x: 10, y: 12, z: 8 }

const POSITIONS = {}

// Time-Circuit zones on hexagon
for (let i = 0; i < CIRCUIT_ZONES.length; i++) {
  const z = CIRCUIT_ZONES[i]
  const angle = (Math.PI / 2) + (2 * Math.PI * i / CIRCUIT_ZONES.length)
  POSITIONS[z] = {
    x: CIRCUIT_CENTER.x + Math.sin(angle) * 7,
    y: CIRCUIT_CENTER.y,
    z: CIRCUIT_CENTER.z + Math.cos(angle) * 7 * 1.1,  // stretch Z for isometric depth
  }
}

// Warp (above circuit)
POSITIONS[3] = { x: CIRCUIT_CENTER.x - 5, y: 24, z: CIRCUIT_CENTER.z }
POSITIONS[6] = { x: CIRCUIT_CENTER.x + 5, y: 24, z: CIRCUIT_CENTER.z }

// Plex (below circuit)
POSITIONS[0] = { x: CIRCUIT_CENTER.x - 3, y: 0, z: CIRCUIT_CENTER.z }
POSITIONS[9] = { x: CIRCUIT_CENTER.x + 3, y: 0, z: CIRCUIT_CENTER.z }

// ── Canonical Connections ───────────────────────────────────────

const TIME_CIRCUIT_PATH = [
  [1, 8], [8, 2], [2, 7], [7, 5], [5, 4], [4, 1]
]

const WARP_CONNECTIONS = [[3, 6]]
const PLEX_CONNECTIONS = [[0, 9]]

// Syzygy cross-connections (pairs summing to 9)
const SYZYGIES = [
  { pair: [4, 5], current: 1, color: '#ff6644', label: 'Current 1' },
  { pair: [3, 6], current: 3, color: '#ffaa33', label: 'Current 3' },
  { pair: [2, 7], current: 5, color: '#44ff66', label: 'Current 5' },
  { pair: [1, 8], current: 7, color: '#44aaff', label: 'Current 7' },
  { pair: [0, 9], current: 9, color: '#aa44ff', label: 'Current 9' },
]

// Gates (triangular-indexed connections)
const GATES = [
  [6, 3], [3, 6],  // Gt-6 / Gt-21 — Warp internal
  [8, 9],          // Gt-36 — Zone-8 → Plex plunge
]

// ── Build Scene ─────────────────────────────────────────────────

const heerich = new Heerich({
  tile: 3,
  camera: {
    type: 'oblique',
    angle: 315,
    distance: 55,
  },
  style: {
    default: { fill: '#1a1a1a', stroke: '#333', strokeWidth: 0.2 },
  },
  gap: 0.08,
})

// ── 1. Zone chambers ────────────────────────────────────────────

for (let z = 0; z <= 9; z++) {
  const pos = POSITIONS[z]
  const { size: [sx, sy, sz] } = ZONE_DATA[z]
  const { color, stroke, region } = ZONE_DATA[z]

  // Region-specific styling
  const topFill = region === 'Warp' ? '#ff8833' :
                  region === 'Plex' ? '#333366' :
                  '#446688'

  heerich.applyGeometry({
    type: 'box',
    center: [pos.x, pos.y + sy / 2, pos.z],
    size: [sx, sy, sz],
    style: {
      default: { fill: color, stroke, strokeWidth: 0.3 },
      top: { fill: topFill, stroke: '#888', strokeWidth: 0.15 },
      bottom: { fill: '#111', stroke: '#333', strokeWidth: 0.1 },
    },
  })
}

// ── 2. Time-Circuit currents (anticlockwise) ────────────────────

for (const [from, to] of TIME_CIRCUIT_PATH) {
  const a = POSITIONS[from]
  const b = POSITIONS[to]
  const sy = ZONE_DATA[from].size[1]

  const midX = (a.x + b.x) / 2
  const midY = a.y + sy
  const midZ = (a.z + b.z) / 2

  // Riser + tread staircase
  heerich.applyGeometry({
    type: 'line',
    from: [a.x, a.y + sy, a.z],
    to: [midX, midY, midZ],
    radius: 0.8,
    shape: 'rounded',
    style: { default: { fill: '#4488cc', stroke: '#aaddff', strokeWidth: 0.15 } },
  })
  heerich.applyGeometry({
    type: 'line',
    from: [midX, midY, midZ],
    to: [b.x, b.y, b.z],
    radius: 0.8,
    shape: 'rounded',
    style: { default: { fill: '#4488cc', stroke: '#aaddff', strokeWidth: 0.15 } },
  })
}

// ── 3. Syzygy lanes ─────────────────────────────────────────────

for (const s of SYZYGIES) {
  const [z1, z2] = s.pair
  const a = POSITIONS[z1]
  const b = POSITIONS[z2]
  const { color } = s

  // Draw syzygy as a direct line between zone centers
  heerich.applyGeometry({
    type: 'line',
    from: [a.x, a.y + 1, a.z],
    to: [b.x, b.y + 1, b.z],
    radius: 0.4,
    shape: 'rounded',
    style: { default: { fill: color, stroke: '#fff', strokeWidth: 0.1 } },
  })
}

// ── 4. Warp connection (3↔6) ────────────────────────────────────

for (const [from, to] of WARP_CONNECTIONS) {
  const a = POSITIONS[from]
  const b = POSITIONS[to]
  const midX = (a.x + b.x) / 2
  const midY = a.y + 3
  const midZ = (a.z + b.z) / 2

  // Arch shape: two lines forming a peak
  heerich.applyGeometry({
    type: 'line',
    from: [a.x, a.y, a.z],
    to: [midX, midY, midZ],
    radius: 1,
    shape: 'rounded',
    style: { default: { fill: '#ff8833', stroke: '#ffcc66', strokeWidth: 0.2 } },
  })
  heerich.applyGeometry({
    type: 'line',
    from: [midX, midY, midZ],
    to: [b.x, b.y, b.z],
    radius: 1,
    shape: 'rounded',
    style: { default: { fill: '#ff8833', stroke: '#ffcc66', strokeWidth: 0.2 } },
  })
}

// ── 5. Plex connection (0↔9) ────────────────────────────────────

for (const [from, to] of PLEX_CONNECTIONS) {
  const a = POSITIONS[from]
  const b = POSITIONS[to]
  heerich.applyGeometry({
    type: 'line',
    from: [a.x, a.y + ZONE_DATA[from].size[1], a.z],
    to: [b.x, b.y + ZONE_DATA[to].size[1], b.z],
    radius: 0.6,
    shape: 'rounded',
    style: { default: { fill: '#6644cc', stroke: '#aa88ff', strokeWidth: 0.15 } },
  })
}

// ── 6. Gate-arches (triangular gates) ────────────────────────────

for (const [z1, z2] of GATES) {
  const a = POSITIONS[z1]
  const b = POSITIONS[z2]

  // Gate etch: small subtraction at midpoint
  const midX = (a.x + b.x) / 2
  const midY = (a.y + ZONE_DATA[z1].size[1]/2 + b.y + ZONE_DATA[z2].size[1]/2) / 2
  const midZ = (a.z + b.z) / 2

  heerich.removeGeometry({
    type: 'sphere',
    center: [midX, midY, midZ],
    radius: 1.5,
  })
}

// ── 7. Ground plane ─────────────────────────────────────────────

heerich.applyGeometry({
  type: 'box',
  center: [10, -0.5, 8],
  size: [26, 0.3, 18],
  style: {
    top: { fill: '#0d0d1a' },
    default: { fill: '#0d0d1a', stroke: '#1a1a33', strokeWidth: 0.1 },
  },
})

// ── Region labels using voxel text (line primitives) ────────────

function makeLabel(text, x, y, z, color) {
  // Simple label: small box platform + current path letters
  heerich.applyGeometry({
    type: 'box',
    center: [x, y, z],
    size: [text.length + 1, 0.5, 1],
    style: { top: { fill: color }, default: { fill: color, stroke: '#888', strokeWidth: 0.1 } },
  })
}

// Region label platforms
makeLabel('WARP',   POSITIONS[3].x - 2,  27, POSITIONS[3].z, '#ff8833')
makeLabel('CIRCUIT', CIRCUIT_CENTER.x,     15, CIRCUIT_CENTER.z - 8, '#4488cc')
makeLabel('PLEX',   POSITIONS[0].x + 3,   -1, POSITIONS[0].z, '#6644cc')

// ── Render ───────────────────────────────────────────────────────

const svg = heerich.toSVG({
  padding: 50,
})

const outPath = resolve(OUT_DIR, 'numogram-canonical-v3.svg')
writeFileSync(outPath, svg, 'utf-8')

const rawSizeKb = (svg.length / 1024).toFixed(1)
const faces = heerich.getFaces()

console.log(`✓ Wrote ${outPath}`)
console.log(`  SVG size: ${rawSizeKb} KB`)
console.log(`  Visible faces: ${faces.length}`)
console.log(`  Layout: ${CIRCUIT_ZONES.length}-zone hexagon (Time-Circuit) + Warp above + Plex below`)
console.log(`  Time-Circuit path: ${TIME_CIRCUIT_PATH.map(p => `${p[0]}→${p[1]}`).join(' → ')}`)
