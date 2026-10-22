
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Chim Cánh Cụt Vượt Băng 3D",
    page_icon="🐧",
    layout="wide"
)

st.title("🐧 CHIM CÁNH CỤT VƯỢT BĂNG 3D")
st.caption("Dùng phím ← → để chọn hướng, nhấn SPACE để nhảy lên tảng băng trả lời.")

game_html = r"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
* { box-sizing: border-box; }
body {
    margin: 0;
    background: #061b30;
    color: white;
    font-family: Arial, sans-serif;
    overflow: hidden;
}
#game {
    position: relative;
    width: 100%;
    height: 720px;
    overflow: hidden;
    border-radius: 14px;
    background: linear-gradient(#75d8f5, #d5f7ff 48%, #0a5578);
}
#scene {
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
}
#top {
    position: absolute;
    top: 12px;
    left: 12px;
    right: 12px;
    z-index: 5;
    padding: 13px;
    border-radius: 13px;
    text-align: center;
    background: rgba(3, 28, 54, .88);
    border: 2px solid #8de9ff;
}
#question {
    font-weight: bold;
    font-size: 19px;
    margin-bottom: 8px;
}
#subject {
    font-size: 13px;
    color: #a9f2ff;
    margin-bottom: 5px;
}
#status {
    font-size: 14px;
    color: #fff4a3;
}
#hint {
    position: absolute;
    z-index: 5;
    left: 12px;
    right: 12px;
    bottom: 105px;
    text-align: center;
    font-weight: bold;
    font-size: 15px;
    text-shadow: 1px 2px 3px black;
    pointer-events: none;
}
#controls {
    position: absolute;
    z-index: 8;
    bottom: 12px;
    left: 0;
    right: 0;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 18px;
    pointer-events: none;
}
.control-group {
    display: flex;
    gap: 12px;
    pointer-events: auto;
}
button {
    border: 2px solid #d7f8ff;
    border-radius: 50%;
    width: 62px;
    height: 62px;
    background: rgba(3, 38, 70, .9);
    color: white;
    font-size: 27px;
    font-weight: bold;
    box-shadow: 0 4px 0 #031827;
    touch-action: manipulation;
}
#jump {
    width: 92px;
    height: 72px;
    border-radius: 20px;
    font-size: 15px;
    background: #ff9f26;
    color: #19283b;
    border-color: #fff1bd;
}
button:active { transform: translateY(3px); box-shadow: none; }
#overlay {
    position: absolute;
    inset: 0;
    z-index: 10;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 20px;
    background: rgba(1, 18, 38, .78);
}
#panel {
    max-width: 440px;
    width: 100%;
    padding: 25px;
    border: 3px solid #83eaff;
    border-radius: 24px;
    background: linear-gradient(145deg, #104b70, #061d3d);
    text-align: center;
    box-shadow: 0 0 30px #36d7ff66;
}
#panel h2 { color: #a4f2ff; font-size: 27px; }
#panel p { line-height: 1.6; }
#start {
    width: auto;
    height: auto;
    padding: 13px 28px;
    border-radius: 14px;
    background: #ffcc4d;
    color: #142b40;
    font-size: 18px;
}
@media(max-width: 600px) {
    #game { height: 690px; }
    #question { font-size: 16px; }
    #top { top: 6px; left: 6px; right: 6px; padding: 9px; }
    button { width: 56px; height: 56px; }
    #jump { width: 82px; height: 64px; }
}
</style>
</head>
<body>
<div id="game">
    <div id="scene"></div>

    <div id="top">
        <div id="subject">SẴN SÀNG CHƯA?</div>
        <div id="question">Hãy bắt đầu chuyến vượt băng!</div>
        <div id="status">Câu 1/8 · Thời gian: 15 giây</div>
    </div>

    <div id="hint">← → CHỌN TẢNG BĂNG · SPACE ĐỂ NHẢY</div>

    <div id="controls">
        <div class="control-group">
            <button id="left" aria-label="Sang trái">◀</button>
            <button id="right" aria-label="Sang phải">▶</button>
        </div>
        <button id="jump">NHẢY</button>
    </div>

    <div id="overlay">
        <div id="panel">
            <h2>🐧 VƯỢT BĂNG 3D</h2>
            <p>Chim cánh cụt phải vượt qua 8 hàng băng để đến bờ bên kia lấy xô cá!</p>
            <p>🧊 Mỗi hàng có 4 tảng băng mang đáp án A, B, C, D.</p>
            <p>⬅️ ➡️ Chọn hướng · SPACE nhảy vào tảng băng.</p>
            <p>Trả lời đúng sẽ làm vách chắn hạ xuống. Trả lời sai hoặc hết giờ sẽ phải chơi lại.</p>
            <button id="start">BẮT ĐẦU</button>
        </div>
    </div>
