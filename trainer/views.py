from django.shortcuts import render
from django.db import connection
from django.db.models.functions import Length
from trainer import forms, models, utils
import random


def home(request):
    search_input_form = forms.SearchInputForm()
    context = {
        'search_input_form': search_input_form
        }
    return render(request, 'trainer/home.html', context)
    
    
def word_lists(request):
    return render(request, 'trainer/word_lists.html', {})
    

def get_matching_words(request):
    search_input = request.GET.get('search_input', '')
    word_matches = None
    if search_input != '':
        search_input = utils.clean_search_input(search_input)
        word_matches = utils.get_matching_words(search_input)
    search_input_form = forms.SearchInputForm()
    context = {
        'search_input': search_input,
        'word_matches': word_matches,
        'search_input_form': search_input_form,
        }
    return render(request, 'trainer/get_matching_words.html', context)
    

def n_letter_words(request, n):
    n = int(n)
    word_matches, word_matches_end = utils.get_n_letter_words(n)
    context = {
        'n': n,
        'word_matches': word_matches,
        'word_matches_end': word_matches_end,
        }
    return render(request, 'trainer/n_letter_words.html', context)
    
    
def n_letter_word_stems(request, n):
    n = int(n)
    word_stems = utils.get_word_stems(stem_length=n, top_n=100)
    for i in range(0, len(word_stems)):
        word_stems[i].get_word_stem_words()
    context = {
        'n': n,
        'word_stems': word_stems,
        }
    return render(request, 'trainer/n_letter_word_stems.html', context)
    

def n_letter_word_fragments(request, n):
    n = int(n)
    word_fragments = utils.get_word_fragments(fragment_length=n, top_n=100)
    for i in range(0, len(word_fragments)):
        word_fragments[i].get_word_fragment_words()
    context = {
        'n': n,
        'word_fragments': word_fragments,
        }
    return render(request, 'trainer/n_letter_word_fragments.html', context)
    
    
def get_prefix_suffix_list(request):
    search_input = request.GET.get('search_input', '')
    if search_input != '':
        search_input = search_input.upper()
    
    search_input_form = forms.SearchInputFormPrefixSuffix()
    
    try:
        word = models.Word.objects.get(word=search_input)
    except:
        word = None
    word_prefix_suffix_list = utils.get_word_prefix_suffix_list(word)
    context = {
        'search_input_form': search_input_form,
        'search_input': search_input,
        'word': word,
        'word_prefix_suffix_list': word_prefix_suffix_list,
        }
    return render(request, 'trainer/get_prefix_suffix_list.html', context)


def olaughlin_words(request):
    word_matches = utils.get_olaughlin_words_extended()
    context = {
        'word_matches': word_matches,
        }
    return render(request, 'trainer/olaughlin_words.html', context)


def vowel_consonant_heavy_words(request):
    if 'vowel' in request.get_full_path():
        display_type = 'vowel'
        word_vowel_consonant_heavy = utils.get_word_vowel_consonant_heavy(display_type)
    else:
        display_type = 'consonant'
        word_vowel_consonant_heavy = utils.get_word_vowel_consonant_heavy(display_type)
    context = {
        'display_type': display_type,
        'word_vowel_consonant_heavy': word_vowel_consonant_heavy,
        }
    return render(request, 'trainer/vowel_consonant_heavy_words.html', context)
    

def jqxz_words(request):
    word_matches = utils.get_jqxz_words()
    context = {
        'word_matches': word_matches,
        }
    return render(request, 'trainer/jqxz_words.html', context)
    

def q_without_u_words(request):
    word_matches = utils.get_q_without_u_words()
    context = {
        'word_matches': word_matches,
        }
    return render(request, 'trainer/q_without_u_words.html', context)



##### TOOLS ####
def tools_home(request):
    '''
    Go to homepage of Tools, with links to specific tools
    '''
    return render(request, 'trainer/tools/home.html', {})


def tools_find_all_words(request):
    '''
    This will provide user with a rack of letters. Their goal is to find as many valid words as possible.
    '''
    # Check for user options / use defaults
    letter_count = int(request.GET.get('letter_count', 4)) # check format of POST vars
    check = request.GET.get('require_jqxz')
    require_jqxz = True if check == 'on' else False
    check = request.GET.get('require_n_letter_word', False)
    require_n_letter_word = True if check == 'on' else True

    options_form = forms.FindAllWordsOptions({
        'letter_count': letter_count,
        'require_jqxz': require_jqxz,
        'require_n_letter_word': require_n_letter_word,
        })

    # Pull random letters until at least 1 word is possible. 
    # Vast majority of time, this loop will resolve on first attempt. But a few letter combinations cannot make even 1 word.
    total_word_count = 0
    while total_word_count == 0:
        search_input = utils.generate_search_input(letter_count, require_jqxz, require_n_letter_word)
        word_matches = utils.get_matching_words(search_input)
        total_word_count = utils.get_total_word_count_from_word_matches(word_matches)
    search_input = list(search_input)

    context = {
        'letter_count': letter_count,
        'letter_count_loop': range(letter_count, 1, -1),
        'require_jqxz': require_jqxz,
        'require_n_letter_word': require_n_letter_word,
        'options_form': options_form,
        'search_input': search_input,
        'word_matches': word_matches,
        'total_word_count': total_word_count,
        }
    return render(request, 'trainer/tools/find_all_words.html', context)


