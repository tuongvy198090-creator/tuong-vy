
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Chim Cánh Cụt Vượt Băng",
    page_icon="🐧",
    layout="wide"
)

st.title("🐧 CHIM CÁNH CỤT VƯỢT BĂNG")
st.caption("Vượt sông băng • Trả lời kiến thức lớp 8 • Thu thập thùng cá")

game = r"""
<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
*{box-sizing:border-box}
body{margin:0;font-family:Arial,sans-serif;background:#dff7ff;color:#12334b}
button{font-weight:bold;cursor:pointer;border:0;border-radius:12px;padding:11px}
#app{max-width:1100px;margin:auto;padding:10px}
#hud{display:flex;justify-content:space-between;gap:8px;flex-wrap:wrap;margin-bottom:10px}
.pill{background:white;border-radius:12px;padding:10px 14px;font-weight:bold;box-shadow:0 3px 8px #75bad055}
#scene{height:470px;position:relative;overflow:hidden;border-radius:18px;
background:linear-gradient(#8bdfff 0%,#e0faff 48%,#63c8e9 49%,#167eae 100%);
perspective:800px;border:3px solid white}
.mountain{position:absolute;top:0;width:0;height:0;border-left:90px solid transparent;border-right:90px solid transparent;border-bottom:150px solid #f5ffff;opacity:.9}
#mount1{left:0}#mount2{right:0;border-bottom-color:#c4edfa;transform:scale(.8)}
.bank{position:absolute;bottom:0;height:110px;background:linear-gradient(#faffff,#bdeaf6);width:24%;z-index:2;border-top:7px solid white}
#startBank{left:0;clip-path:polygon(0 0,100% 0,80% 100%,0 100%)}
#goalBank{right:0;clip-path:polygon(20% 0,100% 0,100% 100%,0 100%)}
.bankname{position:absolute;top:12px;font-weight:bold;font-size:12px;color:#16516d}
#startBank .bankname{left:10px}#goalBank .bankname{right:10px}
#water{position:absolute;left:18%;right:18%;top:0;bottom:0;
background:repeating-linear-gradient(175deg,transparent 0 32px,#b8f1ff55 33px 36px)}
#course{position:absolute;left:19%;right:19%;top:95px;height:265px;
display:flex;flex-direction:column;justify-content:space-between;
transform:rotateX(8deg);z-index:3}
.rowice{height:37px;display:grid;grid-template-columns:repeat(4,1fr);gap:5px;position:relative}
.ice{background:linear-gradient(145deg,#fff,#a8eaff);border:2px solid #fff;
border-radius:7px;box-shadow:0 5px 0 #63b6dc, inset 0 -5px 0 #a5e6fa;
display:flex;align-items:center;justify-content:center;color:#14739a;font-size:12px;font-weight:bold}
.ice.selected{outline:4px solid #ffcf40;background:#fff4a9;transform:translateY(-5px)}
.gate{position:absolute;left:-2%;width:104%;height:13px;top:-8px;
background:linear-gradient(#f4ffff,#7ec8e5);border:2px solid white;border-radius:5px;
box-shadow:0 4px 0 #4d9fc4;z-index:6;transition:transform .5s,opacity .5s}
.gate.open{transform:translateY(-32px);opacity:.1}
#penguin{position:absolute;z-index:9;bottom:72px;left:50%;transform:translateX(-50%);
font-size:53px;filter:drop-shadow(0 5px 2px #174b6655);transition:left .25s,bottom .25s}
#chick{position:absolute;z-index:8;bottom:72px;left:57%;font-size:28px}
#bucket{position:absolute;z-index:8;right:5%;bottom:75px;font-size:42px}
#questionCard{position:absolute;z-index:10;top:10px;left:50%;transform:translateX(-50%);
width:min(94%,600px);text-align:center;background:#ffffffed;border:2px solid #fff;
border-radius:14px;padding:10px;box-shadow:0 5px 18px #15547530}
#subject{font-size:11px;color:#087ba8;font-weight:bold}
#question{font-size:16px;font-weight:bold;margin:5px 0}
#answers{display:grid;grid-template-columns:repeat(4,1fr);gap:6px;margin-top:8px}
.ans{background:#e0f6ff;border:2px solid #8dd4ee;color:#15415a;padding:7px 3px;min-height:42px;font-size:12px}
.ans.chosen{background:#ffe895;border-color:#e5a500}
#message{background:#fff;border-radius:12px;padding:10px;margin-top:10px;min-height:42px;font-weight:bold;text-align:center}
#controls{display:flex;gap:8px;justify-content:center;flex-wrap:wrap;margin-top:10px}
#controls button{background:#087eaf;color:white;min-width:70px}
#jump{background:#e9a800!important}
#restart{background:#237b50!important}
#help{text-align:center;font-size:12px;margin:9px;color:#315c70}
#startScreen{position:absolute;inset:0;background:#dff8ffed;z-index:20;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:20px}
#startScreen h2{color:#087eaf}
#startScreen button{background:#087eaf;color:white;font-size:17px;padding:14px 28px}
#result{display:none;position:absolute;inset:0;background:#eafaffef;z-index:21;align-items:center;justify-content:center;flex-direction:column;text-align:center;padding:20px}
#result h2{color:#087d50}
@media(max-width:500px){
#scene{height:500px}
#course{top:145px;height:240px;left:16%;right:16%}
.rowice{height:33px;gap:3px}
.ice{font-size:10px}
#questionCard{top:8px;padding:8px}
#question{font-size:14px}
.ans{font-size:10px;min-height:48px}
#penguin{font-size:45px}
}
</style>
</head>
<body>
<div id="app">
 <div id="hud">
  <div class="pill" id="round">🎯 Lượt 1</div>
  <div class="pill" id="progress">📚 Câu 1/8</div>
  <div class="pill" id="timer">⏱️ 15 giây</div>
  <div class="pill" id="lives">❤️❤️❤️</div>
 </div>

 <div id="scene">
  <div class="mountain" id="mount1"></div>
  <div class="mountain" id="mount2"></div>
  <div id="water"></div>
  <div class="bank" id="startBank"><div class="bankname">🏁 BỜ XUẤT PHÁT</div></div>
  <div class="bank" id="goalBank"><div class="bankname">🏆 BỜ THÙNG CÁ</div></div>
  <div id="course"></div>
  <div id="penguin">🐧</div>
  <div id="chick">🐧</div>
  <div id="bucket">🪣🐟</div>

  <div id="questionCard">
   <div id="subject">MÔN HỌC</div>
   <div id="question">Sẵn sàng vượt sông băng?</div>
   <div id="answers"></div>
  </div>

  <div id="startScreen">
   <div style="font-size:65px">🐧</div>
   <h2>CHIM CÁNH CỤT VƯỢT BĂNG</h2>
   <p>8 môn học • 4 tảng băng mỗi hàng • 15 giây mỗi câu</p>
   <p>Chọn đáp án, nhảy lên đúng tảng băng và vượt qua vách ngăn!</p>
   <button onclick="startGame()">▶ BẮT ĐẦU</button>
  </div>

  <div id="result">
   <div style="font-size:60px">🏆🐧🐟</div>
   <h2>GIẢI CỨU THÀNH CÔNG!</h2>
   <p id="resultText"></p>
   <button onclick="startGame()">🔄 Chơi lượt mới</button>
  </div>
 </div>

 <div id="message">Nhấn BẮT ĐẦU để chơi nhé!</div>
 <div id="controls">
  <button onclick="move(-1)">⬅ Trái</button>
  <button onclick="move(1)">Phải ➡</button>
  <button id="jump" onclick="submitAnswer()">🦘 NHẢY!</button>
  <button id="restart" onclick="startGame()">🔄 Chơi lại</button>
 </div>
 <div id="help">Máy tính: dùng ← → để chọn tảng băng, nhấn Space để nhảy. Điện thoại: chạm đáp án rồi nhấn NHẢY!</div>
</div>

<script>
const bank = [
 {subject:"Toán số",q:"Giá trị của 2³ + 3 là?",a:["6","8","11","16"],c:2,d:0},
 {subject:"Toán số",q:"Khai triển (x + 2)² được?",a:["x² + 4","x² + 4x + 4","x² + 2x + 4","x² - 4"],c:1,d:1},
 {subject:"Toán số",q:"Phân tích x² - 9 thành nhân tử.",a:["(x-9)(x+1)","(x-3)²","(x+3)²","(x-3)(x+3)"],c:3,d:2},
 {subject:"Toán hình",q:"Tổng các góc trong tứ giác bằng?",a:["180°","270°","360°","540°"],c:2,d:0},
 {subject:"Toán hình",q:"Hình chữ nhật 8 cm × 5 cm có diện tích?",a:["13 cm²","26 cm²","80 cm²","40 cm²"],c:3,d:1},
 {subject:"Toán hình",q:"Hình bình hành có góc 70°. Góc kề bằng?",a:["70°","110°","90°","140°"],c:1,d:2},
 {subject:"Tiếng Anh",q:"She ___ to school every day.",a:["go","goes","going","gone"],c:1,d:0},
 {subject:"Tiếng Anh",q:"Opposite of 'noisy' is ___.",a:["quiet","busy","crowded","modern"],c:0,d:1},
 {subject:"Tiếng Anh",q:"He can ___ well.",a:["sings","cans sing","sing","to sing"],c:2,d:2},
 {subject:"Vật lý",q:"Khối lượng riêng cho biết điều gì?",a:["Khối lượng một đơn vị thể tích","Thể tích vật","Trọng lượng vật","Nhiệt độ vật"],c:0,d:0},
 {subject:"Vật lý",q:"Công thức khối lượng riêng là?",a:["D=V/m","D=m/V","D=m×V","D=m+V"],c:1,d:1},
 {subject:"Vật lý",q:"Vật 600 g có thể tích 200 cm³. Khối lượng riêng là?",a:["0,3 g/cm³","2 g/cm³","3 g/cm³","120000 g/cm³"],c:2,d:2},
 {subject:"Vật lý",q:"Đơn vị nào dùng cho khối lượng riêng?",a:["kg","m³","N","kg/m³"],c:3,d:0},
 {subject:"Vật lý",q:"Vật 2,7 kg có thể tích 0,001 m³. Khối lượng riêng là?",a:["270 kg/m³","2700 kg/m³","27000 kg/m³","0,0027 kg/m³"],c:1,d:2},
 {subject:"Vật lý",q:"Hai vật cùng thể tích, A nặng 2 kg, B nặng 5 kg. Vật nào có khối lượng riêng lớn hơn?",a:["A","B","Bằng nhau","Không thể so sánh"],c:1,d:1},
 {subject:"Hóa học",q:"Chất nào là đơn chất?",a:["H₂O","O₂","NaCl","CO₂"],c:1,d:0},
 {subject:"Hóa học",q:"Dấu hiệu quan trọng của phản ứng hóa học là?",a:["Vật đổi chỗ","Nước chảy","Đường tan","Chất mới tạo thành"],c:3,d:1},
 {subject:"Hóa học",q:"Công thức của calcium oxide là?",a:["CaO","CaOH","Ca₂O","CO₂"],c:0,d:1},
 {subject:"Hóa học",q:"Phương trình cân bằng đúng là?",a:["H₂+O₂→H₂O","2H₂+O₂→2H₂O","H₂+2O₂→H₂O","2H₂+2O₂→H₂O"],c:1,d:2},
 {subject:"Sinh học",q:"Cơ quan nào bơm máu đi khắp cơ thể?",a:["Phổi","Tim","Gan","Dạ dày"],c:1,d:0},
 {subject:"Sinh học",q:"Cơ quan chính trao đổi khí ở người là?",a:["Phổi","Thận","Ruột non","Thực quản"],c:0,d:1},
 {subject:"Sinh học",q:"Phần lớn chất dinh dưỡng được hấp thụ tại?",a:["Miệng","Dạ dày","Ruột già","Ruột non"],c:3,d:1},
 {subject:"Sinh học",q:"Đơn vị cấu tạo cơ bản của cơ thể là?",a:["Mô","Tế bào","Cơ quan","Hệ cơ quan"],c:1,d:2},
 {subject:"Lịch sử",q:"Cách mạng tư sản Pháp bùng nổ năm nào?",a:["1776","1848","1789","1917"],c:2,d:0},
 {subject:"Lịch sử",q:"Cách mạng công nghiệp lần thứ nhất bắt đầu ở đâu?",a:["Pháp","Anh","Đức","Nga"],c:1,d:1},
 {subject:"Lịch sử",q:"Phong trào Tây Sơn bùng nổ năm nào?",a:["1771","1789","1802","1858"],c:0,d:1},
 {subject:"Lịch sử",q:"Ai lãnh đạo cuộc khởi nghĩa Lam Sơn?",a:["Nguyễn Huệ","Ngô Quyền","Lê Lợi","Đinh Bộ Lĩnh"],c:2,d:2},
 {subject:"Địa lý",q:"Việt Nam thuộc khu vực nào của châu Á?",a:["Đông Á","Nam Á","Tây Á","Đông Nam Á"],c:3,d:0},
 {subject:"Địa lý",q:"Đặc điểm khí hậu nổi bật của Việt Nam là?",a:["Nhiệt đới ẩm gió mùa","Hàn đới","Hoang mạc","Địa Trung Hải"],c:0,d:1},
 {subject:"Địa lý",q:"Đồng bằng lớn nhất Việt Nam là?",a:["Thanh Hóa","Sông Cả","Sông Cửu Long","Ven biển Nam Trung Bộ"],c:2,d:1},
 {subject:"Địa lý",q:"Đồi núi chiếm khoảng bao nhiêu diện tích Việt Nam?",a:["1/4","3/4","1/2","Toàn bộ"],c:1,d:2}
];

let round=0, questions=[], index=0, lane=1, selected=null;
let time=15, timer=null, active=false, score=0, returning=false;
let used=new Set();

const $=id=>document.getElementById(id);

function shuffle(arr){
 for(let i=arr.length-1;i>0;i--){
  const j=Math.floor(Math.random()*(i+1));
  [arr[i],arr[j]]=[arr[j],arr[i]];
 }
 return arr;
}

function makeQuestions(){
 const subjects=["Toán số","Toán hình","Tiếng Anh","Vật lý","Hóa học","Sinh học","Lịch sử","Địa lý"];
 let result=[];
 for(const s of subjects){
  let options=bank.filter(q=>q.subject===s && !used.has(q.q));
  if(options.length===0){
   options=bank.filter(q=>q.subject===s);
  }
  const q=options[Math.floor(Math.random()*options.length)];
  used.add(q.q);
  result.push({...q,a:[...q.a],c:q.c});
 }
 return result;
}

function buildCourse(){
 const course=$("course");
 course.innerHTML="";
 for(let r=0;r<8;r++){
  const row=document.createElement("div");
  row.className="rowice";
  row.id="row"+r;
  for(let c=0;c<4;c++){
   const ice=document.createElement("div");
   ice.className="ice";
   ice.id=`ice${r}-${c}`;
   ice.textContent="🧊";
   row.appendChild(ice);
  }
  if(r>0){
   const gate=document.createElement("div");
   gate.className="gate";
   gate.id="gate"+r;
   row.appendChild(gate);
  }
  course.appendChild(row);
 }
}

function startGame(){
 clearInterval(timer);
 round++;
 questions=makeQuestions();
 index=0;lane=1;selected=null;score=0;time=15;active=true;returning=false;
 $("startScreen").style.display="none";
 $("result").style.display="none";
 $("penguin").style.display="block";
 $("penguin").textContent="🐧";
 $("penguin").style.bottom="72px";
 $("penguin").style.left="50%";
 $("chick").style.display="block";
 $("bucket").textContent="🪣🐟";
 buildCourse();
 $("round").textContent="🎯 Lượt "+round;
 showQuestion();
}

function showQuestion(){
 if(!active)return;
 clearInterval(timer);
 if(index>=questions.length){
  winGame();return;
 }
 lane=1;selected=null;time=15;
 const q=questions[index];
 $("subject").textContent="MÔN: "+q.subject.toUpperCase()+" • CÂU "+(index+1)+"/8";
 $("question").textContent=q.q;
 $("progress").textContent="📚 Câu "+(index+1)+"/8";
 $("timer").textContent="⏱️ 15 giây";
 $("message").textContent="Chọn một đáp án rồi nhấn NHẢY!";
 const ans=$("answers");ans.innerHTML="";
 const correct=q.a[q.c];
 const shuffled=shuffle(q.a.map((v,i)=>({v,old:i})));
 q.c=shuffled.findIndex(x=>x.old===q.c);
 q.a=shuffled.map(x=>x.v);
 q.a.forEach((a,i)=>{
  const b=document.createElement("button");
  b.className="ans";b.textContent=String.fromCharCode(65+i)+". "+a;
  b.onclick=()=>choose(i);
  ans.appendChild(b);
 });
 updateLane();
 timer=setInterval(()=>{
  time--;
  $("timer").textContent="⏱️ "+time+" giây";
  if(time<=0){
   clearInterval(timer);
   fall("Hết 15 giây! Chim mẹ rơi xuống sông băng!");
  }
 },1000);
}

function choose(i){
 if(!active)return;
 selected=i;lane=i;updateLane();
 document.querySelectorAll(".ans").forEach((b,j)=>b.classList.toggle("chosen",j===i));
 $("message").textContent="Đã chọn đáp án "+String.fromCharCode(65+i)+". Nhấn NHẢY để xác nhận!";
}

function move(d){
 if(!active)return;
 lane=Math.max(0,Math.min(3,lane+d));
 selected=lane;updateLane();
 document.querySelectorAll(".ans").forEach((b,j)=>b.classList.toggle("chosen",j===lane));
}
function updateLane(){
 document.querySelectorAll(".ice").forEach(el=>el.classList.remove("selected"));
 const current=$("ice"+index+"-"+lane);
 if(current)current.classList.add("selected");
 $("penguin").style.left=(24+lane*17)+"%";
}

function submitAnswer(){
 if(!active)return;
 if(selected===null){
  $("message").textContent="Hãy chọn một đáp án trước nhé!";
  return;
 }
 clearInterval(timer);
 const q=questions[index];
 if(selected===q.c){
  score++;
  const gate=$("gate"+(index+1));
  if(gate)gate.classList.add("open");
  $("message").textContent="🎉 Chính xác! Vách ngăn ngang đang hạ xuống!";
  $("ice"+index+"-"+selected).textContent="🐧";
  $("penguin").style.bottom=(78+index*2)+"px";
  index++;
  setTimeout(showQuestion,700);
 }else{
  fall("Sai mất rồi! Chim mẹ rơi xuống nước!");
 }
}

function fall(msg){
 if(!active)return;
 active=false;clearInterval(timer);
 $("penguin").style.bottom="0px";
 $("penguin").textContent="💦🐧";
 $("message").textContent=msg+" Đang tạo bộ câu hỏi mới...";
 $("lives").textContent="💙";
 setTimeout(()=>{
  $("lives").textContent="❤️❤️❤️";
  startGame();
 },1400);
}

function winGame(){
 active=false;clearInterval(timer);
 $("penguin").textContent="🐧🐟";
 $("penguin").style.left="88%";
 $("bucket").textContent="🎉🪣";
 $("message").textContent="Tuyệt vời! Em đã vượt qua đủ 8 môn!";
 $("resultText").textContent="Em trả lời đúng cả 8 câu và đã đến bờ thùng cá!";
 $("result").style.display="flex";
}

document.addEventListener("keydown",e=>{
 if(e.key==="ArrowLeft"){e.preventDefault();move(-1)}
 if(e.key==="ArrowRight"){e.preventDefault();move(1)}
 if(e.code==="Space"){e.preventDefault();submitAnswer()}
});
buildCourse();
</script>
</body>
</html>
"""

components.html(game, height=790, scrolling=True)
