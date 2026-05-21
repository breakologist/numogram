/**
 * zone-chambers.js — Numogram decimal labyrinth as 3D voxel SVG
 *
 * Renders 10 zone chambers with currents and gates using heerich.js.
 * First prototype: vertical tower with descending chambers,
 * connected by stair-like currents with carved gate-arches.
 */

import { Heerich } from 'heerich'
import { writeFileSync, mkdirSync } from 'fs'
import { resolve, dirname } from 'path'
import { fileURLToPath } from 'url'

const __dirname = dirname(fileURLToPath(import.meta.url))
const OUT_DIR = resolve(__dirname, 'outputs')
mkdirSync(OUT_DIR, { recursive: true })

// ── Zone Definitions ─────────────────────────────────────────────

const ZONES = {
  0: { name: 'Void',   color: '#0a0a0a',  stroke: '#222',  size: [5, 2, 5],  y: 0,  desc: 'Total compression, unmanifest' },
  1: { name: 'Gate 1', color: '#1a3a5c',  stroke: '#2a5a8c', size: [5, 3, 5],  y: 3,  desc: 'First emergence' },
  2: { name: 'Gate 2', color: '#2a5a3c',  stroke: '#3a8a5c', size: [5, 3, 5],  y: 6,  desc: 'Second path' },
  3: { name: 'Gate 3', color: '#5a3a1c',  stroke: '#8a5a2c', size: [5, 3, 5],  y: 9,  desc: 'Third path' },
  4: { name: 'Zone 4', color: '#5a1a3c',  stroke: '#8a2a5c', size: [6, 3, 6],  y: 12, desc: 'Turning, structured' },
  5: { name: 'Abyss',  color: '#3a1a5c',  stroke: '#5a2a8c', size: [8, 4, 8],  y: 15, desc: 'Maximum entropy, the pivot' },
  6: { name: 'Zone 6', color: '#1c3a5a',  stroke: '#2c5a8a', size: [6, 3, 6],  y: 18, desc: 'Return current' },
  7: { name: 'Gate 7', color: '#3a5a1c',  stroke: '#5a8a2c', size: [5, 3, 5],  y: 21, desc: 'Seventh gate' },
  8: { name: 'Gate 8', color: '#5a3a5a',  stroke: '#8a5a8a', size: [5, 3, 5],  y: 24, desc: 'Eighth gate' },
  9: { name: 'Plex',   color: '#1a1a3a',  stroke: '#4a4a8a', size: [7, 3, 7],  y: 27, desc: 'Total interconnection' },
}

// Currents: ordered paths through the decimal labyrinth
const CURRENTS = [
  // Current 1 (left): 0 → 1 → 6 → 9
  { zones: [0, 1, 6, 9], color: '#4488cc', label: 'Current 1' },
  // Current 2 (center): 0 → 2 → 5 → 7 → 9
  { zones: [0, 2, 5, 7, 9], color: '#44cc88', label: 'Current 2' },
  // Current 3 (right): 0 → 3 → 4 → 8 → 9
  { zones: [0, 3, 4, 8, 9], color: '#cc8844', label: 'Current 3' },
]

// Gates (syzygies) — additional connections between zones
const GATES = [
  [1, 2], [2, 3],  // upper cross-connections
  [6, 5], [5, 4],  // mid cross-connections
  [7, 8],          // lower cross-connection
]

// ── Layout ──────────────────────────────────────────────────────

// Compute X positions so currents spread left-to-right
// Current 1 (left): zones 0,1,6    → x=6
// Current 2 (center): zones 0,2,5,7 → x=12
// Current 3 (right): zones 0,3,4,8  → x=18
// Zone 9 (Plex) sits at center: x=12

const ZONE_X = {}
for (const z of [0, 1, 6]) ZONE_X[z] = 6
for (const z of [0, 2, 5, 7]) ZONE_X[z] = 12
for (const z of [0, 3, 4, 8]) ZONE_X[z] = 18
ZONE_X[9] = 12  // Plex at center

// Z offset — alternate for visual depth
const ZONE_Z = {
  0: 6, 1: 5, 2: 7, 3: 5, 4: 7, 5: 6, 6: 5, 7: 7, 8: 5, 9: 6,
}

// ── Build Scene ─────────────────────────────────────────────────

