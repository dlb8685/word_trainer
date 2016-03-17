from django.test import TestCase, TransactionTestCase
from django.db import connection
from trainer import models, utils


class Trainer_Test_Cases(TestCase):

    def setUp(self):
        pass


    def test_clean_search_input_1(self):
        '''
        User enters normal search input. Make sure it is passed correctly.
        '''
        search_input = 'ABCEEOQ'
        search_input = utils.clean_search_input(search_input)
        self.assertEqual(search_input, 'ABCEEOQ')


    def test_clean_search_input_2(self):
        '''
        Search input is too long (n's default is 7 chars)
        Check that function returns truncated version
        '''
        search_input = 'ABCEEOQXXX'
        search_input = utils.clean_search_input(search_input)
        self.assertEqual(search_input, 'ABCEEOQ')
        
    
    def test_clean_search_input_3(self):
        '''
        Lower case letters in search input.
        They should be capitalized, and remain in final result
        '''
        search_input = 'abceeoq'
        search_input = utils.clean_search_input(search_input)
        self.assertEqual(search_input, 'ABCEEOQ')


    def test_clean_search_input_4(self):
        '''
        All kinds of random shit, upper and lower-case, disallowed characters, _'s, etc.
        Make sure, holisitcally, that function trims this down to what you want.
        '''
        search_input = '3fw $GRGR _*effwec n'
        search_input = utils.clean_search_input(search_input)
        self.assertEqual(search_input, 'FGGRRW_')

        
    def test_clean_search_input_5(self):
        '''
        Feeble attempt at SQL injection.
        Should be accounted for anyway, but also check here for redunancy.
        '''
        search_input = '\'\' limit 1;select * from top_secret_data;'
        search_input = utils.clean_search_input(search_input)
        self.assertEqual(search_input, 'EIILMST')
    
    
    def test_clean_search_input_6(self):
        '''
        Allow 8 characters to be returned. Testing n parameter
        '''
        search_input = 'ABCEEOQZ'
        search_input = utils.clean_search_input(search_input, n=8)
        self.assertEqual(search_input, 'ABCEEOQZ')

    
    def test_get_matching_words_1(self):
        '''
        Test matching feature. Should return based on search_input
        '''
        set_up_dictionary()
        search_input = 'AABELNO'
        word_matches = utils.get_matching_words(search_input)
        self.assertEqual(word_matches[0], 'ABALONE')
        self.assertEqual(len(word_matches), 5)


    def test_get_matching_words_2(self):
        '''
        Test matching feature with blanks. Should return based on search_input
        '''
        set_up_dictionary()
        search_input = 'AABELN__'
        word_matches = utils.get_matching_words(search_input)
        self.assertEqual(word_matches[0], 'ABALONE')
        self.assertEqual(len(word_matches), 18)
        

    def test_get_matching_words_3(self):
        '''
        Test matching feature with less than 7 characters
        '''
        set_up_dictionary()
        search_input = 'AAA'
        word_matches = utils.get_matching_words(search_input)
        self.assertEqual(word_matches[0], 'AA')
        self.assertEqual(len(word_matches), 1)

    
    def test_get_word_prefix_suffix_list_1(self):
        '''
        Pull word where suffixes should be present, see if it appears.
        '''
        set_up_dictionary_and_prefix_suffix()
        word = models.Word.objects.get(word='ABATE')
        word_prefix_suffix_list = utils.get_word_prefix_suffix_list(word)
        self.assertEqual(len(word_prefix_suffix_list.suffix_list), 2)
        
        
    def test_get_word_prefix_suffix_list_2(self):
        '''
        Pull word without Prefixes-Suffixes, make sure it returns None
        '''
        set_up_dictionary_and_prefix_suffix()
        word = models.Word.objects.get(word='AAS')
        word_prefix_suffix_list = utils.get_word_prefix_suffix_list(word)
        self.assertEqual(word_prefix_suffix_list, None)


    def test_get_n_letter_words_1(self):
        '''
        Get two-letter words, check that they come back in expected format
        '''
        set_up_dictionary()
        word_matches = utils.get_n_letter_words(2)
        self.assertEqual(len(word_matches), 1)
        self.assertEqual(word_matches[0]['stem'], 'A')
        self.assertEqual(len(word_matches[0]['words']), 2)
        self.assertEqual(word_matches[0]['words'][0], 'AA')
    
    
    def test_get_n_letter_words_2(self):
        '''
        Get four-letter words, check that they come back in expected format
        '''
        set_up_dictionary()
        word_matches = utils.get_n_letter_words(4)
        self.assertEqual(len(word_matches), 2)
        self.assertEqual(word_matches[0]['stem'], 'AA')
        self.assertEqual(len(word_matches[0]['words']), 2)
        self.assertEqual(word_matches[0]['words'][0], 'AAHS')
        
    
    def test_get_jqxz_words_1(self):
        '''
        See if any JQXZ words come back
        '''
        set_up_dictionary()
        word_matches = utils.get_jqxz_words()
        self.assertEqual(len(word_matches), 2)
        self.assertEqual(word_matches[0], 'ABAXIAL')


    def test_get_q_without_u_words_1(self):
        '''
        See if any JQXZ words come back
        '''
        set_up_dictionary_q_no_u_word()  
        word_matches = utils.get_q_without_u_words()
        self.assertEqual(len(word_matches), 1)
        self.assertEqual(word_matches[0], 'QAT')
      
        

