"""Unit tests for Knowledge Base, CBT distortions, and Assessments."""

from core.knowledge_base import ASSESSMENT_QUIZZES, COGNITIVE_DISTORTIONS, PSYCHOEDU_ARTICLES, PSYCHOLOGICAL_FACILITIES


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
        assert art["references"]


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
    assert "SÀNG LỌC, KHÔNG PHẢI chẩn đoán y khoa" in phq9["disclaimer"]
    assert phq9["sources"]
    assert "chưa có bằng chứng" in phq9["translation_note"]


def test_psychological_facilities_structure():
    expected_ids = {
        "bv_tamthan_tw2",
        "bvdsk_dongnai_thankinh",
        "bv_nhidong_dongnai_tamly",
        "pk_bs_nguyen_van_cau",
        "pk_tamly_minhtri",
        "vien_phapy_tamthan_bienhoa",
    }
    assert {facility["id"] for facility in PSYCHOLOGICAL_FACILITIES} == expected_ids
    for f in PSYCHOLOGICAL_FACILITIES:
        assert "id" in f
        assert "name" in f
        assert "category" in f
        assert "location" in f
        verification = f["verification"]
        assert verification["status"] in {"unverified", "partially_verified"}
        assert verification["compliance_flag"] in {"hold", "partial"}
        for field, verification_key in (
            ("address", "address_verified"),
            ("phone", "phone_verified"),
            ("hotline", "hotline_verified"),
            ("email", "email_verified"),
            ("timing", "hours_verified"),
        ):
            if verification[verification_key]:
                assert f[field] is not None
            else:
                assert f[field] is None
        assert "specialties" in f
        assert isinstance(f["specialties"], list)
        if not verification["specialties_verified"]:
            assert not f["specialties"]
        assert f["website"]
        if verification["status"] == "partially_verified":
            assert verification["sources"]
        else:
            assert not verification["sources"]

    central_hospital = next(f for f in PSYCHOLOGICAL_FACILITIES if f["id"] == "bv_tamthan_tw2")
    assert central_hospital["verification"]["status"] == "partially_verified"
    assert central_hospital["address"] == "Số 1310 đường Nguyễn Ái Quốc, khu phố 7, phường Tân Triều, thành phố Đồng Nai"
    assert central_hospital["phone"] == "0251 3822 965"
    assert central_hospital["timing"] is None
    assert central_hospital["reported_timing"] == "Khám ngoại trú theo lịch bác sĩ, thứ Hai - thứ Sáu"

    minh_tri = next(f for f in PSYCHOLOGICAL_FACILITIES if f["id"] == "pk_tamly_minhtri")
    assert minh_tri["phone"] == "0251 3685 676"
    assert minh_tri["address"].startswith("Lô BN2-LK24")


def test_audio_assets_are_blocked_until_license_evidence_exists():
    from core.knowledge_base import AUDIO_TRACKS, BREATHING_REFERENCES

    assert len(AUDIO_TRACKS) == 3
    for track in AUDIO_TRACKS:
        assert track["source_url"] is None
        assert track["license"] is None
        assert track["publishable"] is False
        assert track["compliance_status"] == "blocked_unverified_license"
    assert len(BREATHING_REFERENCES) >= 2


def test_school_examples_and_content_references():
    overgeneralization = next(
        item for item in COGNITIVE_DISTORTIONS if item["id"] == "overgeneralization"
    )
    assert "bài kiểm tra" in overgeneralization["example"]
    assert "phỏng vấn" not in overgeneralization["example"]
