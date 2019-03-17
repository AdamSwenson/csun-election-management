"""
Created by adam on 3/11/19
"""
__author__ = 'adam'


# String processing of result cells

def find_dept( field ):
    """Returns the string inside the first set of parentheses
    encountered, including the parentheses
    input "Idris Elba (Age 46),Dwayne Johnson (Age 48)"
    output '(Age 46)'
    """
    if type(field) == float:
        return field
    return field[ field.find( "(" ): field.find( ")" ) + 1 ]


def normalize_names( name ):
    return name.strip().lower()


def remove_depts( field ):
    """Removes all strings inside parentheses, including the
    parentheses.
    This does not yet clean up whitespace or
    separate selections.
    input "Idris Elba (Age 46),Dwayne Johnson (Age 48)"
    output 'Idris Elba ,Dwayne Johnson (Age 48)'
    """
    if type(field) != str:
        return field
    try:
        while True:
            dept_string = find_dept( field )
            if not dept_string:
                raise StopIteration
            # re-join the list into a string for another pass
            field = ''.join( field.split( dept_string ) )
    except StopIteration:
        return field
    # except AttributeError:
    #     return field


if __name__ == '__main__':
    pass
