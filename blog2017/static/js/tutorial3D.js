var wireframes = {};

var createWireframe1 = function() {
    var wireframe = new Canvas3D("tutorial_canvas_1");
    wireframes['wf1'] = wireframe;
    
    var axes = {
        edgeColour: '#111',
        nodes: [[40.5,   40.5,  40.5],
                [140.5,  40.5,  40.5], [135.5,  37.5,  40.5], [135.5, 43.5, 40.5],
                [ 40.5, 140.5,  40.5], [ 37.5, 135.5,  40.5], [ 43.5, 135.5, 40.5],
                [ 40.5,  40.5, 140.5], [ 40.5,  37.5, 135.5], [ 40.5, 43.5, 135.5]],
        edges: [[0,1], [1,2], [1,3], [0,4], [4,5], [4,6], [0,7], [7,8], [7,9]]
    };

    var labels = {
        nodes: [[145.5, 40.5, 40.5], [40.5, 148.5, 40.5], [40.5, 40.5, 145.5]],
        text: ["x", "y", "z"]
    };

    var point = {
        nodeColour: '#28A86B',
        nodes: [[70.5, 120.5, 95.5]]
    };

    var vector = {
        edgeColour: '#d88',
        nodes: [[70.5, 120.5, 95.5], [40.5, 120.5, 95.5], [70.5, 40.5, 95.5], [70.5, 120.5, 40.5]],
        edges: [[0, 1], [0, 2], [0, 3]]
    };
    
    wireframe.shapes.push(vector);
    wireframe.shapes.push(axes);
    wireframe.shapes.push(point);
    wireframe.shapes.push(labels);
    wireframe.setRotateCentre(90, 90, 80);
    wireframe.rotateX(0.35);
    wireframe.rotateY(0.35);
    
    wireframe.draw();
};

var createWireframe2 = function() {
    var wireframe = new Canvas3D("wireframe_canvas_1");
    wireframes['wf2'] = wireframe;
    
    var cube = {
        edgeColour: '#24c',
        nodeColour: '#28A86B',
        nodes: [[40, 40, 40], [40, 40, 140], [40, 140, 140], [40, 140, 40],
                [140, 40, 40], [140, 40, 140], [140, 140, 140], [140, 140, 40]],
        edges: [[0,1], [1,2], [2,3], [3,0],
                [4,5], [5,6], [6,7], [7,4],
                [0, 4], [1, 5], [2, 6], [3, 7]]
    };
    
    wireframe.shapes.push(cube);
    wireframe.setRotateCentre(90, 90, 90);
    wireframe.rotateX(0.35);
    wireframe.rotateY(0.35);
    
    wireframe.draw();
};

var createWireframe3 = function() {
    var wireframe3 = new Canvas3D("cube-nodes-canvas");
    wireframes['wf3'] = wireframe3;
    
    var axes = {
        edgeColour: '#888',
        nodes: [[10.5, 90.5, 90.5], [170.5,  90.5,  90.5],
                [90.5, 10.5, 90.5], [ 90.5, 170.5,  90.5],
                [90.5, 90.5, 10.5], [ 90.5,  90.5, 170.5]],
        edges: [[0,1], [2,3], [4,5]]
    };
    
    var cube = {
        nodeColour: '#28A86B',
        nodes: [[40, 40, 40], [40, 40, 140], [40, 140, 40], [40, 140, 140],
                [140, 40, 40], [140, 40, 140], [140, 140, 40], [140, 140, 140]]
    };
    
    var labels = {
        nodes: [[ 18, 30, 40], [ 18, 30, 140], [ 18, 150, 140], [ 18, 150, 40],
                [118, 30, 40], [118, 30, 140], [118, 150, 140], [118, 150, 40]],
        text: ["[-1, -1, -1]", "[-1, -1, 1]", "[-1, 1, 1]" , "[-1, 1, -1]",
               "[ 1, -1, -1]", "[ 1, -1, 1]", "[ 1, 1, 1]" , "[ 1, 1, -1]"]
    };
    
    wireframe3.shapes.push(axes);
    wireframe3.shapes.push(cube);
    wireframe3.shapes.push(labels);
    wireframe3.setRotateCentre(90, 90, 90);
    wireframe3.rotateX(0.25);
    wireframe3.rotateY(0.25);
    
    wireframe3.draw();
};

