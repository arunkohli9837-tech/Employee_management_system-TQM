# Failure Mode and Effects Analysis (FMEA)

## Purpose

FMEA is used to identify possible system failures, their effects, causes, and existing reliability controls in the Employee Management System.

## RPN Calculation

**RPN = Severity × Occurrence × Detection**

| Rating | Meaning |
|---|---|
| 1–3 | Low |
| 4–6 | Moderate |
| 7–10 | High |

## FMEA Matrix

| Feature | Failure Mode | Effect | Control | S | O | D | RPN |
|---|---|---|---|---:|---:|---:|---:|
| Login | Invalid credentials accepted | Unauthorized access | Password verification | 9 | 3 | 3 | 81 |
| Login | Inactive user logs in | Unauthorized access | Account status check | 9 | 2 | 3 | 54 |
| Employee | Duplicate employee code | Incorrect records | Database constraint | 7 | 4 | 2 | 56 |
| Employee | Invalid input | Incorrect data | Input validation | 7 | 5 | 2 | 70 |
| Employee | Update operation fails | Data operation interrupted | Transaction rollback | 8 | 3 | 3 | 72 |
| User Management | Unauthorized action | Account changes | RBAC | 9 | 2 | 3 | 54 |
| Audit Logging | Operation not recorded | Loss of traceability | Audit logging | 8 | 3 | 5 | 120 |
| Database | Database operation fails | Data operation interrupted | Commit/Rollback | 9 | 3 | 4 | 108 |
| Backup | Automatic backup fails | Recovery risk | Automatic logout backup | 9 | 3 | 4 | 108 |
| Backup | Invalid backup restored | Restore failure | Integrity validation | 9 | 2 | 3 | 54 |
| Backup | Restore fails | Data recovery problem | Safety backup | 10 | 2 | 4 | 80 |
| Application | Runtime exception | Feature interruption | Error handling | 8 | 3 | 4 | 96 |

## Reliability Controls

The system uses the following controls to reduce reliability risks:

- Input validation
- Database constraints
- Role-Based Access Control
- Database transactions and rollback
- Audit logging
- Automatic backup
- Backup integrity validation
- Safety backup before restore
- Centralized error handling

## Reliability Improvement

FMEA helps identify potential failures and connect them with appropriate reliability controls. It also helps prioritize risks using the RPN value.

## Review

The FMEA can be updated when new reliability risks or system features are identified.