def tools_is_this_a_word(request):
    # Will show something that may/may not be a word to the user, they must choose
    # We should show a real word 1/2 the time, a fake word 1/2 the time
    if random.random() < 0.5:
        is_real_word = True
        word = models.Word.objects.annotate(word_length=Length('word')).filter(word_length__lte=8).order_by('?')[0]
        word = word.word
        context = {
            'is_real_word': is_real_word,
            'word': word,            
            }
    else:
        is_real_word = False
        word = models.Word.objects.annotate(word_length=Length('word')).filter(word_length__lte=8).order_by('?')[0]
        word = word.word
        word = utils.create_fake_word_from_word(word)
        context = {
            'is_real_word': is_real_word,
            'word': word,            
            }
    
    # If there was an answer last turn (will be POST), process it.
    previous_word = request.GET.get('word')
    previous_guess = request.GET.get('guess')
    if previous_word:
        previous_is_correct = utils.check_previous_guess(previous_word, previous_guess)
        context['previous_word'] = previous_word
        context['previous_guess'] = previous_guess
        context['previous_is_correct'] = previous_is_correct
    
    return render(request, 'trainer/tools/is_this_a_word.html', context)
        
    
def tools_words_by_length_and_stem(request):
    '''
    Take a word-length between 2-7 letters and test users.
    Will provide stem, like "All 7-letter words ending in AYERS"
    '''
    word_length = int(request.GET.get('word_length', random.randint(2,7)))
    stem_type = 'beginning' if random.random() < 0.5 else 'ending'
        
    # Build a search query to get a random word stem, get all words with similar stem, given stem_type
    stem_length = utils.get_stem_length(word_length)
    word_stem = utils.get_word_stem(word_length, stem_type, stem_length)
    search_query = utils.build_search_query_by_stem(stem_type)
    
    if stem_type == 'beginning':
        word_stem_string = word_stem + '%'
    else:
        word_stem_string = '%' + word_stem
    
    cursor = connection.cursor()
    cursor.execute(search_query, [word_length, word_stem_string,])
    results = cursor.fetchone()
    word_matches = results[0]
    
    # Other params to pass
    total_word_count = len(word_matches)
    letters_to_enter = word_length - len(word_stem)
    
    options_form = forms.WordStemLengthOptions({'word_length': word_length,})
    
    context = {
        'word_length': word_length,
        'stem_type': stem_type,
        'word_stem': word_stem,
        'word_matches': word_matches,
        'letters_to_enter': letters_to_enter,
        'total_word_count': total_word_count,
        'options_form': options_form,
        }
    return render(request, 'trainer/tools/words_by_length_and_stem.html', context)


def tools_7_letter_words_by_stem(request):
    '''
    Get a 6-letter stem that can make 10 or more 7-letter words. Display it and append a _ tile at end.
    '''
    word_stem, word_matches = utils.get_word_stem_and_word_matches()
    total_word_count = len(word_matches)
    
    context = {
        'word_stem': word_stem,
        'word_matches': word_matches,
        'total_word_count': total_word_count,
        }
    return render(request, 'trainer/tools/7_letter_words_by_stem.html', context)
    

def tools_vowel_heavy_words(request):
    '''
    Vowel-heavy words for user to guess (5 letters, no more than 1 consonant)
    '''
    search_query = """
        select
          array_agg(w.word order by w.word)
        from
          trainer_word_vowel_consonant_heavy ch
          inner join trainer_word w on w.id = ch.word_id
        where 
          vowel_heavy_flg = true
          and length(word) between 5 and 7
          and length(regexp_replace(word, '[AEIOU]', '', 'g')) <= 1  -- no more than 1 consonant
        """
    cursor = connection.cursor()
    cursor.execute(search_query, [])
    result = cursor.fetchone()
    word_matches = result[0]
    total_word_count = len(word_matches)
    context = {
        'word_matches': word_matches,
        'total_word_count': total_word_count,
        }
    return render(request, 'trainer/tools/vowel_heavy_words.html', context)


def tools_2_letter_words(request):
    '''
    Return all 2-letter words
    '''
    search_query = """
        select
          array_agg(word order by word)
        from
          trainer_word
        where 
          length(word) = 2
        """
    cursor = connection.cursor()
    cursor.execute(search_query, [])
    result = cursor.fetchone()
    word_matches = result[0]
    total_word_count = len(word_matches)
    context = {
        'word_matches': word_matches,
        'total_word_count': total_word_count,
        }
    return render(request, 'trainer/tools/2_letter_words.html', context)


def tools_olaughlin_words(request):
    '''
    Return top 20 O'Laughlin Replacement scores for words between 2-7 letters.
    '''
    word_matches = utils.get_olaughlin_words()
    total_word_count = utils.get_total_word_count_from_word_matches(word_matches)
    context = {
        'word_matches': word_matches,
        'total_word_count': total_word_count,
        }
    return render(request, 'trainer/tools/olaughlin_words.html', context)


##### EXTERNAL RESOURCES #####
def external_resources(request):
    return render(request, 'trainer/external_resources.html', {})


##### ARTICLES #####
### Route any article page hit to the right article template
def article(request):
    full_uri = request.get_full_path()
    template_name = utils.get_article_template_from_uri(full_uri)
    return render(request, template_name, {})