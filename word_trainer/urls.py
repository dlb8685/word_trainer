from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    
    url(r'^$', 'trainer.views.home', name='home'),
    url(r'^get-matching-words/$', 'trainer.views.get_matching_words', name="trainer_get_matching_words"),
    url(r'^get-prefix-suffix-list/$', 'trainer.views.get_prefix_suffix_list', name="trainer_get_prefix_suffix_list"),
    url(r'^word-lists/$', 'trainer.views.word_lists', name="trainer_word_lists"),
    url(r'^(?P<n>[2-7]+)-letter-words/$', 'trainer.views.n_letter_words', name="trainer_n_letter_words"),
    url(r'^(?P<n>[3]+)-letter-word-fragments/$', 'trainer.views.n_letter_word_fragments', name="trainer_n_letter_word_fragments"),
    url(r'^(?P<n>[2-6]+)-letter-word-stems/$', 'trainer.views.n_letter_word_stems', name="trainer_n_letter_word_stems"),
    url(r'^olaughlin-words/$', 'trainer.views.olaughlin_words', name="trainer_olaughlin_words"),
    url(r'^vowel-heavy-words/$', 'trainer.views.vowel_consonant_heavy_words', name="trainer_vowel_heavy_words"),
    url(r'^consonant-heavy-words/$', 'trainer.views.vowel_consonant_heavy_words', name="trainer_consonant_heavy_words"),
    url(r'^jqxz-words/$', 'trainer.views.jqxz_words', name="trainer_jqxz_words"),
    url(r'^q-without-u-words/$', 'trainer.views.q_without_u_words', name="trainer_q_without_u_words"),

    # Tools
    url(r'^tools/home/$', 'trainer.views.tools_home', name="trainer_tools_home"),
    url(r'^tools/find-all-words/$', 'trainer.views.tools_find_all_words', name="trainer_tools_find_all_words"),
    url(r'^tools/is-this-a-word/$', 'trainer.views.tools_is_this_a_word', name="trainer_tools_is_this_a_word"),
    url(r'^tools/words-by-length-and-stem/$', 'trainer.views.tools_words_by_length_and_stem', 
        name="trainer_tools_words_by_length_and_stem"),
    url(r'^tools/7-letter-words-by-stem/$', 'trainer.views.tools_7_letter_words_by_stem', 
        name="trainer_tools_7_letter_words_by_stem"),
    url(r'^tools/vowel-heavy-words/$', 'trainer.views.tools_vowel_heavy_words', name="trainer_tools_vowel_heavy_words"),
    url(r'^tools/2-letter-words/$', 'trainer.views.tools_2_letter_words', name="trainer_tools_2_letter_words"),
    url(r'^tools/olaughlin-words/$', 'trainer.views.tools_olaughlin_words', name="trainer_tools_olaughlin_words"),
    
    # Resources
    url(r'^external-resources/$', 'trainer.views.external_resources', name="trainer_external_resources"),

    # Articles (since a static number of these, each one coded individually)
    url(r'^article/overview/$', 'trainer.views.article', name="trainer_article_overview"),
    url(r'^article/opening/$', 'trainer.views.article', name="trainer_article_opening"),
    url(r'^article/endgame/$', 'trainer.views.article', name="trainer_article_endgame"),
    url(r'^article/space-and-position/$', 'trainer.views.article', name="trainer_article_space_and_position"),
    url(r'^article/2-3-letter-words/$', 'trainer.views.article', name="trainer_article_2_3_letter_words"),
    url(r'^article/olaughlin-words/$', 'trainer.views.article', name="trainer_article_olaughlin_words"),
    url(r'^article/finding-words/$', 'trainer.views.article', name="trainer_article_finding_words"),
    url(r'^article/drawing-7-letter-words/$', 'trainer.views.article', name="trainer_article_drawing_7_letter_words"),
    url(r'^article/jqxz/$', 'trainer.views.article', name="trainer_article_jqxz"),
    url(r'^article/prefixes-suffixes/$', 'trainer.views.article', name="trainer_article_prefixes_suffixes"),
    url(r'^article/consonant-vowel-distribution/$', 'trainer.views.article', name="trainer_article_consonant_vowel_distribution"),
    url(r'^article/sample-game-1/$', 'trainer.views.article', name="trainer_article_sample_game_1"),
    url(r'^article/sample-game-2/$', 'trainer.views.article', name="trainer_article_sample_game_2"),
    url(r'^article/sample-game-3/$', 'trainer.views.article', name="trainer_article_sample_game_3"),
    url(r'^article/sample-game-4/$', 'trainer.views.article', name="trainer_article_sample_game_4"),
    url(r'^article/sample-game-5/$', 'trainer.views.article', name="trainer_article_sample_game_5"),

]
