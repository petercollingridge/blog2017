var svg_parameters = {
    width: 700,
    height: 300
};

var sequences = [
    {
        x: 30,
        y: 20,
        sequence: 'tacgtgacttagacgtccgcgacgtttttt',
        strand: 'both'
    }
];

var complement = {'a': 't', 't': 'a', 'c': 'g', 'g': 'c'};

var text_style = 'style="fill:#fff;font-family:sans;text-anchor:middle;font-size:16px;"';
var defs = [
    '\n  <def>',
    '\n    <g class="base" id="a">',
    '\n      <path fill="#c0504d" d="m0 66 h16 v-24 l-8 -8 -8 8z"/>',
    '\n      <text ' + text_style + ' x="8" y="62">A</text>',
    '\n    </g>',
    '\n    <g class="base" id="a2">',
    '\n      <path fill="#c0504d" d="m0 8 h16 v24 l-8 8 -8 -8z"/>',
    '\n      <text ' + text_style + ' x="8" y="24">A</text>',
    '\n    </g>',
    '\n    <g class="base" id="t">',
    '\n      <path fill="#f79646" d="m0 66 h16 v-32 l-8 8 -8 -8z"/>',
    '\n      <text ' + text_style + ' x="8" y="62">T</text>',
    '\n    </g>',
    '\n    <g class="base" id="t2">',
    '\n      <path fill="#f79646" d="m0 8 h16 v32 l-8 -8 -8 8z"/>',
    '\n      <text ' + text_style + ' x="8" y="24">T</text>',
    '\n    </g>',
    '\n    <g class="base" id="g">',
    '\n      <path fill="#4bacc6" d="m0 66 h16 v-16 l-16 -16z"/>',
    '\n      <text ' + text_style + ' x="8" y="62">G</text>',
    '\n    </g>',
    '\n    <g class="base" id="g2">',
    '\n      <path fill="#4bacc6" d="m0 8 h16 v32 l-16 -16z"/>',
    '\n      <text ' + text_style + ' x="8" y="24">G</text>',
    '\n    </g>',
    '\n    <g class="base" id="c">',
    '\n      <path fill="#9bbb59" d="m0 66 h16 v-24 l-16 -16z"/>',
    '\n      <text ' + text_style + ' x="8" y="62">C</text>',
    '\n    </g>',
    '\n    <g class="base" id="c2">',
    '\n      <path fill="#9bbb59" d="m0 8 h16 v40 l-16 -16z"/>',
    '\n      <text ' + text_style + ' x="8" y="24">C</text>',
    '\n    </g>',
    '\n  </def>'
];
def_string = defs.join("");

var drawSVG = function() {
    var svg_string = '<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"';
    svg_string += ' width="' + svg_parameters.width + '"';
    svg_string += ' height="' + svg_parameters.height + '">';

    svg_string += '\n  <style>';
    svg_string += '\n    rect {\n    \tfill: #aaa;\n    }';
    /*svg_string += '\n    text {\n    \tfont-family: Calibri;\n    }';
    svg_string += '\n    .base {\n    \tfont-size: 16px;\n    \ttext-anchor: middle;\n    \tfill: #fff;\n    }';
    svg_string += '\n    .label {\n    \tfont-size: 24px;\n    \tfill: #3f3f3f;\n    }';
    svg_string += '\n    .prime {\n    \ttext-anchor: middle;\n    }';*/
    svg_string += '\n  </style>';

    svg_string += def_string;

    for (var i=0; i<sequences.length; i++) {
        var sequence = sequences[i].sequence.toLowerCase();
        var x = parseInt(sequences[i].x, 10) || 0;
        var y = parseInt(sequences[i].y, 10) || 0;
        var strand = sequences[i].strand;

        // Bases
        var bx = x + 4;
        for (var j=0; j<sequence.length; j++) {
            var base = sequence[j] ;
            if (complement[base]) {
                if (strand === 'both' || strand === 'top') {
                    svg_string += '\n  <use x="' + bx + '" y="' + y + '" xlink:href="#' + base + '2"/>';
                }
                if (strand === 'both' || strand === 'bottom') {
                    svg_string += '\n  <use x="' + bx + '" y="' + y + '" xlink:href="#' + complement[base] + '"/>';
                }
                bx += 20;
            }
            if (base === 'n') { bx += 20; }
        }

        // Backbone
        var width = bx - x;
        if (width > 4) {
            if (strand === 'both' || strand === 'top') {
                svg_string += '\n  <rect x="' + x + '" y="' + y + '" width="' + width + '" height="8"/>';
            }
            if (strand === 'both' || strand === 'bottom') {
                svg_string += '\n  <rect x="' + x + '" y="' + (y+66) + '" width="' + width + '" height="8"/>';
            }
        }
        
    }

    svg_string += '\n</svg>';

    var $svg_wrapper = $('#dna-svg');
    var $svg = $('<div>' + svg_string + '</div>');
    $svg_wrapper.empty();
    $svg_wrapper.append($svg);
    $('#svg-string').val(svg_string);
};

var addSequence = function()  {
    var n = sequences.length;

    // Add data
    var old_sequence = sequences[n - 1];
    var x = old_sequence.x;
    var y = parseInt(old_sequence.y, 10) + 120;

    sequences.push({
        x: x,
        y: y,
        sequence: '',
        strand: 'both'
    });

    var $sequence = $('<div id="sequence' + n + '" class="sequence">');

    $sequence.append($('<div class="sequence-header">Sequence ' + (n+1) + '</div>'));

    var position = '<div class="sequence-parameter"> Position: (';
    position += '<input id="dna-' + n + '-x" class="small-input" value="' + x + '" maxlength="4">, ';
    position += '<input id="dna-' + n + '-y" class="small-input" value="' + y + '" maxlength="4">)</div>';

    $sequence.append($(position));
    $sequence.append($('<div class="sequence-parameter">Sequence: <input class="dna-input" id="dna-' + n + '-sequence"></div>'));

    var drop_down = '<form class="sequence-parameter" action="">Strands:';
    drop_down += '<select id="dna-' + n + '-strand">';
    drop_down += '<option value="both">Both</option>';
    drop_down += '<option value="top">Top</option>';
    drop_down += '<option value="bottom">Bottom</option>';
    drop_down += '</select></form>';

    $sequence.append($(drop_down));
    $('#sequences').append($sequence);
    
    $('input').keyup(updateParameter);
    $('select').change(updateParameter);
};

var updateParameter = function(evt) {
    var element = $(evt.target);
    var value = element.val();

    var param = element.attr('id').split('-');

    if (param[0] === 'svg') {
        value = parseInt(value, 10);
        if (!isNaN(value)) {
            svg_parameters[param[1]] = Math.max(value, 100);
        }
    } else if (param[0] === 'dna') {
        var sequence = sequences[parseInt(param[1], 10)];
        sequence[param[2]] = value;
    }

    drawSVG();
};

$(document).ready(function() {
    $('#add-sequence').on('click', addSequence);
    $('input').keyup(updateParameter);
    $('select').change(updateParameter);
    drawSVG();
});