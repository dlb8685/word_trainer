from trainer import models
from django.db import connection
from django.db.models.functions import Length
from cache_util import cache_util
import random, re


def clean_search_input(search_input, n=10):
    '''
    1) Search input should be limited to N characters
    2) All letters should be in upper case
    3) Only non-letter allowed is _ (meaning blank)
    4) Should be in alphabetical order (blanks last)
    Convert to uppercase, strip bad characters, strip anything after Nth character, sort, return.
    Returns string (not list, etc. etc. etc)
    '''
    search_input = search_input.upper()
    search_input = re.sub('[^A-Z_]', '', search_input)
    search_input = search_input[:n]
    search_input = ''.join(sorted(search_input))
    return search_input
    

def get_matching_words(search_input):
    '''
    Have coded logic in DB to rapidly get matching words to a given search query.
    Query should be of type string ('AAAAAA_') with only capital letters and underscores (blank).
    '''
    assert search_input == ''.join(sorted(search_input)), "search_input must be alphabetical for query to work"
    assert search_input.upper() == search_input, "search_input must be in upper case"
    assert len(search_input) >= 2, "search_input must be more than 2 characters"

    search_query = """
        drop table if exists temp_search_letters;
        create temp table temp_search_letters as
        select
          search_letters
          ,length(search_letters) as length
          ,length(regexp_replace(search_letters, '[_]', '', 'g')) as length_wo_blanks
        from
          (
          select
            %s::text as search_letters
          ) a
        ;

        drop table if exists temp_search_step_1;
        create temp table temp_search_step_1 as
        select
          word
        from
          trainer_word 
        where
          -- Sum of matches (incl. end of word automatic matches, i.e. on 3 letter word) >= number of letters on rack without blanks?
          (
            case when substring(word, 1, 1) in (
              (select substring(search_letters,1,1) from temp_search_letters),
              (select substring(search_letters,2,1) from temp_search_letters),
              (select substring(search_letters,3,1) from temp_search_letters),
              (select substring(search_letters,4,1) from temp_search_letters),
              (select substring(search_letters,5,1) from temp_search_letters),
              (select substring(search_letters,6,1) from temp_search_letters),
              (select substring(search_letters,7,1) from temp_search_letters),
              (select substring(search_letters,8,1) from temp_search_letters),
              (select substring(search_letters,9,1) from temp_search_letters),
              (select substring(search_letters,10,1) from temp_search_letters)
              ) then 1 else 0 end
            + case when substring(word, 2, 1) in (
              (select substring(search_letters,1,1) from temp_search_letters),
              (select substring(search_letters,2,1) from temp_search_letters),
              (select substring(search_letters,3,1) from temp_search_letters),
              (select substring(search_letters,4,1) from temp_search_letters),
              (select substring(search_letters,5,1) from temp_search_letters),
              (select substring(search_letters,6,1) from temp_search_letters),
              (select substring(search_letters,7,1) from temp_search_letters),
              (select substring(search_letters,8,1) from temp_search_letters),
              (select substring(search_letters,9,1) from temp_search_letters),
              (select substring(search_letters,10,1) from temp_search_letters)
              ) then 1 else 0 end
            + case when substring(word, 3, 1) in (
              (select substring(search_letters,1,1) from temp_search_letters),
              (select substring(search_letters,2,1) from temp_search_letters),
              (select substring(search_letters,3,1) from temp_search_letters),
              (select substring(search_letters,4,1) from temp_search_letters),
              (select substring(search_letters,5,1) from temp_search_letters),
              (select substring(search_letters,6,1) from temp_search_letters),
              (select substring(search_letters,7,1) from temp_search_letters),
              (select substring(search_letters,8,1) from temp_search_letters),
              (select substring(search_letters,9,1) from temp_search_letters),
              (select substring(search_letters,10,1) from temp_search_letters)
              ) or length(word) < 3 then 1 else 0 end
            + case when substring(word, 4, 1) in (
              (select substring(search_letters,1,1) from temp_search_letters),
              (select substring(search_letters,2,1) from temp_search_letters),
              (select substring(search_letters,3,1) from temp_search_letters),
              (select substring(search_letters,4,1) from temp_search_letters),
              (select substring(search_letters,5,1) from temp_search_letters),
              (select substring(search_letters,6,1) from temp_search_letters),
              (select substring(search_letters,7,1) from temp_search_letters),
              (select substring(search_letters,8,1) from temp_search_letters),
              (select substring(search_letters,9,1) from temp_search_letters),
              (select substring(search_letters,10,1) from temp_search_letters)
              ) or length(word) < 4 then 1 else 0 end
            + case when substring(word, 5, 1) in (
              (select substring(search_letters,1,1) from temp_search_letters),
              (select substring(search_letters,2,1) from temp_search_letters),
              (select substring(search_letters,3,1) from temp_search_letters),
              (select substring(search_letters,4,1) from temp_search_letters),
              (select substring(search_letters,5,1) from temp_search_letters),
              (select substring(search_letters,6,1) from temp_search_letters),
              (select substring(search_letters,7,1) from temp_search_letters),
              (select substring(search_letters,8,1) from temp_search_letters),
              (select substring(search_letters,9,1) from temp_search_letters),
              (select substring(search_letters,10,1) from temp_search_letters)
              ) or length(word) < 5 then 1 else 0 end
            + case when substring(word, 6, 1) in (
              (select substring(search_letters,1,1) from temp_search_letters),
              (select substring(search_letters,2,1) from temp_search_letters),
              (select substring(search_letters,3,1) from temp_search_letters),
              (select substring(search_letters,4,1) from temp_search_letters),
              (select substring(search_letters,5,1) from temp_search_letters),
              (select substring(search_letters,6,1) from temp_search_letters),
              (select substring(search_letters,7,1) from temp_search_letters),
              (select substring(search_letters,8,1) from temp_search_letters),
              (select substring(search_letters,9,1) from temp_search_letters),
              (select substring(search_letters,10,1) from temp_search_letters)
              ) or length(word) < 6 then 1 else 0 end
            + case when substring(word, 7, 1) in (
              (select substring(search_letters,1,1) from temp_search_letters),
              (select substring(search_letters,2,1) from temp_search_letters),
              (select substring(search_letters,3,1) from temp_search_letters),
              (select substring(search_letters,4,1) from temp_search_letters),
              (select substring(search_letters,5,1) from temp_search_letters),
              (select substring(search_letters,6,1) from temp_search_letters),
              (select substring(search_letters,7,1) from temp_search_letters),
              (select substring(search_letters,8,1) from temp_search_letters),
              (select substring(search_letters,9,1) from temp_search_letters),
              (select substring(search_letters,10,1) from temp_search_letters)
              ) or length(word) < 7 then 1 else 0 end
            + case when substring(word, 8, 1) in (
              (select substring(search_letters,1,1) from temp_search_letters),
              (select substring(search_letters,2,1) from temp_search_letters),
              (select substring(search_letters,3,1) from temp_search_letters),
              (select substring(search_letters,4,1) from temp_search_letters),
              (select substring(search_letters,5,1) from temp_search_letters),
              (select substring(search_letters,6,1) from temp_search_letters),
              (select substring(search_letters,7,1) from temp_search_letters),
              (select substring(search_letters,8,1) from temp_search_letters),
              (select substring(search_letters,9,1) from temp_search_letters),
              (select substring(search_letters,10,1) from temp_search_letters)
              ) or length(word) < 8 then 1 else 0 end
            + case when substring(word, 9, 1) in (
              (select substring(search_letters,1,1) from temp_search_letters),
              (select substring(search_letters,2,1) from temp_search_letters),
              (select substring(search_letters,3,1) from temp_search_letters),
              (select substring(search_letters,4,1) from temp_search_letters),
              (select substring(search_letters,5,1) from temp_search_letters),
              (select substring(search_letters,6,1) from temp_search_letters),
              (select substring(search_letters,7,1) from temp_search_letters),
              (select substring(search_letters,8,1) from temp_search_letters),
              (select substring(search_letters,9,1) from temp_search_letters),
              (select substring(search_letters,10,1) from temp_search_letters)
              ) or length(word) < 9 then 1 else 0 end
            + case when substring(word, 10, 1) in (
              (select substring(search_letters,1,1) from temp_search_letters),
              (select substring(search_letters,2,1) from temp_search_letters),
              (select substring(search_letters,3,1) from temp_search_letters),
              (select substring(search_letters,4,1) from temp_search_letters),
              (select substring(search_letters,5,1) from temp_search_letters),
              (select substring(search_letters,6,1) from temp_search_letters),
              (select substring(search_letters,7,1) from temp_search_letters),
              (select substring(search_letters,8,1) from temp_search_letters),
              (select substring(search_letters,9,1) from temp_search_letters),
              (select substring(search_letters,10,1) from temp_search_letters)
              ) or length(word) < 10 then 1 else 0 end
          ) >= (select length_wo_blanks from temp_search_letters)
          and length(word) <= least(10, (select length from temp_search_letters))
        ;

        select
          length(word) as letter_count
         ,array_agg(word order by word)
        from
          (
          select
            word

            ,case when (select substring(search_letters,1,1) from temp_search_letters) <> '_'
              then least(
                -- How many does "search_term"'s 1st position's letter cover in "word".
                (length(word) - length(regexp_replace(word, '[' || (select substring(search_letters,1,1) from temp_search_letters) || ']', '', 'g')))
                ,-- How many does "search_term"'s 1st position's letter cover in "search_term".
                ((select length from temp_search_letters) 
                        - length(regexp_replace((select search_letters from temp_search_letters), '[' || (select substring(search_letters,1,1) from temp_search_letters) || ']','', 'g')))
                )
              else 0 end as covered_by_letter_1_count

            ,case when (select substring(search_letters,2,1) from temp_search_letters) <> '_'
                and (select length from temp_search_letters) >= 2
                and (select substring(search_letters,2,1) from temp_search_letters) <> (select substring(search_letters,1,1) from temp_search_letters)
              then least(
                -- How many does "search_term"'s 2nd position's letter cover in "word".
                (length(word) - length(regexp_replace(word, '[' || (select substring(search_letters,2,1) from temp_search_letters) || ']', '', 'g')))
                ,-- How many does "search_term"'s 2nd position's letter cover in "search_term".
                ((select length from temp_search_letters) 
                        - length(regexp_replace((select search_letters from temp_search_letters), '[' || (select substring(search_letters,2,1) from temp_search_letters) || ']','', 'g')))
                )
              else 0 end as covered_by_letter_2_count

            ,case when (select substring(search_letters,3,1) from temp_search_letters) <> '_'
                and (select length from temp_search_letters) >= 3
                and (select substring(search_letters,3,1) from temp_search_letters) <> (select substring(search_letters,2,1) from temp_search_letters)
              then least(
                -- How many does "search_term"'s 3rd position's letter cover in "word".
                (length(word) - length(regexp_replace(word, '[' || (select substring(search_letters,3,1) from temp_search_letters) || ']', '', 'g')))
                ,-- How many does "search_term"'s 3rd position's letter cover in "search_term".
                ((select length from temp_search_letters) 
                        - length(regexp_replace((select search_letters from temp_search_letters), '[' || (select substring(search_letters,3,1) from temp_search_letters) || ']','', 'g')))
                )
              else 0 end as covered_by_letter_3_count

            ,case when (select substring(search_letters,4,1) from temp_search_letters) <> '_'
                and (select length from temp_search_letters) >= 4
                and (select substring(search_letters,4,1) from temp_search_letters) <> (select substring(search_letters,3,1) from temp_search_letters)
              then least(
                -- How many does "search_term"'s 4th position's letter cover in "word".
                (length(word) - length(regexp_replace(word, '[' || (select substring(search_letters,4,1) from temp_search_letters) || ']', '', 'g')))
                ,-- How many does "search_term"'s 4th position's letter cover in "search_term".
                ((select length from temp_search_letters) 
                        - length(regexp_replace((select search_letters from temp_search_letters), '[' || (select substring(search_letters,4,1) from temp_search_letters) || ']','', 'g')))
                )
              else 0 end as covered_by_letter_4_count

            ,case when (select substring(search_letters,5,1) from temp_search_letters) <> '_'
                and (select length from temp_search_letters) >= 5
                and (select substring(search_letters,5,1) from temp_search_letters) <> (select substring(search_letters,4,1) from temp_search_letters)
              then least(
                -- How many does "search_term"'s 5th position's letter cover in "word".
                (length(word) - length(regexp_replace(word, '[' || (select substring(search_letters,5,1) from temp_search_letters) || ']', '', 'g')))
                ,-- How many does "search_term"'s 5th position's letter cover in "search_term".
                ((select length from temp_search_letters) 
                        - length(regexp_replace((select search_letters from temp_search_letters), '[' || (select substring(search_letters,5,1) from temp_search_letters) || ']','', 'g')))
                )
              else 0 end as covered_by_letter_5_count

            ,case when (select substring(search_letters,6,1) from temp_search_letters) <> '_'
                and (select length from temp_search_letters) >= 6
                and (select substring(search_letters,6,1) from temp_search_letters) <> (select substring(search_letters,5,1) from temp_search_letters)
              then least(
                -- How many does "search_term"'s 6th position's letter cover in "word".
                (length(word) - length(regexp_replace(word, '[' || (select substring(search_letters,6,1) from temp_search_letters) || ']', '', 'g')))
                ,-- How many does "search_term"'s 6th position's letter cover in "search_term".
                ((select length from temp_search_letters) 
                        - length(regexp_replace((select search_letters from temp_search_letters), '[' || (select substring(search_letters,6,1) from temp_search_letters) || ']','', 'g')))
                )
              else 0 end as covered_by_letter_6_count

            ,case when (select substring(search_letters,7,1) from temp_search_letters) <> '_'
                and (select length from temp_search_letters) >= 7
                and (select substring(search_letters,7,1) from temp_search_letters) <> (select substring(search_letters,6,1) from temp_search_letters)
              then least(
                -- How many does "search_term"'s 7th position's letter cover in "word".
                (length(word) - length(regexp_replace(word, '[' || (select substring(search_letters,7,1) from temp_search_letters) || ']', '', 'g')))
                ,-- How many does "search_term"'s 7th position's letter cover in "search_term".
                ((select length from temp_search_letters) 
                        - length(regexp_replace((select search_letters from temp_search_letters), '[' || (select substring(search_letters,7,1) from temp_search_letters) || ']','', 'g')))
                )
              else 0 end as covered_by_letter_7_count

            ,case when (select substring(search_letters,8,1) from temp_search_letters) <> '_'
                and (select length from temp_search_letters) >= 8
                and (select substring(search_letters,8,1) from temp_search_letters) <> (select substring(search_letters,7,1) from temp_search_letters)
              then least(
                -- How many does "search_term"'s 8th position's letter cover in "word".
                (length(word) - length(regexp_replace(word, '[' || (select substring(search_letters,8,1) from temp_search_letters) || ']', '', 'g')))
                ,-- How many does "search_term"'s 8th position's letter cover in "search_term".
                ((select length from temp_search_letters) 
                        - length(regexp_replace((select search_letters from temp_search_letters), '[' || (select substring(search_letters,8,1) from temp_search_letters) || ']','', 'g')))
                )
              else 0 end as covered_by_letter_8_count

            ,case when (select substring(search_letters,9,1) from temp_search_letters) <> '_'
                and (select length from temp_search_letters) >= 9
                and (select substring(search_letters,9,1) from temp_search_letters) <> (select substring(search_letters,8,1) from temp_search_letters)
              then least(
                -- How many does "search_term"'s 9th position's letter cover in "word".
                (length(word) - length(regexp_replace(word, '[' || (select substring(search_letters,9,1) from temp_search_letters) || ']', '', 'g')))
                ,-- How many does "search_term"'s 9th position's letter cover in "search_term".
                ((select length from temp_search_letters) 
                        - length(regexp_replace((select search_letters from temp_search_letters), '[' || (select substring(search_letters,9,1) from temp_search_letters) || ']','', 'g')))
                )
              else 0 end as covered_by_letter_9_count

            ,case when (select substring(search_letters,10,1) from temp_search_letters) <> '_'
                and (select length from temp_search_letters) >= 10
                and (select substring(search_letters,10,1) from temp_search_letters) <> (select substring(search_letters,9,1) from temp_search_letters)
              then least(
                -- How many does "search_term"'s 10th position's letter cover in "word".
                (length(word) - length(regexp_replace(word, '[' || (select substring(search_letters,10,1) from temp_search_letters) || ']', '', 'g')))
                ,-- How many does "search_term"'s 10th position's letter cover in "search_term".
                ((select length from temp_search_letters) 
                        - length(regexp_replace((select search_letters from temp_search_letters), '[' || (select substring(search_letters,10,1) from temp_search_letters) || ']','', 'g')))
                )
              else 0 end as covered_by_letter_10_count

          from
            temp_search_step_1
          ) a
        where
          (covered_by_letter_1_count + covered_by_letter_2_count + covered_by_letter_3_count
            + covered_by_letter_4_count + covered_by_letter_5_count + covered_by_letter_6_count
            + covered_by_letter_7_count + covered_by_letter_8_count + covered_by_letter_9_count
            + covered_by_letter_10_count
          )
          + (select length(search_letters) - length(regexp_replace(search_letters, '[_]', '', 'g')) from temp_search_letters)
          >= length(word)
        group by 
          length(word)
        order by 
          length(word) desc;
        """
    cursor = connection.cursor()
    cursor.execute(search_query, [search_input,])
    results = cursor.fetchall()

    word_matches = []
    for result in results:
        temp_word_match = {}
        temp_word_match['letter_count'] = result[0]
        temp_word_match['words'] = result[1]
        word_matches.append(temp_word_match)
    return word_matches
    

