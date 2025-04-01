# 시험 예약 시스템 (Reservation System)

시험 예약 관리를 위한 REST API 기반 시스템입니다.

## 실행 방법

```bash
docker-compose up -d
```

## API 문서

서버 실행 후 다음 URL에서 Swagger UI를 통해 API 문서를 확인할 수 있습니다:

- http://localhost:8000/docs

## 시스템 요구 사항

- 동시간에 최대 5만명까지 예약 가능 (초과 불가)
- 한 사용자는 동시간대에 여러 개의 예약이 가능

## 시스템 아키텍처

### Flow Chart

```mermaid
flowchart TB
    %% 메인 시스템 컴포넌트
    Client([사용자 브라우저]) <--> Auth{인증 미들웨어}
    Auth --> Route[라우터]
    Route --> Controller[컨트롤러]
    Controller --> DB[(데이터베이스)]

    %% 인증 플로우
    subgraph 인증_프로세스
        Login[로그인] --> |"유저네임/비밀번호"| AuthController[인증 컨트롤러]
        AuthController --> |"유저 검증"| BCrypt[비밀번호 검증]
        AuthController --> |"성공 시"| JWT[JWT 토큰 생성]
        JWT --> |"토큰 쿠키 저장"| Response[응답 & 사용자 정보 반환]
    end

    %% 사용자 플로우
    subgraph 사용자_관리
        Register[일반 사용자 등록] --> UserController[유저 컨트롤러]
        RegisterAdmin[관리자 등록] --> UserController
        UserController --> |"Snowflake ID 생성"| Snowflake[ID 생성기]
        UserController --> |"비밀번호 해싱"| BCryptHash[비밀번호 해싱]
        UserController --> |"사용자 DB 저장"| UserDB[(Users)]
    end

    %% 시험 카테고리 및 정보 관리
    subgraph 시험_관리
        CategoryCreate[카테고리 생성] --> |"관리자 권한"| CategoryController[카테고리 컨트롤러]
        CategoryController --> CategoryDB[(시험 카테고리)]

        ExamCreate[시험 정보 생성] --> |"관리자 권한"| ExamController[시험 정보 컨트롤러]
        ExamController --> ExamInfoDB[(시험 정보)]

        ScheduleCreate[시험 일정 생성] --> |"관리자 권한"| ScheduleController[시험 일정 컨트롤러]
        ScheduleController --> |"시간 슬롯 생성"| TimeSlotCreate[시간 슬롯 생성]
        ScheduleController --> ScheduleDB[(시험 일정)]
        TimeSlotCreate --> TimeslotDB[(시간 슬롯)]
    end

    %% 예약 프로세스
    subgraph 예약_프로세스
        ReservationCreate[예약 요청] --> ReservationController[예약 컨트롤러]
        ReservationController --> |"예약 상태: PENDING"| ReservationDB[(예약)]
        BatchConfirm[배치 예약 확인] --> |"관리자 작업"| ReservationBatchController[배치 예약 컨트롤러]
        ReservationBatchController --> |"수용 인원 확인"| CapacityCheck{인원 초과?}
        CapacityCheck --> |"No"| ConfirmUpdate[예약 상태: CONFIRM]
        CapacityCheck --> |"Yes"| CancelUpdate[예약 상태: CANCEL]
        ConfirmUpdate --> |"슬롯 인원 증가"| TimeslotUpdate[시간 슬롯 업데이트]
        CancelUpdate --> ReservationDB
        TimeslotUpdate --> TimeslotDB
        ReservationCancel[예약 취소] --> |"시험 3일 전 검증"| CancelCheck{취소 가능?}
        CancelCheck --> |"Yes"| CancelProcess[취소 처리]
        CancelCheck --> |"No"| CancelReject[취소 거부]
        CancelProcess --> |"슬롯 인원 감소"| TimeslotUpdate
    end

    %% 미들웨어 검증
    subgraph 권한_검증
        AuthCheck{인증 필요 경로?} --> |"Yes"| TokenCheck{토큰 존재?}
        AuthCheck --> |"No"| NextHandler[다음 핸들러]
        TokenCheck --> |"Yes"| ValidateToken{토큰 유효?}
        TokenCheck --> |"No"| AuthError[인증 오류]
        ValidateToken --> |"Yes"| AdminCheck{관리자 경로?}
        ValidateToken --> |"No"| AuthError
        AdminCheck --> |"Yes & 관리자"| NextHandler
        AdminCheck --> |"Yes & 일반 사용자"| ForbiddenError[권한 오류]
        AdminCheck --> |"No"| NextHandler
    end

    %% 시스템 연결
    인증_프로세스 --> 사용자_관리
    사용자_관리 --> 시험_관리
    시험_관리 --> 예약_프로세스
    Auth --> 권한_검증
```

