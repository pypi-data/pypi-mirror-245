from .bigbench_groups import *
from .blimp_groups import *
from .popularity import *

imppres_presupposition=['presupposition_all_n_presupposition',
 'presupposition_both_presupposition',
 'presupposition_change_of_state',
 'presupposition_cleft_existence',
 'presupposition_cleft_uniqueness',
 'presupposition_only_presupposition',
 'presupposition_possessed_definites_existence',
 'presupposition_possessed_definites_uniqueness',
 'presupposition_question_presupposition']

imppres_implicature=['implicature_connectives',
 'implicature_gradable_adjective',
 'implicature_gradable_verb',
 'implicature_modals',
 'implicature_numerals_10_100',
 'implicature_numerals_2_3',
 'implicature_quantifiers']

crossfit=['emo',
 'wiki_auto',
 'liar',
 'tab_fact',
 'sms_spam',
 'google_wellformed_query',
 'glue',
 'poem_sentiment',
 'emotion',
 'hate_speech18',
 'hatexplain',
 'yahoo_answers_topics',
 'mc_taco',
 'glue',
 'mocha',
 'super_glue',
 'glue',
 'yelp_polarity',
 'tweet_eval',
 'glue',
 'art',
 'super_glue',
 'ethos',
 'app_reviews',
 'yelp_review_full',
 'anli',
 'hate_speech_offensive',
 'climate_fever',
 'circa',
 'financial_phrasebank',
 'wiki_qa',
 'rotten_tomatoes',
 'trec',
 'medical_questions_pairs',
 'glue',
 'super_glue',
 'ade_corpus_v2',
 'sick',
 'super_glue',
 'blimp',
 'discovery',
 'health_fact',
 'ag_news',
 'boolq',
 'glue',
 'amazon_polarity',
 'scicite',
 'dbpedia_14',
 'onestop_english',
 'crows_pairs',
 'scitail',
 'piqa',
 'glue',
 'paws',
 'imdb',
 'glue',
 'trec']

#en_esl, en_gumreddit are faulty on HF 
udep_en_configs = ['en_ewt', 'en_gum', 'en_lines', 'en_partut']
udep_en_labels = ['_', 'acl', 'acl:relcl', 'advcl', 'advmod', 'amod', 'appos', 'aux', 'aux:pass', 'case', 'cc', 'cc:preconj', 'ccomp', 'compound', 'compound:prt', 'conj', 'cop', 'csubj', 'csubj:pass', 'dep', 'det', 'det:predet', 'discourse', 'dislocated', 'expl', 'fixed', 'flat', 'flat:foreign', 'goeswith', 'iobj', 'list', 'mark', 'nmod', 'nmod:npmod', 'nmod:poss', 'nmod:tmod', 'nsubj', 'nsubj:pass', 'nummod', 'obj', 'obl', 'obl:npmod', 'obl:tmod', 'orphan', 'parataxis', 'punct', 'reparandum', 'root', 'vocative', 'xcomp']