def get_word_prefix_suffix_list(word):
    '''
    Return letters for a given word that also make valid word, both as prefix and suffix.
    All of this has been pre-calculated and saved in the DB.
    '''
    word_prefix_suffix_list = models.Word_Prefix_Suffix_List.objects.filter(word=word)
    if len(word_prefix_suffix_list) >= 1:
        word_prefix_suffix_list = word_prefix_suffix_list[0]
    else:
        word_prefix_suffix_list = None
    return word_prefix_suffix_list


@cache_util(60 * 60 * 24 * 7)
def get_word_stems(stem_length=6, top_n=100):
    '''
    Get a list of n "stem_length"-letter stems which can lead to a 7 letter word.
    Will have different letter combinations listed that do so, along with count and odds.
    All of this has been pre-calculated and saved in the DB.
    '''
    word_stems = models.Word_Stem.objects.annotate(stem_length=Length('word_stem')).filter(
        stem_length=stem_length
        ).order_by('id')[:top_n]
    return word_stems


@cache_util(60 * 60 * 24 * 7)
def get_word_fragments(fragment_length=3, top_n=100):
    '''
    Get a list of n "fragment_length"-letter blocks which are part of the most words.
    i.e., "ING" is a three-letter block found in numerous words.
    '''
    word_fragments = models.Word_Fragment.objects.annotate(fragment_length=Length('word_fragment')).filter(
        fragment_length=fragment_length
        ).order_by('id')[:top_n]
    return word_fragments
    

