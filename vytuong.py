
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="🐧 Hành trình qua hồ băng",
    page_icon="🐧",
    layout="wide"
)

st.title("🐧 Hành trình qua hồ băng")
st.write("Trả lời đúng 5 câu hỏi, vượt hồ băng và đến bờ bên kia để cứu chim con!")

game_html = r"""
<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body{margin:0;overflow:hidden;font-family:Arial}
#hud{position:absolute;top:10px;left:10px;right:10px;z-index:5;
background:#ffffffed;padding:12px;border-radius:14px;color:#17435c}
#question{font-size:19px;font-weight:bold}
#answers{display:grid;grid-template-columns:repeat(4,1fr);gap:5px}
button{padding:10px;border:2px solid #7bc5e7;border-radius:10px;
background:#e6f8ff;font-weight:bold;cursor:pointer}
#message{font-size:20px;color:#14784b;font-weight:bold}
#controls{position:absolute;bottom:15px;left:10px;right:10px;
display:flex;justify-content:space-between;z-index:5}
.pad{display:grid;grid-template-columns:repeat(3,48px);gap:4px}
.pad button{font-size:22px;padding:8px}
</style>
</head>
<body>
<div id="hud">
 <div>❄️ HÀNH TRÌNH QUA HỒ BĂNG</div>
 <div id="question">Câu 1: Số đối của -7 là số nào?</div>
 <div id="answers"></div>
 <div id="message">Hãy vượt qua hồ băng!</div>
</div>
<div id="controls">
 <div class="pad">
  <span></span><button onclick="move(0,-1)">↑</button><span></span>
  <button onclick="move(-1,0)">←</button>
  <button onclick="move(0,1)">↓</button>
  <button onclick="move(1,0)">→</button>
 </div>
 <button onclick="jump()">⬆ NHẢY</button>
</div>
<script src="https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.min.js"></script>
<script>
const scene=new THREE.Scene();
scene.background=new THREE.Color(0xb9e8fa);
scene.fog=new THREE.Fog(0xb9e8fa,35,90);

const camera=new THREE.PerspectiveCamera(65,innerWidth/innerHeight,.1,200);
const renderer=new THREE.WebGLRenderer({antialias:true});
renderer.setSize(innerWidth,innerHeight);
renderer.setPixelRatio(Math.min(devicePixelRatio,1.5));
document.body.appendChild(renderer.domElement);
renderer.domElement.style.position='fixed';
renderer.domElement.style.inset='0';

scene.add(new THREE.HemisphereLight(0xffffff,0x6d9bb2,2));
const light=new THREE.DirectionalLight(0xffffff,2);
light.position.set(-5,15,10);
scene.add(light);

const material=c=>new THREE.MeshStandardMaterial({color:c,roughness:.45});
const water=material(0x4aaacb);
const ice=material(0x9ee8fa);
const snow=material(0xf4fcff);

const lake=new THREE.Mesh(new THREE.PlaneGeometry(70,100),water);
lake.rotation.x=-Math.PI/2;
lake.position.set(0,-.7,-38);
scene.add(lake);

function shore(z){
 const m=new THREE.Mesh(new THREE.BoxGeometry(16,1,7),snow);
 m.position.set(0,-.3,z);
 scene.add(m);
}
shore(7);
shore(-70);

// Tuyết rơi
const count=900;
const geo=new THREE.BufferGeometry();
const positions=new Float32Array(count*3);
const speeds=[];
for(let i=0;i<count;i++){
 positions[i*3]=(Math.random()-.5)*60;
 positions[i*3+1]=Math.random()*25;
 positions[i*3+2]=Math.random()*100-70;
 speeds.push(2+Math.random()*4);
}
geo.setAttribute('position',new THREE.BufferAttribute(positions,3));
scene.add(new THREE.Points(geo,new THREE.PointsMaterial({
 color:0xffffff,size:.14,transparent:true,opacity:.9
})));

// Chim cánh cụt
const penguin=new THREE.Group();
scene.add(penguin);
const dark=material(0x202f46);
const white=material(0xffffff);
const orange=material(0xffa32c);

function ball(parent,mat,x,y,z,sx,sy,sz){
 const m=new THREE.Mesh(new THREE.SphereGeometry(1,16,12),mat);
 m.position.set(x,y,z);m.scale.set(sx,sy,sz);parent.add(m);
 return m;
}
ball(penguin,dark,0,.9,0,.42,.7,.38);
ball(penguin,white,0,.85,-.3,.31,.52,.17);
ball(penguin,dark,0,1.75,0,.34,.34,.33);
ball(penguin,white,0,1.7,-.25,.24,.21,.13);
ball(penguin,orange,0,1.61,-.4,.09,.07,.15);
for(const x of [-.12,.12])ball(penguin,dark,x,1.78,-.37,.035,.035,.025);
for(const x of [-.17,.17])ball(penguin,orange,x,.17,-.12,.14,.07,.23);
penguin.position.set(0,0,4);

// Chim con ở bờ đối diện
const baby=penguin.clone();
baby.scale.setScalar(.65);
baby.position.set(2,0,-70);
scene.add(baby);

// 5 câu hỏi minh họa
const questions=[
 {q:"Toán số: Số đối của -7 là?",a:["-7","7","0","1"],c:1},
 {q:"Toán hình: Tổng góc trong tứ giác?",a:["90°","180°","270°","360°"],c:3},
 {q:"Địa lí: Việt Nam thuộc khu vực nào?",a:["Đông Á","Đông Nam Á","Nam Á","Tây Á"],c:1},
 {q:"Vật lí: Công thức tốc độ là?",a:["v=s/t","v=t/s","v=s+t","v=s×t"],c:0},
 {q:"Sinh học: Đơn vị cơ bản của cơ thể?",a:["Mô","Cơ quan","Tế bào","Hệ cơ quan"],c:2}
];

const rows=[];
for(let r=0;r<5;r++){
 const group=new THREE.Group();
 const z=-3-r*12;
 const tiles=[];
 const order=[0,1,2,3];
 for(let i=3;i>0;i--){
  const j=Math.floor(Math.random()*(i+1));
  [order[i],order[j]]=[order[j],order[i]];
 }
 for(let lane=0;lane<4;lane++){
  const g=new THREE.Group();
  const m=new THREE.Mesh(new THREE.BoxGeometry(2.5,.4,3),ice.clone());
  g.add(m);
  // Vết nứt nhỏ tự nhiên, không có dấu X
  if(Math.random()<.5){
   const crack=new THREE.Mesh(
    new THREE.BoxGeometry(.04,.015,.7),material(0x358cac)
   );
   crack.position.set(.1,.21,0);
   crack.rotation.y=.35;
   g.add(crack);
  }
  g.position.set((lane-1.5)*2.8,0,z);
  group.add(g);
  tiles.push({g,m,answer:order[lane],lane});
 }
 const wall=new THREE.Mesh(
  new THREE.BoxGeometry(12,.8,.25),material(0x7fb9d1)
 );
 wall.position.set(0,.5,z+5.5);
 group.add(wall);
 scene.add(group);
 rows.push({group,tiles,wall,z,cleared:false});
}

// Bảng đáp án trên màn hình
let current=0,score=0,locked=false,won=false;
function showQuestion(){
 if(current>=5){
  document.getElementById('question').textContent=
   "🎉 Đã trả lời đủ 5 câu! Hãy đến bờ đối diện!";
  document.getElementById('answers').innerHTML="";
  document.getElementById('message').textContent=
   "Di chuyển về phía trước để đến chỗ chim con!";
  return;
 }
 const q=questions[current];
 document.getElementById('question').textContent=
  "Câu "+(current+1)+"/5: "+q.q;
 const a=document.getElementById('answers');
 a.innerHTML="";
 q.a.forEach((v,i)=>{
  const b=document.createElement('button');
  b.textContent=String.fromCharCode(65+i)+". "+v;
  b.onclick=()=>choose(i);
  a.appendChild(b);
 });
}
function choose(i){
 if(locked||won||current>=5)return;
 const q=questions[current];
 if(i!==q.c){
  document.getElementById('message').textContent="Chưa đúng, em thử lại nhé!";
  return;
 }
 locked=true;
 score+=10;
 document.getElementById('message').textContent="Đúng rồi! Vách băng đang hạ xuống!";
 const row=rows[current];
 row.cleared=true;
 const start=row.wall.position.y;
 const t0=performance.now();
 function lower(t){
  const p=Math.min(1,(t-t0)/650);
  row.wall.position.y=start*(1-p);
  if(p<1)requestAnimationFrame(lower);
 }
 requestAnimationFrame(lower);
 setTimeout(()=>{
  row.group.visible=false;
  current++;
  locked=false;
  showQuestion();
 },800);
}

let jumping=false,jumpY=0,jumpV=0;
function jump(){
 if(!jumping&&!won){
  jumping=true;jumpV=6;
 }
}
const keys={};
function move(x,z){
 if(won)return;
 penguin.position.x+=x*1.2;
 penguin.position.z+=z*1.2;
 penguin.position.x=Math.max(-5,Math.min(5,penguin.position.x));
 penguin.position.z=Math.max(-72,Math.min(8,penguin.position.z));
 checkLanding();
}
window.move=move;
window.jump=jump;

document.addEventListener('keydown',e=>{
 const k=e.key.toLowerCase();
 if(k==='arrowup'||k==='w')move(0,-.65);
 if(k==='arrowdown'||k==='s')move(0,.65);
 if(k==='arrowleft'||k==='a')move(-.65,0);
 if(k==='arrowright'||k==='d')move(.65,0);
 if(k===' ')jump();
});
function checkLanding(){
 if(locked||won)return;
 const row=rows[current];
 if(!row||row.cleared)return;
 for(const tile of row.tiles){
  const dx=Math.abs(penguin.position.x-tile.g.position.x);
  const dz=Math.abs(penguin.position.z-tile.g.position.z);
  if(dx<1&&dz<1.3&&jumping===false){
   choose(tile.answer);
   return;
  }
 }
}

const clock=new THREE.Clock();
let time=0;
function animate(){
 requestAnimationFrame(animate);
 const dt=Math.min(clock.getDelta(),.04);
 time+=dt;
 const p=geo.attributes.position.array;
 for(let i=0;i<count;i++){
  p[i*3+1]-=speeds[i]*dt;
  if(p[i*3+1]<-1)p[i*3+1]=25;
 }
 geo.attributes.position.needsUpdate=true;

 // Băng nhấp nhô và nghiêng rất nhẹ
 rows.forEach((r,ri)=>r.tiles.forEach((t,i)=>{
  t.g.position.y=Math.sin(time*1.1+i+ri)*.05;
  t.g.rotation.z=Math.sin(time*.7+i)*.012;
 }));

 if(jumping){
  jumpV-=15*dt;
  jumpY+=jumpV*dt;
  if(jumpY<=0){jumpY=0;jumping=false;jumpV=0;checkLanding();}
  penguin.position.y=jumpY;
 }

 if(current>=5&&!won&&penguin.position.z<=-67){
  won=true;
  document.getElementById('message').textContent=
   "🎉 CHÚC MỪNG! Chim mẹ đã đến bờ đối diện và cứu được chim con!";
  document.getElementById('question').textContent="🏆 CHIẾN THẮNG!";
  document.getElementById('answers').innerHTML=
   '<button onclick="location.reload()">Chơi lại</button>';
 }

 camera.position.lerp(
  new THREE.Vector3(penguin.position.x*.25,5,penguin.position.z+10),
  1-Math.exp(-4*dt)
 );
 camera.lookAt(penguin.position.x,1.2,penguin.position.z-5);
 baby.position.y=Math.sin(time*2)*.06;
 renderer.render(scene,camera);
}
window.addEventListener('resize',()=>{
 camera.aspect=innerWidth/innerHeight;
 camera.updateProjectionMatrix();
 renderer.setSize(innerWidth,innerHeight);
});
showQuestion();
animate();
</script>
</body>
</html>
"""

components.html(game_html, height=850, scrolling=False)
