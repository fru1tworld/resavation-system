### 실행방법

```bash
docker-compose up -d
```

### API 문서 정보

## 실행 후

URL: http://localhost:8000/docs

에서 확인할 수 있습니다.

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
