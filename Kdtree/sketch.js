var tree;
var center;
var data = [];

function randomdata(){
    for ( let i = 0; i < 12; i ++) {
        var x = Math.floor ( Math.random () * height );
        var y = Math.floor ( Math.random () * height );
        data.push ([x, y]) ;        
    }
}
function graficar(){
    // grafica las lineas del plano cartesiano
    for (var x = 0; x < width; x += width / 10) {
        for (var y = 0; y < height; y += height / 5) {
            stroke (125 , 125 , 125) ;
            strokeWeight (1) ;
            line (x, 0, x, height );
            line (0 , y, width , y);
        }
    }
    // grafica los puntos del array data
    for ( let i = 0; i < 12; i ++) {
        fill (255 , 255 , 255) ;
        circle (data[i][0], height - data[i][1], 3) ; // 200 -y para q se dibuje apropiadamente
        // circle (x, height - y, 3) ; 
        textSize (5) ;
        text (data[i][0] + ',' + data[i][1], data[i][0] + 5, height - data[i][1]);// 200 -y para q se dibuje
        // text (x + ',' + y, x + 5, height - y);
        
    }
}
function setup () {
    var width = 200;
    var height = 200;
    createCanvas (width , height ) ;

    background (0) ;
    
    randomdata();
    console.log(data)
    graficar();

    tree = build_kdtree ( data ) ;
    console.log ( tree );
}
   
function draw(){
    background(0);
    graficar();

     // 
     var radio = 30;
     var x = mouseX;
     var y = mouseY;;
     //center 
     var center = new Node([x,height-y],k);
     queue = []
 
     range_query_circle(tree,center,radio,queue);
     for(var i = 0; i < queue.length; i++){
        fill (0 , 255 , 0) ;
        circle (queue[i][0], height - queue[i][1], 3) ;
     }
 
     
     stroke (0 ,255 ,0) ;
     strokeWeight(2);
     noFill()
     circle ( mouseX, mouseY,radio ,radio)
}