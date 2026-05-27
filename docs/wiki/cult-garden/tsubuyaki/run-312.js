// Tsubuyaki -- Run #292 | dodecagon | 9
// Zones: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9] | Hyp: 34.0% | Kills: 7 | Turns: 1060
let t=0;
function setup(){createCanvas(200,200);background(10,0,20);}
function draw(){
  t+=0.01;
  background(10,0,20,6);
  noFill();
  stroke(153,0,255,86);
  strokeWeight(1);
  let n=max(3,10);
  beginShape();
  for(let i=0;i<=n;i++){
    let a=t*5.3+i*TWO_PI/n;
    let r=60+7*sin(t*2+i);
    vertex(100+cos(a)*r,100+sin(a)*r);
  }
  endShape();
  fill(153,0,255,28);
  noStroke();
  ellipse(100,100,8,8);
}