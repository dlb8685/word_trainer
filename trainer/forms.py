from django import forms

class SearchInputForm(forms.Form):
    search_input = forms.CharField(
        label='Enter 2-10 letters to obtain a list of matching words. Use _ for blanks',
        max_length=10
        )
        
class SearchInputFormPrefixSuffix(forms.Form):
    search_input = forms.CharField(
        label='Enter a word (up to 10 letters) to view a list of one-letter prefixes and suffixes.',
        max_length=10
        )
        

class FindAllWordsOptions(forms.Form):
    letter_count = forms.IntegerField(
        label='Letter Count',
        initial=7,
        min_value=3,
        max_value=7
        )
    require_jqxz = forms.BooleanField(
        label='Require J,Q,X,Z?',
        initial=False,
        required=False,
        )
    require_n_letter_word = forms.BooleanField(
        label='Require word with Letter Count?',
        initial=False,
        required=False,
        )
        

class WordStemLengthOptions(forms.Form):
    word_length = forms.IntegerField(
        label='Word Length',
        initial=5,
        min_value=2,
        max_value=7
        )