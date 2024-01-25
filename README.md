# CredFriend

The Loan Management System is a Django-based application designed to help a Loan service company efficiently lend loans to users. The system provides functionalities to register users, calculate their credit scores, apply for loans, manage loan details, calculate EMIs, and track payments. This project adheres to best practices in Django development, including models, views, APIs, flows, and authentication.


## Table of Contents

- [Run Locally](#Run-Locally)
- [APIs](#apis)
- [Contributing](#contributing)
- [Contact](#contact)



## Tech Stack

- **Server:** Django, Django REST Framework
- **Database:** PostgreSQL
- **Deployment:** Docker Compose

## Run Locally

Clone the project

```bash
  git clone https://github.com/RaunakDasgupta/CredFriend
```

Go to the project directory

```bash
  cd CredFriend
```

Start backend on docker

```bash
docker-compose up

```




## API Reference

**Please note that all of these routes can be accessed through Django Rest Framework HTML Forms for easy access.**

- **Create Customer:** `POST http://127.0.0.1:8000/api/customer`.

- | field |              |
  | :-------- | :------------------------- |
  | `first_name:`  | Required |
  | `last_name:`  | Required |
  | `age`  | Required |
  | `monthly_income`  | Required |
  | `phone_number`  | Required |


- **Check Eligibility View** `POST http://127.0.0.1:8000/api/check-eligibility/`
  Check loan eligibility based on credit score.

- | field |              |
  | :-------- | :------------------------- |
  | `customer_id:`  | Required |
  | `loan_amount`  | Required |
  | `interest_rate`  | Required |
  | `tenure`  | Required |

- **Check Eligibility View** `POST http://127.0.0.1:8000/api/create-loan/`
  Create loan based on eligibility.

- | field |              |
  | :-------- | :------------------------- |
  | `customer_id:`  | Required |
  | `loan_amount`  | Required |
  | `interest_rate`  | Required |
  | `tenure`  | Required |

- **View Loan by Loan ID** `http://127.0.0.1:8000/api/loan/view-loan/<int:loan_id>/`
  View Loan by loan_id
- | field |              |
  | :-------- | :------------------------- |
  | `loan_id:`  | Required |

- **View Loans by Customer ID** `http://127.0.0.1:8000/api/loan/view-loan/<int:customer_id>/`
  View Loans of a Customer by customer_id
- | field |              |
  | :-------- | :------------------------- |
  | `customer_id:`  | Required |
## Authors
- [@RaunakDasgupta](https://www.github.com/RaunakDasgupta)