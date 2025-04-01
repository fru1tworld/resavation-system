### 실행방법

```bash
docker-compose up -d
```

### API 문서 정보

## 실행 후

URL: http://localhost:8000/docs

에서 확인할 수 있습니다.

### Flow_chart

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

### ERD

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
        bigint exam_id FK
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

### 방식

- USER와 ADMIN은 RBAC 방식으로 user table에 role을 추가하여 구분하였습니다.
- test는 카테고리가 존재하고 하나의 카테고리는 0개 이상의 시험 정보를 가지고 있을 수 있습니다.
- 그리고 시험 정보는 0개 이상의 스케쥴을 가지고 있을 수 있습니다.
- 스케쥴을 생성하는 경우 time_slot이 시작과 끝에 row 들을 확인해서 존재하지 않으면 생성하고, 존재할 경우 생성하지 않습니다.
- time_slot은 examinee_count라는 컬럼이 존재하여 examinee_count이 max_capacity 이하인 경우에만 ADMIN이 확정지을 수 있습니다.
- 이때 time_slot은 exam_schedule에 종속적이지 않기 때문에 독립적으로 관리할 수 있습니다.
