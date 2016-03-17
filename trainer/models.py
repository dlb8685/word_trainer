from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.
class Word(models.Model):
    '''
    List of all WWF words in database form.
    '''
    word = models.TextField()
    
    def __str__(self):
        return self.word
        

class Word_Prefix_Suffix_List(models.Model):
    '''
    Words where one letter prefix/suffix also creates a valid word. 
    '''
    word = models.ForeignKey(Word)
    prefix_list = ArrayField(models.CharField(max_length=1), null=True)
    suffix_list = ArrayField(models.CharField(max_length=1), null=True)
    

class Word_Stem(models.Model):
    '''
    Given a stem (in alphabetical order) of X letters, how many combinations are
        there to get to a 7 letter word?
    '''
    word_stem = models.TextField()
    letter_combo_count = models.SmallIntegerField()
    letter_combo_list = ArrayField(models.CharField(max_length=7))
    letter_combo_likelihood = models.FloatField(default=0)
    word_count = models.SmallIntegerField()
    word_list = ArrayField(models.IntegerField(), null=True)
    
    def get_word_stem_words(self, n=10):
        words = Word.objects.filter(id__in=self.word_list)[:n]
        self.words = words
        

class Word_Fragment(models.Model):
    '''
    Take a 3 or 4 letter chunk. Which ones can create the most words of up to 8 letters?
    '''
    word_fragment = models.TextField()
    word_count = models.SmallIntegerField()
    word_list = ArrayField(models.IntegerField(), null=True)
    
    def get_word_fragment_words(self, n=10):
        words = Word.objects.filter(id__in=self.word_list)[:n]
        self.words = words
        

class Word_Vowel_Consonant_Heavy(models.Model):
    '''
    For quick lookups, list words that are heavy in vowels or consonants.
    '''
    word = models.ForeignKey(Word)
    vowel_heavy_flg = models.BooleanField()
    vowel_count = models.SmallIntegerField()
    consonant_heavy_flg = models.BooleanField()
    consonant_count = models.SmallIntegerField()
    

class Word_OLaughlin_Score(models.Model):
    '''
    Save O'Laughlin Playablity scores for each word.
        See: http://pages.cs.wisc.edu/~o-laughl/collins/all/ 
        See: http://www.eugenedeon.com/scrabble/
        See: http://www.science20.com/brain_trust_diy_science_today039s_top_minds/scrabble_champs_words_friends_secrets-88540
    '''
    word = models.ForeignKey(Word)
    olaughlin_score = models.IntegerField()