[中文](README.md) · [日本語](README.ja.md) · 한국어 · [English](README.en.md)

AI 번역이라 표현이 다소 어색할 수 있으며, 저는 다른 언어를 몰라 중국어판만 검토했으므로 내용은 [중국어판](README.md)을 기준으로 해 주세요.

# 『블루 아카이브』의 Gnosticism 대응 모델

『블루 아카이브』의 스토리와 Gnosticism 우주론의 대응 관계에 관한 개인적인 연구입니다. 총학생회장, 선생님, 이름 없는 신들, 무명사제, 잊혀진 신들, 그리고 학생들의 헤일로가 무엇에 대응하는지를 중심으로 다룹니다.

이건 그저 제가 이것저것 상상해 본 개인적인 생각입니다. 생각이 이리저리 튀는 데다 AI도 많이 사용했으니 부정확한 내용이 많을 겁니다.

## 읽기 안내

- **[논문 전문](gnostic_correspondence_ko.md)**: 대부분 제가 직접 썼습니다. AI가 쓴 글은 좋지 않았습니다. 핵심 생각은 모두 여기에 정리되어 있으니 이것만 읽으면 됩니다. 다른 문서들은 전부 AI가 썼습니다.
- **[용어 설명](GNOSTIC_GLOSSARY_ko.md)**: 이 분야를 처음 접하는 분들을 위해 본문에 나오는 용어와 문헌을 설명합니다.
- **[우주론 관계도](06_comparative_analysis/gnostic_atlas/index.html)**: 내려받은 뒤 브라우저에서 HTML 파일을 열어 주세요.
- **[인용 기술 색인](01_sources/paper_citation_index.md)**: 논문의 주석과 원문 코퍼스 번호, 데이터 표, 행 번호의 대응 관계를 기록합니다.

제 생각에 관심이 있고 저장소를 내려받았다면, AI가 [작업 안내](AGENTS.md), [연구 대화 기록](CHAT_BACKUP.md), [현재 상태](PROJECT_STATUS.md), [논의 결정 기록](08_review_queue/decision_log.md)을 먼저 읽고 이어서 작업하도록 할 수 있습니다. 이 프로젝트는 그대로 Agent에게 넘겨도 됩니다. 이 보조 문서들은 중국어로 되어 있습니다.

## 자료 구성

| 폴더 | 내용 |
| --- | --- |
| [01_sources](01_sources/) | 출처 기록, 문헌 목록, 인용 기술 색인 |
| [02_corpus](02_corpus/) | 코퍼스 버전과 수록 범위 설명 |
| [03_tools](03_tools/) | 검색, 코퍼스 구축, 관계도 도구 |
| [04_evidence](04_evidence/) | 스토리 인용문, 중국어 번역, 주제별 근거 자료 |
| [05_hypotheses](05_hypotheses/) | 각 대응 관계에 관한 검토 노트 |
| [06_comparative_analysis](06_comparative_analysis/) | 원전의 구조와 비교 자료 |
| [07_writing](07_writing/) | 이전 초안과 집필 자료 |
| [08_review_queue](08_review_queue/) | 논의에서 내린 결정과 과거 기록 |

## 로컬 검색

로컬 연구 코퍼스는 고정된 데이터 스냅샷에서 만들었으며, 비어 있지 않은 일본어 기록 237,386건을 포함합니다. 저장소에는 읽기 쉬운 형태의 전체 코퍼스와 압축된 데이터베이스가 들어 있습니다. 원본 데이터의 외부 출처와 고정 리비전은 별도로 기록되어 있으며, 출처와 버전은 [코퍼스 설명](02_corpus/coverage_report.md)을 참고해 주세요.

```powershell
python 03_tools/restore_corpus.py
python 03_tools/search.py -q "名もなき神" -C 3
python 03_tools/search.py -q "忘却は" -C 3
```

## 원본 데이터와 이력

일상적인 검색에는 위의 방법으로 데이터베이스를 복원하는 것만으로 충분합니다. 데이터베이스를 다시 만들거나 원본 데이터와 대조하려면 먼저 다음 명령을 실행해 주세요.

```powershell
git clone https://github.com/electricgoat/ba-data.git 02_corpus/ba-data-jp
git -C 02_corpus/ba-data-jp checkout 3428d2a0943bdfe7d6453adfcb06676509972b02
python 03_tools/search.py --test
```

업로드 전의 로컬 커밋과 태그는 [Git 이력 백업](08_review_queue/archive/pre_github_history.bundle)에 모두 보존되어 있습니다.

## 라이선스

이 프로젝트의 창작 글, 연구·정리 내용 및 코드는 [CC0 1.0 Universal](LICENSE)로 공개합니다. 게임 텍스트, 제3자 문헌, 외부 데이터의 권리와 출처는 각각 유지되며, 이 프로젝트의 CC0 선언으로 바뀌지 않습니다.
