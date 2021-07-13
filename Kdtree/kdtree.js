k = 2;
let root;
class Node {
    constructor (point , axis ){
        this.point = point;// x y z f 
        this.left = null;
        this.right = null;
        this.axis = axis; //4 
    }
}
function distanceSquared ( point1 , point2 ){
    var distance = 0;
    for (var i = 0; i < k; i ++)
        distance += Math.pow (( point1 [i] - point2 [i]) , 2) ;
    return Math.sqrt ( distance );
}
function closest_point_brute_force(points, point){
    var distance = null;
    var best_distance = null;
    var best_point = null;
    for(let i = 0; i < points.length; i++){
        distance = distanceSquared(points[i], point);

        //console.log(distance);
        if(best_distance === null || distance < best_distance){
            best_distance = distance;
            //best_point = { 'point': points[i], 'distance': distance }
            best_point = points[i];
        }
    }

    return best_point;
}

function naive_closest_point(node, point, depth = 0, best = null){
    //algorithm
    //1. best = min(distance(point, node.point), best)
    //2. chose the branch according to axis per level
    //3. recursevely call by branch chosed

    if (node === null)
        return best;

    var axis = depth % k;
    var next_best = null; //next best point
    var next_branch = null; //next node brach to look for

    if (best === null || (distanceSquared(best, point) > distanceSquared(node.point, point)))
        next_best = node.point;
    else
        next_best   = best;

    if (point[axis] < node.point[axis])
        next_branch = node.left
    else
        next_branch = node.right

    return  naive_closest_point(next_branch, point, depth +1, next_best);
}

function contains(node, center, size){
    var flag = true;
    for(var i = 0; i < k; i++){
        flag &= (node.point[i] >= center[i] - size[i] && 
            node.point[i] <= center[i] + size[i]);
    }
    return flag;
}
function range_query_rec (node , center , size, queue , depth = 0) {
    if (node === null)
        return ;

    var axis = depth % k;
    // console.log('node: ' + node.point + 'center '+center.point + ' contains:' +  contains(node, center,size));
    if (contains(node, center,size)){ 
        //si la distancia entre los puntos es menor se encuentra dentro del circulo 
        queue.push(node.point);
    }
    if (Math.abs(center[axis] - node.point[axis]) < size[axis]){ 
        
        range_query_rec(node.left, center, size, queue, depth +1);
        range_query_rec(node.right, center, size, queue, depth +1);
    }
    else{// de lo contrario va por un de sus hijos 
        if (center[axis] < node.point[axis])
            next_branch = node.left
        else
            next_branch = node.right
        
        range_query_rec(next_branch, center, size, queue, depth +1);
    }
}
// ve que puntos intersectan los el circulo 
function range_query_circle (node , center , radio , queue , depth = 0) {
    if (node === null)
        return ;

    var axis = depth % k;
    // console.log('node: ' + node.point + 'center '+center.point + ' distancia ' +  distanceSquared(node.point, center.point));
    if (distanceSquared(node.point, center) <= radio){ 
        //si la distancia entre los puntos es menor se encuentra dentro del circulo 
        queue.push(node.point);
    }
    if (Math.abs(center[axis] - node.point[axis]) < radio){ 
        // si choca el radio con el punto en el eje actual se tiene que buscar en los dos hijos  
        range_query_circle(node.left, center, radio, queue, depth +1);
        range_query_circle(node.right, center, radio, queue, depth +1);
    }
    else{// de lo contrario va por un de sus hijos 
        if (center[axis] < node.point[axis])
            next_branch = node.left
        else
            next_branch = node.right
        
        range_query_circle(next_branch, center, radio, queue, depth +1);
    }
}
function closest_point (node , point , depth = 0) {
    //metodo que devuelve el punto mas cercano  search 

}


function KNN (node , point, k, depth = 0) {
    //metodo que devuelve los k puntos mas cercanos 
}

function getHeight(node) {
    if (node === null){
        return 0;
    }

    // find the height of each subtree
    var lh = getHeight(node.left);
    var rh = getHeight(node.right);

    return 1 + max(lh,rh);
}

function generate_dot(node){
    if (node === null){
        return "";
    }

    var tmp = '';

    if (node.left != null){
        tmp += '"' + node.point.toString() + '"' + ' -> ' + '"' + node.left.point.toString() + '"' + ';\n';
        tmp += generate_dot(node.left);
    }
    if (node.right != null){
        tmp += '"' + node.point.toString() + '"' + ' -> ' + '"' + node.right.point.toString() + '"' + ';\n';
        tmp += generate_dot(node.right);
    }

    return tmp;

}
function build_kdtree(points, depth = 0){
    var n = points.length;
    var axis = depth % k;


    if (n <= 0){
        return null;
    }
    if (n == 1){
        return new Node(points[0], axis)
    }

    var median = Math.floor(points.length / 2);

    // sort by the axis
    points.sort(function(a, b)
    {
        return a[axis] - b[axis];
    });
    //console.log(points);

    var left = points.slice(0, median);
    var right = points.slice(median + 1);

    //console.log(right);

    var node = new Node(points[median].slice(0, k), axis);
    node.left = build_kdtree(left, depth + 1);
    node.right = build_kdtree(right, depth + 1);

    return node;

}
