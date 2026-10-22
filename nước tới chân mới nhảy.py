
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Chim Cánh Cụt Vượt Băng 3D",
    page_icon="🐧",
    layout="wide"
)

st.title("🐧 CHIM CÁNH CỤT VƯỢT BĂNG 3D")
st.caption("Điều khiển chim cánh cụt vượt biển băng, trả lời câu hỏi để mở đường!")

game_html = r"""
<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<style>
body {margin:0;background:#071c32;color:white;font-family:Arial;text-align:center}
canvas {width:100%;height:480px;display:block;border-radius:14px}
button {padding:12px;margin:5px;border:0;border-radius:10px;cursor:pointer;font-weight:bold}
#answers button {width:45%;min-height:48px;background:#e6f7ff;color:#123}
#question {font-size:19px;font-weight:bold;margin:10px}
#message {min-height:25px;color:#ffe477}
</style>
</head>
<body>
<div>Hàng <span id="level">0</span>/8 · Còn <span id="time">15</span> giây</div>
<canvas id="game"></canvas>
<div id="question">Nhấn BẮT ĐẦU để chơi!</div>
<div id="answers"></div>
<div id="message">Trả lời đúng để hạ vách chắn.</div>
<button onclick="startGame()">▶ BẮT ĐẦU / CHƠI LẠI</button>
<div>
<button onclick="move(-1)">⬅ TRÁI</button>
<button onclick="jump()">⬆ NHẢY</button>
<button onclick="move(1)">PHẢI ➡</button>
</div>

<script src="https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.min.js"></script>
<script>
const canvas=document.getElementById("game");
const scene=new THREE.Scene();
scene.background=new THREE.Color(0x91dafa);
scene.fog=new THREE.Fog(0x91dafa,35,120);

const camera=new THREE.PerspectiveCamera(65,1,.1,200);
const renderer=new THREE.WebGLRenderer({canvas,antialias:true});
renderer.setPixelRatio(Math.min(devicePixelRatio,2));
renderer.shadowMap.enabled=true;

scene.add(new THREE.HemisphereLight(0xffffff,0x426779,2));
const sun=new THREE.DirectionalLight(0xffffff,2.5);
sun.position.set(-6,15,8);
sun.castShadow=true;
scene.add(sun);

function material(color){
 return new THREE.MeshStandardMaterial({color,roughness:.55});
}
function cube(w,h,d,color,x,y,z){
 const m=new THREE.Mesh(new THREE.BoxGeometry(w,h,d),material(color));
 m.position.set(x,y,z);
 m.castShadow=true;
 m.receiveShadow=true;
 scene.add(m);
 return m;
}

// Biển băng 3D
const sea=new THREE.Mesh(
 new THREE.PlaneGeometry(180,180),
 material(0x087db4)
);
sea.rotation.x=-Math.PI/2;
sea.position.set(0,-.7,-35);
scene.add(sea);

// Hai bờ
cube(20,1,12,0xf2fbff,0,-.2,7);
cube(20,1,9,0xf2fbff,0,-.2,-88);

// Chim cánh cụt 3D, camera nhìn từ sau lưng
const penguin=new THREE.Group();
scene.add(penguin);

const black=material(0x172b3a);
const white=material(0xf6f3e9);
const orange=material(0xff9d35);

function part(geo,mat,x,y,z,sx=1,sy=1,sz=1){
 const m=new THREE.Mesh(geo,mat);
 m.position.set(x,y,z);
 m.scale.set(sx,sy,sz);
 m.castShadow=true;
 penguin.add(m);
 return m;
}

part(new THREE.SphereGeometry(.65,24,20),black,0,1.05,0,.85,1.15,.8);
part(new THREE.SphereGeometry(.47,20,18),black,0,2.02,0,1,1,.9);
part(new THREE.SphereGeometry(.48,20,18),white,0,1.04,-.34,.83,1.08,.3);

for(const side of [-1,1]){
 const wing=part(new THREE.SphereGeometry(.3,16,12),black,side*.57,1.05,0,.45,1.3,.48);
 wing.rotation.z=side*.12;
 part(new THREE.SphereGeometry(.19,12,10),orange,side*.23,.22,-.12,1,.35,1.4);
}
const beak=part(new THREE.ConeGeometry(.13,.25,8),orange,0,1.98,-.44);
beak.rotation.x=-Math.PI/2;

// 8 hàng, mỗi hàng 4 tảng băng và một vách chắn ngang
const rows=[];
for(let r=0;r<8;r++){
 const z=-5-r*9;
 const platforms=[];
 for(let lane=0;lane<4;lane++){
  const x=(lane-1.5)*2.5;
  cube(2.2,.35,3.3,0xafe9ff,x,-.12,z);
  cube(2.2,.12,3.3,0x4d9fc8,x,-.35,z);
  platforms.push({x,z});
 }
 const wall=cube(10,1.7,.3,0xffc96d,0,.8,z-3.6);
 rows.push({z,platforms,wall});
}

// Xô cá ở đích
cube(1.2,1.1,1.2,0xdde5ec,0,.55,-88);
cube(1.35,.12,1.35,0x364c5a,0,1.12,-88);
for(let i=0;i<5;i++){
 const fish=new THREE.Mesh(
  new THREE.SphereGeometry(.17,12,10),orange
 );
 fish.scale.set(1,.45,1.7);
 fish.position.set((Math.random()-.5)*.6,1.4,-88);
 scene.add(fish);
}

// Câu hỏi theo 8 môn
const bank={
"Toán đại số":[
["3² bằng bao nhiêu?",["6","9","12","8"],1],
["2x+3x bằng?",["5","5x","6x","x"],1],
["(a+b)² bằng?",["a²+b²","a²+2ab+b²","a²-b²","2ab"],1]],
"Toán hình":[
["Tổng góc tứ giác?",["180°","270°","360°","90°"],2],
["Hình chữ nhật có hai đường chéo?",["Vuông góc luôn","Bằng nhau","Song song","Không bằng nhau"],1],
["Diện tích tam giác?",["Đáy×cao","Đáy×cao/2","2×đáy×cao","Chu vi×cao"],1]],
"Tiếng Anh":[
["She ___ to school every day.",["go","goes","going","gone"],1],
["Past tense of eat?",["eated","eats","ate","eaten"],2],
["Opposite of difficult?",["easy","hard","large","late"],0]],
"Vật lý":[
["Khối lượng riêng cho biết?",["Thể tích","Khối lượng trong một đơn vị thể tích","Trọng lượng","Chiều dài"],1],
["Công thức khối lượng riêng?",["D=V/m","D=m/V","D=m×V","D=m+V"],1],
["600 g, thể tích 200 cm³. D bằng?",["2","3","4","5"],1]],
"Hóa học":[
["Kí hiệu hóa học của oxi?",["Ox","O","Oi","X"],1],
["Công thức nước?",["CO₂","O₂","H₂O","NaCl"],2],
["Khí oxi O₂ là?",["Hợp chất","Đơn chất","Hỗn hợp","Dung dịch"],1]],
"Sinh học":[
["Đơn vị cơ bản của cơ thể sống?",["Mô","Cơ quan","Tế bào","Hệ cơ quan"],2],
["Bộ phận quang hợp chủ yếu?",["Rễ","Lá","Hoa","Quả"],1],
["Cơ quan bơm máu?",["Phổi","Gan","Tim","Thận"],2]],
"Lịch sử":[
["Ngô Quyền thắng quân Nam Hán năm?",["938","981","1010","1288"],0],
["Chiến thắng Bạch Đằng năm 938 gắn với?",["Trần Hưng Đạo","Ngô Quyền","Lý Thường Kiệt","Lê Lợi"],1],
["Ai dời đô ra Thăng Long năm 1010?",["Lý Công Uẩn","Trần Thái Tông","Đinh Bộ Lĩnh","Quang Trung"],0]],
"Địa lý":[
["Xích đạo chia Trái Đất thành?",["Đông và Tây","Bắc và Nam","Đất và biển","Hai lục địa"],1],
["Địa hình đồng bằng thường?",["Thấp, tương đối bằng phẳng","Dốc đứng","Núi cao","Băng tuyết"],0],
["Trái Đất tự quay theo hướng?",["Đông sang Tây","Tây sang Đông","Bắc xuống Nam","Nam lên Bắc"],1]]
};

let questions=[],index=0,lane=1,active=false,locked=false;
let timer=null,seconds=15,jumpY=0,jumpV=0,used={};

function shuffle(a){return a.slice().sort(()=>Math.random()-.5)}

function makeQuestions(){
 return shuffle(Object.keys(bank)).map(subject=>{
  if(!used[subject])used[subject]=[];
  if(used[subject].length===bank[subject].length)used[subject]=[];
  const pool=bank[subject].map((q,i)=>i).filter(i=>!used[subject].includes(i));
  const n=pool[Math.floor(Math.random()*pool.length)];
  used[subject].push(n);
  const q=bank[subject][n];
  const options=shuffle(q[1].map((text,i)=>({text,correct:i===q[2]})));
  return {subject,q:q[0],options};
 });
}

function startGame(){
 clearInterval(timer);
 questions=makeQuestions();index=0;lane=1;active=true;locked=false;
 penguin.position.set(0,0,7);
 rows.forEach(r=>r.wall.position.y=.8);
 document.getElementById("message").textContent="Chọn đáp án đúng để mở đường!";
 showQuestion();
}
function showQuestion(){
 if(index>=questions.length){win();return;}
 const q=questions[index];
 document.getElementById("level").textContent=index;
 document.getElementById("question").textContent=q.subject+" · "+q.q;
 const area=document.getElementById("answers");
 area.innerHTML="";
 q.options.forEach((o,i)=>{
  const b=document.createElement("button");
  b.textContent=String.fromCharCode(65+i)+". "+o.text;
  b.onclick=()=>answer(i);
  area.appendChild(b);
 });
 seconds=15;
 document.getElementById("time").textContent=seconds;
 clearInterval(timer);
 timer=setInterval(()=>{
  if(!active||locked)return;
  seconds--;
  document.getElementById("time").textContent=seconds;
  if(seconds<=0)fall("Hết giờ! Chơi lại nhé.");
 },1000);
}
function answer(i){
 if(!active||locked)return;
 locked=true;clearInterval(timer);
 if(!questions[index].options[i].correct){
  fall("Sai đáp án! Chim rơi xuống nước.");
  return;
 }
 document.getElementById("message").textContent="Đúng rồi! Vách chắn đang hạ!";
 const wall=rows[index].wall;
 const from=performance.now();
 function lower(now){
  const t=Math.min(1,(now-from)/500);
  wall.position.y=.8-1.5*t;
  if(t<1)requestAnimationFrame(lower);
 }
 requestAnimationFrame(lower);
 index++;
 setTimeout(()=>{
  if(!active)return;
  penguin.position.z=rows[index-1].z+1;
  showQuestion();
 },650);
}
function fall(message){
 if(!active)return;
 active=false;locked=true;clearInterval(timer);
 document.getElementById("message").textContent=message+" Đang tạo lượt mới…";
 penguin.position.y=-2;
 setTimeout(startGame,1500);
}
function win(){
 active=false;locked=true;clearInterval(timer);
 document.getElementById("level").textContent=8;
 document.getElementById("question").textContent="🎉 ĐÃ ĐẾN BỜ CÓ XÔ CÁ!";
 document.getElementById("answers").innerHTML="";
 document.getElementById("message").textContent="Vượt qua đủ 8 môn học thành công!";
 penguin.position.z=-88;
}
function move(d){
 if(!active)return;
 lane=Math.max(0,Math.min(3,lane+d));
 penguin.position.x=(lane-1.5)*2.5;
}
function jump(){if(active&&jumpY===0)jumpV=.18;}
window.addEventListener("keydown",e=>{
 if(e.key==="ArrowLeft"||e.key==="a")move(-1);
 if(e.key==="ArrowRight"||e.key==="d")move(1);
 if(e.code==="Space"||e.key==="ArrowUp")jump();
});
function resize(){
 const w=canvas.clientWidth,h=canvas.clientHeight;
 renderer.setSize(w,h,false);
 camera.aspect=w/h;camera.updateProjectionMatrix();
}
window.addEventListener("resize",resize);resize();

function animate(){
 requestAnimationFrame(animate);
 jumpY+=jumpV;
 jumpV-=.009;
 if(jumpY<0){jumpY=0;jumpV=0;}
 penguin.position.y=jumpY;
 camera.position.x+=(penguin.position.x-camera.position.x)*.08;
 camera.position.y+=(penguin.position.y+4-camera.position.y)*.08;
 camera.position.z+=(penguin.position.z+8-camera.position.z)*.08;
 camera.lookAt(penguin.position.x,1.1+penguin.position.y,penguin.position.z-7);
 renderer.render(scene,camera);
}
animate();
</script>
</body>
</html>
"""

components.html(game_html, height=850, scrolling=True)
