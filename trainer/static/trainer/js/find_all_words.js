

(function() {
var word_letter_source = document.getElementById('word_letter_source');
var sourceSortable = new Sortable(word_letter_source, { group:'word_letter', });
var word_letter_destination = document.getElementById('word_letter_destination');
var destinationSortable = new Sortable(word_letter_destination, { 
    group:'word_letter', 
    onStart: function (/**Event*/evt) {
        evt.oldIndex;  // element index within parent
        
        // Clear span saying "Drop tiles here..." if it is present
        $("#word_letter_destination_text").remove();
        },
    onAdd: function (/**Event*/evt) {
        var itemEl = evt.item;  // dragged HTMLElement
        evt.from;  // previous list
        // + indexes from onEnd
        
        // Clear span saying "Drop tiles here..." if it is present
        $("#word_letter_destination_text").remove();
        }
    });
var findAllWords = findAllWords_temp;
// word_matches_guessed is like word_matches, except starts blank and filled in as user guesses them
findAllWords.word_matches_guessed = [];
for (var i=0; i<findAllWords.word_matches.length; i++) {
    var temp_element = {};
    temp_element['letter_count'] = findAllWords.word_matches[i]['letter_count'];
    temp_element['words'] = [];
    findAllWords.word_matches_guessed.push(temp_element);
    }


function textModeClick() {
    // Change "Text Mode" link to "Tile Mode", to enable toggling back
    $("#word_letter_button_controls").html(
        '\
        <li><a href="#" role="button" id="word_letter_button_tile_mode">Tile Mode</a></li>\
        <li><a href="#" role="button" id="word_letter_button_shuffle">Shuffle Tiles</a></li>\
        <li><a href="#" role="button" id="word_letter_button_reset">Reset Tiles</a></li>\
        '
        );
    
    // Make sure all relevant functions are reactivated
    $("#word_letter_button_tile_mode").click(function() {
        tileModeClick();
        });
    $("#word_letter_button_reset").click(function() {
        resetWordLetterSource(text_mode=true, reset_click=true);
        });
    $("#word_letter_button_shuffle").click(function() {
        shuffleTiles(text_mode=true);
        });

    // Reset letters in source area
    resetWordLetterSource(text_mode=false, reset_click=false);

    // Put text box into destination area
    $("#word_letter_destination").html(
        '<input id="word_letter_submit_input" class="word_letter_large_font" type="text" maxlength="' 
        + findAllWords.letter_count 
        + '" placeholder="ENTER to submit"></input>'
        );
    $("#word_letter_submit_input").bind("keypress", {}, keypressWordLetterSubmit);
    
    // Focus cursor in text box
    $("#word_letter_submit_input").focus();
    
    // Disable ability to drag letters to destination area
    destinationSortable.option("disabled", true);
    
    
    }


function tileModeClick() {
    $("#word_letter_button_controls").html(
        '\
        <li><a href="#" role="button" id="word_letter_button_text_mode">Text Mode</a></li>\
        <li><a href="#" role="button" id="word_letter_button_shuffle">Shuffle Tiles</a></li>\
        <li><a href="#" role="button" id="word_letter_button_reset">Reset Tiles</a></li>\
        '
        );
    
    // Make sure all relevant functions are reactivated
    $("#word_letter_button_text_mode").click(function() {
        textModeClick();
        });
    $("#word_letter_button_text_mode").click(function() {
        textModeClick();
        });
    $("#word_letter_button_reset").click(function() {
        resetWordLetterSource(text_mode=false, reset_click=true);
        });
    $("#word_letter_button_shuffle").click(function() {
        shuffleTiles(text_mode=false);
        });

    // Reset letters in source area
    resetWordLetterSource(text_mode=false, reset_click=false);
    
    // Remove text box in destination area
    $("#word_letter_destination").html('');
    
    // Enable ability to drag letters to destination area
    destinationSortable.option("disabled", false);

    }


function resetWordLetterSource(text_mode, reset_click) {
    
    if (text_mode == true) {
        $("#word_letter_destination").html(
            '<input id="word_letter_submit_input" class="word_letter_large_font" type="text" maxlength="' 
            + findAllWords.letter_count 
            + '" placeholder="ENTER to submit"></input>'
            );
        $("#word_letter_submit_input").bind("keypress", {}, keypressWordLetterSubmit);
        
        // Focus cursor in text box
        $("#word_letter_submit_input").focus();
        }
    else {
        $("#word_letter_destination").html('');
        }
        
    if (reset_click == true || text_mode == false) { 
        // IF tile mode only, reset tiles in source div
        var word_letter_source_html = '';
        for (var i=0; i < findAllWords.search_input.length; i++) {
            word_letter_source_html += ('<div class="force_pointer word_letter_frame_1" unselectable="on" >'
                + findAllWords.search_input[i]
                + '</div>');
            }
        $("#word_letter_source").html(word_letter_source_html);
        }
    }


function shuffleTiles(text_mode) {
    var word_letter_source_html = '';
    var temp_search_input = findAllWords.search_input.slice();
    temp_search_input = shuffle(temp_search_input);
    for (var i=0; i < temp_search_input.length; i++) {
        word_letter_source_html += ('<div class="force_pointer word_letter_frame_1" unselectable="on" >'
            + temp_search_input[i]
            + '</div>');
        }
    if (text_mode == true) {
        $("#word_letter_destination").html(
            '<input id="word_letter_submit_input" class="word_letter_large_font" type="text" maxlength="' 
            + findAllWords.letter_count 
            + '" placeholder="ENTER to submit"></input>'
            );
        $("#word_letter_submit_input").bind("keypress", {}, keypressWordLetterSubmit);
        
        // Focus cursor in text box
        $("#word_letter_submit_input").focus();
        }
    else {
        $("#word_letter_destination").html('');
        }
    $("#word_letter_source").html(word_letter_source_html);
    }




function keypressWordLetterSubmit(e) {
    // If user presses enter while typing in word_letter_submit_input text box, submit word
    // See http://stackoverflow.com/questions/10905345/pressing-enter-on-a-input-type-text-how
    var code = (e.keyCode ? e.keyCode : e.which);
    if (code == 13) { //Enter keycode                        
        e.preventDefault();
        submitWord();
    }
};


function submitWord() {
    var user_word = $("#word_letter_destination").text();
    var text_mode = false;
    // If user is typing the word instead of using blocks, need to get it a different way
    if (document.getElementById('word_letter_submit_input')) {
        text_mode = true;
        var user_word = $("#word_letter_submit_input").val();
        user_word = user_word.toUpperCase().replace(/[^A-Z]/g,""); 
        }
    if (user_word != '') {
        checkAndUpdateUserWord(user_word);
        }
    
    // Clear #word_letter_destination
    resetWordLetterSource(text_mode, reset_click=false);
    
    
    }


function checkAndUpdateUserWord(user_word) {
    var user_word_valid = false;
    var update_point_count = true;
    var temp_letter_count = user_word.length;
    for (var i=0; i < findAllWords.word_matches.length; i++) {
        if (findAllWords.word_matches[i]['letter_count'] == temp_letter_count) {
            if (findAllWords.word_matches[i]['words'].indexOf(user_word) != -1) {
                user_word_valid = true;
                if (findAllWords.word_matches_guessed[i]['words'].indexOf(user_word) == -1) {
                    addWordMatchGuessed(user_word);   // Update list of words guessed if this word not already there
                    }
                else {  // neither reward or penalize if player guesses word they already guessed
                    update_point_count = false;
                    }
                }
            }
        }
    // Update scoring total
    if (user_word_valid == true && user_word.length == 7) {
        var long_word = true;
        }
    else {
        var long_word = false;
        }
    updatePointCount(user_word_valid, update_point_count, long_word);
    }
    

function addWordMatchGuessed(user_word) {
    var temp_letter_count = user_word.length;
    for (var i=0; i < findAllWords.word_matches_guessed.length; i++) {
        if (findAllWords.word_matches_guessed[i]['letter_count'] == temp_letter_count) {
            if (findAllWords.word_matches_guessed[i]['words'].indexOf(user_word) == -1) {
                findAllWords.word_matches_guessed[i]['words'].push(user_word);
                findAllWords.word_matches_guessed[i]['words'].sort();
                var word_match_letter_text = '';
                for (var j=0; j<findAllWords.word_matches_guessed[i]['words'].length; j++) {
                    if (findAllWords.word_matches_guessed[i]['words'][j] == user_word) {
                        word_match_letter_text += '<span class="word_match_correct">' + findAllWords.word_matches_guessed[i]['words'][j] + '</span>';
                        }
                    else {
                        word_match_letter_text += findAllWords.word_matches_guessed[i]['words'][j];
                        }
                    // don't add comma if approaching end
                    if (j < findAllWords.word_matches_guessed[i]['words'].length - 1) {
                        word_match_letter_text += ', ';
                        }
                    
                    }
                $("#word_match_letter_" + temp_letter_count).html(word_match_letter_text);
                }
            }
        
        else {
            var word_match_letter_text = '';
            var word_match_letter_count = findAllWords.word_matches_guessed[i]['letter_count'];
            for (var j=0; j<findAllWords.word_matches_guessed[i]['words'].length; j++) {
                word_match_letter_text += findAllWords.word_matches_guessed[i]['words'][j];
                // don't add comma if approaching end
                if (j < findAllWords.word_matches_guessed[i]['words'].length - 1) {
                    word_match_letter_text += ', ';
                    }
                }
            $("#word_match_letter_" + word_match_letter_count).html(word_match_letter_text);
            }
        
        }
    }
    

function updatePointCount(user_word_valid, update_point_count, long_word) {
    if (update_point_count == false) {
        findAllWords.total_point_count += 0;
        }
    else if (user_word_valid == true && long_word == true) {
        findAllWords.total_point_count += 10;
        }
    else if (user_word_valid == true && long_word == false) {
        findAllWords.total_point_count += 3;
        }
    else {
        findAllWords.total_point_count -= 1;
        }
    $("#word_letter_point_count").text(findAllWords.total_point_count);
    }


function buildFinalWordList(all_guessed_words) {
    // Show all words. Red and bold if not in all_guessed_words.
    var word_matches_guessed_list = '';
        

    for (var i=0; i < findAllWords.word_matches.length; i++) {
        var temp_letter_count = findAllWords.word_matches[i]['letter_count'];
        word_matches_guessed_list += (
            '<li><strong>' 
            + temp_letter_count
            + ' Letters:</strong> '
            );
        for (var j=0; j < findAllWords.word_matches[i]['words'].length; j++) {
            var temp_word = findAllWords.word_matches[i]['words'][j]; 
            // Red if not guessed, normal if otherwise
            if (all_guessed_words.indexOf(temp_word) == -1) {
                word_matches_guessed_list += '<span class="word_match_missed">' + temp_word + '</span>';
                }
            else  {
                word_matches_guessed_list += temp_word;
                } 
            // If last word in loop, don't put a comma after it
            if (j < findAllWords.word_matches[i]['words'].length - 1) {
                word_matches_guessed_list += ', ';
                }
            }
        word_matches_guessed_list += '</li>';
        }
    $("#word_matches_guessed_list").html(word_matches_guessed_list);
    
    }


$("#word_letter_submit").click(function() {
    submitWord();
    });


$("#word_letter_destination_text").click(function() {
    textModeClick();
    });
$("#word_letter_button_text_mode").click(function() {
    textModeClick();
    });
    

$("#word_letter_button_tile_mode").click(function() {
    tileModeClick();
    });


$("#word_letter_button_reset").click(function() {
    resetWordLetterSource(text_mode=false, reset_click=true);
    });
    

$("#word_letter_button_shuffle").click(function() {
    shuffleTiles();
    });

$("#final_score_button").click(function() {
    $("#word_letter_buttons_1").remove();
    $("#word_letter_buttons_2").remove();
    $("#word_letter_destination").remove();
    var total_possible_points = (findAllWords.total_word_count * 3);
    var missed_word_count = 0;
    var all_guessed_words = [];
    for (var i=0; i<findAllWords.word_matches_guessed.length ; i++) {
        all_guessed_words = all_guessed_words.concat(findAllWords.word_matches_guessed[i]['words']);
        }
    var all_non_guessed_words = [];
    // Add 7 to possible points for each 7 letter word, since those worth 10
    for (var i=0; i<all_guessed_words.length; i++) {
        if (all_guessed_words[i].length == 7) {
            total_possible_points += 7;
            }
        }
    for (var i=0; i<all_non_guessed_words.length; i++) {
        if (all_guessed_words[i].length == 7) {
            total_possible_points += 7;
            }
        }
        
    
    for (var i=0; i<findAllWords.word_matches.length; i++) {
        for (var j=0; j<findAllWords.word_matches[i]['words'].length; j++) {
            var temp_word = findAllWords.word_matches[i]['words'][j];
            if (all_guessed_words.indexOf(temp_word) == -1) {
                all_non_guessed_words.push(temp_word);
                }
            }
        }
    var total_word_count = all_guessed_words.length + all_non_guessed_words.length;
    findAllWords.total_point_count += (all_non_guessed_words.length * -1);
    var updated_text = ('<p class="lead">Your final score was <strong>' 
        + findAllWords.total_point_count 
        + '</strong>, out of a possible ' 
        + total_possible_points
        + ' points.</p><p>You guessed '
        + all_guessed_words.length
        + ' out of '
        + total_word_count
        + ' possible words.</p><p>Any words you missed are highlighted in red below. Click <strong><a href="">here</a></strong> to try again.</p>'
        );
    $("#word_letter_intro").html(updated_text);
    $("#word_letter_point_count").text(findAllWords.total_point_count);
    buildFinalWordList(all_guessed_words);
    });


}) ();



function shuffle(array) {
  var m = array.length, t, i;

  // While there remain elements to shuffle…
  while (m) {

    // Pick a remaining element…
    i = Math.floor(Math.random() * m--);

    // And swap it with the current element.
    t = array[m];
    array[m] = array[i];
    array[i] = t;
  }

  return array;
}