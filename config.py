PATH_TO_FILE_WITH_TITLES="../mounted_dump/final_merged_output"
PATH_TO_FILE_WITH_INV_INDEX_STARTING_TERMS="../mounted_dump/final_merged_output/fin_placement_details.txt"
PATH_TO_DIR_WITH_INV_INDEXES="../mounted_dump/final_merged_output/fin_inverted_indexes"
PATH_TO_QUERY_TESTER="./moodle_sample_queries/moodle_queries.txt"
PATH_TO_QUERY_ANSWERING="./queries_op.txt"

ZONE_COEFF={
    't':10,
    'i':4,
    'c':3,
    'b':1,
    'l':1,
    'r':1
}

ZONE_INDEXES={
    't':0,
    'i':1,
    'c':2,
    'b':3,
    'l':4,
    'r':5
}

BONUS_FREQ_DESERVED=1000
BONUS_OUTSIDE_FREQ_DESERVED=1