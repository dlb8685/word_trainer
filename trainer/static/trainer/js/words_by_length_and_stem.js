

(function () {

var wordsByLengthStem = wordsByLengthStem_temp;
wordsByLengthStem.word_matches_guessed = [];


// Focus cursor in text box
$("#word_letter_submit_input").focus();
// Button Functions
$("#word_letter_submit_input").bind("keypress", {}, keypressWordLetterSubmit);
$("#word_letter_submit").click(function() {submitWord();});
$("#final_score_button").click(function() {
    $("#word_letter_buttons_1").remove();
    $("#word_letter_buttons_2").remove();
    $("#word_letter_destination").remove();
    buildFinalWordList();
    var total_possible_points = (wordsByLengthStem.total_word_count * 3);
    var all_non_guessed_words = [];
    for (var i=0; i<wordsByLengthStem.word_matches.length; i++) {
        var temp_word = wordsByLengthStem.word_matches[i];
        if (wordsByLengthStem.word_matches_guessed.indexOf(temp_word) == -1) {
            all_non_guessed_words.push(temp_word);
            }
        }
    wordsByLengthStem.total_point_count += (all_non_guessed_words.length * -1);
    var updated_text = ('<p class="lead">Your final score was <strong>' 
        + wordsByLengthStem.total_point_count 
        + '</strong>, out of a possible ' 
        + total_possible_points
        + ' points.</p><p>You guessed '
        + wordsByLengthStem.word_matches_guessed.length
        + ' out of '
        + wordsByLengthStem.total_word_count
        + ' possible words.</p><p>Any words you missed are highlighted in red below. Click <strong><a href="">here</a></strong> to try again.</p>'
        );
    $("#word_letter_intro").html(updated_text);
    $("#word_letter_point_count").text(wordsByLengthStem.total_point_count);
    });


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
    var user_word = $("#word_letter_submit_input").val();
    user_word = user_word.toUpperCase().replace(/[^A-Z]/g,""); 
    
    if (wordsByLengthStem.stem_type == 'beginning') {
        user_word = wordsByLengthStem.word_stem + user_word;
        }
    else {
        user_word = user_word + wordsByLengthStem.word_stem;
        }
    
    if (user_word != wordsByLengthStem.word_stem) {
        checkAndUpdateUserWord(user_word);
        }
    
    // Clear #word_letter_destination
    resetWordLetterSource();
    
    
    }


function resetWordLetterSource() {
    // Clear anything that has been entered
    $("#word_letter_submit_input").val('');
    // Focus cursor in text box
    $("#word_letter_submit_input").focus();
    }
    
    
function checkAndUpdateUserWord(user_word) {
    var user_word_valid = false;
    var update_point_count = true;
    if (wordsByLengthStem.word_matches.indexOf(user_word) != -1) {
        user_word_valid = true;
        if (wordsByLengthStem.word_matches_guessed.indexOf(user_word) == -1) {
            wordsByLengthStem.word_matches_guessed.push(user_word);
            wordsByLengthStem.word_matches_guessed.sort();
            
            addWordMatchGuessed(user_word);
            }
        else {
            update_point_count = false;
            }
        }
    
    if (update_point_count == true) {
        updatePointCount(user_word_valid);
        
        }    
    }


function updatePointCount(user_word_valid) {
    if (user_word_valid == true) {
        wordsByLengthStem.total_point_count += 3;
        }
    else {
        wordsByLengthStem.total_point_count -= 1;
        }
    
    $("#word_letter_point_count").html(wordsByLengthStem.total_point_count);
    }
    

function addWordMatchGuessed(user_word) {
    var word_match_letter_text = '';
    for (var i=0; i < wordsByLengthStem.word_matches_guessed.length; i++) {
        if (wordsByLengthStem.word_matches_guessed[i] == user_word) {
            word_match_letter_text += '<span class="word_match_correct">' + wordsByLengthStem.word_matches_guessed[i] + '</span>';
            }
        else {
            word_match_letter_text += wordsByLengthStem.word_matches_guessed[i];
            }
        
        if (i < wordsByLengthStem.word_matches_guessed.length - 1) {
            word_match_letter_text += ', ';
            }
        }
    $("#word_match_by_length_and_stem").html(word_match_letter_text);
    }


function buildFinalWordList() {
    // Show all words. Red and bold if not in all_guessed_words.
    var word_matches_guessed_list = '';
    for (var i=0; i < wordsByLengthStem.word_matches.length; i++) {
        var temp_word = wordsByLengthStem.word_matches[i];
        // Red if not guessed, normal if otherwise
        if (wordsByLengthStem.word_matches_guessed.indexOf(temp_word) == -1) {
            word_matches_guessed_list += '<span class="word_match_missed">' + temp_word + '</span>';
            }
        else  {
            word_matches_guessed_list += temp_word;
            } 
        // If last word in loop, don't put a comma after it
        if (i < wordsByLengthStem.word_matches.length - 1) {
            word_matches_guessed_list += ', ';
            }
        }
    $("#word_match_by_length_and_stem").html(word_matches_guessed_list);
    
    }


}) ();