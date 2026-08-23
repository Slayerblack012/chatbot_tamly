"""Unit tests for Knowledge Base, CBT distortions, and Assessments."""

from core.knowledge_base import ASSESSMENT_QUIZZES, COGNITIVE_DISTORTIONS, PSYCHOEDU_ARTICLES


def test_cognitive_distortions_structure():
    assert len(COGNITIVE_DISTORTIONS) >= 8
    for d in COGNITIVE_DISTORTIONS:
        assert "id" in d
        assert "name" in d
        assert "icon" in d
        assert "description" in d
        assert "example" in d
        assert "reframing" in d


def test_psychoedu_articles_structure():
    assert len(PSYCHOEDU_ARTICLES) >= 3
    for art in PSYCHOEDU_ARTICLES:
        assert "id" in art
        assert "title" in art
        assert "category" in art
        assert "readTime" in art
        assert "summary" in art
        assert "content" in art


def test_gad7_quiz_structure():
    assert "gad7" in ASSESSMENT_QUIZZES
    gad7 = ASSESSMENT_QUIZZES["gad7"]
    assert len(gad7["questions"]) == 7
    assert len(gad7["options"]) == 4
    assert len(gad7["brackets"]) == 4

    # Max score calculation
    max_score = len(gad7["questions"]) * 3
    assert max_score == 21

    # Verify brackets coverage
    for bracket in gad7["brackets"]:
        r = bracket["range"]
        assert len(r) == 2
        assert r[0] <= r[1]
        assert "level" in bracket
        assert "advice" in bracket


def test_phq9_quiz_structure():
    assert "phq9" in ASSESSMENT_QUIZZES
    phq9 = ASSESSMENT_QUIZZES["phq9"]
    assert len(phq9["questions"]) == 9
    assert len(phq9["options"]) == 4
    assert len(phq9["brackets"]) == 5

    # Max score calculation
    max_score = len(phq9["questions"]) * 3
    assert max_score == 27

    # Verify brackets coverage
    for bracket in phq9["brackets"]:
        r = bracket["range"]
        assert len(r) == 2
        assert r[0] <= r[1]
        assert "level" in bracket
        assert "advice" in bracket