</div>

<script src="https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.min.js"></script>
<script>
(() => {
const host = document.getElementById("scene");
const questionEl = document.getElementById("question");
const subjectEl = document.getElementById("subject");
const statusEl = document.getElementById("status");
const hintEl = document.getElementById("hint");
const overlay = document.getElementById("overlay");
const panel = document.getElementById("panel");

if (!window.THREE) {
    questionEl.textContent = "Không tải được thư viện 3D. Hãy tải lại trang.";
    return;
}

const scene = new THREE.Scene();
scene.background = new THREE.Color(0x87d9f3);
scene.fog = new THREE.Fog(0x87d9f3, 35, 100);

const camera = new THREE.PerspectiveCamera(
    65, host.clientWidth / host.clientHeight, 0.1, 250
);
const renderer = new THREE.WebGLRenderer({antialias:true});
renderer.setSize(host.clientWidth, host.clientHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.outputColorSpace = THREE.SRGBColorSpace;
host.appendChild(renderer.domElement);

scene.add(new THREE.HemisphereLight(0xd8f7ff, 0x284b6c, 2.1));
const sun = new THREE.DirectionalLight(0xffffff, 2.2);
sun.position.set(-8, 18, 12);
sun.castShadow = true;
scene.add(sun);

const mat = (color, roughness=0.75, metalness=0) =>
    new THREE.MeshStandardMaterial({color, roughness, metalness});

const waterMat = mat(0x087aab, 0.3, 0.15);
const iceMat = mat(0x9beaff, 0.25, 0.1);
const iceTopMat = mat(0xd8fbff, 0.22, 0.05);
const darkIceMat = mat(0x4cb9df, 0.35, 0.1);
const wallMat = mat(0x7fe6ff, 0.25, 0.1);

function box(parent, w, h, d, material, x, y, z) {
    const mesh = new THREE.Mesh(
        new THREE.BoxGeometry(w,h,d), material
    );
    mesh.position.set(x,y,z);
    mesh.castShadow = true;
    mesh.receiveShadow = true;
    parent.add(mesh);
    return mesh;
}

const water = new THREE.Mesh(
    new THREE.PlaneGeometry(180, 180), waterMat
);
water.rotation.x = -Math.PI/2;
water.position.y = -0.65;
water.position.z = -32;
water.receiveShadow = true;
scene.add(water);

// Hai bờ
const shoreMat = mat(0xd7e9e9);
box(scene, 25, 1.4, 13, shoreMat, 0, -0.15, 13);
box(scene, 25, 1.4, 12, shoreMat, 0, -0.15, -87);

const snowMat = mat(0xf4ffff);
box(scene, 25, 0.25, 13, snowMat, 0, 0.6, 13);
box(scene, 25, 0.25, 12, snowMat, 0, 0.6, -87);

// Những khối băng trang trí nổi trên nước
for (let i=0; i<45; i++) {
    const x = (Math.random()-0.5)*48;
    const z = 6-Math.random()*95;
    const s = 0.25 + Math.random()*0.8;
    const floe = box(
        scene, s*2, 0.18, s*1.5, iceMat,
        x, -0.25, z
    );
    floe.rotation.y = Math.random()*Math.PI;
}

// Tạo chim cánh cụt 3D bằng các khối hình
const penguin = new THREE.Group();
scene.add(penguin);

const blackMat = mat(0x172332, 0.48);
const whiteMat = mat(0xf4fbff, 0.4);
const orangeMat = mat(0xffa52f, 0.45);
const eyeMat = mat(0x050a12, 0.2);

const body = new THREE.Mesh(
    new THREE.SphereGeometry(0.62, 24, 20), blackMat
);
body.scale.set(0.82, 1.25, 0.72);
body.position.y = 1.18;
body.castShadow = true;
penguin.add(body);

const belly = new THREE.Mesh(
    new THREE.SphereGeometry(0.48, 24, 20), whiteMat
);
belly.scale.set(0.78, 1.08, 0.22);
belly.position.set(0, 1.12, -0.39);
penguin.add(belly);

const head = new THREE.Mesh(
    new THREE.SphereGeometry(0.43, 24, 20), blackMat
);
head.position.set(0, 2.13, 0);
head.castShadow = true;
penguin.add(head);

const face = new THREE.Mesh(
    new THREE.SphereGeometry(0.3, 20, 16), whiteMat
);
face.scale.set(1, 0.8, 0.25);
face.position.set(0, 2.08, -0.32);
penguin.add(face);

// Mắt và mỏ hướng về phía trước, tức phía âm Z
for (const x of [-0.16, 0.16]) {
    const eye = new THREE.Mesh(
        new THREE.SphereGeometry(0.055, 12, 12), eyeMat
    );
    eye.position.set(x, 2.18, -0.405);
    penguin.add(eye);
}
const beak = new THREE.Mesh(
    new THREE.ConeGeometry(0.13, 0.28, 5), orangeMat
);
beak.rotation.x = -Math.PI/2;
beak.position.set(0, 1.99, -0.51);
penguin.add(beak);

const wings = [];
for (const side of [-1,1]) {
    const wing = new THREE.Mesh(
        new THREE.SphereGeometry(0.2, 16, 12), blackMat
    );
    wing.scale.set(0.65, 1.5, 0.4);
    wing.position.set(side*0.51, 1.25, -0.02);
    wing.rotation.z = side * -0.22;
    penguin.add(wing);
    wings.push(wing);

    const foot = new THREE.Mesh(
        new THREE.BoxGeometry(0.3,0.12,0.38), orangeMat
    );
    foot.position.set(side*0.23,0.28,-0.12);
    penguin.add(foot);
}

penguin.position.set(-3.75, 0.7, 18);

// Câu hỏi lớp 8
const questionBank = [
 {subject:"TOÁN ĐẠI SỐ", q:"Giá trị của (x + 2)(x - 2) bằng gì?",
  a:["x² + 4","x² - 4","x² - 2","2x - 4"], c:1},
 {subject:"TOÁN HÌNH", q:"Tổng các góc trong một tứ giác bằng bao nhiêu?",
  a:["180°","270°","360°","90°"], c:2},
 {subject:"TIẾNG ANH", q:"Chọn dạng đúng: She ___ to school every day.",
  a:["go","goes","going","gone"], c:1},
 {subject:"VẬT LÝ", q:"Công thức tính khối lượng riêng là gì?",
  a:["D = m/V","D = V/m","D = m × V","D = V + m"], c:0},
 {subject:"HÓA HỌC", q:"Kí hiệu hóa học của oxi là gì?",
  a:["Ox","O","Oi","O₂⁻"], c:1},
 {subject:"SINH HỌC", q:"Bộ phận nào của cây chủ yếu hấp thụ nước?",
  a:["Lá","Hoa","Rễ","Quả"], c:2},
 {subject:"LỊCH SỬ", q:"Ngô Quyền chiến thắng quân Nam Hán năm nào?",
  a:["938","981","1009","1077"], c:0},
 {subject:"ĐỊA LÝ", q:"Việt Nam thuộc châu lục nào?",
  a:["Châu Âu","Châu Á","Châu Phi","Châu Mỹ"], c:1}
];

const questions = questionBank.map(q => ({
    ...q, a:q.a.slice()
}));

// Các hàng băng cố định: mỗi hàng có 4 tảng và một vách chắn
const lanes = [-3.75,-1.25,1.25,3.75];
const rows = [];
const firstZ = 8;
const stepZ = -10;

function makeLabel(text) {
    const canvas = document.createElement("canvas");
    canvas.width = 512;
    canvas.height = 180;
    const ctx = canvas.getContext("2d");
    ctx.fillStyle = "rgba(4,32,62,0.94)";
    ctx.beginPath();
    ctx.roundRect(8,8,496,164,22);
    ctx.fill();
    ctx.strokeStyle = "#b5f5ff";
    ctx.lineWidth = 7;
    ctx.stroke();

    ctx.fillStyle = "#ffffff";
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    ctx.font = "bold 35px Arial";
    const words = text.split(" ");
    let lines = [];
    let line = "";
    for (const word of words) {
        const test = line ? line+" "+word : word;
        if (ctx.measureText(test).width > 450 && line) {
            lines.push(line);
            line = word;
        } else line = test;
    }
    if (line) lines.push(line);
    lines = lines.slice(0,3);
    const startY = lines.length===1 ? 90 : lines.length===2 ? 65 : 45;
    lines.forEach((s,i) => ctx.fillText(s,256,startY+i*43));

    const texture = new THREE.CanvasTexture(canvas);
    texture.colorSpace = THREE.SRGBColorSpace;
    const sprite = new THREE.Sprite(
        new THREE.SpriteMaterial({map:texture, transparent:true})
    );
    sprite.scale.set(2.55,0.9,1);
    return sprite;
}

for (let r=0; r<questions.length; r++) {
    const z = firstZ + stepZ*(r+1);
    const group = new THREE.Group();
    scene.add(group);

    const platforms = [];
    const labels = [];

    for (let lane=0; lane<4; lane++) {
        const platform = box(
            group, 2.15, 0.55, 3.7, iceMat,
            lanes[lane], 0.05, z
        );
        box(
            group, 2.0, 0.14, 3.5, iceTopMat,
            lanes[lane], 0.39, z
        );

        // Viền xanh ở mép tảng băng
        box(group, 2.18,0.13,0.16,darkIceMat,
            lanes[lane],0.45,z-1.78);
        box(group, 2.18,0.13,0.16,darkIceMat,
            lanes[lane],0.45,z+1.78);

        const label = makeLabel(
            String.fromCharCode(65+lane)+". "+questions[r].a[lane]
        );
        label.position.set(lanes[lane],1.65,z);
        group.add(label);
        labels.push(label);
        platforms.push(platform);
    }

    // Vách chắn ngang đường, gồm 3 phần để không che đáp án
    const wallGroup = new THREE.Group();
    group.add(wallGroup);
    box(wallGroup,10.7,0.28,0.32,wallMat,0,1.1,z-4.1);
    box(wallGroup,0.3,1.4,0.4,darkIceMat,-5.2,0.6,z-4.1);
    box(wallGroup,0.3,1.4,0.4,darkIceMat,5.2,0.6,z-4.1);

    rows.push({
        z, group, platforms, labels,
        wall:wallGroup,
        lowered:false
    });
}

// Cột băng trang trí dọc hai bên đường
for (const side of [-1,1]) {
    for (let i=0;i<18;i++) {
        const z = 8-i*5;
        const h = 0.5+Math.random()*1.7;
        const crystal = new THREE.Mesh(
            new THREE.OctahedronGeometry(0.6+Math.random()*0.5),
            iceMat
        );
        crystal.position.set(side*(7+Math.random()*3),h/2,z);
        crystal.scale.y = h;
        crystal.castShadow = true;
        scene.add(crystal);
    }
}

// Xô cá ở bờ đích
const bucket = new THREE.Group();
scene.add(bucket);
const bucketMat = mat(0x477d9e,0.5,0.25);
const bucketBody = new THREE.Mesh(
    new THREE.CylinderGeometry(0.8,0.58,1.2,16,1,true),bucketMat
);
bucketBody.position.y = 0.65;
bucket.add(bucketBody);
const rim = new THREE.Mesh(
    new THREE.TorusGeometry(0.78,0.08,8,24),mat(0xd7f5ff)
);
rim.rotation.x = Math.PI/2;
rim.position.y = 1.25;
bucket.add(rim);
for(let i=0;i<5;i++) {
    const fish = new THREE.Mesh(
        new THREE.SphereGeometry(0.17,12,10),orangeMat
    );
    fish.scale.set(1.5,0.55,0.6);
    fish.position.set((Math.random()-0.5)*0.7,1.1+Math.random()*0.3,
        (Math.random()-0.5)*0.5);
    bucket.add(fish);
}
bucket.position.set(0,0,-87);

// Trạng thái trò chơi
let current = 0;
let lane = 0;
let running = false;
let jumping = false;
let locked = false;
let jumpT = 0;
let jumpFrom = new THREE.Vector3();
let jumpTo = new THREE.Vector3();
let timeLeft = 15;
let lastTick = performance.now();
let lastFrame = performance.now();
let messageTimer = null;
let gameToken = 0;
let win = false;

function setHint(text) {
    hintEl.textContent = text;
}

function updateLaneVisual() {
    rows.forEach((row,r) => {
        row.platforms.forEach((p,i) => {
            const selected = (r===current && i===lane);
            p.material = selected ? mat(0xffd34f,0.22,0.1) : iceMat;
            p.scale.y = selected ? 1.12 : 1;
        });
        row.labels.forEach((label,i) => {
            label.position.y = (i===lane && r===current) ? 1.9 : 1.65;
        });
    });
}

function updateHUD() {
    if (current >= questions.length) return;
    const q = questions[current];
    subjectEl.textContent = q.subject;
    questionEl.textContent = q.q;
    statusEl.textContent =
        "Câu " +(current+1)+"/"+questions.length+
        " · Thời gian: "+Math.max(0,Math.ceil(timeLeft))+" giây";
    updateLaneVisual();
}

function showPanel(title, text, buttonText, callback) {
    overlay.style.display = "flex";
    panel.innerHTML = "";
    const h = document.createElement("h2");
    h.textContent = title;
    const p = document.createElement("p");
    p.textContent = text;
    p.style.lineHeight = "1.7";
    const b = document.createElement("button");
    b.id = "start";
    b.textContent = buttonText;
    b.onclick = callback;
    panel.append(h,p,b);
}

function resetPenguin() {
    penguin.position.set(lanes[0],0.7,18);
    penguin.rotation.set(0,0,0);
    lane = 0;
    current = 0;
    timeLeft = 15;
    jumping = false;
    locked = false;
    win = false;
    rows.forEach(row => {
        row.lowered = false;
        row.wall.position.y = 0;
        row.wall.visible = true;
    });
    rows.forEach(row => {
        row.labels.forEach(label => {
            row.group.remove(label);
            label.material.map.dispose();
            label.material.dispose();
        });
    });

    // Xáo trộn thứ tự câu hỏi và đáp án ở mỗi lượt chơi
    const shuffled = questionBank.map(q => {
        const correctAnswer = q.a[q.c];
        const answers = q.a.slice();
        for (let i=answers.length-1;i>0;i--) {
            const j=Math.floor(Math.random()*(i+1));
            [answers[i],answers[j]]=[answers[j],answers[i]];
        }
        return {...q,a:answers,c:answers.indexOf(correctAnswer)};
    });
    shuffled.forEach((q,i) => {
        questions[i].subject=q.subject;
        questions[i].q=q.q;
        questions[i].a=q.a;
        questions[i].c=q.c;

        const row=rows[i];
        row.labels.forEach(label => {
            row.group.remove(label);
            if(label.material.map) label.material.map.dispose();
            label.material.dispose();
        });
        row.labels=[];
        for(let laneIndex=0;laneIndex<4;laneIndex++) {
            const label=makeLabel(
                String.fromCharCode(65+laneIndex)+". "+q.a[laneIndex]
            );
            label.position.set(lanes[laneIndex],1.65,row.z);
            row.group.add(label);
            row.labels.push(label);
        }
    });

    camera.position.set(0,5.5,26);
    camera.lookAt(0,1,-2);
    updateHUD();
}

function beginGame() {
    if(messageTimer) clearTimeout(messageTimer);
    gameToken++;
    resetPenguin();
    overlay.style.display = "none";
    running = true;
    lastTick = performance.now();
    lastFrame = performance.now();
    setHint("← → CHỌN TẢNG BĂNG · SPACE ĐỂ NHẢY");
}

function moveLane(dir) {
    if(!running || jumping || locked || win) return;
    lane = Math.max(0,Math.min(3,lane+dir));
    updateHUD();
}

function startJump() {
    if(!running || jumping || locked || win) return;
    if(current >= rows.length) return;

    jumping = true;
    locked = true;
    jumpT = 0;
    jumpFrom.copy(penguin.position);
    jumpTo.set(lanes[lane],0.7,rows[current].z);
    setHint("🐧 ĐANG NHẢY TỚI TẢNG BĂNG "+String.fromCharCode(65+lane)+"...");
}

function landOnPlatform() {
    jumping = false;
    const q = questions[current];
    const chosen = lane;
    if(chosen === q.c) {
        const row = rows[current];
        row.lowered = true;
        locked = true;
        setHint("✅ CHÍNH XÁC! VÁCH CHẮN ĐANG HẠ XUỐNG!");
        const token = gameToken;

        // Hạ vách chắn bằng hoạt ảnh
        const startY = row.wall.position.y;
        const start = performance.now();
        function lowerWall(now) {
            if(token !== gameToken) return;
            const t=Math.min(1,(now-start)/550);
            row.wall.position.y=startY-2.0*t;
            if(t<1) requestAnimationFrame(lowerWall);
            else {
                row.wall.visible=false;
                current++;
                lane=chosen;
                timeLeft=15;
                locked=false;
                if(current>=questions.length) {
                    win=true;
                    running=false;
                    showPanel(
                        "🏆 CHIẾN THẮNG!",
                        "Tuyệt vời! Chim cánh cụt đã vượt qua tất cả các hàng băng và lấy được xô cá! 🐟",
                        "CHƠI LẠI",
                        beginGame
                    );
                    setHint("🎉 EM ĐÃ VƯỢT BĂNG THÀNH CÔNG!");
                } else {
                    updateHUD();
                    setHint("ĐÚNG RỒI! Chọn hướng cho câu tiếp theo rồi nhấn SPACE.");
                }
            }
        }
        requestAnimationFrame(lowerWall);
    } else {
        running=false;
        const token=gameToken;
        penguin.position.y=-1.2;
        setHint("💦 ÔI! TẢNG BĂNG CHƯA ĐÚNG!");
        messageTimer=setTimeout(() => {
            if(token!==gameToken) return;
            showPanel(
                "💦 RƠI XUỐNG NƯỚC!",
                "Đáp án chưa chính xác. Em hãy thử lại và chọn tảng băng mang đáp án đúng nhé!",
                "CHƠI LẠI",
                beginGame
            );
        },800);
    }
}

function onKey(e) {
    if(e.code==="ArrowLeft" || e.code==="KeyA") {
        e.preventDefault(); moveLane(-1);
    } else if(e.code==="ArrowRight" || e.code==="KeyD") {
        e.preventDefault(); moveLane(1);
    } else if(e.code==="Space" || e.code==="ArrowUp" || e.code==="KeyW") {
        e.preventDefault(); startJump();
    }
}
window.addEventListener("keydown",onKey);

document.getElementById("left").addEventListener("click",()=>moveLane(-1));
document.getElementById("right").addEventListener("click",()=>moveLane(1));
document.getElementById("jump").addEventListener("click",startJump);
document.getElementById("start").addEventListener("click",beginGame);

function animate(now) {
    requestAnimationFrame(animate);
    const dt=Math.min((now-lastFrame)/1000,0.04);
    lastFrame=now;

    if(running && !jumping && !locked) {
        if(now-lastTick>=1000) {
            timeLeft--;
            lastTick=now;
            updateHUD();
            if(timeLeft<=0) {
                running=false;
                const token=gameToken;
                setHint("⏰ HẾT GIỜ!");
                messageTimer=setTimeout(()=>{
                    if(token!==gameToken) return;
                    showPanel(
                        "⏰ HẾT THỜI GIAN!",
                        "Em chưa kịp nhảy vào tảng băng. Thử lại nhé!",
                        "CHƠI LẠI",
                        beginGame
                    );
                },400);
            }
        }
    }

    if(jumping) {
        jumpT += dt/0.85;
        const t=Math.min(1,jumpT);
        penguin.position.x=jumpFrom.x+(jumpTo.x-jumpFrom.x)*t;
        penguin.position.z=jumpFrom.z+(jumpTo.z-jumpFrom.z)*t;
        penguin.position.y=0.7+Math.sin(t*Math.PI)*2.6;
        penguin.rotation.z=(jumpTo.x-jumpFrom.x)*0.08;
        wings.forEach((w,i)=>w.rotation.z=Math.sin(now*0.025)*0.65*(i===0?-1:1));

        if(t>=1) {
            penguin.position.copy(jumpTo);
            penguin.rotation.z=0;
            landOnPlatform();
        }
    } else if(running) {
        wings.forEach((w,i)=>w.rotation.z=Math.sin(now*0.008)*0.12*(i===0?-1:1));
    }

    // Camera luôn theo sau chim cánh cụt
    camera.position.x += (penguin.position.x-camera.position.x)*0.07;
    camera.position.y += (5.2-camera.position.y)*0.04;
    camera.position.z += ((penguin.position.z+7.5)-camera.position.z)*0.07;
    camera.lookAt(
        penguin.position.x*0.35,
        1.2,
        penguin.position.z-6.0
    );

    renderer.render(scene,camera);
}
requestAnimationFrame(animate);

window.addEventListener("resize",()=>{
    const w=host.clientWidth, h=host.clientHeight;
    camera.aspect=w/h;
    camera.updateProjectionMatrix();
    renderer.setSize(w,h);
});

updateHUD();
})();
</script>
</body>
</html>
"""

components.html(game_html, height=740, scrolling=False)
