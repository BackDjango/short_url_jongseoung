# short_url_jongseoung
DRF로 간단한 단축 URL 챌린지
<br>
기능 단위에 초점을 맞춰 커밋하고, 이슈 및 PR 생성

<br>

# 프로젝트 목적
앞선 프로젝트 "Initailize_Django"의 문제 인지 및 개선
<br>
나만의 단축 URL 간단 프로젝트를 통해 DRF 실력 향상
<br>
삽질일기 (블로그 포스팅 or 노션) 작성

<br>

# 구현 기능
- Auth
- 단축 URL
    - 단축 URL 생성
    - 단축 URL 삭제
    - 단축 URL 조회(redirect)
    - 단축 URL 통계
- 환경변수 관리
    - 보안적 요소
- Logging 기능
    - 로그를 어떻게 관리를 하는지, OS 관점
- swagger
    - drf-yasg
- black
    - 코드 컨벤션 관리
- logging

<br>

# 구현 기능 추가 설명
긴 URL을 단축 URL로 변경
<p>URL 생성 시 만료 옵션을 추가하면 해당 만료일시 이후의 요청에는 응답하지 않음 (삭제)
<p>만료 옵션이 있는 URL에 대해 재생성 요청을 하게 되는 경우 이전 옵션을 무시
<p>단축 URL 호출 시 원본 URL로 리다이렉트
<p>만들어진 URL 뒤에 '+' 를 붙이면 통계 기능 제공
<li> 일간 조회수 (최근 7일)</li>
<li> 전체 조회수</li>
<li> 전체 리퍼러 별 조회수</li>

<br>

# 프로젝트 환경
- Python 3.11
- Django 5.0.4
- djangorestframework 3.15.1
- drf-yasg 1.21.7
- postgresql
