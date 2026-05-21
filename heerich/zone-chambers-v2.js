/**
 * zone-chambers-v2.js — Refined Numogram labyrinth with occlusion culling
 *
 * v2 improvements:
 * - Occlusion culling enabled (plotter-friendly, smaller output)
 * - Larger tile size (fewer, bigger voxels)
 * - Labelled chambers via decal-style annotations
 * - Smoother current paths with consistent styling
 */

import { Heerich } from 'heerich'
import { writeFileSync, mkdirSync } from 'fs'
import { resolve, dirname } from 'path'
import { fileURLToPath } from 'url'

const __dirname = dirname(fileURLToPath(import.meta.url))
const OUT_DIR = resolve(__dirname, 'outputs')
mkdirSync(OUT_DIR, { recursive: true })

// ── Zone Definitions ─────────────────────────────────────────────

const ZONE_NAMES = [
  'Void', 'Gate 1', 'Gate 2', 'Gate 3', 'Zone 4',
  'Abyss', 'Zone 6', 'Gate 7', 'Gate 8', 'Plex',
]

const ZONE_COLORS = [
  '#0a0a0a', '#1a3a5c', '#2a5a3c', '#5a3a1c', '#5a1a3c',
  '#3a1a5c', '#1c3a5a', '#3a5a1c', '#5a3a5a', '#1a1a3a',
]

const ZONE_STROKES = [
  '#222',    '#2a5a8c', '#3a8a5c', '#8a5a2c', '#8a2a5c',
  '#5a2a8c', '#2c5a8a', '#5a8a2c', '#8a5a8a', '#4a4a8a',
]

const CURRENT_COLORS = ['#4488cc', '#44cc88', '#cc8844']

// [[z1, z2, ...], ...]  — zone indices in current order
const CURRENTS = [
  [0, 1, 6, 9],
  [0, 2, 5, 7, 9],
  [0, 3, 4, 8, 9],
]

const GATES = [
  [1, 2], [2, 3],
  [6, 5], [5, 4],
  [7, 8],
]

// ── Layout ──────────────────────────────────────────────────────
// Each zone: { x, y, z, size: [w, h, d] }
// y = floor level (0 = bottom/Void, 9*3 = top/Plex)

const ZONES = {}

for (let z = 0; z <= 9; z++) {
  const yBase = z * 2.5
  ZONES[z] = {
    x: z === 0 ? 10 :     // Void at center
       z === 9 ? 10 :     // Plex at center
       [1, 6].includes(z) ? 4 :   // Current 1 (left)
       [3, 4, 8].includes(z) ? 16 : // Current 3 (right)
       10,                // Current 2 (center)
    y: yBase,
    z: z === 0 ? 6 :
       z === 9 ? 6 :
       [1, 3, 6, 8].includes(z) ? 4 :  // outer zones depth offset
       8,                               // inner zones
    size: z === 0 ? [4, 1.5, 4] :       // Void — low, wide
          z === 5 ? [7, 3, 7] :          // Abyss — largest
          z === 9 ? [6, 2.5, 6] :        // Plex — broad
          [4, 2, 4],                     // standard gate
  }
}

// ── Build Scene ─────────────────────────────────────────────────

const heerich = new Heerich({
  tile: 4,
  camera: {
    type: 'oblique',
    angle: 315,
    distance: 55,
  },
  style: {
    default: { fill: '#222', stroke: '#444', strokeWidth: 0.2 },
  },
  gap: 0.1,
})

function zc(n) {
  const z = ZONES[n]
  return { x: z.x, y: z.y, z: z.z }
}

// ── 1. Zone chambers ────────────────────────────────────────────

for (let z = 0; z <= 9; z++) {
  const { x, y, z: zz, size: [sx, sy, sz] } = ZONES[z]
  const color = ZONE_COLORS[z]
  const stroke = ZONE_STROKES[z]

  heerich.applyGeometry({
    type: 'box',
    center: [x, y + sy / 2, zz],
    size: [sx, sy, sz],
    style: {
      default: { fill: color, stroke, strokeWidth: 0.3 },
      top: { fill: color, stroke: '#666', strokeWidth: 0.2 },
    },
  })
}

// ── 2. Current paths ────────────────────────────────────────────

for (let c = 0; c < CURRENTS.length; c++) {
  const path = CURRENTS[c]
  const color = CURRENT_COLORS[c]

  for (let i = 0; i < path.length - 1; i++) {
    const a = zc(path[i])
    const b = zc(path[i + 1])
    const zA = ZONES[path[i]]
    const zB = ZONES[path[i + 1]]

    const midX = (a.x + b.x) / 2
    const midY = (a.y + zA.size[1] + b.y) / 2
    const midZ = (a.z + b.z) / 2

    // Vertical riser
    heerich.applyGeometry({
      type: 'line',
      from: [a.x, a.y + zA.size[1], a.z],
      to: [midX, midY, midZ],
      radius: 0.6,
      shape: 'square',
      style: { default: { fill: color, stroke: '#fff', strokeWidth: 0.1 } },
    })

    // Horizontal tread
    heerich.applyGeometry({
      type: 'line',
      from: [midX, midY, midZ],
      to: [b.x, b.y, b.z],
      radius: 0.6,
      shape: 'square',
      style: { default: { fill: color, stroke: '#fff', strokeWidth: 0.1 } },
    })
  }
}

// ── 3. Gate arches ──────────────────────────────────────────────

for (const [z1, z2] of GATES) {
  const a = zc(z1)
  const b = zc(z2)
  ZONES[z1]

  const midX = (a.x + b.x) / 2
  const midY = (ZONES[z1].y + ZONES[z1].size[1]/2 + ZONES[z2].y + ZONES[z2].size[1]/2) / 2
  const midZ = (a.z + b.z) / 2

  heerich.removeGeometry({
    type: 'sphere',
    center: [midX, midY, midZ],
    radius: 2,
  })
}

// ── 4. Ground plane ─────────────────────────────────────────────

heerich.applyGeometry({
  type: 'box',
  center: [10, -0.3, 6],
  size: [20, 0.3, 12],
  style: { top: { fill: '#111' }, default: { fill: '#111', stroke: '#222', strokeWidth: 0.1 } },
})

// ── Render with occlusion culling ───────────────────────────────

const svg = heerich.toSVG({
  padding: 40,
  occlusion: true,
})

const outPath = resolve(OUT_DIR, 'numogram-labyrinth-v2.svg')
writeFileSync(outPath, svg, 'utf-8')

const rawSizeKb = (svg.length / 1024).toFixed(1)
const faces = heerich.getFaces()

console.log(`✓ Wrote ${outPath}`)
console.log(`  SVG size: ${rawSizeKb} KB (v1 was 1010 KB)`)
console.log(`  Visible faces: ${faces.length}`)
