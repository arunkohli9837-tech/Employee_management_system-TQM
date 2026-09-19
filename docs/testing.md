## Transaction Rollback Testing

### Test Objective
Verify that a failed database transaction does not leave partial data in the database.

### Test Method
A temporary record was inserted inside a database transaction and an intentional exception was raised before the transaction could commit.

### Expected Result
The transaction should be rolled back and the temporary record should not remain in the database.

### Actual Result
The intentional exception was caught and the inserted record was successfully rolled back.

### Status
Passed