@cache_util(60 * 60 * 24 * 7)
def get_word_vowel_consonant_heavy(type='vowel'):
    '''
    Get a list of words by letter count which are heavy in vowels or consonants (depending on input)
    '''
    if type == 'vowel':
        vowel_flg = 'true'
    else:
        vowel_flg = 'false'
    search_query = ("""
        select
          length(w.word) as letter_count
          ,array_agg(w.word order by w.word)
        from 
          trainer_word_vowel_consonant_heavy vc
          inner join trainer_word w
            on w.id = vc.word_id
        where
          vowel_heavy_flg = """
        + vowel_flg +
          """
        group by 
          length(w.word)
        order by 
          length(w.word) desc
        """)
    cursor = connection.cursor()
    cursor.execute(search_query)
    results = cursor.fetchall()
    
    word_matches = []
    for result in results:
        temp_word_match = {}
        temp_word_match['letter_count'] = result[0]
        temp_word_match['words'] = result[1]
        word_matches.append(temp_word_match)
    return word_matches


@cache_util(60 * 60 * 24 * 7)
def get_jqxz_words():
    '''
    Run query to get words with JQXZ in them.
    '''
    search_query = """
        select
          b.*
        from

          (
          select
            case 
              when contains_j_flg = true 
                and contains_q_flg = false
                and contains_X_flg = false
                and contains_Z_flg = false 
                then 'J'
              when contains_j_flg = true 
                and contains_q_flg = true
                and contains_X_flg = false
                and contains_Z_flg = false 
                then 'J & Q'
              when contains_j_flg = true 
                and contains_q_flg = false
                and contains_X_flg = true
                and contains_Z_flg = false 
                then 'J & X'
              when contains_j_flg = true 
                and contains_q_flg = false
                and contains_X_flg = false
                and contains_Z_flg = true 
                then 'J & Z'
              when contains_j_flg = true 
                and contains_q_flg = true
                and contains_X_flg = true
                and contains_Z_flg = false 
                then 'J, Q, & X'
              when contains_j_flg = true 
                and contains_q_flg = true
                and contains_X_flg = false
                and contains_Z_flg = true 
                then 'J, Q, & Z'
              when contains_j_flg = true 
                and contains_q_flg = false
                and contains_X_flg = true
                and contains_Z_flg = true 
                then 'J, X, & Z'
              when contains_j_flg = true 
                and contains_q_flg = true
                and contains_X_flg = true
                and contains_Z_flg = true 
                then 'J, Q, X, & Z'
              when contains_j_flg = false 
                and contains_q_flg = true
                and contains_X_flg = false
                and contains_Z_flg = false 
                then 'Q'
              when contains_j_flg = false 
                and contains_q_flg = true
                and contains_X_flg = true
                and contains_Z_flg = false 
                then 'Q & X'
              when contains_j_flg = false 
                and contains_q_flg = true
                and contains_X_flg = false
                and contains_Z_flg = true 
                then 'Q & Z'
              when contains_j_flg = false 
                and contains_q_flg = true
                and contains_X_flg = true
                and contains_Z_flg = true 
                then 'Q, X, & Z'
              when contains_j_flg = false 
                and contains_q_flg = false
                and contains_X_flg = true
                and contains_Z_flg = false 
                then 'X'
              when contains_j_flg = false 
                and contains_q_flg = false
                and contains_X_flg = true
                and contains_Z_flg = true 
                then 'X & Z'
              when contains_j_flg = false 
                and contains_q_flg = false
                and contains_X_flg = false
                and contains_Z_flg = true 
                then 'Z'
              end as letters
            ,length(word)
            ,array_agg(word order by word) as word_list
          from
            (

            select
              word
              ,length(regexp_replace(word, '[J]', '')) < length(word) as contains_j_flg
              ,length(regexp_replace(word, '[Q]', '')) < length(word) as contains_q_flg
              ,length(regexp_replace(word, '[X]', '')) < length(word) as contains_x_flg
              ,length(regexp_replace(word, '[Z]', '')) < length(word) as contains_z_flg
            from
              trainer_word
            where
              length(word) between 2 and 7
              and length(regexp_replace(word, '[JQXZ]', '')) < length(word)
            order by
              length(word) desc, word

            )a
    
          group by 1,2
          order by 1,2 desc
          )b
        order by 
          length(b.letters)
          ,b.letters
          ,b.length desc
        """
    cursor = connection.cursor()
    cursor.execute(search_query, [])
    results = cursor.fetchall()
    
    word_matches = []
    for i in range(0, len(results)):
        if i == 0:
            temp_word_match_list = []
            temp_word_match_element = {}
            temp_word_match_element['length'] = results[i][1]
            temp_word_match_element['word_list'] = results[i][2]
            temp_word_match_list.append(temp_word_match_element)
        elif results[i][0] == results[i-1][0] and i != len(results) - 1:
            temp_word_match_element = {}
            temp_word_match_element['length'] = results[i][1]
            temp_word_match_element['word_list'] = results[i][2]
            temp_word_match_list.append(temp_word_match_element)
        elif i != len(results) - 1:
            word_match = {}
            word_match['letter'] = results[i-1][0]
            word_match['results'] = temp_word_match_list
            word_matches.append(word_match)
            temp_word_match_list = []
            temp_word_match_element = {}
            temp_word_match_element['length'] = results[i][1]
            temp_word_match_element['word_list'] = results[i][2]
            temp_word_match_list.append(temp_word_match_element)
        else:
            word_match = {}
            word_match['letter'] = results[i-1][0]
            word_match['results'] = temp_word_match_list
            word_matches.append(word_match)
    return word_matches


