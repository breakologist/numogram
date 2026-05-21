/**
 * zone-chambers-v4.js — Canonical qliphoth labyrinth layout
 *
 * Uses exact zone positions, colors, and regions from lumpenspace/ccru
 * (positions.ts, zones.ts, currents.ts, syzygies.ts, gates.ts).
 *
 * Three Y-levels: Warp↑ | Torque (Time-Circuit) | Plex↓
 * Zone colors, particles, and demon names from canonical qliphoth data.
 */

import { Heerich } from 'heerich'
import { writeFileSync, mkdirSync } from 'fs'
import { resolve, dirname } from 'path'
import { fileURLToPath } from 'url'

const __dirname = dirname(fileURLToPath(import.meta.url))
const OUT_DIR = resolve(__dirname, 'outputs')
mkdirSync(OUT_DIR, { recursive: true })

// ── Canonical Qliphoth Data ─────────────────────────────────────

// From positions.ts — Labyrinth layout (pixel coords)
const QPOS = {
  6: { x: 305, y: 60 },   3: { x: 495, y: 60 },
  2: { x: 400, y: 220 },
  5: { x: 200, y: 335 },  7: { x: 600, y: 335 },
  4: { x: 200, y: 540 },  8: { x: 600, y: 540 },
  1: { x: 400, y: 655 },
  9: { x: 305, y: 815 },  0: { x: 495, y: 815 },
}

// From zones.ts
const ZONE_CLR = {
  0: '#aaaaaa', 1: '#ee44ee', 2: '#4488ff', 3: '#44cc77', 4: '#ee4444',
  5: '#ee8833', 6: '#ddcc33', 7: '#7755cc', 8: '#9944ee', 9: '#666666',
}

const ZONE_REGION = {
  0: 'plex', 1: 'torque', 2: 'torque', 3: 'warp', 4: 'torque',
  5: 'torque', 6: 'warp', 7: 'torque', 8: 'torque', 9: 'plex',
}

const ZONE_PARTICLE = {
  0: 'eiaoung', 1: 'gl', 2: 'dt', 3: 'zx', 4: 'skr',
  5: 'ktt', 6: 'tch', 7: 'pb', 8: 'mnm', 9: 'tn',
}

const ZONE_DEMON = {
  1: 'Lurgo', 2: 'Duoddod', 3: 'Ixix', 4: 'Krako',
  5: 'Tokhatto', 6: 'Djynxx', 7: 'Oddubb', 8: 'Murrumur',
}

// From currents.ts — named flows
const CURRENTS = [
  { from: 8, to: 7, name: 'Surge', diff: 7, color: '#cc66ff' },
  { from: 2, to: 5, name: 'Hold',  diff: 5, color: '#66ccff' },
  { from: 4, to: 1, name: 'Sink',  diff: 1, color: '#ff6644' },
  { from: 6, to: 3, name: 'Warp',  diff: 3, color: '#ffcc33' },
  { from: 9, to: 9, name: 'Plex',  diff: 9, color: '#8844ff' },
]

// From gates.ts — key gates
const GATES = [
  { name: 'Gt-06', from: 3, to: 6, cum: 6 },
  { name: 'Gt-21', from: 6, to: 3, cum: 21 },
  { name: 'Gt-15', from: 5, to: 6, cum: 15 },
  { name: 'Gt-36', from: 8, to: 9, cum: 36 },
]

// ── 3D Layout ───────────────────────────────────────────────────
// Scale pixel coords to voxel grid
// Three Y levels: Warp=24, Torque=12, Plex=0

const REGION_Y = { warp: 24, torque: 12, plex: 0 }

function to3D(z) {
  const p = QPOS[z]
  const region = ZONE_REGION[z]
  return {
    x: (p.x - 400) / 15,     // center at 400, spread wider
    y: REGION_Y[region],
    z: (875 - p.y) / 20 + 1,  // invert y → z, spread deeper
  }
}

const POS = {}
for (let z = 0; z <= 9; z++) {
  POS[z] = to3D(z)
}

// ── Build Scene ─────────────────────────────────────────────────

const heerich = new Heerich({
  tile: 6,
  camera: {
    type: 'oblique',
    angle: 315,
    distance: 60,
  },
  style: {
    default: { fill: '#111', stroke: '#333', strokeWidth: 0.2 },
  },
  gap: 0.1,
})

// ── 1. Zone chambers ────────────────────────────────────────────

