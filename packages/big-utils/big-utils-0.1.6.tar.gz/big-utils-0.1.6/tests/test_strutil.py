"""
String utilities unit tests
"""
import pytest
from big_utils.utils.strutil import (
    truncate_long_text,
    trim,
    trim_to_lower,
    trim_to_upper,
    ensure_not_blank,
    combine_url,
    string_2_bool
)
from tests.conftest import BLANK_VALUES

# noinspection SpellCheckingInspection
LONG_TEXT_1 = """
At vero eos et accusamus et iusto odio dignissimos ducimus qui blanditiis praesentium voluptatum deleniti atque
corrupti quos dolores et quas molestias excepturi sint occaecati cupiditate non provident, similique sunt in culpa
qui officia deserunt mollitia animi, id est laborum et dolorum fuga. Et harum quidem rerum facilis est et expedita
distinctio. Nam libero tempore, cum soluta nobis est eligendi optio cumque nihil impedit quo minus id quod maxime
placeat facere possimus, omnis voluptas assumenda est, omnis dolor repellendus. Temporibus autem quibusdam et aut
officiis debitis aut rerum necessitatibus saepe eveniet ut et voluptates repudiandae sint et molestiae non recusandae.
Itaque earum rerum hic tenetur a sapiente delectus, ut aut reiciendis voluptatibus maiores alias consequatur aut
perferendis doloribus asperiores repellat."""

# noinspection SpellCheckingInspection
LONG_TEXT_2 = """
Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna
aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.
Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."""