const heerich = new Heerich({
  tile: 3,
  camera: {
    type: 'oblique',
    angle: 315,
    distance: 60,
  },
  style: {
    default: { fill: '#222', stroke: '#444', strokeWidth: 0.3 },
  },
  gap: 0.08,
})

// Helper: interpolate between two zone centers
function zoneCenter(z) {
  const info = ZONES[z]
  const x = ZONE_X[z]
  const y = info.y
  const zz = ZONE_Z[z]
  return { x, y, z: zz }
}

// ── 1. Build Zone Chambers ──────────────────────────────────────

for (const [id, info] of Object.entries(ZONES)) {
  const z = Number(id)
  const { x, y, z: zz } = zoneCenter(z)
  const [sx, sy, sz] = info.size

  // Compute brightness gradient based on zone depth
  const depthFactor = 1 - (y / 30)  // 0 (top) to 1 (bottom)
  const luminance = Math.round(20 + depthFactor * 40)

  heerich.applyGeometry({
    type: 'box',
    center: [x, y + sy/2, zz],
    size: [sx, sy, sz],
    style: {
      default: (vx, vy, vz) => ({
        fill: info.color,
        stroke: info.stroke,
        strokeWidth: 0.4,
      }),
      top: { fill: info.color.replace(')', ', 0.8)').replace('rgb', 'rgba') || info.color },
      bottom: { fill: '#111', stroke: '#333' },
    },
  })
}

// ── 2. Build Currents (stair-like connections) ───────────────────

for (const current of CURRENTS) {
  const { zones, color, label } = current

  for (let i = 0; i < zones.length - 1; i++) {
    const from = zones[i]
    const to = zones[i + 1]
    const c1 = zoneCenter(from)
    const c2 = zoneCenter(to)

    // Draw a stepped path: from top of lower zone to bottom of higher zone
    const midY = (c1.y + c2.y) / 2 + (ZONES[from].size[1] / 2)
    const midX = (c1.x + c2.x) / 2
    const midZ = (c1.z + c2.z) / 2

    // Vertical riser
    heerich.applyGeometry({
      type: 'line',
      from: [c1.x, c1.y + ZONES[from].size[1], c1.z],
      to: [midX, midY, midZ],
      radius: 0.8,
      shape: 'rounded',
      style: {
        default: { fill: color, stroke: '#fff', strokeWidth: 0.2 },
      },
    })

    // Horizontal tread
    heerich.applyGeometry({
      type: 'line',
      from: [midX, midY, midZ],
      to: [c2.x, c2.y, c2.z],
      radius: 0.8,
      shape: 'rounded',
      style: {
        default: { fill: color, stroke: '#fff', strokeWidth: 0.2 },
      },
    })
  }
}

// ── 3. Carve Gate Arches (syzygy connections) ───────────────────

for (const [z1, z2] of GATES) {
  const c1 = zoneCenter(z1)
  const c2 = zoneCenter(z2)

  // Gate arch: carve a sphere (tunnel) between the two zone chambers
  const midX = (c1.x + c2.x) / 2
  const midY = (c1.y + ZONES[z1].size[1]/2 + c2.y + ZONES[z2].size[1]/2) / 2
  const midZ = (c1.z + c2.z) / 2

  heerich.removeGeometry({
    type: 'sphere',
    center: [midX, midY, midZ],
    radius: 2.5,
  })
}

// ── 4. Ground Plane ─────────────────────────────────────────────

heerich.applyGeometry({
  type: 'box',
  center: [12, -0.5, 6],
  size: [24, 0.5, 14],
  style: {
    default: { fill: '#1a1a2e', stroke: '#2a2a4e', strokeWidth: 0.2 },
    top: { fill: '#1a1a2e' },
  },
})

// ── Render ───────────────────────────────────────────────────────

const svg = heerich.toSVG({
  padding: 40,
})

const outPath = resolve(OUT_DIR, 'numogram-labyrinth.svg')
writeFileSync(outPath, svg, 'utf-8')
console.log(`✓ Wrote ${outPath}`)
console.log(`  SVG size: ${(svg.length / 1024).toFixed(1)} KB`)

// ── Also export raw face data for use in other tools ────────────

const faces = heerich.getFaces()
console.log(`  Total visible faces: ${faces.length}`)
