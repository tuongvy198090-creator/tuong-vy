
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Giải cứu chim cánh cụt",
    page_icon="🐧",
    layout="wide"
)

GAME = r"""
<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
*{box-sizing:border-box}
body{margin:0;overflow:hidden;font-family:Arial;background:#b9e8fa}
#game{position:fixed;inset:0}
#hud{
 position:fixed;top:10px;left:10px;right:10px;
 display:flex;justify-content:space-between;gap:8px;
 pointer-events:none;z-index:5
}
.panel{
 background:#ffffffed;border:2px solid #a5dff4;
 border-radius:15px;padding:10px 14px;
 color:#15405a;font-weight:bold;box-shadow:0 3px 12px #5689a633
}
#question{
 position:fixed;top:75px;left:50%;transform:translateX(-50%);
 width:min(900px,94%);z-index:5;text-align:center;
 background:#ffffffed;border:3px solid #a5dff4;
 border-radius:18px;padding:10px;color:#17435c;
 box-shadow:0 5px 15px #477b9944
}
#qtext{font-size:clamp(15px,2.3vw,23px);font-weight:bold}
#answers{
 display:grid;grid-template-columns:repeat(4,1fr);gap:6px;margin-top:8px
}
.answer{
 background:#e8f7ff;border:2px solid #80c8e9;
 border-radius:10px;padding:7px 3px;font-size:clamp(11px,1.5vw,16px)
}
#message{
 position:fixed;top:36%;left:50%;transform:translateX(-50%);
 z-index:6;background:#fff;border-radius:18px;padding:18px;
 font-size:22px;font-weight:bold;text-align:center;
 color:#18506b;display:none;max-width:90%
}
#controls{
 position:fixed;bottom:12px;left:12px;right:12px;
 display:flex;justify-content:space-between;align-items:end;
 z-index:8;pointer-events:none
}
.pad{display:grid;grid-template-columns:repeat(3,52px);gap:5px;pointer-events:auto}
.btn{
 width:52px;height:48px;border:2px solid #ffffff;
 border-radius:14px;background:#e8f8ffdd;color:#17435c;
 font-size:22px;font-weight:bold;touch-action:none
}
.actions{display:flex;gap:8px;pointer-events:auto}
#help{
 position:fixed;bottom:120px;left:10px;z-index:5;
 background:#ffffffdf;border-radius:10px;padding:8px;
 color:#17435c;font-size:12px
}
select{
 border:1px solid #9acfe7;border-radius:8px;padding:5px;
 background:white;color:#17435c
}
@media(max-width:600px){
 #question{top:100px}
 .panel{padding:7px;font-size:12px}
 #help{bottom:118px;max-width:150px}
 .btn{width:46px;height:43px}
 .pad{grid-template-columns:repeat(3,46px)}
}
</style>
</head>
<body>
<div id="game"></div>

<div id="hud">
 <div class="panel">🐧 Giải cứu chim con</div>
 <div class="panel">💎 Điểm: <span id="score">0</span></div>
 <div class="panel">📚 Câu: <span id="progress">1</span></div>
</div>

<div id="question">
 <div style="margin-bottom:5px">
  <select id="grade">
   <option value="7">Lớp 7</option>
   <option value="8" selected>Lớp 8</option>
  </select>
  <select id="subject">
   <option value="all">Tất cả môn</option>
   <option value="Toán số">Toán số</option>
   <option value="Toán hình">Toán hình</option>
   <option value="Địa lí">Địa lí</option>
   <option value="Lịch sử">Lịch sử</option>
   <option value="Hóa học">Hóa học</option>
   <option value="Vật lí">Vật lí</option>
   <option value="Sinh học">Sinh học</option>
  </select>
 </div>
 <div id="qtext">Chuẩn bị xuất phát nào!</div>
 <div id="answers"></div>
</div>

<div id="message"></div>

<div id="help">
 WASD / phím mũi tên: di chuyển<br>
 SPACE: nhảy · Chạm đáp án để chọn
</div>

<div id="controls">
 <div class="pad">
  <div></div><button class="btn" data-key="up">↑</button><div></div>
  <button class="btn" data-key="left">←</button>
  <button class="btn" data-key="down">↓</button>
  <button class="btn" data-key="right">→</button>
 </div>
 <div class="actions">
  <button class="btn" id="jump">⬆</button>
 </div>
</div>

<script src="https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.min.js"></script>
<script>
(() => {
const root=document.getElementById('game');
if(!window.THREE){
 document.getElementById('qtext').textContent=
 'Không tải được thư viện 3D. Em hãy kiểm tra kết nối Internet rồi tải lại trang.';
 return;
}

const scene=new THREE.Scene();
scene.background=new THREE.Color(0xb9e8fa);
scene.fog=new THREE.Fog(0xb9e8fa,35,100);

const camera=new THREE.PerspectiveCamera(
 65,innerWidth/innerHeight,0.1,200
);
const renderer=new THREE.WebGLRenderer({antialias:true});
renderer.setSize(innerWidth,innerHeight);
renderer.setPixelRatio(Math.min(devicePixelRatio,1.7));
renderer.shadowMap.enabled=true;
renderer.shadowMap.type=THREE.PCFSoftShadowMap;
root.appendChild(renderer.domElement);

scene.add(new THREE.HemisphereLight(0xe8f8ff,0x6eabc5,2));
const sun=new THREE.DirectionalLight(0xffffff,2.2);
sun.position.set(-8,18,12);
sun.castShadow=true;
scene.add(sun);

const mat=(color,roughness=0.8)=>new THREE.MeshStandardMaterial({
 color,roughness
});

const snowMat=mat(0xf0fbff);
const waterMat=mat(0x4eafce,0.3);
const iceMat=mat(0xa7e8f7,0.28);
const crackMat=mat(0x358eaf);
const darkMat=mat(0x202f46);
const whiteMat=mat(0xffffff);
const orangeMat=mat(0xffa52d);
const blackMat=mat(0x152432);

const floor=new THREE.Mesh(
 new THREE.PlaneGeometry(150,180),
 waterMat
);
floor.rotation.x=-Math.PI/2;
floor.position.set(0,-0.7,-48);
scene.add(floor);

// Bờ xuất phát và bờ đích
function shore(z){
 const m=new THREE.Mesh(
  new THREE.BoxGeometry(18,1.2,8),snowMat
 );
 m.position.set(0,-0.25,z);
 m.receiveShadow=true;
 scene.add(m);
}
shore(7);
shore(-66);

// Tuyết rơi
const snowCount=1100;
const snowGeo=new THREE.BufferGeometry();
const snowPos=new Float32Array(snowCount*3);
const snowSpeed=[];
for(let i=0;i<snowCount;i++){
 snowPos[i*3]=(Math.random()-.5)*65;
 snowPos[i*3+1]=Math.random()*25;
 snowPos[i*3+2]=Math.random()*110-65;
 snowSpeed.push(2+Math.random()*4);
}
snowGeo.setAttribute(
 'position',new THREE.BufferAttribute(snowPos,3)
);
const snow=new THREE.Points(
 snowGeo,new THREE.PointsMaterial({
  color:0xffffff,size:0.14,transparent:true,opacity:0.9
 })
);
scene.add(snow);

// Cây thông trang trí hai bên
function tree(x,z){
 const group=new THREE.Group();
 const trunk=new THREE.Mesh(
  new THREE.CylinderGeometry(.16,.25,1.2,7),mat(0x77533b)
 );
 trunk.position.y=.3;
 group.add(trunk);
 for(let i=0;i<3;i++){
  const cone=new THREE.Mesh(
   new THREE.ConeGeometry(1.15-i*.2,2.1,7),
   mat(i===1?0x438c83:0x357c78)
  );
  cone.position.y=1.1+i*1.0;
  group.add(cone);
 }
 group.position.set(x,0,z);
 scene.add(group);
}
for(let z=0;z>-75;z-=8){
 tree(-9-Math.random()*2,z);
 tree(9+Math.random()*2,z-3);
}

// Chim cánh cụt 3D
const penguin=new THREE.Group();
scene.add(penguin);

const body=new THREE.Mesh(
 new THREE.SphereGeometry(.48,20,16),darkMat
);
body.scale.set(.8,1.25,.75);
body.position.y=.85;
body.castShadow=true;
penguin.add(body);

const belly=new THREE.Mesh(
 new THREE.SphereGeometry(.36,20,16),whiteMat
);
belly.scale.set(.83,1.05,.35);
belly.position.set(0,.83,-.20);
penguin.add(belly);

const head=new THREE.Mesh(
 new THREE.SphereGeometry(.39,20,16),darkMat
);
head.position.set(0,1.85,-.02);
head.castShadow=true;
penguin.add(head);

const face=new THREE.Mesh(
 new THREE.SphereGeometry(.29,20,16),whiteMat
);
face.scale.set(1,.72,.4);
face.position.set(0,1.8,-.30);
penguin.add(face);

for(const x of [-.14,.14]){
 const eye=new THREE.Mesh(
  new THREE.SphereGeometry(.045,10,10),blackMat
 );
 eye.position.set(x,1.91,-.43);
 penguin.add(eye);
}
const beak=new THREE.Mesh(
 new THREE.ConeGeometry(.11,.24,5),orangeMat
);
beak.rotation.x=Math.PI/2;
beak.position.set(0,1.73,-.53);
penguin.add(beak);

for(const x of [-.43,.43]){
 const wing=new THREE.Mesh(
  new THREE.SphereGeometry(.16,12,10),darkMat
 );
 wing.scale.set(.55,1.5,.6);
 wing.position.set(x,1.0,-.02);
 wing.rotation.z=x<0?.25:-.25;
 penguin.add(wing);
}
const feet=[];
for(const x of [-.2,.2]){
 const foot=new THREE.Mesh(
  new THREE.SphereGeometry(.17,12,8),orangeMat
 );
 foot.scale.set(1,.35,1.4);
 foot.position.set(x,.15,-.12);
 penguin.add(foot);
 feet.push(foot);
}
penguin.position.set(0,0,4);

// Chim con ở bờ đích
const baby=penguin.clone();
baby.scale.setScalar(.65);
baby.position.set(2,0,-66);
scene.add(baby);

// Ngân hàng câu hỏi
const bank={
 7:[
  ['Toán số','Giá trị của (-3)² là bao nhiêu?',['-9','6','9','-6'],2],
  ['Toán số','Số đối của -7 là số nào?',['-7','7','0','1'],1],
  ['Toán hình','Hai góc đối đỉnh thì như thế nào?',['Bù nhau','Bằng nhau','Vuông góc','Không liên quan'],1],
  ['Toán hình','Tam giác có ba cạnh bằng nhau gọi là gì?',['Tam giác vuông','Tam giác cân','Tam giác đều','Tam giác tù'],2],
  ['Địa lí','Lớp vỏ Trái Đất gồm những gì?',['Đất và nước','Các mảng kiến tạo','Chỉ đá','Chỉ đại dương'],1],
  ['Lịch sử','Văn hóa Phục hưng khởi đầu ở đâu?',['Anh','Ý','Nga','Trung Quốc'],1],
  ['Hóa học','Kí hiệu hóa học của oxi là gì?',['Ox','O','Oi','X'],1],
  ['Vật lí','Tốc độ được tính bằng công thức nào?',['v=s/t','v=s×t','v=t/s','v=s+t'],0],
  ['Sinh học','Quang hợp chủ yếu diễn ra ở bào quan nào?',['Nhân','Ribosome','Lục lạp','Không bào'],2],
  ['Sinh học','Cơ quan hấp thụ nước chủ yếu của cây là gì?',['Lá','Rễ','Hoa','Quả'],1]
 ],
 8:[
  ['Toán số','Khai triển (x+2)² được kết quả nào?',['x²+4','x²+2x+4','x²+4x+4','x²-4x+4'],2],
  ['Toán số','Phân tích x²-9 thành nhân tử.',['(x-9)(x+1)','(x-3)(x+3)','(x-3)²','x(x-9)'],1],
  ['Toán hình','Tứ giác có hai cặp cạnh đối song song là gì?',['Hình thang','Hình bình hành','Hình diều','Tam giác'],1],
  ['Toán hình','Tổng các góc trong một tứ giác bằng bao nhiêu?',['180°','270°','360°','90°'],2],
  ['Địa lí','Việt Nam nằm trong khu vực nào?',['Đông Á','Đông Nam Á','Nam Á','Tây Á'],1],
  ['Lịch sử','Cách mạng tư sản Pháp bùng nổ năm nào?',['1776','1789','1815','1848'],1],
  ['Hóa học','Công thức hóa học của nước là gì?',['CO₂','O₂','H₂O','NaCl'],2],
  ['Vật lí','Khối lượng riêng được tính bằng công thức nào?',['D=m/V','D=V/m','D=m×V','D=m+V'],0],
  ['Sinh học','Đơn vị cấu tạo cơ bản của cơ thể là gì?',['Mô','Cơ quan','Tế bào','Hệ cơ quan'],2],
  ['Sinh học','Máu thuộc loại mô nào?',['Mô cơ','Mô thần kinh','Mô liên kết','Mô biểu bì'],2]
 ]
};

let questions=[];
let qIndex=0;
let score=0;
let rowState='ready';
let currentRow=-1;
let locked=false;
let gameWon=false;

const rows=[];
const rowStart=-3;
const rowGap=4.1;
const laneGap=2.65;

function shuffle(a){
 for(let i=a.length-1;i>0;i--){
  const j=Math.floor(Math.random()*(i+1));
  [a[i],a[j]]=[a[j],a[i]];
 }
 return a;
}
function loadQuestions(){
 const grade=document.getElementById('grade').value;
 const subject=document.getElementById('subject').value;
 let list=bank[grade].filter(q=>subject==='all'||q[0]===subject);
 if(list.length===0)list=bank[grade];
 questions=shuffle([...list]).slice(0,Math.min(5,list.length));
 qIndex=0;score=0;currentRow=-1;locked=false;gameWon=false;
 document.getElementById('score').textContent=score;
 rows.forEach(r=>scene.remove(r.group));
 rows.length=0;
 for(let i=0;i<questions.length;i++)makeRow(i);
 penguin.position.set(0,0,4);
 showQuestion();
 document.getElementById('message').style.display='none';
 rowState='ready';
}
function makeRow(index){
 const group=new THREE.Group();
 const z=rowStart-index*rowGap;
 const tiles=[];
 const q=questions[index];
 const answerOrder=shuffle([0,1,2,3]);
 for(let lane=0;lane<4;lane++){
  const tileGroup=new THREE.Group();
  const geo=new THREE.BoxGeometry(2.25,.38,2.35,2,1,2);
  const mesh=new THREE.Mesh(geo,iceMat.clone());
  mesh.position.y=0;
  mesh.receiveShadow=true;
  mesh.castShadow=true;
  tileGroup.add(mesh);

  // Vết nứt tự nhiên nhỏ, không có dấu X
  if(Math.random()<.48){
   const crack=new THREE.Mesh(
    new THREE.BoxGeometry(.035,.018,.72),crackMat
   );
   crack.position.set(.1,.205,.05);
   crack.rotation.y=Math.random()*.8;
   tileGroup.add(crack);
  }

  const answerIndex=answerOrder[lane];
  const label=document.createElement('div');
  label.className='answer';
  label.textContent=String.fromCharCode(65+answerIndex)+'. '+q[2][answerIndex];
  const spriteCanvas=document.createElement('canvas');
  spriteCanvas.width=512;spriteCanvas.height=128;
  const ctx=spriteCanvas.getContext('2d');
  ctx.fillStyle='#ffffff';
  ctx.fillRect(0,0,512,128);
  ctx.strokeStyle='#66bfe4';ctx.lineWidth=7;
  ctx.strokeRect(4,4,504,120);
  ctx.fillStyle='#17435c';
  ctx.font='bold 29px Arial';
  ctx.textAlign='center';ctx.textBaseline='middle';
  let text=String.fromCharCode(65+answerIndex)+'. '+q[2][answerIndex];
  while(ctx.measureText(text).width>470&&text.length>5)text=text.slice(0,-2)+'…';
  ctx.fillText(text,256,64);
  const texture=new THREE.CanvasTexture(spriteCanvas);
  const sprite=new THREE.Sprite(new THREE.SpriteMaterial({
   map:texture,transparent:true,depthTest:false
  }));
  sprite.scale.set(3.0,.75,1);
  sprite.position.set(0,1.5,0);
  tileGroup.add(sprite);

  tileGroup.position.set((lane-1.5)*laneGap,0,z);
  group.add(tileGroup);
  tiles.push({group:tileGroup,lane,answerIndex,mesh});
 }
 // Vách ngăn giữa các hàng
 const wall=new THREE.Mesh(
  new THREE.BoxGeometry(11,.85,.22),mat(0x91c8d9)
 );
 wall.position.set(0,.5,z+rowGap/2);
 wall.castShadow=true;
 group.add(wall);
 scene.add(group);
 rows.push({group,tiles,wall,z,index,cleared:false});
}
function showQuestion(){
 if(qIndex>=questions.length){
  win();
  return;
 }
 const q=questions[qIndex];
 document.getElementById('progress').textContent=(qIndex+1)+'/'+questions.length;
 document.getElementById('qtext').textContent=
  'Câu '+(qIndex+1)+' · '+q[0]+': '+q[1];
 const a=document.getElementById('answers');
 a.innerHTML='';
 for(let i=0;i<4;i++){
  const el=document.createElement('div');
  el.className='answer';
  el.textContent=String.fromCharCode(65+i)+'. '+q[2][i];
  a.appendChild(el);
 }
}
function showMessage(text){
 const m=document.getElementById('message');
 m.textContent=text;m.style.display='block';
 setTimeout(()=>{if(!gameWon)m.style.display='none'},1400);
}
function win(){
 gameWon=true;rowState='won';
 document.getElementById('qtext').textContent='🎉 ĐÃ ĐẾN ĐÍCH!';
 document.getElementById('answers').innerHTML='';
 const m=document.getElementById('message');
 m.innerHTML='🎉 Chúc mừng!<br>Chim mẹ đã cứu được chim con!<br><br><button id="again">Chơi lại</button>';
 m.style.display='block';
 document.getElementById('again').onclick=loadQuestions;
}
function answerTile(row,tile){
 if(locked||row.cleared||gameWon)return;
 if(row.index!==qIndex)return;
 locked=true;
 const correct=questions[qIndex][3];
 if(tile.answerIndex===correct){
  score+=10;
  document.getElementById('score').textContent=score;
  tile.mesh.material.color.set(0x8ff0b2);
  showMessage('✅ Chính xác! Vách băng đang hạ xuống!');
  row.cleared=true;
  rowState='cleared';
  const startY=row.wall.position.y;
  const start=performance.now();
  function lower(now){
   const t=Math.min(1,(now-start)/650);
   row.wall.position.y=startY*(1-t);
   if(t<1)requestAnimationFrame(lower);
  }
  requestAnimationFrame(lower);
  setTimeout(()=>{
   scene.remove(row.group);
   qIndex++;currentRow=-1;locked=false;rowState='ready';
   showQuestion();
   if(qIndex>=questions.length)win();
  },900);
 }else{
  tile.mesh.material.color.set(0xff9292);
  showMessage('❄️ Chưa đúng rồi! Em thử chọn lại nhé.');
  setTimeout(()=>{
   tile.mesh.material.color.set(0xa7e8f7);
   locked=false;
  },850);
 }
}

// Điều khiển bàn phím và nút cảm ứng
const keys={up:false,down:false,left:false,right:false};
let jumpRequested=false;
function setKey(k,v){if(k in keys)keys[k]=v;}
document.addEventListener('keydown',e=>{
 const k=e.key.toLowerCase();
 if(['arrowup','w'].includes(k))setKey('up',true);
 if(['arrowdown','s'].includes(k))setKey('down',true);
 if(['arrowleft','a'].includes(k))setKey('left',true);
 if(['arrowright','d'].includes(k))setKey('right',true);
 if(k===' '){jumpRequested=true;e.preventDefault();}
});
document.addEventListener('keyup',e=>{
 const k=e.key.toLowerCase();
 if(['arrowup','w'].includes(k))setKey('up',false);
 if(['arrowdown','s'].includes(k))setKey('down',false);
 if(['arrowleft','a'].includes(k))setKey('left',false);
 if(['arrowright','d'].includes(k))setKey('right',false);
});
document.querySelectorAll('[data-key]').forEach(btn=>{
 const k=btn.dataset.key;
 btn.addEventListener('pointerdown',e=>{e.preventDefault();setKey(k,true)});
 ['pointerup','pointercancel','pointerleave'].forEach(ev=>
  btn.addEventListener(ev,()=>setKey(k,false))
 );
});
document.getElementById('jump').addEventListener('pointerdown',e=>{
 e.preventDefault();jumpRequested=true;
});
let verticalVelocity=0;
let onGround=true;
let jumpHeight=0;
function jump(){
 if(onGround){
  verticalVelocity=7;
  onGround=false;
 }
}
function checkLanding(){
 if(gameWon||locked)return;
 for(const row of rows){
  if(row.cleared||row.index!==qIndex)continue;
  for(const tile of row.tiles){
   const p=tile.group.position;
   const dx=p.x-penguin.position.x;
   const dz=p.z-penguin.position.z;
   if(Math.abs(dx)<.88&&Math.abs(dz)<.9&&onGround){
    answerTile(row,tile);
    return;
   }
  }
 }
}
const clock=new THREE.Clock();
let elapsed=0;
function animate(){
 requestAnimationFrame(animate);
 const dt=Math.min(clock.getDelta(),.035);
 elapsed+=dt;

 // Tuyết rơi
 const pos=snowGeo.attributes.position.array;
 for(let i=0;i<snowCount;i++){
  pos[i*3+1]-=snowSpeed[i]*dt;
  pos[i*3]+=(Math.sin(elapsed+i)*.15)*dt;
  if(pos[i*3+1]<-1){
   pos[i*3+1]=24;
   pos[i*3]=(Math.random()-.5)*65;
   pos[i*3+2]=Math.random()*110-65;
  }
 }
 snowGeo.attributes.position.needsUpdate=true;

 // Băng lắc lư nhẹ, mỗi tảng một nhịp
 rows.forEach(row=>{
  row.tiles.forEach((tile,i)=>{
   const t=elapsed+i*1.7+row.index*.8;
   tile.group.position.y=Math.sin(t*1.1)*.055;
   tile.group.rotation.z=Math.sin(t*.65)*.012;
   tile.group.rotation.x=Math.cos(t*.7)*.009;
  });
 });

 if(!gameWon){
  let mx=0,mz=0;
  if(keys.left)mx-=1;
  if(keys.right)mx+=1;
  if(keys.up)mz-=1;
  if(keys.down)mz+=1;
  const len=Math.hypot(mx,mz)||1;
  mx/=len;mz/=len;
  const speed=4.2;
  penguin.position.x+=mx*speed*dt;
  penguin.position.z+=mz*speed*dt;
  penguin.position.x=THREE.MathUtils.clamp(penguin.position.x,-5.1,5.1);
  penguin.position.z=THREE.MathUtils.clamp(penguin.position.z,-71,8);

  if(mx||mz){
   penguin.rotation.y=Math.atan2(mx,-mz);
   feet[0].rotation.x=Math.sin(elapsed*12)*.25;
   feet[1].rotation.x=-Math.sin(elapsed*12)*.25;
  }
  if(jumpRequested){jump();jumpRequested=false;}
  if(!onGround||verticalVelocity>0){
   verticalVelocity-=18*dt;
   jumpHeight+=verticalVelocity*dt;
   if(jumpHeight<=0){
    jumpHeight=0;verticalVelocity=0;onGround=true;
   }
   penguin.position.y=jumpHeight;
  }
  checkLanding();
 }

 // Camera theo sau chim mẹ
 const desired=new THREE.Vector3(
  penguin.position.x*.35,
  5.0+jumpHeight*.3,
  penguin.position.z+10.5
 );
 camera.position.lerp(desired,1-Math.exp(-4*dt));
 camera.lookAt(
  penguin.position.x,
  1.0+jumpHeight*.4,
  penguin.position.z-5.5
 );

 // Chim con nhấp nhô
 baby.position.y=Math.sin(elapsed*2)*.07;
 renderer.render(scene,camera);
}
document.getElementById('grade').addEventListener('change',loadQuestions);
document.getElementById('subject').addEventListener('change',loadQuestions);
window.addEventListener('resize',()=>{
 camera.aspect=innerWidth/innerHeight;
 camera.updateProjectionMatrix();
 renderer.setSize(innerWidth,innerHeight);
});
loadQuestions();
animate();
})();
</script>
</body>
</html>
"""

components.html(GAME, height=850, scrolling=False)