# noinspection SpellCheckingInspection
@pytest.mark.parametrize('long_text, expected_output', [
    (LONG_TEXT_1, 'At vero eos et accusamus et iusto odio dignissimos ducimus qui b...'),
    (LONG_TEXT_2, 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do ...'),
    ('Not so long', 'Not so long'),
    ('', ''),
    (None, ''),
    (' \t\t\t  \n', ''),
    ('\t\t\t\n  \t\t\t\r', ''),
    ('  ', '')
])
def test_truncate_long_text_default_max_len(long_text, expected_output):
    output = truncate_long_text(long_text)
    assert output == expected_output


# noinspection SpellCheckingInspection
@pytest.mark.parametrize('long_text, max_len, expected_output', [
    (LONG_TEXT_1, 32, 'At vero eos et accusamus et iust...'),
    (LONG_TEXT_2, 16, 'Lorem ipsum dolo...'),
    ('Not so long', 24, 'Not so long'),
    ('Not so long', 3, 'Not...'),
    ('', 24, ''),
    (None, 24, ''),
    (' \t\t\t  \n', 24, ''),
    ('\t\t\t\n  \t\t\t\r', 24, ''),
    ('  ', 24, '')
])
def test_truncate_long_text_explicit_max_len(long_text, max_len, expected_output):
    output = truncate_long_text(long_text, max_len)
    assert output == expected_output


@pytest.mark.parametrize('base_url, parts, expected_url', [
    ('https://www.base.com', ('part1', 'part2', 'part3'), 'https://www.base.com/part1/part2/part3'),
    ('https://www.base.com/', ('part1', 'part2', 'part3'), 'https://www.base.com/part1/part2/part3'),
    ('https://www.base.com/', ('/part1', '/part2', '/part3'), 'https://www.base.com/part1/part2/part3'),
    ('https://www.base.com/', ('/part1/', '/part2/', '/part3/'), 'https://www.base.com/part1/part2/part3'),
    ('https://www.base.com', ('/part1', '/part2', '/part3'), 'https://www.base.com/part1/part2/part3'),
    ('https://www.base.com', ('part1', '/part2', '/part3'), 'https://www.base.com/part1/part2/part3'),
    ('https://www.base.com', ('part1', 'part2', '/part3'), 'https://www.base.com/part1/part2/part3'),
    ('https://www.base.com/', ('/part1', 'part2/', '/part3'), 'https://www.base.com/part1/part2/part3'),
    ('https://www.base.com///', ('/part1///', 'part2/', '///part3'), 'https://www.base.com/part1/part2/part3'),
])
def test_combine_url(base_url, parts, expected_url):
    url = combine_url(base_url, *parts)
    assert url == expected_url


@pytest.mark.parametrize('test_value, expected_result', [
    ('1', True),
    ('true', True),
    ('yes', True),
    ('on', True),
    ('no', False),
    ('0', False),
    ('off', False),
    ('false', False),
    ('TRUE', True),
    ('YES', True),
    ('On', True),
    ('nO', False),
    ('oFf', False),
    ('FaLsE', False),

])
def test_string_2_bool_valid(test_value, expected_result):
    res = string_2_bool(test_value)
    assert res == expected_result


@pytest.mark.parametrize('test_value', ['nope', 'YEP', 'ok', 'kk'] + BLANK_VALUES)
def test_string_2_bool_invalid(test_value):
    with pytest.raises(ValueError, match='The value must be one of .*'):
        string_2_bool(test_value)


class TestTrim(object):
    """
    Unit tests for the ```trim``` function
    """

    @pytest.mark.parametrize("value, expected", [
        (None, ''),
        ('      ', ''),
        (' \n \t  ', ''),
        (' \n \t  test1', 'test1'),
        ('test1 \n \t  ', 'test1'),
        ('  test1', 'test1'),
        ('test1  ', 'test1'),
        ('  test1  ', 'test1'),
        (' \n \t  test1 \n \t  ', 'test1')
    ])
    def test_trim_str_implicit(self, value, expected):
        assert trim(value) == expected

    @pytest.mark.parametrize("value, expected", [
        (None, None),
        ('      ', None),
        (' \n \t  ', None),
        (' \n \t  test1', 'test1'),
        ('test1 \n \t  ', 'test1'),
        ('  test1', 'test1'),
        ('test1  ', 'test1'),
        ('  test1  ', 'test1'),
        (' \n \t  test1 \n \t  ', 'test1')
    ])
    def test_trim_str_explicit_none(self, value, expected):
        assert trim(value, None) == expected

    @pytest.mark.parametrize("value, expected", [
        (None, 'stuff'),
        ('      ', 'stuff'),
        (' \n \t  ', 'stuff'),
        (' \n \t  test1', 'test1'),
        ('test1 \n \t  ', 'test1'),
        ('  test1', 'test1'),
        ('test1  ', 'test1'),
        ('  test1  ', 'test1'),
        (' \n \t  test1 \n \t  ', 'test1')
    ])
    def test_trim_str_explicit_stuff(self, value, expected):
        assert trim(value, 'stuff') == expected

    @pytest.mark.parametrize("value, expected", [
        (None, b''),
        (b'      ', b''),
        (b' \n \t  ', b''),
        (b' \n \t  test1', b'test1'),
        (b'test1 \n \t  ', b'test1'),
        (b'  test1', b'test1'),
        (b'test1  ', b'test1'),
        (b'  test1  ', b'test1'),
        (b' \n \t  test1 \n \t  ', b'test1')
    ])
    def test_trim_byte_explicit(self, value, expected):
        assert trim(value, b'') == expected

    @pytest.mark.parametrize("value, expected", [
        (None, None),
        (b'      ', None),
        (b' \n \t  ', None),
        (b' \n \t  test1', b'test1'),
        (b'test1 \n \t  ', b'test1'),
        (b'  test1', b'test1'),
        (b'test1  ', b'test1'),
        (b'  test1  ', b'test1'),
        (b' \n \t  test1 \n \t  ', b'test1')
    ])
    def test_trim_byte_explicit_none(self, value, expected):
        assert trim(value, None) == expected

    @pytest.mark.parametrize("value, expected", [
        (None, 'stuff'),
        (b'      ', 'stuff'),
        (b' \n \t  ', 'stuff'),
        (b' \n \t  test1', b'test1'),
        (b'test1 \n \t  ', b'test1'),
        (b'  test1', b'test1'),
        (b'test1  ', b'test1'),
        (b'  test1  ', b'test1'),
        (b' \n \t  test1 \n \t  ', b'test1')
    ])
    def test_trim_byte_explicit_stuff(self, value, expected):
        assert trim(value, 'stuff') == expected

    @pytest.mark.parametrize("value, expected", [
        (None, ''),
        (b'      ', ''),
        (b' \n \t  ', ''),
        (b' \n \t  test1', b'test1'),
        (b'test1 \n \t  ', b'test1'),
        (b'  test1', b'test1'),
        (b'test1  ', b'test1'),
        (b'  test1  ', b'test1'),
        (b' \n \t  test1 \n \t  ', b'test1')
    ])
    def test_trim_byte_implicit(self, value, expected):
        assert trim(value) == expected

    @pytest.mark.parametrize("value,expected", [
        (u'      ', u''),
        (u' \n \t  ', u''),
        (u' \n \t  test1', u'test1'),
        (u'test1 \n \t  ', u'test1'),
        (u'  test1', u'test1'),
        (u'test1  ', u'test1'),
        (u'  test1  ', u'test1'),
        (u' \n \t  test1 \n \t  ', u'test1')
    ])
    def test_trim_unicode(self, value, expected):
        assert trim(value) == expected


# noinspection PyMethodMayBeStatic
class TestCheckNotBlank(object):
    """
    Unit tests for the ```ensure_not_blank``` function
    """

    def test_value_must_be_non_blank(self):
        test_value = 'some value'
        ensure_not_blank(test_value, 'blah')

    def test_value_must_not_be_none(self):
        test_value = None
        with pytest.raises(ValueError):
            # noinspection PyTypeChecker
            ensure_not_blank(test_value, 'blah')

    def test_value_must_not_be_empty(self):
        test_value = ''
        with pytest.raises(ValueError):
            ensure_not_blank(test_value, 'blah')

    def test_value_must_not_be_all_spaces(self):
        test_value = '   '
        with pytest.raises(ValueError):
            ensure_not_blank(test_value, 'blah')

    def test_value_must_not_be_whitespace(self):
        test_value = ' \n \t  '
        with pytest.raises(ValueError):
            ensure_not_blank(test_value, 'blah')

    def test_message_valid_message(self):
        test_message = 'some message'
        ensure_not_blank('test', test_message)

    def test_message_none(self):
        test_message = None
        # noinspection PyTypeChecker
        ensure_not_blank('test', test_message)

    def test_message_empty(self):
        test_message = ''
        ensure_not_blank('test', test_message)

    def test_message_all_spaces(self):
        test_message = '   '
        ensure_not_blank('test', test_message)

    def test_message_whitespace(self):
        test_message = ' \n \t  '
        ensure_not_blank('test', test_message)

    @pytest.mark.parametrize("value,expected", [
        (' \n \t  test1', 'test1'),
        ('test1 \n \t  ', 'test1'),
        ('  test1', 'test1'),
        ('test1  ', 'test1'),
        ('  test1  ', 'test1'),
        (' \n \t  test1 \n \t  ', 'test1')
    ])
    def test_ensure_not_blank(self, value, expected):
        assert ensure_not_blank(value) == expected

    @pytest.mark.parametrize("value,expected", [
        (b' \n \t  test1', b'test1'),
        (b'test1 \n \t  ', b'test1'),
        (b'  test1', b'test1'),
        (b'test1  ', b'test1'),
        (b'  test1  ', b'test1'),
        (b' \n \t  test1 \n \t  ', b'test1')
    ])
    def test_ensure_not_blank_byte(self, value, expected):
        assert ensure_not_blank(value) == expected

    @pytest.mark.parametrize("value,expected", [
        (u' \n \t  test1', u'test1'),
        (u'test1 \n \t  ', u'test1'),
        (u'  test1', u'test1'),
        (u'test1  ', u'test1'),
        (u'  test1  ', u'test1'),
        (u' \n \t  test1 \n \t  ', u'test1')
    ])
    def test_ensure_not_blank_unicode(self, value, expected):
        assert ensure_not_blank(value) == expected


@pytest.mark.parametrize("value, expected", [
    (None, ''),
    ('      ', ''),
    (' \n \t  ', ''),
    (' \n \t  TeSt1', 'test1'),
    ('TEST1 \n \t  ', 'test1'),
    ('  tEsT1', 'test1'),
    ('TEST1  ', 'test1'),
    ('  TEST1  ', 'test1'),
    (' \n \t  TEST1 \n \t  ', 'test1'),
    (' \n \t  test1 \n \t  ', 'test1')
])
def test_trim_to_lower_str_implicit(value, expected):
    assert trim_to_lower(value) == expected


@pytest.mark.parametrize("value, default_value, expected", [
    (None, 'TeSt1', 'test1'),
    ('      ', 'TeSt1', 'test1'),
    (' \n \t  ', 'TEST1', 'test1'),
])
def test_trim_to_lower_str_explicit(value, default_value, expected):
    assert trim_to_lower(value, default_value) == expected


@pytest.mark.parametrize("value, expected", [
    (None, ''),
    ('      ', ''),
    (' \n \t  ', ''),
    (' \n \t  TeSt1', 'TEST1'),
    ('test1 \n \t  ', 'TEST1'),
    ('  tEsT1', 'TEST1'),
    ('test1  ', 'TEST1'),
    ('  test1  ', 'TEST1'),
    (' \n \t  TEST1 \n \t  ', 'TEST1'),
    (' \n \t  test1 \n \t  ', 'TEST1')
])
def test_trim_to_upper_str_implicit(value, expected):
    assert trim_to_upper(value) == expected


@pytest.mark.parametrize("value, default_value, expected", [
    (None, 'TeSt1', 'TEST1'),
    ('      ', 'TeSt1', 'TEST1'),
    (' \n \t  ', 'test1', 'TEST1'),
])
def test_trim_to_upper_str_explicit(value, default_value, expected):
    assert trim_to_upper(value, default_value) == expected