@cache_util(60 * 60 * 24 * 7)
def get_q_without_u_words():
    '''
    Run query to get words with Q and no U.
    '''
    search_query = """
        select
          length(word)
          ,array_agg(word order by word)
        from
          trainer_word
        where
          length(regexp_replace(word, '[Q]', '')) < length(word)
          and length(regexp_replace(word, '[U]', '')) = length(word)
        group by 
          length(word)
        order by 
          length(word) desc
        """
    cursor = connection.cursor()
    cursor.execute(search_query, [])
    results = cursor.fetchall()
    
    word_matches = []
    for result in results:
        temp_word_match = {}
        temp_word_match['letter_count'] = result[0]
        temp_word_match['words'] = result[1]
        word_matches.append(temp_word_match)
    return word_matches


@cache_util(60 * 60 * 24 * 7)
def check_word_stem(word_stem):
    '''
    Check if a given combination of letters is a stem for a 7 letter word.
    word_stem should be alphabetical and capitalized
    '''
    try:
        word_stem = models.Word_Stem.objects.get(word_stem=word_stem)
    except:
        word_stem = None
    return word_stem


@cache_util(60 * 60 * 24 * 7)
def get_n_letter_words(n, start=None, end=None, stem_length=None):
    '''
    Get n-letter words, matching start and end chars if provided
    '''
    if not stem_length:
        stem_length = max(n-2, 1)
    if n == 7:
        stem_length = 4
    
    # Words that start with "X"
    search_query = build_n_letter_search_query(n, start, end, stem_length)
    cursor = connection.cursor()
    if start and end:
        cursor.execute(search_query, [stem_length, n, start, end])
    elif start:
        cursor.execute(search_query, [stem_length, n, start,])
    elif end:
        cursor.execute(search_query, [stem_length, n, end])
    else:
        cursor.execute(search_query, [stem_length, n,])
    results = cursor.fetchall()
    word_matches = build_word_matches_from_results(results)
    
    # Words that end with "X"
    search_query = build_n_letter_search_query_end(n, start, end, stem_length)
    cursor = connection.cursor()
    if start and end:
        cursor.execute(search_query, [stem_length, stem_length, n, start, end])
    elif start:
        cursor.execute(search_query, [stem_length, stem_length, n, start,])
    elif end:
        cursor.execute(search_query, [stem_length, stem_length, n, end])
    else:
        cursor.execute(search_query, [stem_length, stem_length, n,])
    results = cursor.fetchall()
    word_matches_end = build_word_matches_from_results(results)    
    
    return word_matches, word_matches_end
    

