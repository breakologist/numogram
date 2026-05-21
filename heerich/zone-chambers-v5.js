/**
 * zone-chambers-v5.js — Canonical qliphoth layout WITH TEXT LABELS
 *
 * Uses face data from getFaces() to position SVG text labels
 * at each zone chamber's projected screen center.
 *
 * Labels show: Zone number, Qliphoth name, Demon name, Particle
 */

import { Heerich } from 'heerich'
import { writeFileSync, mkdirSync } from 'fs'
import { resolve, dirname } from 'path'
import { fileURLToPath } from 'url'

const __dirname = dirname(fileURLToPath(import.meta.url))
const OUT_DIR = resolve(__dirname, 'outputs')
mkdirSync(OUT_DIR, { recursive: true })

// ── Canonical Qliphoth Data ─────────────────────────────────────

const QPOS = {
  6: { x: 305, y: 60 },   3: { x: 495, y: 60 },
  2: { x: 400, y: 220 },
  5: { x: 200, y: 335 },  7: { x: 600, y: 335 },
  4: { x: 200, y: 540 },  8: { x: 600, y: 540 },
  1: { x: 400, y: 655 },
  9: { x: 305, y: 815 },  0: { x: 495, y: 815 },
}

const ZONE_CLR = {
  0: '#aaaaaa', 1: '#ee44ee', 2: '#4488ff', 3: '#44cc77', 4: '#ee4444',
  5: '#ee8833', 6: '#ddcc33', 7: '#7755cc', 8: '#9944ee', 9: '#666666',
}

const ZONE_REGION = { 0: 'plex', 1: 'torque', 2: 'torque', 3: 'warp', 4: 'torque',
  5: 'torque', 6: 'warp', 7: 'torque', 8: 'torque', 9: 'plex' }

const ZONE_PARTICLE = { 0: 'eiaoung', 1: 'gl', 2: 'dt', 3: 'zx', 4: 'skr',
  5: 'ktt', 6: 'tch', 7: 'pb', 8: 'mnm', 9: 'tn' }

const ZONE_DEMON = { 1: 'Lurgo', 2: 'Duoddod', 3: 'Ixix', 4: 'Krako',
  5: 'Tokhatto', 6: 'Djynxx', 7: 'Oddubb', 8: 'Murrumur' }

const ZONE_PLANET = { 0: 'Sun', 1: 'Mercury', 2: 'Venus', 3: 'Earth', 4: 'Mars',
  5: 'Jupiter', 6: 'Saturn', 7: 'Uranus', 8: 'Neptune', 9: 'Pluto' }

const ZONE_NAME = { 0: 'Void', 1: 'Gate 1', 2: 'Gate 2', 3: 'Gate 3',
  4: 'Zone 4', 5: 'Abyss', 6: 'Zone 6', 7: 'Gate 7', 8: 'Gate 8', 9: 'Plex' }

const CURRENTS = [
  { from: 8, to: 7, name: 'Surge', diff: 7, color: '#cc66ff' },
  { from: 2, to: 5, name: 'Hold',  diff: 5, color: '#66ccff' },
  { from: 4, to: 1, name: 'Sink',  diff: 1, color: '#ff6644' },
  { from: 6, to: 3, name: 'Warp',  diff: 3, color: '#ffcc33' },
  { from: 9, to: 9, name: 'Plex',  diff: 9, color: '#8844ff' },
]

const GATES = [
  { name: 'Gt-06', from: 3, to: 6, cum: 6 },
  { name: 'Gt-21', from: 6, to: 3, cum: 21 },
  { name: 'Gt-15', from: 5, to: 6, cum: 15 },
  { name: 'Gt-36', from: 8, to: 9, cum: 36 },
]

const REGION_Y = { warp: 24, torque: 12, plex: 0 }

function to3D(z) {
  const p = QPOS[z]
  const region = ZONE_REGION[z]
  return {
    x: (p.x - 400) / 15,
    y: REGION_Y[region],
    z: (875 - p.y) / 20 + 1,
  }
}