### 데이터베이스 구조 (ERD)

```mermaid
erDiagram
    users ||--o{ exam_reservation : "makes"
    exam_categorie ||--o{ exam_info : "contains"
    exam_info ||--o{ exam_schedule : "has"
    exam_schedule ||--o{ exam_reservation : "receives"
    exam_time_slot ||--o{ exam_schedule : "associated with"

    users {
        bigint user_id PK
        varchar password
        varchar name
        varchar role
        timestamp created_at
    }

    exam_categorie {
        bigint exam_categorie_id PK
        varchar name
        timestamp created_at
    }

    exam_info {
        bigint exam_info_id PK
        varchar exam_name
        varchar exam_description
        bigint exam_category_id FK
        timestamp created_at
    }

    exam_schedule {
        bigint exam_schedules_id PK
        bigint exam_info_id FK
        timestamp start_time
        timestamp end_time
        timestamp created_at
    }

    exam_reservation {
        bigint exam_reservations_id PK
        bigint user_id FK
        bigint exam_schedule_id FK
        varchar reservation_status
        timestamp created_at
    }

    exam_time_slot {
        bigint exam_time_slot_id PK
        date exam_date
        integer time_slot
        integer examinee_count
        timestamp created_at
    }
```

## 시스템 설계 특징

### 사용자 권한 관리

- RBAC(Role-Based Access Control) 방식으로 `users` 테이블의 `role` 필드를 통해 USER와 ADMIN을 구분
- 관리자 전용 API 엔드포인트는 `/adm` 경로로 통일

### 시험 관리 구조

- 시험은 계층 구조로 설계:
  - 카테고리(exam_categorie) → 시험 정보(exam_info) → 시험 일정(exam_schedule)
- 각 카테고리는 여러 시험 정보를 포함할 수 있음
- 각 시험 정보는 여러 스케줄을 가질 수 있음

### 시간 슬롯 관리

- 시험 일정을 생성할 때 시작 시간과 종료 시간 사이의 시간 슬롯을 자동으로 생성
- 이미 존재하는 시간 슬롯은 중복 생성하지 않음
- 시간 슬롯은 독립적으로 관리되며, 특정 시험 일정에 종속되지 않음

### 예약 프로세스

- 사용자 예약 요청 시 최초 상태는 `PENDING`
- 관리자가 배치 처리를 통해 수용 인원을 확인하여 예약을 확정(`CONFIRM`) 또는 취소(`CANCEL`)
- 시험 시작 3일 전부터는 예약 취소 불가능

### 용량 관리

- 동시간대 최대 5만명까지 예약 가능
- 각 시간 슬롯의 `examinee_count` 필드를 통해 현재 인원 추적

## 기술 스택

- **백엔드**: FastAPI
- **데이터베이스**: PostgreSQL
- **인증**: JWT
- **배포**: Docker, Docker Compose
- **ID 생성**: Snowflake 알고리즘

## 개발자 정보

- GitHub: [https://github.com/fru1tworld/resavation-system](https://github.com/fru1tworld/resavation-system)

```

```
