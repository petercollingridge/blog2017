function Canvas3D(id) {
    var canvas = $("#" + id);
    var context = canvas.get(0).getContext("2d");
    var WIDTH = canvas.width();
    var HEIGHT = canvas.height();
    var CANVAS_X = canvas.offset().left;
    var CANVAS_Y = canvas.offset().top;
    var self = this;
    
    this.highlightNodes = {};
    this.highlightEdges = {};
    
    this.camera = [[1, 0, 0],
                   [0, 1, 0],
                   [0, 0, 1]];
    this.shapes = [];
    this.rotateCentre = [0, 0, 0];
    
    // Mouse events
    this.mouseIsDown = false;
    this.dragOffset = [0, 0];
    
    canvas.bind('mousedown', mouseDown);
    canvas.bind('mousemove', mouseMove);
    canvas.bind('mouseup', mouseUp);
    canvas.bind('mouseout', mouseUp);
    
    this.setRotateCentre = function(x, y, z) {
        for (var s in this.shapes) {
            var shape = this.shapes[s];
            
            for (var n in shape.nodes) {
                shape.nodes[n][0] -= x;
                shape.nodes[n][1] -= y;
                shape.nodes[n][2] -= z;
            }
        }
        this.rotateCentre = [x, y, z];
    };
    
    this.draw = function() {
        // Background
        context.clearRect(0, 0, WIDTH, HEIGHT);
    
        for (var s in this.shapes) {
            var shape = this.shapes[s];
            if (shape.edgeColour) {
                this.drawShapeEdges(shape, s);
            }
            if (shape.nodeColour) {
                this.drawShapeNodes(shape, s);
            }
            if (shape.text) {
                this.drawShapeText(shape, s);
            }
        }
    };
    
    // Given a node, return its (x, y) coordinate from the point of view of the camera
    this.viewFromCamera = function(node) {
        var x = node[0] * this.camera[0][0] + node[1] * this.camera[0][1] + node[2] * this.camera[0][2] + this.rotateCentre[0];
        var y = node[0] * this.camera[1][0] + node[1] * this.camera[1][1] + node[2] * this.camera[1][2] + this.rotateCentre[1];
        return [x, HEIGHT - y];
    };
    
    this.drawShapeEdges = function(shape, s) {
        var nodes = shape.nodes;
        
        for (var e in shape.edges) {
            var coord = this.viewFromCamera(nodes[shape.edges[e][0]]);
            
            if (this.highlightEdges[s + "," + e]) {
                context.strokeStyle = this.highlightEdges[s + "," + e];
                context.lineWidth = 2;
            } else {
                context.strokeStyle = shape.edgeColour;
                context.lineWidth = 1;
            }
            
            context.beginPath();
            context.moveTo(coord[0], coord[1]);
            coord = this.viewFromCamera(nodes[shape.edges[e][1]]);
            context.lineTo(coord[0], coord[1]);
            context.stroke();
        }
    };
    
    this.drawShapeNodes = function(shape, s) {
        var radius = 4;
        for (var n in shape.nodes) {
            var coord = this.viewFromCamera(shape.nodes[n]);
            context.fillStyle = this.highlightNodes[s + "," + n] || shape.nodeColour;
            
            context.beginPath();
            context.arc(coord[0], coord[1], radius, 0 , 2 * Math.PI, false);
            context.fill();
        }
    };
    
    this.drawShapeText = function(shape, s) {
        context.fillStyle = "#222";
        
        for (var n in shape.nodes) {
            var coord = this.viewFromCamera(shape.nodes[n]);
            context.textBaseline = 'middle';
            context.fillText(shape.text[n], coord[0], coord[1]);
        }
    };

    // Multiply camera matrix by 3x3 transform matrix, T
    this.cameraTransform = function(T) {
        var newMatrix = [];
        
        for (var row in T) {
            var t = T[row];
            var newRow = [];
            newRow.push(t[0] * this.camera[0][0] + t[1] * this.camera[1][0] + t[2] * this.camera[2][0]);
            newRow.push(t[0] * this.camera[0][1] + t[1] * this.camera[1][1] + t[2] * this.camera[2][1]);
            newRow.push(t[0] * this.camera[0][2] + t[1] * this.camera[1][2] + t[2] * this.camera[2][2]);
            newMatrix.push(newRow);
        }
        return newMatrix;
    };
    
    this.rotateX = function(theta) {
        var c = Math.cos(theta);
        var s = Math.sin(theta);
        var T = [
            [1, 0,  0],
            [0, c, -s],
            [0, s,  c]];
        
        this.camera = this.cameraTransform(T);
        this.draw();
    };
    
    this.rotateY = function(theta) {
        var c = Math.cos(theta);
        var s = Math.sin(theta);
        var T = [
            [ c, 0, s],
            [ 0, 1, 0],
            [-s, 0, c]];
        
        this.camera = this.cameraTransform(T);
        this.draw();
    };
    
    function mouseDown(evt){
        self.mouseIsDown = true;
        self.dragOffset = [evt.pageX - CANVAS_X, evt.pageY - CANVAS_Y];
    }
    
    function mouseMove(evt){
        if (self.mouseIsDown) {
            var x = evt.pageX - CANVAS_X;
            var y = evt.pageY - CANVAS_Y;
            var dx = 0.01 * (x - self.dragOffset[0]);
            var dy = 0.01 * (y - self.dragOffset[1]);
            
            self.rotateY(-dx);
            self.rotateX(dy);
            self.dragOffset = [x, y];
        }
    }
    
    function mouseUp(evt){
        self.mouseIsDown = false;
    }
}