class Trainer_Test_Cases_DB(TransactionTestCase):

    def test_get_word_stems_1(self):
        '''
        Get word stems with default options.
        '''
        set_up_dictionary_and_word_stem()
        word_stems = utils.get_word_stems(stem_length=6, top_n=100)
        self.assertEqual(word_stems[0].word_stem, 'AABEHS')
        self.assertEqual(len(word_stems), 75)
        
        
    def test_get_word_stems_2(self):
        '''
        Override options to get four-letter stems.
        Should return empty list, since none have been defined.
        '''
        set_up_dictionary_and_word_stem()
        word_stems = utils.get_word_stems(stem_length=4, top_n=5)
        self.assertEqual(len(word_stems), 0)
    

    def test_check_word_stem_1(self):
        '''
        Check a stem that is present in the table, should return object.
        '''
        set_up_dictionary_and_word_stem()
        word_stem = 'AABEHS'
        word_stem = utils.check_word_stem(word_stem)
        ## The id's for these two words should be in the word_list list
        word_1 = models.Word.objects.get(word='ABASHED')
        word_2 = models.Word.objects.get(word='ABASHES')
        
        self.assertEqual(word_stem.word_stem, 'AABEHS')
        self.assertEqual(word_stem.letter_combo_list, ['D','S'])
        self.assertEqual(word_stem.word_list, [word_1.id,word_2.id])
        
        
    def test_check_word_stem_2(self):
        '''
        Check a stem that is not present in the table, should return None.
        '''
        set_up_dictionary_and_word_stem()
        word_stem = 'ZZZZZZ'
        word_stem = utils.check_word_stem(word_stem)
        self.assertEqual(word_stem, None)


    def test_word_stem_get_word_stem_words_1(self):
        '''
        For a Word_Stem object, check that get_word_stem method works and assigns value.
        '''
        set_up_dictionary_and_word_stem()
        word_stem = 'AABDNO'
        word_stem = utils.check_word_stem(word_stem)
        word_stem.get_word_stem_words()
        word_1 = models.Word.objects.get(word='ABANDON')
        self.assertEqual(len(word_stem.words), 1)
        self.assertEqual(word_stem.words[0], word_1)

        
########## HELPER FUNCTIONS ############  
def set_up_dictionary():
    words = open(file='words_with_friends.txt', newline='\n')
    words = words.readlines()
    for i in range(0,100):
        word = words[i].replace('\n', '')
        new_word = models.Word.objects.create(word=word)
        new_word.save()


def set_up_dictionary_q_no_u_word():
    words = open(file='words_with_friends.txt', newline='\n')
    words = words.readlines()
    for i in range(0,100):
        word = words[i].replace('\n', '')
        new_word = models.Word.objects.create(word=word)
        new_word.save()
    word = models.Word.objects.create(word='QAT')


