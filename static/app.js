$(document).ready(function() {
   $('#retrieve').click(function(){
     console.log('here')
       var l = $('#leftInput').val();
       var t = $('#topInput').val();
       var r = $('#rightInput').val();
       var b = $('#bottomInput').val();
       var num = $('input[name=num]:checked').val();

       $.ajax({
         url: "/transform",
         type: "get",
         data: {left: l, top: t, right: r, bottom: b, number: num},
         success: function(response) {
           console.log(response);
         $("#results").show();
         $("#results").html(response.html);
        },
        error: function(xhr) {
          //Do Something to handle error
     }
     });
   });

// drawing

const cursor = document.querySelector('div.cursor');
const canvasIn = document.querySelector('canvas.in');
const canvasOut = document.querySelector('canvas.out');

let isMouseDown = false;

const growCursor = function() {
  cursor.classList.add("is-down");
  cursor.innerHTML = '<span>Scratch to reveal answers!</span>';
}

const shrinkCursor = function() {
  cursor.classList.remove("is-down");
}

const moveCursor = function(x,y) {
  cursor.style.left = x + "px";
  cursor.style.top = y + "px";
}

const setupCanvas = function(c) {

//   const bodyTag = document.querySelector("body");

  const w = window.innerWidth;
  const halfw = w/2;
//   const h = document.querySelector("body").offsetHeight;
  const h = window.innerHeight;
  const dpi = window.devicePixelRatio;

  c.width = w * dpi;
  c.height = h * dpi;
  c.style.width = w + "px";
  c.style.height = h + "px";

  // set up context
  const context = c.getContext("2d");
  context.scale(dpi, dpi);

  if (c.classList.contains("in")) {
      context.fillStyle = '#000000';
      context.strokeStyle = '#ffffff';
  } else {
      context.fillStyle = '#ffffff';
      context.strokeStyle = '#000000';
	}

//   context.fillStyle = 'red';
  context.lineWidth = 80;
  context.lineCap = 'round';
  context.lineJoin = 'round';

  context.shadowBlur = 10;
  context.shadowColor = context.strokeStyle;

  context.rect(halfw,0,w,h);
  context.fill();
};

const startDraw = function(c, x, y) {
  const context = c.getContext("2d");
  context.moveTo(x,y);
  context.beginPath();
}

const moveDraw = function(c, x, y) {
  if (isMouseDown) {
    const context = c.getContext("2d");
  //   context.rect(x-30, y-20, 60, 40)
  //   context.fill();
    context.lineTo(x,y);
    context.stroke();
  }
};


setupCanvas(canvasIn);
setupCanvas(canvasOut);

document.addEventListener('mousedown', function(event) {
  isMouseDown = true;
  console.log(event.pageX, event.pageY);
  if (event.pageX >= 500) {
    growCursor();
    startDraw(canvasIn, event.pageX, event.pageY);
    startDraw(canvasOut, event.pageX, event.pageY);
  }
});

document.addEventListener('mouseup', function() {
  isMouseDown = false;
  shrinkCursor();
});

document.addEventListener('mousemove', function(event) {
  moveCursor(event.pageX, event.pageY);
  moveDraw(canvasIn, event.pageX, event.pageY);
  moveDraw(canvasOut, event.pageX, event.pageY);
});


window.addEventListener("resize", function () {
  setupCanvas(canvasIn)
  setupCanvas(canvasOut)
})

});