udep_labels = ['_', 'acl', 'acl:adv', 'acl:appos', 'acl:attr', 'acl:cleft', 'acl:focus', 'acl:inf', 'acl:part', 'acl:periph', 'acl:poss', 'acl:relat', 'acl:relcl', 'advcl', 'advcl:arg', 'advcl:cleft', 'advcl:cmpr', 'advcl:cond', 'advcl:coverb', 'advcl:lmod', 'advcl:mmod', 'advcl:periph', 'advcl:relcl', 'advcl:sp', 'advcl:svc', 'advcl:tcl', 'advcl:tmod', 'advmod', 'advmod:arg', 'advmod:cc', 'advmod:deg', 'advmod:det', 'advmod:df', 'advmod:emph', 'advmod:lmod', 'advmod:locy', 'advmod:mmod', 'advmod:mode', 'advmod:neg', 'advmod:periph', 'advmod:que', 'advmod:tfrom', 'advmod:tlocy', 'advmod:tmod', 'advmod:to', 'advmod:tto', 'amod', 'amod:advmod', 'amod:att', 'amod:emph', 'amod:flat', 'amod:mode', 'amod:obl', 'appos', 'appos:trans', 'aux', 'aux:aglt', 'aux:aspect', 'aux:caus', 'aux:clitic', 'aux:cnd', 'aux:imp', 'aux:mood', 'aux:neg', 'aux:opt', 'aux:part', 'aux:pass', 'aux:poss', 'aux:q', 'aux:tense', 'case', 'case:acc', 'case:adv', 'case:circ', 'case:dec', 'case:det', 'case:gen', 'case:loc', 'case:pred', 'case:pref', 'case:voc', 'cc', 'cc:nc', 'cc:preconj', 'ccomp', 'ccomp:agent', 'ccomp:cleft', 'ccomp:obj', 'ccomp:obl', 'ccomp:pmod', 'ccomp:pred', 'clf', 'compound', 'compound:a', 'compound:affix', 'compound:coll', 'compound:conjv', 'compound:dir', 'compound:ext', 'compound:lv', 'compound:lvc', 'compound:nn', 'compound:nv', 'compound:plur', 'compound:preverb', 'compound:prt', 'compound:quant', 'compound:redup', 'compound:smixut', 'compound:svc', 'compound:vo', 'compound:vv', 'conj', 'conj:expl', 'conj:extend', 'conj:svc', 'cop', 'cop:expl', 'cop:locat', 'cop:own', 'csubj', 'csubj:cleft', 'csubj:cop', 'csubj:pass', 'dep', 'dep:alt', 'dep:comp', 'dep:mod', 'dep:prt', 'det', 'det:adj', 'det:def', 'det:noun', 'det:numgov', 'det:nummod', 'det:poss', 'det:predet', 'det:pron', 'det:rel', 'discourse', 'discourse:emo', 'discourse:filler', 'discourse:intj', 'discourse:sp', 'dislocated', 'dislocated:acl', 'dislocated:cleft', 'dislocated:conj', 'dislocated:nmod', 'dislocated:nsubj', 'dislocated:obj', 'dislocated:obl', 'expl', 'expl:comp', 'expl:impers', 'expl:pass', 'expl:poss', 'expl:pv', 'expl:subj', 'fixed', 'flat', 'flat:abs', 'flat:foreign', 'flat:name', 'flat:num', 'flat:range', 'flat:repeat', 'flat:sibl', 'flat:title', 'flat:vv', 'goeswith', 'iobj', 'iobj:agent', 'iobj:appl', 'iobj:caus', 'iobj:loc', 'iobj:patient', 'list', 'mark', 'mark:adv', 'mark:advb', 'mark:comp', 'mark:prt', 'mark:rel', 'mark:relcl', 'nmod', 'nmod:abl', 'nmod:advmod', 'nmod:agent', 'nmod:appos', 'nmod:arg', 'nmod:att', 'nmod:attr', 'nmod:bahuv', 'nmod:cau', 'nmod:clas', 'nmod:cmp', 'nmod:comp', 'nmod:dat', 'nmod:flat', 'nmod:gen', 'nmod:gmod', 'nmod:gobj', 'nmod:gsubj', 'nmod:lmod', 'nmod:npmod', 'nmod:obl', 'nmod:obllvc', 'nmod:own', 'nmod:part', 'nmod:periph', 'nmod:pmod', 'nmod:poss', 'nmod:pred', 'nmod:ref', 'nmod:relat', 'nmod:tmod', 'nsubj', 'nsubj:appos', 'nsubj:bfoc', 'nsubj:caus', 'nsubj:cop', 'nsubj:ifoc', 'nsubj:lfoc', 'nsubj:lvc', 'nsubj:nc', 'nsubj:obj', 'nsubj:own', 'nsubj:pass', 'nsubj:periph', 'nummod', 'nummod:det', 'nummod:entity', 'nummod:flat', 'nummod:gov', 'nummod:mod', 'nummod:periph', 'obj', 'obj:advmod', 'obj:agent', 'obj:appl', 'obj:cau', 'obj:caus', 'obj:lvc', 'obj:periph', 'obl', 'obl:abl', 'obl:advmod', 'obl:agent', 'obl:appl', 'obl:arg', 'obl:ben', 'obl:cmpr', 'obl:inst', 'obl:lmod', 'obl:loc', 'obl:mod', 'obl:npmod', 'obl:own', 'obl:patient', 'obl:pmod', 'obl:poss', 'obl:prep', 'obl:sentcon', 'obl:smod', 'obl:soc', 'obl:tmod', 'obl:x', 'orphan', 'parataxis', 'parataxis:appos', 'parataxis:conj', 'parataxis:deletion', 'parataxis:discourse', 'parataxis:dislocated', 'parataxis:hashtag', 'parataxis:insert', 'parataxis:newsent', 'parataxis:nsubj', 'parataxis:obj', 'parataxis:parenth', 'parataxis:rel', 'parataxis:rep', 'parataxis:restart', 'parataxis:speech', 'parataxis:trans', 'punct', 'reparandum', 'root', 'vocative', 'vocative:mention', 'xcomp', 'xcomp:adj', 'xcomp:cleft', 'xcomp:ds', 'xcomp:obj', 'xcomp:obl', 'xcomp:pred', 'xcomp:sp', 'xcomp:subj']