const canvas = document.createElement('canvas');
canvas.style.cssText = 'position:fixed;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:-1;';
document.body.appendChild(canvas);
const ctx = canvas.getContext('2d');
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

const pieces = Array.from({length: 150}, () => ({
x: Math.random() * canvas.width,
y: Math.random() * -canvas.height,
w: Math.random() * 10 + 6,
h: Math.random() * 6 + 4,
color: ['#1DB954','#ffffff','#ff6b6b','#ffd93d','#6bceff'][Math.floor(Math.random()*5)],
speed: Math.random() * 3 + 2,
angle: Math.random() * 360,
spin: Math.random() * 4 - 2,
wobble: Math.random() * 2 - 1
}));

function draw() {
ctx.clearRect(0, 0, canvas.width, canvas.height);
pieces.forEach(p => {
    ctx.save();
    ctx.translate(p.x, p.y);
    ctx.rotate(p.angle * Math.PI / 180);
    ctx.fillStyle = p.color;
    ctx.fillRect(-p.w/2, -p.h/2, p.w, p.h);
    ctx.restore();

    p.y += p.speed;
    p.angle += p.spin;
    p.x += p.wobble;

    if (p.y > canvas.height) {  // cuando sale por abajo, reaparece arriba
    p.y = -10;
    p.x = Math.random() * canvas.width;
    }
});
requestAnimationFrame(draw);
}
draw();