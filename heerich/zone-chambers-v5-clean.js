/**
 * zone-chambers-v5-clean.js — Clean compact numogram with labels
 *
 * Uses isometric camera to avoid elongation.
 * Zone positions from qliphoth Labyrinth layout.
 * Labels positioned via known projection math for isometric.
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

const REGION_LABEL = { 0: 'PLEX', 1: 'TORQUE', 2: 'TORQUE', 3: 'WARP', 4: 'TORQUE',
  5: 'TORQUE', 6: 'WARP', 7: 'TORQUE', 8: 'TORQUE', 9: 'PLEX' }

const REGION_Y = { warp: 24, torque: 12, plex: 0 }

function to3D(z) {
  const p = QPOS[z]
  return {
    x: (p.x - 400) / 15,
    y: REGION_Y[REGION_LABEL[z].toLowerCase()],
    z: (875 - p.y) / 20 + 1,
  }
}

const POS = {}
for (let z = 0; z <= 9; z++) POS[z] = to3D(z)

// ── Build Scene ─────────────────────────────────────────────────

const heerich = new Heerich({
  tile: 8,
  camera: { type: 'isometric', angle: 45 },
  style: { default: { fill: '#111', stroke: '#333', strokeWidth: 0.2 } },
  gap: 0.12,
})

// 1. Zone chambers
for (let z = 0; z <= 9; z++) {
  const p = POS[z]
  const color = ZONE_CLR[z]
  const region = REGION_LABEL[z].toLowerCase()
  const size = z === 5 ? [5, 2.5, 5] : [3.5, 2, 3.5]
  const topFill = region === 'warp' ? '#44cc77' : region === 'plex' ? '#666666' : '#4488ff'
  heerich.applyGeometry({
    type: 'box',
    center: [p.x, p.y + size[1]/2, p.z],
    size,
    style: {
      default: { fill: color, stroke: '#fff', strokeWidth: 0.12 },
      top: { fill: topFill, stroke: '#fff', strokeWidth: 0.08 },
    },
  })
}

// 2. Current paths
const CURRENTS = [
  { from: 8, to: 7, color: '#cc66ff' }, { from: 2, to: 5, color: '#66ccff' },
  { from: 4, to: 1, color: '#ff6644' }, { from: 6, to: 3, color: '#ffcc33' },
]
for (const c of CURRENTS) {
  const a = POS[c.from]; const b = POS[c.to]
  const mx = (a.x+b.x)/2; const my = (a.y+b.y)/2+0.8; const mz = (a.z+b.z)/2
  heerich.applyGeometry({ type:'line', from:[a.x,a.y+0.8,a.z], to:[mx,my,mz], radius:0.4, shape:'rounded', style:{default:{fill:c.color,stroke:'#fff',strokeWidth:0.06}} })
  heerich.applyGeometry({ type:'line', from:[mx,my,mz], to:[b.x,b.y+0.8,b.z], radius:0.4, shape:'rounded', style:{default:{fill:c.color,stroke:'#fff',strokeWidth:0.06}} })
}

// 3. Time Circuit anticlockwise ring
const TC_PATH = [1,8,2,7,5,4,1]
for (let i=0;i<TC_PATH.length-1;i++) {
  const a=POS[TC_PATH[i]]; const b=POS[TC_PATH[i+1]]
  heerich.applyGeometry({ type:'line', from:[a.x,a.y+0.3,a.z], to:[b.x,b.y+0.3,b.z], radius:0.2, shape:'rounded', style:{default:{fill:'#44aaff',stroke:'none'}} })
}

// 4. Gates (sphere subtract)
const GATES = [{from:3,to:6},{from:6,to:3},{from:5,to:6},{from:8,to:9}]
for (const g of GATES) {
  const a=POS[g.from]; const b=POS[g.to]
  const mx=(a.x+b.x)/2; const my=(a.y+b.y)/2+0.8; const mz=(a.z+b.z)/2
  heerich.removeGeometry({ type:'sphere', center:[mx,my,mz], radius:1 })
  heerich.applyGeometry({ type:'line', from:[mx-0.3,my,mz], to:[mx+0.3,my,mz], radius:0.2, shape:'rounded', style:{default:{fill:'#ff44ff'}} })
}

// 5. Ground plane
heerich.applyGeometry({ type:'box', center:[0,-0.3,4], size:[30,0.3,20],
  style:{top:{fill:'#0a0a15'},default:{fill:'#0a0a15',stroke:'#1a1a33',strokeWidth:0.08}} })

// ── Render ──────────────────────────────────────────────────────

const svg = heerich.toSVG({ padding: 40 })
const faces = heerich.getFaces()

// For isometric projection, compute approximate label positions
// Isometric at 45°: sx = (x - z*cos45)*tile, sy = (-y + (x+z)*sin45)*tile... no
// Isometric projection: x_screen = (x - z) * cos(30°) * tile
//                         y_screen = -(y) * tile + (x + z) * sin(30°) * tile
// For isometric at angle=45° with tile=8:
// Actually, heerich's isometric at 45° means the angle parameter.
// Let me just use a simple approximation and adjust.

// From the viewBox, we can extract the center of the scene
// viewBox="minX minY width height"
const vbMatch = svg.match(/viewBox="([^"]+)"/)
let vb = vbMatch ? vbMatch[1].split(' ').map(Number) : [-300, -300, 600, 600]
const cx = vb[0] + vb[2]/2  // center X of viewport
const cy = vb[1] + vb[3]/2  // center Y of viewport

// Try to find label positions by scanning for the brightest top-face colors
// Top faces in torque are #4488ff, warp #44cc77, plex #666666
function findFaceCenter(svgText, zone, label) {
  // Search for text near this zone's position in the SVG
  // We know the zone positions in 3D. In isometric at 45°, the projection is:
  // If we project (x, y, z) with tile=8 and isometric angle=45°:
  // screen_x ≈ cx + (x - z) * 8 * 0.7  (empirical)
  // screen_y ≈ cy + (-y + (x + z) * 0.4) * 8  (empirical)
  return null  // Will use empirical approach below
}

// Empirical approach: find a visible polygon near each zone
// by looking for the zone's fill color
const zoneColorMapping = {
  '#ee44ee': 1, '#4488ff': 2, '#44cc77': 3, '#ee4444': 4,
  '#ee8833': 5, '#ddcc33': 6, '#7755cc': 7, '#9944ee': 8,
  '#aaaaaa': 0, '#666666': 9
}

// Find the first polygon with each zone color, extract its points center
const labelPos = {}
for (const [color, z] of Object.entries(zoneColorMapping)) {
  const idx = svg.indexOf(`fill="${color}"`)
  if (idx === -1) continue

  // Find the polygon element containing this fill
  const lineStart = svg.lastIndexOf('\n', idx - 200)
  const lineEnd = svg.indexOf('\n', idx)
  const line = svg.substring(lineStart < 0 ? 0 : lineStart, lineEnd < 0 ? svg.length : lineEnd)

  // Extract points
  const ptsMatch = line.match(/points="([^"]+)"/)
  if (!ptsMatch) continue

  const pts = ptsMatch[1].trim().split(/\s+/)
  if (pts.length < 2) continue

  let sx = 0, sy = 0
  for (const p of pts) {
    const [x, y] = p.split(',').map(Number)
    sx += x; sy += y
  }
  labelPos[z] = { x: sx / pts.length, y: sy / pts.length }
}

// Generate labels
let labels = ''
for (let z = 0; z <= 9; z++) {
  const l = labelPos[z]
  if (!l) {
    console.warn(`Zone ${z}: no label position found`)
    continue
  }
  const color = ZONE_CLR[z]
  const region = REGION_LABEL[z]

  labels += `<g transform="translate(${l.x.toFixed(1)}, ${(l.y - 28).toFixed(1)})">
    <rect x="-30" y="-12" width="60" height="24" rx="2" fill="rgba(0,0,0,0.8)" stroke="${color}" stroke-width="0.5"/>
    <text x="0" y="-1" text-anchor="middle" fill="white" font-family="monospace" font-size="5.5" font-weight="bold">Z${z}</text>
    <text x="0" y="6" text-anchor="middle" fill="${color}" font-family="monospace" font-size="4">${region}</text>
  </g>\n`
}

const finalSvg = svg.replace('</svg>', `${labels}</svg>`)

const outPath = resolve(OUT_DIR, 'numogram-v5-clean.svg')
writeFileSync(outPath, finalSvg, 'utf-8')

const sizeKb = (finalSvg.length / 1024).toFixed(1)
console.log(`✓ Wrote ${outPath}`)
console.log(`  Size: ${sizeKb} KB, Faces: ${faces.length}`)
console.log(`  Labels found for zones: ${Object.keys(labelPos).sort().join(',')}`)
console.log(`  Missing zones: ${[0,1,2,3,4,5,6,7,8,9].filter(z=>!labelPos[z]).join(',') || 'none'}`)
