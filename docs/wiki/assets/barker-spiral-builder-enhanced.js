/* p5.js sketch for interactive Barker Spiral v2 */
let arms = [];
let hoveredArm = -1;
const numArms = 45;
const baseRadius = 40;
const growthFactor = 1.08;
const centerX = 450;
const centerY = 320;

function setup() {
  createCanvas(900, 600);
  background(15, 23, 42);
  textSize(10);
  textAlign(LEFT, CENTER);
  
  // Precompute arm data
  arms = [];
  for (let k = 0; k < numArms; k++) {
    const angle = -HALF_PI + k * TWO_PI / numArms;
    const rInner = baseRadius * Math.pow(growthFactor, k);
    const rOuter = rInner * growthFactor;
    const zone = k % 10;
    const phase = Math.floor(k / 10);
    
    // Determine if this arm should have a gap (zones 3,7,8 at phase 0)
    let hasGap = false;
    if (phase === 0 && [3, 7, 8].includes(zone)) {
      hasGap = true;
    }
    
    arms.push({
      k,
      angle,
      rInner,
      rOuter,
      zone,
      phase,
      hasGap,
      xInner: centerX + rInner * Math.cos(angle),
      yInner: centerY + rInner * Math.sin(angle),
      xOuter: centerX + rOuter * Math.cos(angle),
      yOuter: centerY + rOuter * Math.sin(angle)
    });
  }
}

function draw() {
  background(15, 23, 42);
  
  // Draw concentric reference circles
  stroke(51, 65, 85);
  strokeWeight(0.5);
  noFill();
  for (let r of [60, 110, 170, 240, 320]) {
    circle(centerX, centerY, r * 2);
  }
  
  // Draw arms
  for (let arm of arms) {
    drawArm(arm);
  }
  
  // Draw zone labels (placed strategically)
  drawLabels();
  
  // Draw center info
  drawCenter();
}

function drawArm(arm) {
  push();
  translate(centerX, centerY);
  
  const isHovered = (hoveredArm === arm.k);
  const baseColor = color(96, 165, 250); // light blue
  const hoverColor = color(255, 255, 255);
  const currentColor = isHovered ? hoverColor : baseColor;
  
  stroke(currentColor);
  strokeWeight(isHovered ? 2 : 1);
  opacity = isHovered ? 0.8 : 0.3;
  stroke(96, 165, 250, opacity * 255);
  
  // Draw arc segment using quadratic Bezier for smoothness
  if (!arm.hasGap) {
    beginShape();
    // Inner arc start
    vertex(arm.rInner * Math.cos(arm.angle), arm.rInner * Math.sin(arm.angle));
    // Inner arc end (arm.angle + 8°)
    vertex(arm.rInner * Math.cos(arm.angle + TWO_PI/45), arm.rInner * Math.sin(arm.angle + TWO_PI/45));
    // Outer arc end
    vertex(arm.rOuter * Math.cos(arm.angle + TWO_PI/45), arm.rOuter * Math.sin(arm.angle + TWO_PI/45));
    // Outer arc start
    vertex(arm.rOuter * Math.cos(arm.angle), arm.rOuter * Math.sin(arm.angle));
    endShape(CLOSE);
  }
  
  // Draw zone label on the arm
  if (!arm.hasGap) {
    const labelR = arm.rInner - 15;
    const labelX = centerX + labelR * Math.cos(arm.angle + TWO_PI/90);
    const labelY = centerY + labelR * Math.sin(arm.angle + TWO_PI/90);
    noStroke();
    fill(255, 255, 255, 150);
    textSize(9);
    textAlign(CENTER, CENTER);
    text("Z" + arm.zone, labelX, labelY);
  }
  
  pop();
}

function drawLabels() {
  const majorZones = [0, 1, 2, 4, 5, 6, 9];
  for (let zone of majorZones) {
    let arm = arms.find(a => a.zone === zone && a.phase === 0 && !a.hasGap);
    if (!arm) {
      arm = arms.find(a => a.zone === zone && !a.hasGap);
    }
    if (arm) {
      const labelR = 330;
      const angle = arm.angle;
      const x = centerX + labelR * Math.cos(angle);
      const y = centerY + labelR * Math.sin(angle);
      stroke(255);
      strokeWeight(0.5);
      line(x, y, centerX + (labelR + 20) * Math.cos(angle), centerY + (labelR + 20) * Math.sin(angle));
      noStroke();
      fill(255, 215, 0);
      textSize(12);
      textAlign(CENTER, CENTER);
      text("ZONE " + zone, x, y);
    }
  }
}

function drawCenter() {
  fill(255, 191, 36);
  noStroke();
  circle(centerX, centerY, 16);
  
  fill(255);
  textSize(10);
  textAlign(LEFT);
  text("Barker Spiral v2 - 45 Arms", centerX + 30, centerY - 10);
  text("Mouse over arms to inspect", centerX + 30, centerY + 10);
}

function mouseMoved() {
  hoveredArm = -1;
  for (let arm of arms) {
    if (arm.hasGap) continue;
    
    const dx = mouseX - centerX;
    const dy = mouseY - centerY;
    const r = Math.sqrt(dx*dx + dy*dy);
    const angle = Math.atan2(dy, dx);
    let normalizedAngle = angle;
    if (normalizedAngle < -HALF_PI) normalizedAngle += TWO_PI;
    if (normalizedAngle > HALF_PI) normalizedAngle -= TWO_PI;
    
    const angleDiff = Math.abs(normalizedAngle - arm.angle);
    if (angleDiff < TWO_PI/90 && r >= arm.rInner && r <= arm.rOuter) {
      hoveredArm = arm.k;
      break;
    }
  }
  
  if (hoveredArm !== -1) {
    cursor(HAND);
  } else {
    cursor(ARROW);
  }
}