const POS = {}
for (let z = 0; z <= 9; z++) POS[z] = to3D(z)

// ── Build Scene ─────────────────────────────────────────────────

const heerich = new Heerich({
  tile: 6,
  camera: { type: 'oblique', angle: 315, distance: 60 },
  style: { default: { fill: '#111', stroke: '#333', strokeWidth: 0.2 } },
  gap: 0.1,
})

// 1. Zone chambers
for (let z = 0; z <= 9; z++) {
  const p = POS[z]
  const color = ZONE_CLR[z]
  const region = ZONE_REGION[z]
  const size = z === 5 ? [7, 3, 7] :
               [5, 2.5, 5]
  const topFill = region === 'warp' ? '#44cc77' :
                  region === 'plex' ? '#666666' : '#4488ff'
  heerich.applyGeometry({
    type: 'box',
    center: [p.x, p.y + size[1]/2, p.z],
    size,
    style: {
      default: { fill: color, stroke: '#fff', strokeWidth: 0.15 },
      top: { fill: topFill, stroke: '#fff', strokeWidth: 0.1 },
    },
  })
}

// 2. Current paths
for (const c of CURRENTS) {
  if (c.from === c.to) { continue }
  const a = POS[c.from]; const b = POS[c.to]
  const midX = (a.x + b.x) / 2; const midY = (a.y + b.y) / 2 + 1; const midZ = (a.z + b.z) / 2
  heerich.applyGeometry({ type: 'line', from: [a.x, a.y + 1, a.z], to: [midX, midY, midZ], radius: 0.5, shape: 'rounded', style: { default: { fill: c.color, stroke: '#fff', strokeWidth: 0.08 } } })
  heerich.applyGeometry({ type: 'line', from: [midX, midY, midZ], to: [b.x, b.y + 1, b.z], radius: 0.5, shape: 'rounded', style: { default: { fill: c.color, stroke: '#fff', strokeWidth: 0.08 } } })
}

// 3. Time Circuit ring
const TC_PATH = [1, 8, 2, 7, 5, 4, 1]
for (let i = 0; i < TC_PATH.length - 1; i++) {
  const a = POS[TC_PATH[i]]; const b = POS[TC_PATH[i+1]]
  heerich.applyGeometry({ type: 'line', from: [a.x, a.y + 0.5, a.z], to: [b.x, b.y + 0.5, b.z], radius: 0.25, shape: 'rounded', style: { default: { fill: '#44aaff', stroke: 'none' } } })
}

// 4. Gates
for (const g of GATES) {
  const a = POS[g.from]; const b = POS[g.to]
  const midX = (a.x + b.x) / 2; const midY = (a.y + b.y) / 2 + 1; const midZ = (a.z + b.z) / 2
  heerich.removeGeometry({ type: 'sphere', center: [midX, midY, midZ], radius: 1.2 })
  heerich.applyGeometry({ type: 'line', from: [midX - 0.5, midY, midZ], to: [midX + 0.5, midY, midZ], radius: 0.3, shape: 'rounded', style: { default: { fill: '#ff44ff', stroke: '#fff', strokeWidth: 0.1 } } })
}

// 5. Ground plane
heerich.applyGeometry({ type: 'box', center: [0, -0.3, 5], size: [40, 0.3, 28],
  style: { top: { fill: '#0a0a15' }, default: { fill: '#0a0a15', stroke: '#1a1a33', strokeWidth: 0.1 } } })

// ── 6. Compute label positions from face data ───────────────────

const faces = heerich.getFaces()

// Build zone centroid accumulator
const zoneCentroids = {}
for (let z = 0; z <= 9; z++) zoneCentroids[z] = { sx: 0, sy: 0, count: 0 }

// Threshold: how close a voxel's 3D center must be to zone center
const THRESH = 3.0