def build_n_letter_search_query(n, start, end, stem_length=1):
    search_query = """
        select 
            substring(word, 1, %s) as stem
            ,array_agg(word order by word) from trainer_word
        where length(word) = %s
        """
    if start:
        search_query += """ and word like '%s%%'"""
    if end:
        search_query += """ and word like '%%%s'"""
    search_query += """ group by 1 order by 1"""
    return search_query


def build_n_letter_search_query_end(n, start, end, stem_length=1):
    '''
    Same as build_n_letter_search_query, but find words that END with letter(s) "X".
    '''
    search_query = """
        select 
            substring(word, (length(word) - %s) + 1, %s) as stem
            ,array_agg(word order by word) from trainer_word
        where length(word) = %s
        """
    if start:
        search_query += """ and word like '%s%%'"""
    if end:
        search_query += """ and word like '%%%s'"""
    search_query += """ group by 1 order by 1"""
    return search_query


def build_search_query_by_stem(stem_type):
    '''
    Return query to find words.
    '''
    search_query = """
        select
            array_agg(word order by word)
        from trainer_word
        where length(word) = %s
        and word like %s """
    return search_query


def build_word_matches_from_results(results):
    word_matches = []
    for result in results:
        temp_word_matches = {}
        temp_word_matches['stem'] = result[0]
        temp_word_matches['words'] = result[1]
        word_matches.append(temp_word_matches)
    return word_matches
    

