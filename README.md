# StrataMap Research Intelligence Platform

공개 연구 데이터를 기반으로 한국 Spatial Transcriptomics 및 Single-cell 연구 생태계를 탐색하는 Streamlit MVP입니다.

## 목적

- 우선 검토할 연구자와 기관 탐색
- 연구자별 우선순위 근거 확인
- Research Intelligence와 Technology Adoption 관점 비교
- 후보 연구자군 내부 공저 네트워크 탐색

이 플랫폼은 구매 확률, 전환 확률 또는 CRM 예측 모델이 아닙니다. 공개 연구 evidence를 이용한 우선순위 검토 프레임워크입니다.

## 데이터 소스

- OpenAlex 기반 연구자·논문·공저 정보
- 공개 ORCID 및 기관 metadata(가용한 경우)
- Phase 1–4에서 생성하고 동결한 researcher-level 분석 결과

앱은 `data/`에 포함된 CSV 복사본만 읽으며 원본 분석 파일을 수정하지 않습니다.

## 분석 구조

```text
Public Data
    ↓
Master Dataset
    ↓
Feature Engineering
    ↓
Dual Scoring Model
    ↓
Commercial Prioritization
    ↓
Web Application
```

### Phase 요약

1. **Master Dataset**: identity, publication, institution, technology evidence 통합
2. **Research Intelligence Features**: RII, TAI, RMI, NII, IOI 생성 및 정제
3. **Dual Scoring Model**: Expert 가중 모델과 PCA Statistical 모델 비교
4. **Commercial Prioritization**: 60/40 hybrid score, segment, tier, explanation profile

## 로컬 실행

Python 3.11 이상을 권장합니다.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Windows에서는 가상환경 활성화 명령으로 `.venv\Scripts\activate`를 사용합니다.

## Streamlit Community Cloud 배포

1. 이 폴더 전체를 새 GitHub repository의 루트에 push합니다.
2. [Streamlit Community Cloud](https://share.streamlit.io/)에서 GitHub 계정으로 로그인합니다.
3. **Create app**을 선택하고 repository, branch, `app.py`를 지정합니다.
4. **Deploy**를 선택합니다. 별도 secret이나 API key는 필요하지 않습니다.
5. 배포 후 생성된 URL에서 Ranking, Profile, Network Map을 확인합니다.

## Repository 구조

```text
StrataMap-Research-Intelligence/
├── app.py
├── requirements.txt
├── README.md
├── .streamlit/config.toml
├── data/
│   ├── master_dataset.csv
│   ├── hybrid_priority_score.csv
│   ├── commercial_segment.csv
│   ├── commercial_tier.csv
│   ├── researcher_explanation_profile.csv
│   └── network_edge.csv
├── modules/
│   ├── data_loader.py
│   ├── ranking.py
│   ├── profile.py
│   ├── network.py
│   └── visualization.py
└── assets/
    └── logo.png
```

## 데이터 오류 처리

필수 CSV가 없거나 컬럼 구조가 다르면 앱은 빈 화면 대신 명확한 한국어 오류 메시지를 표시합니다.

---

Developed by Woongsun Choi  
Illumina Korea  
2026
