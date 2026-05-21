/**
 * zone-chambers-v5-fixed.js — Labels positioned via SVG voxel data parsing
 *
 * Instead of trying to match faces to zones (fragile projection math),
 * we compute each zone center's 3D grid coords, then find the closest
 * visible voxel in the SVG output by parsing data-voxel attributes.
 */

import { Heerich } from 'heerich'
import { writeFileSync, readFileSync, mkdirSync } from 'fs'
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
  { from: 8, to: 7, name: 'Surge', color: '#cc66ff' },
  { from: 2, to: 5, name: 'Hold',  color: '#66ccff' },
  { from: 4, to: 1, name: 'Sink',  color: '#ff6644' },
  { from: 6, to: 3, name: 'Warp',  color: '#ffcc33' },
  { from: 9, to: 9, name: 'Plex',  color: '#8844ff' },
]

const GATES = [
  { name: 'Gt-06', from: 3, to: 6 },
  { name: 'Gt-21', from: 6, to: 3 },
  { name: 'Gt-15', from: 5, to: 6 },
  { name: 'Gt-36', from: 8, to: 9 },
]

const REGION_Y = { warp: 24, torque: 12, plex: 0 }

function to3D(z) {
  const p = QPOS[z]
  return {
    x: (p.x - 400) / 15,
    y: REGION_Y[ZONE_REGION[z]],
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
  const size = z === 5 ? [7, 3, 7] : [5, 2.5, 5]
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

// 2. Current paths + Time Circuit + Gates + Ground
for (const c of CURRENTS) {
  if (c.from === c.to) continue
  const a = POS[c.from]; const b = POS[c.to]
  const mx = (a.x+b.x)/2; const my = (a.y+b.y)/2+1; const mz = (a.z+b.z)/2
  heerich.applyGeometry({ type:'line', from:[a.x,a.y+1,a.z], to:[mx,my,mz], radius:0.5, shape:'rounded', style:{default:{fill:c.color,stroke:'#fff',strokeWidth:0.08}} })
  heerich.applyGeometry({ type:'line', from:[mx,my,mz], to:[b.x,b.y+1,b.z], radius:0.5, shape:'rounded', style:{default:{fill:c.color,stroke:'#fff',strokeWidth:0.08}} })
}

const TC_PATH = [1,8,2,7,5,4,1]
for (let i=0;i<TC_PATH.length-1;i++) {
  const a=POS[TC_PATH[i]]; const b=POS[TC_PATH[i+1]]
  heerich.applyGeometry({ type:'line', from:[a.x,a.y+0.5,a.z], to:[b.x,b.y+0.5,b.z], radius:0.25, shape:'rounded', style:{default:{fill:'#44aaff',stroke:'none'}} })
}

for (const g of GATES) {
  const a=POS[g.from]; const b=POS[g.to]
  const mx=(a.x+b.x)/2; const my=(a.y+b.y)/2+1; const mz=(a.z+b.z)/2
  heerich.removeGeometry({ type:'sphere', center:[mx,my,mz], radius:1.2 })
  heerich.applyGeometry({ type:'line', from:[mx-0.5,my,mz], to:[mx+0.5,my,mz], radius:0.3, shape:'rounded', style:{default:{fill:'#ff44ff',stroke:'#fff',strokeWidth:0.1}} })
}

heerich.applyGeometry({ type:'box', center:[0,-0.3,5], size:[40,0.3,28],
  style:{top:{fill:'#0a0a15'},default:{fill:'#0a0a15',stroke:'#1a1a33',strokeWidth:0.1}} })

// ── Render to SVG, then label via data-voxel parsing ────────────

const rawSvg = heerich.toSVG({ padding: 50 })

// Find the screen position of the center voxel for each zone
// We know each zone chamber's center in 3D. Round to nearest voxel grid.
function findVoxelScreenPos(svgText, z) {
  const p = POS[z]
  const size = z === 5 ? [7, 3, 7] : [5, 2.5, 5]

  // The chamber center voxel coordinates (rounded to nearest integer)
  const cx = Math.round(p.x)
  const cy = Math.round(p.y + size[1]/2)  // top-center of chamber
  const cz = Math.round(p.z)

  // Search SVG for polygons with data-voxel matching our target
  // Pattern: data-voxel="CX,CY,CZ"
  const pattern = `data-voxel="${cx},${cy},${cz}"`
  const lines = svgText.split('\n')
  const matchingLines = lines.filter(l => l.includes(pattern))

  if (matchingLines.length === 0) {
    // Try slightly offset positions
    for (let dy = -1; dy <= 1; dy++) {
      for (let dx = -1; dx <= 1; dx++) {
        for (let dz = -1; dz <= 1; dz++) {
          const altPat = `data-voxel="${cx+dx},${cy+dy},${cz+dz}"`
          const altLines = lines.filter(l => l.includes(altPat))
          if (altLines.length > 0) {
            // Use the first matching polygon to extract screen position
            return extractCenter(altLines[0])
          }
        }
      }
    }
    console.warn(`  Zone ${z}: no voxel found near (${cx},${cy},${cz})`)
    return null
  }

  return extractCenter(matchingLines[0])
}

function extractCenter(line) {
  // Extract polygon points: points="x0,y0 x1,y1 x2,y2 x3,y3"
  const match = line.match(/points="([^"]+)"/)
  if (!match) return null

  const coords = match[1].split(' ')
  let sx = 0, sy = 0
  for (const c of coords) {
    const [x, y] = c.split(',').map(Number)
    sx += x; sy += y
  }
  return {
    x: sx / coords.length,
    y: sy / coords.length,
  }
}

// Find label positions for all 10 zones
const labelPos = {}
for (let z = 0; z <= 9; z++) {
  const pos = findVoxelScreenPos(rawSvg, z)
  if (pos) {
    labelPos[z] = pos
  } else {
    // Last resort: use zone center projected through simple formula
    // Derived empirically: sx = (x - z*cosθ)*tile + offset, sy = (-y + z*sinθ)*tile + offset
    // For angle=315°, cos=0.707, sin=-0.707, tile=6
    const p = POS[z]
    const cosA = Math.cos(315 * Math.PI / 180)  // ≈ 0.707
    const sinA = Math.sin(315 * Math.PI / 180)  // ≈ -0.707
    // viewBox suggests offset around (400, -300)
    const sx = (p.x - p.z * cosA) * 6 + 400
    const sy = (-p.y + p.z * sinA) * 6 - 300
    labelPos[z] = { x: sx, y: sy }
    console.warn(`  Zone ${z}: using estimated position`)
  }
}

// ── Generate labels and inject into SVG ─────────────────────────

function makeLabel(z) {
  const l = labelPos[z]
  const x = l.x.toFixed(1)
  const y = l.y.toFixed(1)
  const color = ZONE_CLR[z]
  const planet = ZONE_PLANET[z]
  const demon = ZONE_DEMON[z] || '—'
  const particle = ZONE_PARTICLE[z]
  const name = ZONE_NAME[z]

  return `<g transform="translate(${x}, ${y})">
    <rect x="-36" y="-16" width="72" height="32" rx="2" fill="rgba(0,0,0,0.75)" stroke="${color}" stroke-width="0.6"/>
    <text x="0" y="-3" text-anchor="middle" fill="white" font-family="monospace" font-size="6.5" font-weight="bold">Z${z} ${name}</text>
    <text x="0" y="4" text-anchor="middle" fill="${color}" font-family="monospace" font-size="5">${planet}</text>
    <text x="0" y="10" text-anchor="middle" fill="#999" font-family="monospace" font-size="4">${demon} ~${particle}~</text>
  </g>`
}

let labels = ''
for (let z = 0; z <= 9; z++) labels += makeLabel(z) + '\n'

const svg = rawSvg.replace('</svg>', `${labels}</svg>`)

const outPath = resolve(OUT_DIR, 'numogram-qliphoth-v5.svg')
writeFileSync(outPath, svg, 'utf-8')

const faces = heerich.getFaces()
const sizeKb = (svg.length / 1024).toFixed(1)
console.log(`✓ Wrote ${outPath}`)
console.log(`  Size: ${sizeKb} KB, Faces: ${faces.length}`)
console.log(`  Labels: ${Object.keys(labelPos).length} zones positioned`)