def get_stem_length(word_length):
    if word_length in (2,3):
        stem_length = 1
    elif word_length == 4:
        stem_length = 2
    elif word_length in (5,6):
        stem_length = 3
    else:
        stem_length = 4
    return stem_length


def get_word_stem(word_length, stem_type, stem_length):
    if stem_type == 'beginning':
        search_query = """
            select
              a.word_stem
            from
              (
              select 
                substring(word, 1, %s) as word_stem
                ,count(word) as word_count
              from
                trainer_word
              where 
                length(word) = %s
              group by 1
              order by 2 desc
              ) a
            where
              a.word_count >= 10
              or length(a.word_stem) = 1
            order by 
              random()
            limit 1
            """
        cursor = connection.cursor()
        cursor.execute(search_query, [stem_length, word_length,])
    else:
        search_query = """
            select
              a.word_stem
            from
              (
              select 
                substring(word, %s - (%s - 1), %s) as word_stem
                ,count(word) as word_count
              from
                trainer_word
              where 
                length(word) = %s
              group by 1
              order by 2 desc
              ) a
            where
              a.word_count >= 10
              or length(a.word_stem) = 1
            order by 
              random()
            limit 1
            """
        cursor = connection.cursor()
        cursor.execute(search_query, [word_length, stem_length, stem_length, word_length,])
    result = cursor.fetchone()
    word_stem = result[0]
    return word_stem