var createWireframe4 = function() {
    var wireframe = new Canvas3D("cube-edges-canvas");
    wireframes['wf4'] = wireframe;
    
    var axes = {
        edgeColour: '#888',
        nodes: [[10.5, 90.5, 90.5], [170.5,  90.5,  90.5],
                [90.5, 10.5, 90.5], [ 90.5, 170.5,  90.5],
                [90.5, 90.5, 10.5], [ 90.5,  90.5, 170.5]],
        edges: [[0,1], [2,3], [4,5]]
    };
    
    var cube = {
        edgeColour: '#24c',
        nodeColour: '#28A86B',
        nodes: [[40, 40, 40], [40, 40, 140], [40, 140, 40], [40, 140, 140],
                [140, 40, 40], [140, 40, 140], [140, 140, 40], [140, 140, 140]],
        edges: [[0,1], [1,3], [3,2], [2,0],
                [4,5], [5,7], [7,6], [6,4],
                [0, 4], [1, 5], [2, 6], [3, 7]]
    };
    
    var labels = {
        nodes: [[ 30, 30, 30], [ 30, 30, 150], [ 30, 150, 30], [ 30, 150, 150],
                [140, 30, 30], [140, 30, 150], [140, 150, 30], [140, 150, 150]],
        text: ["0", "1", "2" , "3", "4", "5", "6" , "7"]
    };
    
    wireframe.shapes.push(axes);
    wireframe.shapes.push(cube);
    wireframe.shapes.push(labels);
    wireframe.setRotateCentre(90, 90, 90);
    wireframe.rotateX(0.25);
    wireframe.rotateY(0.3);
    
    wireframe.draw();
};

var createWireframe5 = function() {
    var wireframe = new Canvas3D("wireframe-cuboid-canvas");
    wireframes['wf5'] = wireframe;
    
    var cube = {
        edgeColour: '#24c',
        nodes: [[40, 40, 40], [40, 40, 65], [40, 120, 40], [40, 120, 65],
                [90, 40, 40], [90, 40, 65], [90, 120, 40], [90, 120, 65]],
        edges: [[0,1], [1,3], [3,2], [2,0],
                [4,5], [5,7], [7,6], [6,4],
                [0, 4], [1, 5], [2, 6], [3, 7]]
    };
    
    wireframe.shapes.push(cube);
    wireframe.setRotateCentre(90, 90, 90);
    wireframe.rotateX(0.25);
    wireframe.rotateY(0.3);
    
    wireframe.draw();
};

// Highlight an edge or node when mouseover code
var highlightElement = function(str) {
    var target = str.split('-');
    var wireframe = wireframes[target[0]];
    var elementID = target[1].substr(1);
    
    if (target[1][0] === 'n') {
        wireframe.highlightNodes[elementID] = '#d44';
    } else {
        wireframe.highlightEdges[elementID] = '#d44';
    }
    
    wireframe.draw();
};

// Remove a highlight from a node or element
var removeHighlight = function(str) {
    var target = str.split('-');
    var wireframe = wireframes[target[0]];
    
    if (target[1][0] === 'n') {
        wireframe.highlightNodes = {};
    } else {
        wireframe.highlightEdges = {};
    }
    
    wireframe.draw();
};


$(document).ready(function() {
    //createWireframe1();
    //createWireframe2();
    //createWireframe3();
    //createWireframe4();
    //createWireframe5();

    $('.code-trigger').hover(
        function() {
            console.log("on");
            highlightElement(this.id);
        },
        function() {
            console.log("off");
            removeHighlight(this.id);
        }
    );

    console.log($('.code-trigger').length);

    $('.code-trigger').click(
        function() {
            console.log("W");
        }
    );
});

var moveSlider1 = function(slider, axis) {
    var value = parseInt($(slider).attr('value'), 10);
    $('#t1' + axis).html(value);
    var axisNum = {'x': 0, 'y': 1, 'z': 2};
    var n = axisNum[axis];
    
    var wireframe = wireframes['wf1'];
    var vector = wireframe.shapes[0];
    var point = wireframe.shapes[2];
    
    for (var i=0; i<4; i++) {
        if (i !== n+1) {
            vector.nodes[i][n] = 40.5 + value - wireframe.rotateCentre[n];
        }
    }
    
    point.nodes[0][n] = 40.5 + value - wireframe.rotateCentre[n];
    
    wireframe.draw();
};

var moveSlider2 = function(slider, axis) {
    var value = parseInt($(slider).attr('value'), 10);
    $('#t5' + axis).html(value);
    var nodes = { 'w': [4, 5, 6, 7],
                  'h': [2, 3, 6, 7],
                  'd': [1, 3, 5, 7] }[axis];
    var coord = { 'w': 0, 'h': 1, 'd': 2 }[axis];
    
    var wireframe = wireframes['wf5'];
    var wf_nodes = wireframe.shapes[0].nodes;
    
    for (var n in nodes) {
        wf_nodes[nodes[n]][coord] = 40.5 + value - wireframe.rotateCentre[coord];
    }
    
    wireframe.draw();
};

$(document).ready(function() {
    createWireframe3();
    createWireframe4();
});