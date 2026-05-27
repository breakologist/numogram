// Tsubuyaki -- Run #313 | grid | 0
// Zones: [0] | Hyp: 40.0% | Kills: 0 | Turns: 430
let t=0;
function setup(){createCanvas(200,200);background(15,0,25);}
function draw(){
  t+=0.02;
  stroke(255,255,255,102);
  strokeWeight(1);
  for(let i=0;i<10;i++){
    let x=noise(i,t)*200;
    let y=noise(i+100,t)*200;
    point(x,y);
  }
}