def get_word_stem_and_word_matches():
    '''
    Get a 6-letter word stem with at least 10 possible 7-letter words.
    '''
    search_query = """
        select
          word_stem
          ,array_agg((select word from trainer_word where id = word_id) order by word_id)
        from
          (
          select
            word_stem
            ,unnest(word_list) as word_id
          from
            (
            select 
              * 
            from 
              trainer_word_stem 
            where 
              length(word_stem) = 6
              and word_count >= 10
            order by random() limit 1
            ) a
          ) b
        group by 
          word_stem
        """
    cursor = connection.cursor()
    cursor.execute(search_query, [])
    result = cursor.fetchone()
    word_stem = result[0]
    word_matches = result[1]
    return word_stem, word_matches


@cache_util(60 * 60 * 24 * 7)
def get_olaughlin_words():
    search_query = """
        select
          a.word_length
          ,array_agg(word order by olaughlin_rank) as word_list
        from
          (
          select
            length(word) as word_length
            ,word
            ,row_number() over (partition by length(w.word) order by os.olaughlin_score desc) as olaughlin_rank
          from
            trainer_word_olaughlin_score os
            inner join trainer_word w
              on w.id = os.word_id
          where 
            length(word) in (2,3,4,7,8)

          union

          select
            length(word) as word_length
            ,word
            ,row_number() over (partition by length(w.word) order by os.olaughlin_score desc) as olaughlin_rank
          from
            trainer_word_olaughlin_score os
            inner join trainer_word w
              on w.id = os.word_id
          where 
            length(word) in (5,6)
            and length(regexp_replace(word, '[Q]', '', 'g')) < length(word)

          union

          select
            length(word) as word_length
            ,word
            ,row_number() over (partition by length(w.word) order by os.olaughlin_score desc) as olaughlin_rank
          from
            trainer_word_olaughlin_score os
            inner join trainer_word w
              on w.id = os.word_id
          where 
            length(word) in (5,6)
            and length(regexp_replace(word, '[Q]', '', 'g')) = length(word)
  
          ) a
        where
          a.olaughlin_rank <= 20
        group by 
          a.word_length
        order by 
          a.word_length desc
        """
    cursor = connection.cursor()
    cursor.execute(search_query, [])
    results = cursor.fetchall()
    word_matches = []
    for result in results:
        temp_word_match = {}
        temp_word_match['letter_count'] = result[0]
        temp_word_match['words'] = result[1]
        word_matches.append(temp_word_match)
    return word_matches


@cache_util(60 * 60 * 24 * 7)
def get_olaughlin_words_extended():
    '''
    Get top 100 O'Laughlin Words for each length, from 2-8 letters
    '''
    search_query = """
        select
          a.word_length
          ,array_agg(word order by olaughlin_rank) as word_list
        from
          (
          select
            length(word) as word_length
            ,word
            ,row_number() over (partition by length(w.word) order by os.olaughlin_score desc) as olaughlin_rank
          from
            trainer_word_olaughlin_score os
            inner join trainer_word w
              on w.id = os.word_id
          where 
            length(word) between 2 and 8
          ) a
        where
          a.olaughlin_rank <= 100
        group by 
          a.word_length
        order by 
          a.word_length desc
        """
    cursor = connection.cursor()
    cursor.execute(search_query, [])
    results = cursor.fetchall()
    word_matches = []
    for result in results:
        temp_word_match = {}
        temp_word_match['letter_count'] = result[0]
        temp_word_match['words'] = result[1]
        word_matches.append(temp_word_match)
    return word_matches


