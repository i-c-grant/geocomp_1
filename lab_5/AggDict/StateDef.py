def stateCodesDict():
    """Initializes state codes dictionary"""
    state_codes_string = """01,Alabama
    02,Alaska
    04,Arizona
    05,Arkansas
    06,California
    08,Colorado
    09,Connecticut
    10,Delaware
    11,District of Columbia
    12,Florida
    13,Georgia
    15,Hawaii
    16,Idaho
    17,Illinois
    18,Indiana
    19,Iowa
    20,Kansas
    21,Kentucky
    22,Louisiana
    23,Maine
    24,Maryland
    25,Massachusetts
    26,Michigan
    27,Minnesota
    28,Mississippi
    29,Missouri
    30,Montana
    31,Nebraska
    32,Nevada
    33,New Hampshire
    34,New Jersey
    35,New Mexico
    36,New York
    37,North Carolina
    38,North Dakota
    39,Ohio
    40,Oklahoma
    41,Oregon
    42,Pennsylvania
    44,Rhode Island
    45,South Carolina
    46,South Dakota
    47,Tennessee
    48,Texas
    49,Utah
    50,Vermont
    51,Virginia
    53,Washington
    54,West Virginia
    55,Wisconsin
    56,Wyoming
    72,Puerto Rico"""
    
    # Parse defintion string into 2D list of format [[code1, state1], [code2, state2], etc.]
    state_codes_def = state_codes_string.split("\n")

    state_codes : dict = {}

    for key_val_str in state_codes_def:
        key_val_list = key_val_str.split(",")
        key = key_val_list[0].strip()
        val = key_val_list[1].strip()
        state_codes[key] = val

    return state_codes