for (let z = 0; z <= 9; z++) {
  const p = POS[z]
  const color = ZONE_CLR[z]
  const region = ZONE_REGION[z]

  // Chamber size varies by region — bigger for clearer visibility
  const size = z === 5 ? [7, 3, 7] :    // Abyss (Zone-5) largest
               z === 0 ? [5, 2, 5] :    // Void — low, wide
               z === 9 ? [5, 2, 5] :    // Plex — low, wide
               [5, 2.5, 5]              // standard

  // Top face color based on region
  const topFill = region === 'warp' ? '#44cc77' :
                  region === 'plex' ? '#666666' :
                  '#4488ff'  // torque

  heerich.applyGeometry({
    type: 'box',
    center: [p.x, p.y + size[1]/2, p.z],
    size,
    style: {
      default: { fill: color, stroke: '#fff', strokeWidth: 0.15, opacity: 0.9 },
      top: { fill: topFill, stroke: '#fff', strokeWidth: 0.1 },
    },
  })
}

// ── 2. Current paths (from currents.ts) ─────────────────────────

for (const c of CURRENTS) {
  if (c.from === c.to) {
    // Self-loop (Plex) — small circle-ish path
    const p = POS[c.from]
    heerich.applyGeometry({
      type: 'line',
      from: [p.x - 1, p.y + 0.5, p.z],
      to: [p.x + 1, p.y + 0.5, p.z],
      radius: 0.4,
      shape: 'rounded',
      style: { default: { fill: c.color, stroke: '#fff', strokeWidth: 0.1 } },
    })
    continue
  }

  const a = POS[c.from]
  const b = POS[c.to]
  const midX = (a.x + b.x) / 2
  const midY = (a.y + b.y) / 2 + 1
  const midZ = (a.z + b.z) / 2

  // Staircase: riser + tread
  heerich.applyGeometry({
    type: 'line',
    from: [a.x, a.y + 1, a.z],
    to: [midX, midY, midZ],
    radius: 0.5,
    shape: 'rounded',
    style: { default: { fill: c.color, stroke: '#fff', strokeWidth: 0.08 } },
  })
  heerich.applyGeometry({
    type: 'line',
    from: [midX, midY, midZ],
    to: [b.x, b.y + 1, b.z],
    radius: 0.5,
    shape: 'rounded',
    style: { default: { fill: c.color, stroke: '#fff', strokeWidth: 0.08 } },
  })
}

// ── 3. Time Circuit anticlockwise ring ───────────────────────────
// Path: 1→8→2→7→5→4→1
const TC_PATH = [1, 8, 2, 7, 5, 4, 1]
for (let i = 0; i < TC_PATH.length - 1; i++) {
  const a = POS[TC_PATH[i]]
  const b = POS[TC_PATH[i + 1]]
  heerich.applyGeometry({
    type: 'line',
    from: [a.x, a.y + 0.5, a.z],
    to: [b.x, b.y + 0.5, b.z],
    radius: 0.25,
    shape: 'rounded',
    style: { default: { fill: '#44aaff', stroke: 'none' } },
  })
}

// ── 4. Gate connections ─────────────────────────────────────────

for (const g of GATES) {
  const a = POS[g.from]
  const b = POS[g.to]
  const midX = (a.x + b.x) / 2
  const midY = (a.y + b.y) / 2 + 1
  const midZ = (a.z + b.z) / 2

  // Gate tunnels: carved sphere at midpoint
  heerich.removeGeometry({
    type: 'sphere',
    center: [midX, midY, midZ],
    radius: 1.2,
  })

  // Gate marker: small bright line
  heerich.applyGeometry({
    type: 'line',
    from: [midX - 0.5, midY, midZ],
    to: [midX + 0.5, midY, midZ],
    radius: 0.3,
    shape: 'rounded',
    style: { default: { fill: '#ff44ff', stroke: '#fff', strokeWidth: 0.1 } },
  })
}

// ── 5. Ground plane ─────────────────────────────────────────────

heerich.applyGeometry({
  type: 'box',
  center: [0, -0.3, 5],
  size: [40, 0.3, 28],
  style: {
    top: { fill: '#0a0a15' },
    default: { fill: '#0a0a15', stroke: '#1a1a33', strokeWidth: 0.1 },
  },
})

// ── Render ───────────────────────────────────────────────────────

const svg = heerich.toSVG({
  padding: 50,
})

const outPath = resolve(OUT_DIR, 'numogram-qliphoth-v4.svg')
writeFileSync(outPath, svg, 'utf-8')

const faces = heerich.getFaces()
const sizeKb = (svg.length / 1024).toFixed(1)

console.log(`✓ Wrote ${outPath}`)
console.log(`  Size: ${sizeKb} KB, Faces: ${faces.length}`)
console.log(`  Regions: Warp↑ (3,6) | Torque (1,2,4,5,7,8) | Plex↓ (0,9)`)
console.log(`  Currents: Surge(8→7) Hold(2→5) Sink(4→1) Warp(6→3) Plex(9→9)`)
console.log(`  Camera: isometric 45°`)
