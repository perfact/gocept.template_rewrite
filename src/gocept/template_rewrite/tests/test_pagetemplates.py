import pytest
from gocept.template_rewrite.pagetemplates import PTParserRewriter
from gocept.template_rewrite.pagetemplates import PTRegexRewriter


@pytest.fixture(scope='module', params=[PTParserRewriter, PTRegexRewriter])
def rewriter(request):
    """Provide all pagetemplate rewriter"""
    yield request.param


@pytest.mark.parametrize('input, expected', [
    ('<p tal:define="x d; y python: str(234); z python: 5; a d"></p>',
     '<p tal:define="x d; y python:rewritten; z python:rewritten; a d"></p>'),
    ('<tal:t define="x d; y python: str(234); z python: 5; a d"></tal:t>',
     '<tal:t define="x d; y python:rewritten; z python:rewritten; a d">'
     '</tal:t>'),
])
def test_pagetemplates__PTParserRewriter____call____1(
        input, expected, rewriter):
    """It rewrites the expression values of the pagetemplate."""
    rw = rewriter(input, lambda x: "rewritten")
    assert rw() == expected


@pytest.mark.xfail(reason='The regex does not respect tal: yet.')
@pytest.mark.parametrize('input, expected', [
    ('<p tal:content="python: str(234)" class="python:script"></p>',
     '<p tal:content="python:rewritten" class="python:script"></p>'),
    ('''<p tal:define="x d; y python: str(';;'); z python: 5"></p>''',
     '<p tal:define="x d; y python:rewritten; z python:rewritten"></p>'),
    ('<tal:t content="python: str(234)" class="python:script"></tal:t>',
     '<tal:t content="python:rewritten" class="python:rewritten"></tal:t>'),
    ('''<tal:t define="x d; y python: str(';;'); z python: 5"></tal:t>''',
     '<tal:t define="x d; y python:rewritten; z python:rewritten"></tal:t>'),
])
def test_pagetemplates__PTParserRewriter____call____1_1(
        input, expected, rewriter=PTRegexRewriter):
    """It rewrites the expression values of the pagetemplate.

    (currently failing with PTRegexRewriter)
    """
    rw = rewriter(input, lambda x: "rewritten")
    assert rw() == expected


@pytest.mark.parametrize('input, expected', [
    ('<p tal:content="python: str(234)" class="python:script"></p>',
     '<p tal:content="python:rewritten" class="python:script"></p>'),
    ('''<p tal:define="x d; y python: str(';;'); z python: 5"></p>''',
     '<p tal:define="x d; y python:rewritten; z python:rewritten"></p>'),
    ('<tal:t content="python: str(234)" class="python:script"></tal:t>',
     '<tal:t content="python:rewritten" class="python:rewritten"></tal:t>'),
    ('''<tal:t define="x d; y python: str(';;'); z python: 5"></tal:t>''',
     '<tal:t define="x d; y python:rewritten; z python:rewritten"></tal:t>'),
])
def test_pagetemplates__PTParserRewriter____call____1_2(
        input, expected, rewriter=PTParserRewriter):
    """It rewrites the expression values of the pagetemplate.

    (working well with PTParserRewriter)
    """
    rw = rewriter(input, lambda x: "rewritten")
    assert rw() == expected


@pytest.mark.parametrize('input, expected', [
    ('''<p tal:define="y python: str(';;')"></p>''',
     '''<p tal:define="y python: unicode(';;')"></p>'''),
    ('''<tal:t define="y python: str(';;')"></tal:t>''',
     '''<tal:t define="y python: unicode(';;')"></tal:t>'''),
    ('''<p tal:define="y python: str(';;;;')"></p>''',
     '''<p tal:define="y python: unicode(';;;;')"></p>'''),
    ('''<tal:t define="y python: str(';;;;')"></tal:t>''',
     '''<tal:t define="y python: unicode(';;;;')"></tal:t>'''),
])
def test_pagetemplates__PTParserRewriter____call____2(
        input, expected, rewriter):
    """It can work with double semicolon (escape for a single one)."""
    rw = rewriter(input, lambda x: x.replace('str', 'unicode'))
    assert rw() == expected


@pytest.mark.xfail(
    reason='These are edge cases of invalid xml.')
@pytest.mark.parametrize('input', [
    ('''
<button tal:attributes="onclick string:go('view?id=${item/is}&re_url=redir')">
</button>'''),
    ('''
<tal:x condition="item/desc"
       replace="structure python:item.replace('\n','<br/>')"/>'''),
])
def test_pagetemplates__PTParserRewriter____call____3(
        input, rewriter=PTParserRewriter):
    """It can handle some edge cases in pagetemplates."""
    rw = rewriter(input, lambda x: x)
    assert rw() == input
