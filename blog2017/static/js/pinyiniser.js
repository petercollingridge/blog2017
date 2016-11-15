pinyin_tonemarks = {
    a: ['a', 'ā', 'á', 'ǎ', 'à'],
    e: ['e', 'ē', 'é', 'ě', 'è'],
    i: ['i', 'ī', 'í', 'ǐ', 'ì'],
    o: ['o', 'ō', 'ó', 'ǒ', 'ò'],
    u: ['u', 'ū', 'ú', 'ǔ', 'ù'],
    v: ['ü', 'ǖ', 'ǘ', 'ǚ', 'ǜ'],
    ve: ['üe', 'üē', 'üé', 'üě', 'üè']
};

var re_pinyin_ue = /(ve?)([0-5])/g;
var re_pinyin_vowel = /(a[io]?|ei?|[iou])(?:n|ng)?r?([0-5])/g;

var newInput = function() {
	var input = $("#pinyiniser-input").val();
	input = input.replace(re_pinyin_ue, function($0, $1, $2) {return pinyin_tonemarks[$1][$2 % 5]; });
	input = input.replace(re_pinyin_vowel, function($0, $1, $2) { return pinyin_tonemarks[$1[0]][$2 % 5] + $0.substring(1, $0.length-1); });
    //input = escape(input);
	$('#pinyiniser-output').text(input);
};

$(document).ready(function() {
    $("#pinyiniser-input").on("keyup", function(event){
        newInput();
    });
});