for (const face of faces) {
  const v = face.voxel
  // v has x, y, z properties (the voxel grid position, which is bottom-left corner)
  // For a chamber centered at (cx, cy, cz) with size (sx, sy, sz),
  // the voxels span from (cx - sx/2, cy - sy/2, cz - sz/2) to (cx + sx/2, cy + sy/2, cz + sz/2)
  // We need to match face voxels to zone chambers

  // Check each zone
  for (let z = 0; z <= 9; z++) {
    const zonePos = POS[z]
    const size = z === 5 ? [7, 3, 7] : [5, 2.5, 5]
    const halfX = size[0] / 2
    const halfY = size[1] / 2
    const halfZ = size[2] / 2

    // Voxel position = face.voxel.x, y, z
    // Zone box spans zonePos.x ± halfX, (zonePos.y) to (zonePos.y + size[1]), zonePos.z ± halfZ
    if (Math.abs(v.x - zonePos.x) < halfX + 1 &&
        v.y >= zonePos.y - 0.5 && v.y <= zonePos.y + size[1] + 0.5 &&
        Math.abs(v.z - zonePos.z) < halfZ + 1) {

      // Found a matching face — use its 2D projected center
      // Average all polygon vertices
      const pts = face.points
      let cx = 0, cy = 0
      const n = pts.length
      for (let i = 0; i < n; i++) {
        cx += pts.x(i)
        cy += pts.y(i)
      }
      zoneCentroids[z].sx += cx / n
      zoneCentroids[z].sy += cy / n
      zoneCentroids[z].count++
      break  // only match one zone per face
    }
  }
}

// Compute average centroids
const labelPos = {}
for (let z = 0; z <= 9; z++) {
  const c = zoneCentroids[z]
  if (c.count > 0) {
    labelPos[z] = { x: c.sx / c.count, y: c.sy / c.count }
  } else {
    // Fallback: estimate from voxel bounding box center
    const p = POS[z]
    const size = z === 5 ? [7, 3, 7] : [5, 2.5, 5]
    // Approximate: take the mid-face of a voxel at the chamber center
    labelPos[z] = { x: p.x * 6, y: -(p.y + size[1]/2) * 6 }  // rough estimate
    console.warn(`  Warning: Zone ${z} has no matching faces, using estimate`)
  }
}

// ── 7. Generate SVG labels ──────────────────────────────────────

function makeLabel(z) {
  const l = labelPos[z]
  const x = l.x.toFixed(1)
  const y = l.y.toFixed(1)
  const color = ZONE_CLR[z]
  const planet = ZONE_PLANET[z]
  const demon = ZONE_DEMON[z] || '—'
  const particle = ZONE_PARTICLE[z]
  const name = ZONE_NAME[z]
  const region = ZONE_REGION[z].toUpperCase()

  return `<g transform="translate(${x}, ${y})">
    <rect x="-40" y="-18" width="80" height="36" rx="3" fill="rgba(0,0,0,0.7)" stroke="${color}" stroke-width="0.8"/>
    <text x="0" y="-4" text-anchor="middle" fill="white" font-family="monospace" font-size="7" font-weight="bold">Z${z} ${name}</text>
    <text x="0" y="4" text-anchor="middle" fill="${color}" font-family="monospace" font-size="5">${planet}</text>
    <text x="0" y="11" text-anchor="middle" fill="#888" font-family="monospace" font-size="4">${demon} ~${particle}~</text>
  </g>`
}

let labels = ''
for (let z = 0; z <= 9; z++) {
  labels += makeLabel(z) + '\n'
}

// ── Render and inject labels ────────────────────────────────────

let svg = heerich.toSVG({ padding: 50 })

// Insert labels before closing </svg>
svg = svg.replace('</svg>', `${labels}</svg>`)

const outPath = resolve(OUT_DIR, 'numogram-qliphoth-v5.svg')
writeFileSync(outPath, svg, 'utf-8')

const sizeKb = (svg.length / 1024).toFixed(1)
console.log(`✓ Wrote ${outPath}`)
console.log(`  Size: ${sizeKb} KB, Faces: ${faces.length}`)
console.log(`  Labels computed for ${Object.keys(labelPos).length} zones`)
