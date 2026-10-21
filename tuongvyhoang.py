import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Giải Cứu Chim Cánh Cụt",
    page_icon="🐧",
    layout="wide"
)

GAME = r"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
*{box-sizing:border-box}
body{margin:0;overflow:hidden;font-family:Arial,sans-serif;background:#79d9ef}
#game{position:relative;width:100%;height:680px;overflow:hidden}
#view{position:absolute;inset:0}
#hud{position:absolute;top:10px;left:10px;right:10px;z-index:5;
color:#12334a;text-align:center;pointer-events:none}
#title{font-size:25px;font-weight:900;text-shadow:0 2px white}
#message{display:inline-block;margin-top:5px;background:#ffffffed;
padding:8px 14px;border-radius:14px;font-weight:bold;max-width:95%}
#question{margin:8px auto 5px;max-width:760px;background:#fffdf0ee;
padding:9px 12px;border-radius:13px;font-weight:bold;font-size:18px}
#answers{display:flex;gap:8px;max-width:900px;margin:auto;justify-content:center}
.answer{flex:1;max-width:210px;min-height:44px;background:#fff;
border:3px solid #63bce4;border-radius:12px;padding:7px 4px;
font-size:14px;font-weight:bold;display:flex;align-items:center;
justify-content:center;box-shadow:0 3px 0 #247eac}
.answer.selected{border-color:#ffb52e;background:#fff2bd}
#controls{position:absolute;bottom:12px;left:0;right:0;z-index:8;
display:flex;justify-content:space-between;align-items:end;padding:0 18px}
.pad{display:grid;grid-template-columns:52px 52px 52px;grid-template-rows:52px 52px;
gap:5px}
.ctrl{border:0;border-radius:50%;background:#ffffffdf;color:#17445d;
font-size:25px;font-weight:bold;box-shadow:0 3px 0 #83b8c9;touch-action:none}
#left{grid-column:1;grid-row:2}
#right{grid-column:3;grid-row:2}
#up{grid-column:2;grid-row:1}
#jump{border:0;border-radius:18px;padding:17px 22px;background:#ffca53;
font-size:17px;font-weight:900;color:#573b0b;box-shadow:0 4px 0 #d18c23;
touch-action:none}
#start{position:absolute;inset:0;z-index:20;display:flex;align-items:center;
justify-content:center;background:linear-gradient(#7ce4f0d9,#d4f9e7e8)}
.panel{background:white;border:4px solid #7ccedb;border-radius:25px;
padding:24px;max-width:480px;width:90%;text-align:center;
box-shadow:0 8px 0 #65b5c4}
.panel h1{color:#167da0;margin:5px}
.panel p{line-height:1.5}
.bigbtn{background:#ffca53;border:0;border-radius:14px;padding:13px 24px;
font-size:18px;font-weight:bold;cursor:pointer}
#finish{display:none;position:absolute;inset:0;z-index:30;
align-items:center;justify-content:center;background:#12394cbf}
#finish .panel{max-width:500px}
@media(max-width:600px){
#game{height:680px}
#title{font-size:21px}
#question{font-size:15px}
.answer{font-size:11px;min-height:48px;padding:4px 2px}
#controls{padding:0 8px}
.pad{grid-template-columns:44px 44px 44px;grid-template-rows:44px 44px}
#jump{padding:14px 15px;font-size:15px}
}
</style>
</head>
<body>
<div id="game">
  <div id="view"></div>
  <div id="hud">
    <div id="title">🐧 GIẢI CỨU CHIM CÁNH CỤT 🐟</div>
    <div id="message">Nhấn BẮT ĐẦU để chơi nhé!</div>
    <div id="question" style="display:none"></div>
    <div id="answers" style="display:none"></div>
  </div>
  <div id="controls" style="display:none">
    <div class="pad">
      <button class="ctrl" id="up">↑</button>
      <button class="ctrl" id="left">←</button>
      <button class="ctrl" id="right">→</button>
    </div>
    <button id="jump">🐧 NHẢY!</button>
  </div>
  <div id="start">
    <div class="panel">
      <div style="font-size:65px">🐧❄️🐟</div>
      <h1>Giải Cứu Chim Cánh Cụt</h1>
      <p>Giúp chim mẹ vượt sông băng, trả lời 5 câu hỏi để lấy cá rồi mang cá về cho chim con nhé!</p>
      <p><b>← →</b> đổi hướng · <b>↑</b> nhảy về phía trước<br>
      Điện thoại: dùng các nút điều khiển trên màn hình.</p>
      <button class="bigbtn" id="startBtn">BẮT ĐẦU CHƠI!</button>
    </div>
  </div>
  <div id="finish">
    <div class="panel">
      <div style="font-size:60px" id="finishIcon">🎉🐧</div>
      <h1 id="finishTitle">Hoàn thành!</h1>
      <p id="finishText"></p>
      <button class="bigbtn" id="again">CHƠI LẠI</button>
    </div>
  </div>
</div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script>
if (!window.THREE) {
  document.getElementById("message").textContent =
    "Không tải được đồ họa 3D. Em hãy kiểm tra kết nối Internet rồi tải lại trang.";
} else {
const scene = new THREE.Scene();
// HIỆU ỨNG TUYẾT RƠI
const snowGeometry = new THREE.BufferGeometry();
const snowCount = 700;
const snowPositions = new Float32Array(snowCount * 3);
const snowSpeeds = [];

for (let i = 0; i < snowCount; i++) {
  snowPositions[i * 3] = (Math.random() - 0.5) * 35;
  snowPositions[i * 3 + 1] = Math.random() * 20;
  snowPositions[i * 3 + 2] = (Math.random() - 0.5) * 65;
  snowSpeeds.push(2 + Math.random() * 4);
}

snowGeometry.setAttribute(
  "position",
  new THREE.BufferAttribute(snowPositions, 3)
);

const snowParticles = new THREE.Points(
  snowGeometry,
  new THREE.PointsMaterial({
    color: 0xffffff,
    size: 0.12,
    transparent: true,
    opacity: 0.9,
    sizeAttenuation: true
  })
);

scene.add(snowParticles);
scene.background = new THREE.Color(0x8ce3f4);
scene.fog = new THREE.Fog(0x8ce3f4, 35, 100);

const camera = new THREE.PerspectiveCamera(62, 1, 0.1, 200);
const renderer = new THREE.WebGLRenderer({antialias:true});
renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
document.getElementById("view").appendChild(renderer.domElement);

scene.add(new THREE.HemisphereLight(0xe9fbff, 0x4e8794, 2));
const sun = new THREE.DirectionalLight(0xffffff, 2.1);
sun.position.set(-8,18,10);
sun.castShadow = true;
scene.add(sun);

const mat = (color, extra={}) => new THREE.MeshStandardMaterial({
  color, roughness:0.78, ...extra
});
const snow = mat(0xf3fcff);
const ice = mat(0x8fe4f6,{transparent:true,opacity:0.94});
const darkIce = mat(0x39b6db);
const waterMat = mat(0x078bc5,{roughness:0.25,metalness:0.1});
const wallMat = mat(0xb7f3ff,{transparent:true,opacity:0.48});
const white = mat(0xffffff);
const black = mat(0x172d3b);
const orange = mat(0xffa52b);
const pink = mat(0xffb5c8);

let objects = [];
let floes = [];
let walls = [];
let cracks = [];
let mother, baby, bucket;
let stage = 0, row = 0, lane = 1;
let busy = false, jumping = false, gameStarted = false;
let weakHits = 0, weakRows = new Set();
let weakLanes = [];
let jumpData = null;
let message = document.getElementById("message");
let questionBox = document.getElementById("question");
let answersBox = document.getElementById("answers");
let controls = document.getElementById("controls");

const xs = [-3.6,-1.2,1.2,3.6];
const questions = [
 {q:"Câu 1: 3 × 4 bằng bao nhiêu?",a:["7","12","14","16"],c:1},
 {q:"Câu 2: Nước đóng băng ở nhiệt độ nào?",a:["0°C","10°C","50°C","100°C"],c:0},
 {q:"Câu 3: Phân số 1/2 bằng số thập phân nào?",a:["0,2","0,25","0,5","2,0"],c:2},
 {q:"Câu 4: Đơn vị đo khối lượng là gì?",a:["Mét","Lít","Giây","Kilôgam"],c:3},
 {q:"Câu 5: Hình có 3 cạnh là hình gì?",a:["Hình vuông","Hình tam giác","Hình tròn","Hình chữ nhật"],c:1}
];

function addMesh(geo, material, x,y,z, parent=scene) {
 const m = new THREE.Mesh(geo, material);
 m.position.set(x,y,z);
 m.castShadow = true;
 m.receiveShadow = true;
 parent.add(m);
 objects.push(m);
 return m;
}
function box(parent,x,y,z,w,h,d,material) {
 const m = new THREE.Mesh(new THREE.BoxGeometry(w,h,d),material);
 m.position.set(x,y,z); m.castShadow=true; m.receiveShadow=true;
 parent.add(m); return m;
}
function sphere(parent,x,y,z,r,material, sx=1,sy=1,sz=1) {
 const m=new THREE.Mesh(new THREE.SphereGeometry(r,20,16),material);
 m.position.set(x,y,z); m.scale.set(sx,sy,sz);
 m.castShadow=true; parent.add(m); return m;
}
function clearScene() {
 for (const o of [...objects]) {
   if(o.parent) o.parent.remove(o);
 }
 objects=[];
 floes=[]; walls=[]; cracks=[];
 if(mother) scene.remove(mother);
 if(baby) scene.remove(baby);
 mother=baby=bucket=null;
}

function makePenguin(isBaby=false) {
 const g=new THREE.Group();
 const bodyMat=mat(isBaby?0x253f55:0x172b3c);
 const bellyMat=mat(0xf7f8f1);
 const head=sphere(g,0,1.55,0,isBaby?0.57:0.69,bodyMat,1,1.03,0.9);
 sphere(g,0,0.88,0,isBaby?0.48:0.63,bodyMat,1,1.15,0.82);
 sphere(g,0,1.03,-0.38,isBaby?0.34:0.46,bellyMat,1,1,0.28);
 // Eyes and beak face toward local -Z, the ice ahead.
 sphere(g,-0.24,1.64,-0.54,0.105,white);
 sphere(g,0.24,1.64,-0.54,0.105,white);
 sphere(g,-0.24,1.64,-0.625,0.052,black);
 sphere(g,0.24,1.64,-0.625,0.052,black);
 const beak=new THREE.Mesh(new THREE.ConeGeometry(0.16,0.32,5),orange);
 beak.rotation.x=-Math.PI/2;
 beak.position.set(0,1.43,-0.68); g.add(beak);
 // Flippers
 const f1=box(g,-0.62,1.05,0.02,0.19,0.68,0.27,bodyMat);
 const f2=box(g,0.62,1.05,0.02,0.19,0.68,0.27,bodyMat);
 f1.rotation.z=-0.25; f2.rotation.z=0.25;
 // Feet
 const foot1=sphere(g,-0.28,0.16,-0.12,0.2,orange,1,0.45,1.35);
 const foot2=sphere(g,0.28,0.16,-0.12,0.2,orange,1,0.45,1.35);
 g.userData.flippers=[f1,f2]; g.userData.feet=[foot1,foot2];
 if(isBaby) {
   sphere(g,-0.35,2.12,-0.02,0.13,pink);
   sphere(g,0.35,2.12,-0.02,0.13,pink);
 }
 scene.add(g);
 return g;
}

function makeBucket(parent) {
 const b=new THREE.Group();
 const pail= new THREE.Mesh(new THREE.CylinderGeometry(0.25,0.19,0.38,16),mat(0xffc857));
 pail.position.y=0.65; b.add(pail);
 const rim=new THREE.Mesh(new THREE.TorusGeometry(0.24,0.035,8,18),mat(0x9b6425));
 rim.rotation.x=Math.PI/2; rim.position.y=0.85; b.add(rim);
 const fish=sphere(b,0,0.98,-0.04,0.15,orange,1.6,0.5,0.6);
 fish.rotation.y=0.4;
 b.position.set(0,0,0.65);
 parent.add(b); return b;
}

function createBanksAndWater() {
 box(scene,0,-0.65,-12,13,0.7,100,waterMat);
 box(scene,-8,0,-12,5,1.2,100,snow);
 box(scene,8,0,-12,5,1.2,100,snow);
 // Snowbanks and little snowy mounds
 for(let i=0;i<18;i++){
   const z=4-i*4.7;
   sphere(scene,-8.2+Math.sin(i)*0.6,0.15,z,1.2,snow,1.5,0.35,1.1);
   sphere(scene,8.2+Math.cos(i)*0.6,0.15,z,1.2,snow,1.5,0.35,1.1);
 }
}

function createFloe(x,z,weak=false) {
 const g=new THREE.Group();
 g.position.set(x,0,z);
 const top=box(g,0,0.02,0,1.85,0.30,2.0,ice);
 box(g,0,-0.19,0,1.65,0.18,1.75,darkIce);
 // Snowy top surface
 box(g,0,0.19,0,1.72,0.08,1.83,snow);
if (weak) {
  // Chỉ để một vết nứt tự nhiên, không tạo dấu X
  const crackMat = mat(0x177baf);
  const crack = box(
    g, 0, 0.245, 0,
    0.035, 0.015, 1.0,
    crackMat
  );

  crack.rotation.y = 0.25;
}
 scene.add(g);
 floes.push({group:g,weak,sunk:false});
 return g;
}

function createWall(z) {
 const g=new THREE.Group();
 box(g,0,1.8,z,10,3.6,0.32,wallMat);
 // icy shining top edge
 box(g,0,3.62,z,10,0.12,0.45,snow);
 scene.add(g);
 walls.push({group:g,down:false});
 return g;
}

function showAnswers() {
 const q=questions[row];
 questionBox.style.display="block";
 answersBox.style.display="flex";
 questionBox.textContent=q.q;
 answersBox.innerHTML="";
 q.a.forEach((a,i)=>{
   const el=document.createElement("div");
   el.className="answer"+(i===lane?" selected":"");
   el.textContent=String.fromCharCode(65+i)+". "+a;
   answersBox.appendChild(el);
 });
}
function updateSelected() {
 [...answersBox.children].forEach((el,i)=>{
   el.classList.toggle("selected",i===lane);
 });
}

function buildStage1() {
 clearScene();
 stage=1; row=0; lane=1; busy=false; jumping=false;
 weakHits=0; weakRows=new Set();
 createBanksAndWater();
 mother=makePenguin(false);
 mother.position.set(xs[lane],0,4);
 baby=makePenguin(true);
 baby.position.set(-6.4,0,3.8);
 baby.rotation.y=-Math.PI/2;
 // Shore
 box(scene,-3,0.1,5,8,0.35,5,snow);
 box(scene,0,0.1,-34,8,0.35,5,snow);
 for(let r=0;r<5;r++){
   const z=-2-r*7;
   for(let i=0;i<4;i++) createFloe(xs[i],z,false);
   createWall(z-3.3);
 }
 message.textContent="Chặng 1/2: Chọn đáp án bằng cách đổi hướng rồi nhấn ↑ hoặc NHẢY!";
 showAnswers();
 controls.style.display="flex";
}

function buildStage2() {
 clearScene();
 stage=2; row=0; lane=1; busy=false; jumping=false;
 weakHits=0; weakRows=new Set();
 createBanksAndWater();
 mother=makePenguin(false);
 // Mother faces back toward the shore (+Z); camera will be behind her.
 mother.rotation.y=Math.PI;
 mother.position.set(xs[lane],0,-35);
 bucket=makeBucket(mother);
 baby=makePenguin(true);
 baby.position.set(-6.4,0,3.8);
 baby.rotation.y=-Math.PI/2;
 box(scene,-3,0.1,5,8,0.35,5,snow);
 weakLanes=Array.from({length:5},()=>Math.floor(Math.random()*4));
 for(let r=0;r<5;r++){
   const z=-30+r*6;
   for(let i=0;i<4;i++) createFloe(xs[i],z,i===weakLanes[r]);
   createWall(z+3);
 }
 questionBox.style.display="none";
 answersBox.style.display="none";
 message.textContent="Chặng 2/2: Mang xô cá về bờ! Né băng nứt, đừng giẫm băng yếu ở 3 hàng.";
}

function setMessage(t){message.textContent=t;}

function animateJump(targetX,targetZ,callback) {
 if(busy || jumping) return;
 busy=true; jumping=true;
 const start=mother.position.clone();
 const end=new THREE.Vector3(targetX,0.35,targetZ);
 jumpData={start,end,t:0,duration:850,callback};
}

function finishJump() {
 if(!jumpData) return;
 const cb=jumpData.callback;
 jumpData=null; jumping=false;
 if(cb) cb();
}

function jumpStage1() {
 if(busy || row>=5) return;
 const targetZ=-2-row*7;
 const q=questions[row];
 const chosen=lane;
 setMessage("Nhảy lên đáp án "+String.fromCharCode(65+chosen)+" nhé!");
 animateJump(xs[chosen],targetZ,()=>{
   if(chosen===q.c) {
     setMessage("🎉 Chính xác! Vách băng đang chìm xuống...");
     const wall=walls[row];
     if(wall) wall.down=true;
     // Move safely beyond the lowered wall, ready for the next question.
     setTimeout(()=>{
       if(stage!==1) return;
       row++;
       if(row>=5) {
         setMessage("Em đã lấy được cá! Chuẩn bị mang cá về cho chim con.");
         setTimeout(()=>{if(stage===1)buildStage2();},1300);
         return;
       }
       mother.position.set(xs[lane],0,-2-(row-1)*7-4.2);
       busy=false;
       showAnswers();
       setMessage("Đúng rồi! Chọn đáp án tiếp theo rồi nhảy.");
     },900);
   } else {
     setMessage("Chưa đúng rồi! Đổi hướng trái/phải để chọn đáp án khác nha.");
     setTimeout(()=>{
       if(stage!==1) return;
       mother.position.set(xs[lane],0,targetZ+3.4);
       busy=false;
       showAnswers();
     },650);
   }
 });
}

function jumpStage2() {
 if(busy || row>=5) return;
 const targetZ=-30+row*6;
 const chosen=lane;
 setMessage("Đang nhảy qua sông băng...");
 animateJump(xs[chosen],targetZ,()=>{
   const tile=floes[row*4+chosen];
   if(tile && tile.weak) {
     weakHits++;
     weakRows.add(row);
     tile.sunk=true;
     setMessage("💥 Băng yếu nứt và chìm xuống! Số hàng băng yếu: "+weakRows.size+"/3");
     let elapsed=0;
     const sink=setInterval(()=>{
       elapsed+=40;
       tile.group.position.y-=0.055;
       tile.group.rotation.z+=0.006;
       if(elapsed>=650) clearInterval(sink);
     },40);
     if(weakRows.size>=3) {
       busy=true;
       setTimeout(()=>endGame(false,"Em đã giẫm trúng băng yếu ở 3 hàng khác nhau. Hãy thử lại từ đầu nhé!"),850);
       return;
     }
   } else {
     setMessage("An toàn! Tiếp tục mang cá về bờ.");
   }
   const wall=walls[row];
   if(wall) wall.down=true;
   setTimeout(()=>{
     if(stage!==2) return;
     row++;
     if(row>=5) {
       setTimeout(()=>endGame(true,"Em đã vượt sông băng và mang cá về cho chim con. Cả hai mẹ con được đoàn tụ!"),250);
       return;
     }
     mother.position.set(xs[lane],0,-30+(row-1)*6+3.5);
     busy=false;
   },500);
 });
}

function jumpForward() {
 if(!gameStarted || busy || jumping) return;
 if(stage===1) jumpStage1();
 else if(stage===2) jumpStage2();
}

function changeLane(delta) {
 if(!gameStarted || busy || jumping) return;
 lane=Math.max(0,Math.min(3,lane+delta));
 updateSelected();
 // Move along the shore / current safe approach area.
 mother.position.x=xs[lane];
}

function endGame(win,text) {
 document.getElementById("finish").style.display="flex";
 document.getElementById("finishIcon").textContent=win?"🎉🐧🐟":"🧊🐧";
 document.getElementById("finishTitle").textContent=win?"GIẢI CỨU THÀNH CÔNG!":"ÔI KHÔNG!";
 document.getElementById("finishText").textContent=text;
 controls.style.display="none";
}
function startGame() {
 document.getElementById("start").style.display="none";
 document.getElementById("finish").style.display="none";
 gameStarted=true;
 buildStage1();
}

document.getElementById("startBtn").onclick=startGame;
document.getElementById("again").onclick=()=>{
 document.getElementById("finish").style.display="none";
 startGame();
};
document.getElementById("left").onclick=()=>changeLane(-1);
document.getElementById("right").onclick=()=>changeLane(1);
document.getElementById("up").onclick=jumpForward;
document.getElementById("jump").onclick=jumpForward;

document.addEventListener("keydown",e=>{
 if(["ArrowLeft","ArrowRight","ArrowUp"," ","a","A","d","D","w","W"].includes(e.key)) e.preventDefault();
 if(e.key==="ArrowLeft"||e.key==="a"||e.key==="A") changeLane(-1);
 if(e.key==="ArrowRight"||e.key==="d"||e.key==="D") changeLane(1);
 if(e.key==="ArrowUp"||e.key==="w"||e.key==="W"||e.key===" ") jumpForward();
});

function resize() {
 const el=document.getElementById("view");
 const w=el.clientWidth,h=el.clientHeight;
 if(!w||!h) return;
 renderer.setSize(w,h);
 camera.aspect=w/h; camera.updateProjectionMatrix();
}
window.addEventListener("resize",resize);
resize();

const clock=new THREE.Clock();
function animate() {
 requestAnimationFrame(animate);
 const dt=clock.getDelta();
 const time=clock.elapsedTime;
 // Cho tuyết rơi liên tục
const positions = snowGeometry.attributes.position.array;

for (let i = 0; i < snowCount; i++) {
  positions[i * 3 + 1] -= snowSpeeds[i] * dt;

  if (positions[i * 3 + 1] < -2) {
    positions[i * 3 + 1] = 18;
    positions[i * 3] = (Math.random() - 0.5) * 35;
    positions[i * 3 + 2] = (Math.random() - 0.5) * 65;
  }
}

snowGeometry.attributes.position.needsUpdate = true;

 if(mother) {
   if(jumpData) {
     jumpData.t+=dt*1000;
     const p=Math.min(1,jumpData.t/jumpData.duration);
     mother.position.x=THREE.MathUtils.lerp(jumpData.start.x,jumpData.end.x,p);
     mother.position.z=THREE.MathUtils.lerp(jumpData.start.z,jumpData.end.z,p);
     mother.position.y=Math.sin(p*Math.PI)*2.5;
     if(p>=1) {
       mother.position.y=0;
       finishJump();
     }
   }
   // Flippers swing while the penguin moves/jumps.
   const swing=(jumping?0.9:0.16)*Math.sin(time*8);
   if(mother.userData.flippers) {
     mother.userData.flippers[0].rotation.z=-0.25-swing;
     mother.userData.flippers[1].rotation.z=0.25+swing;
   }
   const dir=stage===2?1:-1;
   const behindZ=mother.position.z-dir*8;
   camera.position.x+=(mother.position.x*0.55-camera.position.x)*0.08;
   camera.position.y+=(5.5-camera.position.y)*0.08;
   camera.position.z+=(behindZ-camera.position.z)*0.08;
   camera.lookAt(mother.position.x*0.25,1.2,mother.position.z+dir*5);
 }
 renderer.render(scene,camera);
}
animate();
}
</script>
</body>
</html>
"""

components.html(GAME, height=690, scrolling=False)
