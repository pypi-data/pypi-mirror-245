def _capitalise(string: str):
    return string[0].upper() + string[1:]

__doublequote = '"'

def convert(_precondition: str):
    
    gsqs = []
    preconditions = _precondition.split('/')

    for precondition in preconditions:
        _parts = precondition.split(' ')
        
        type = _parts[0]
        
        args = _parts[1:]
        string_args = ' '.join(args)

        if type == 'A':
            gsqs.append(f'!PLAYER_HAS_CONVERSATION_TOPIC Current {args}')
        elif type == 'F':
            gsqs.append(f'!IS_FESTIVAL_DAY ')
        elif type == 'U':
            n = int(args[0])
            for i in range(0, n+1):
                gsqs.append(f'!IS_FESTIVAL_DAY {i}')
        elif type == 'd':
            gsqs.append(f'!DAY_OF_WEEK {string_args}')
        elif type == 'r':
            gsqs.append(f'RANDOM {args[0]}')
        elif type == 'v':
            # TODO
            pass
        elif type == 'w':
            gsqs.append(f'WEATHER TARGET {string_args}')
        elif type == 'y':
            year = int(args[0])
            if year == 1:
                gsqs.append(f'YEAR 1 1')
            else:
                gsqs.append(f'YEAR {year}')
                
        elif type == 'z':
            gsqs.append(f'!SEASON {string_args}')
        elif type == 'N':
            gsqs.append(f'WORLD_STATE_FIELD GoldenWalnutsFound {string_args}')
        elif type == 'B':
            # TODO
            pass
        elif type == 'D':
            gsqs.append(f'PLAYER_IS_DATING Current {string_args}')
        elif type == 'J':
            gsqs.append(f'IS_JOJA_MART_COMPLETE')
        elif type == 'L':
            # TODO
            pass
        elif type == 'M':
            gsqs.append(f'PLAYER_MONEY_EARNED Current {string_args}')
        elif type == 'O':
            gsqs.append(f'PLAYER_IS_MARRIED Current {string_args}')
        elif type == 'S':
            gsqs.append(f'PLAYER_HAS_SECRET_NOTE Current {string_args}')
        elif type == 'a':
            # TODO
            pass
        elif type == 'b':
            # TODO 
            # This is the intended purpose "Current player has reached the bottom floor of the Mines at least that many times. "
            # But this only reaching the bottom at all
            gsqs.append(f'MINE_LOWEST_LEVEL_REACHED 120')
        elif type == 'c':
            # TODO
            pass
        elif type in ['e', 'k']:
            x = '' if type == 'e' else '!'
            if len(args) == 1:
                if '/' in args[0]:
                    for id in args[0].split('/'):
                        gsqs.append(f'{x}PLAYER_HAS_SEEN_EVENT Current {id}')
                else:
                    gsqs.append(f'{x}PLAYER_HAS_SEEN_EVENT Current {string_args}')
            else:
                _temp_gsqs = []
                for id in args:
                    _temp_gsqs.append(f'{x}PLAYER_HAS_SEEN_EVENT Current {id}')
                gsqs.append(f'ANY "{f"{__doublequote} ".join(_temp_gsqs)}"')
        elif type == 'g':
            gsqs.append(f'PLAYER_GENDER Current {_capitalise(string_args)}')
        elif type == 'h':
            gsqs.append(f'!PLAYER_HAS_PET Current')
            gsqs.append(f'PLAYER_PREFERRED_PET Current {_capitalise(string_args)}')
        elif type == 'i':
            gsqs.append(f'PLAYER_HAS_ITEM Current (O){string_args}')
        elif type == 'j':
            gsqs.append(f'PLAYER_STAT Current daysPlayed')
        # elif type == 'k': SEE E
        #    gsqs.append(f'')
        elif type == 'l':
            gsqs.append(f'!PLAYER_HAS_FLAG Current {string_args}')
        elif type == 'm':
            gsqs.append(f'PLAYER_MONEY_EARNED Current {string_args}')
        elif type == 'n':
            gsqs.append(f'PLAYER_HAS_FLAG Current {string_args}')
        elif type == 'o':
            gsqs.append(f'!PLAYER_IS_MARRIED Current {string_args}')
        elif type == 'p':
            # TODO
            pass
        elif type == 'q':
            # TODO: support for multiple IDs
            gsqs.append(f'PLAYER_HAS_DIALOGUE_ANSWER Current {string_args}')
        elif type == 's':
            gsqs.append(f'PLAYER_SHIPPED_BASIC_ITEM Current (O){args[0]} {args[1]}')
        elif type == 't':
            gsqs.append(f'TIME {string_args}')
        elif type == 'u':
            # TODO: figure out how multiple days work
            pass
        elif type == 'x':
            # Cannot be done in GSQs
            pass
        elif type == 'C':
            gsqs.append(f'ANY "IS_COMMUNITY_CENTER_COMPLETE" "IS_JOJA_MART_COMPLETE"')
        elif type == 'X':
            gsqs.append(f'ANY "!IS_COMMUNITY_CENTER_COMPLETE" "!IS_JOJA_MART_COMPLETE"')
        elif type == 'H':
            gsqs.append(f'IS_HOST')
        elif type == 'Hl':
            gsqs.append(f'!PLAYER_HAS_FLAG Host {string_args}')
        elif type == 'Hn':
            gsqs.append(f'PLAYER_HAS_FLAG Host {string_args}')
        elif type == '*l':
            gsqs.append(f'!PLAYER_HAS_FLAG Host {string_args}')
            gsqs.append(f'!PLAYER_HAS_FLAG Current {string_args}')
        elif type == '*n':
            gsqs.append(f'PLAYER_HAS_FLAG Host {string_args}')
            gsqs.append(f'PLAYER_HAS_FLAG Current {string_args}')



    return ', '.join(gsqs)