def set_up_dictionary_and_prefix_suffix():
    words = open(file='words_with_friends.txt', newline='\n')
    words = words.readlines()
    for i in range(0,100):
        word = words[i].replace('\n', '')
        new_word = models.Word.objects.create(word=word)
        new_word.save()
    
    word = models.Word.objects.get(word='ABATE')
    word_prefix_suffix_list = models.Word_Prefix_Suffix_List.objects.create(
        word=word, prefix_list=None, suffix_list=['D','S']
        )
        

def set_up_dictionary_and_word_stem():
    words = open(file='words_with_friends.txt', newline='\n')
    words = words.readlines()
    for i in range(0,100):
        word = words[i].replace('\n', '')
        new_word = models.Word.objects.create(word=word)
        new_word.save()
    
    word_stem_query = """
        drop table if exists temp_7_letter_words;
        create temp table temp_7_letter_words as
        select
          id
          ,word
          ,array_to_string(array(select unnest(string_to_array(word, null)) order by 1), '') as letters
        from
          (select * from trainer_word order by 1 limit 100) a
        where
          length(word) = 7
        ;

        drop table if exists temp_7_letter_words_array;
        create temp table temp_7_letter_words_array as
        select
          letters
          ,string_to_array(letters, null) as letter_array
          ,array_agg(id order by id) as word_list
          ,count(*) as word_count
        from
          temp_7_letter_words
        group by 
          letters
        order by 
          word_count desc
        ;


        begin;

        insert into trainer_word_stem

        select
          row_number() over (order by count(distinct additional_letter) desc, array_to_string(array(select unnest(letter_array_6_letter) order by 1), '')) as id
          ,array_to_string(array(select unnest(letter_array_6_letter) order by 1), '') as word_stem 
          ,count(distinct additional_letter) as letter_combo_count
          ,array_agg(distinct additional_letter order by additional_letter) as letter_combo_list
          ,0.0000::numeric as letter_combo_likelihood
          ,count(distinct word_7_letter) as word_count
          ,array_agg(distinct word_7_letter order by word_7_letter) as word_list
        from
          (
          select
            letter_array[1:6] as letter_array_6_letter
            ,unnest(word_list) as word_7_letter
            ,letter_array[7] as additional_letter
          from
            temp_7_letter_words_array

          union

          select
            letter_array[1] || letter_array[3:7] as letter_array_6_letter
            ,unnest(word_list) as word_7_letter
            ,letter_array[2] as additional_letter
          from
            temp_7_letter_words_array

          union

          select
            letter_array[1:2] || letter_array[4:7] as letter_array_6_letter
            ,unnest(word_list) as word_7_letter
            ,letter_array[3] as additional_letter
          from
            temp_7_letter_words_array

          union

          select
            letter_array[1:3] || letter_array[5:7] as letter_array_6_letter
            ,unnest(word_list) as word_7_letter
            ,letter_array[4] as additional_letter
          from
            temp_7_letter_words_array

          union

          select
            letter_array[1:4] || letter_array[6:7] as letter_array_6_letter
            ,unnest(word_list) as word_7_letter
            ,letter_array[5] as additional_letter
          from
            temp_7_letter_words_array

          union

          select
            letter_array[1:5] || letter_array[7] as letter_array_6_letter
            ,unnest(word_list) as word_7_letter
            ,letter_array[6] as additional_letter
          from
            temp_7_letter_words_array

          union

          select
            letter_array[2:7] as letter_array_6_letter
            ,unnest(word_list) as word_7_letter
            ,letter_array[1] as additional_letter
          from
            temp_7_letter_words_array
          ) a
        group by 
          array_to_string(array(select unnest(letter_array_6_letter) order by 1), '')
        order by 
          count(distinct additional_letter) desc, array_to_string(array(select unnest(letter_array_6_letter) order by 1), '')
        ;

        commit;
        """
    cursor = connection.cursor()
    cursor.execute(word_stem_query)