def generate_search_input(letter_count, require_jqxz, require_n_letter_word):
    '''
    Given parameters, return "letter_count" number of letters.
    User will attempt to find as many valid words as they can from these.
    
    If this must return a JQXZ letter and/or 7-letter word, check to make sure it does that first.
    
    Then, get random letters if not
    '''
    if require_jqxz and require_n_letter_word:
        ''' n-letter word with a J,Q,X, or Z. '''
        cursor = connection.cursor()
        cursor.execute("""
            select
              word
            from
              trainer_word
            where
              length(word) = %s
              and length(regexp_replace(word, '[JQXZ]', '', 'g')) < length(word)
            order by 
              random()
            limit 1
            """, [letter_count,] 
            )
        result = cursor.fetchone()
        search_input = result[0]
        search_input = clean_search_input(search_input)
    
    elif require_jqxz:
        ''' n random letters with at least one J,Q,X, or Z (more are allowed)'''
        search_input = ''
        # Get one of J,Q,X, or Z
        jqxz_letters = ['J','Q','X','Z']
        random.shuffle(jqxz_letters)
        temp_letter = jqxz_letters[0]
        # Get six other letters, making sure to not duplicate the JQXZ letter
        wwf_letters = ['A','A','A','A','A','A','A','A','A','B','B','C','C','D','D','D','D','D','E','E','E','E','E','E','E','E','E','E','E','E','E','F','F','G','G','G','H','H','H','H','I','I','I','I','I','I','I','I','J','K','L','L','L','L','M','M','N','N','N','N','N','O','O','O','O','O','O','O','O','P','P','Q','R','R','R','R','R','R','S','S','S','S','S','T','T','T','T','T','T','T','U','U','U','U','V','V','W','W','X','Y','Y','Z']
        wwf_letters.remove(temp_letter)
        random.shuffle(wwf_letters)
        for i in range(0, (letter_count-1)):
            search_input += wwf_letters[i]
        search_input += temp_letter # Add the JQXZ

    elif require_n_letter_word:
        ''' n-letter word with no other conditions '''
        cursor = connection.cursor()
        cursor.execute("""
            select
              word
            from
              trainer_word
            where
              length(word) = %s
            order by 
              random()
            limit 1
            """, [letter_count,] 
            )
        result = cursor.fetchone()
        search_input = result[0]
        
    else:
        ''' n random letters with no other conditions '''
        search_input = ''
        wwf_letters = ['A','A','A','A','A','A','A','A','A','B','B','C','C','D','D','D','D','D','E','E','E','E','E','E','E','E','E','E','E','E','E','F','F','G','G','G','H','H','H','H','I','I','I','I','I','I','I','I','J','K','L','L','L','L','M','M','N','N','N','N','N','O','O','O','O','O','O','O','O','P','P','Q','R','R','R','R','R','R','S','S','S','S','S','T','T','T','T','T','T','T','U','U','U','U','V','V','W','W','X','Y','Y','Z']
        random.shuffle(wwf_letters)
        for i in range(0, letter_count):
            search_input += wwf_letters[i]

    search_input = clean_search_input(search_input)
    return search_input


def get_total_word_count_from_word_matches(word_matches):
    total_word_count = 0
    for word_match in word_matches:
        total_word_count += len(word_match['words'])
    return total_word_count


def create_fake_word_from_word(word):
    '''
    Take a word, change letters around until it's fake.
    Purpose is to mix some fake words in when asking user if a word is real or not.
    '''
    fake_word_created = False
    wwf_vowels = ['A','A','A','A','A','A','A','A','A','E','E','E','E','E','E','E','E','E','E','E','E','E','I','I','I','I','I','I','I','I','O','O','O','O','O','O','O','O','U','U','U','U']
    wwf_consonants = ['B','B','C','C','D','D','D','D','D','F','F','G','G','G','H','H','H','H','J','K','L','L','L','L','M','M','N','N','N','N','N','P','P','Q','R','R','R','R','R','R','S','S','S','S','S','T','T','T','T','T','T','T','V','V','W','W','X','Z']
    while fake_word_created == False:
        word_key = random.randint(0,len(word)-2)
        if word[word_key] in wwf_vowels:
            new_letter = False
            while new_letter == False:
                letter_key = random.randint(0, len(wwf_vowels)-1)
                if wwf_vowels[letter_key] != word[word_key]:
                    new_letter = True
            word = list(word)
            word[word_key] = wwf_vowels[letter_key]
            word = ''.join(word)
        else:
            new_letter = False
            while new_letter == False:
                letter_key = random.randint(0, len(wwf_consonants)-1)
                if wwf_consonants[letter_key] != word[word_key]:
                    new_letter = True
            word = list(word)
            word[word_key] = wwf_consonants[letter_key]
            word = ''.join(word)
        # Check if the new pseudo-word you've created happens to match an actual word. Return it if not.
        word_check = models.Word.objects.filter(word=word)
        if len(word_check) == 0:
            fake_word_created = True 
    return word


def check_previous_guess(previous_word, previous_guess):
    word = models.Word.objects.filter(word=previous_word)
    if len(word) == 0:
        if previous_guess == 'yes':
            previous_is_correct = False
        else:
            previous_is_correct = True
    else:
        if previous_guess == 'yes':
            previous_is_correct = True
        else:
            previous_is_correct = False
    return previous_is_correct




def get_article_template_from_uri(full_uri):
    full_uri = full_uri.replace('-', '_')[:-1]
    article_template = 'trainer' + full_uri + '.html'
    return article_template


def check_for_word(search_input):
    '''
    DEBUGGING -- is a specific word in DB using custom SQL query
    '''
    cursor = connection.cursor()
    search_query = """
        select word from trainer_word
        where word = %s
        """
    print(cursor.mogrify(search_query, [search_input,]))
    cursor.execute(search_query, [search_input,])
    results = cursor.fetchall()
    print(len(results))
    word_matches = []
    for result in results:
        print(result)
        word_matches.append(result[0])
    return word_matches