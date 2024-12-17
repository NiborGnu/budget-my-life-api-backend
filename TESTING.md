# TESTING

## Validators

### Python

- [PEP8](https://pep8ci.herokuapp.com/) was used to test python files.
- All returned clear.
- ![Validation shown for all tests](./documentation/tests/pep8validation.png)

## Automated Tests

- [Tests Users](https://github.com/NiborGnu/budget-my-life-api-backend/blob/main/users/tests.py)
- ![Validation shown for all tests](./documentation/tests/users_tests.png)

- [Tests Transactions](https://github.com/NiborGnu/budget-my-life-api-backend/blob/main/transactions/tests.py)
- ![Validation shown for all tests](./documentation/tests/transactions_tests.png)

- [Tests Categories](https://github.com/NiborGnu/budget-my-life-api-backend/blob/main/categories/tests.py)
- ![Validation shown for all tests](./documentation/tests/categories_tests.png)

- [Tests Budgets](https://github.com/NiborGnu/budget-my-life-api-backend/blob/main/budgets/tests.py)
- ![Validation shown for all tests](./documentation/tests/budgets_tests.png)

## Using Postman

| **Test Scenario**        | **Action**       | **Expected Result** | **Result** |
| ------------------------ | ---------------- | ------------------- | ---------- |
| **Create a Transaction** | sending the data | get a 201           | 201        |
| **Edit a Transaction**   | sending the data | get a 201           | 201        |
| **View a Transaction**   | sending the data | get a 201           | 201        |
| **Delete a Transaction** | sending the data | get a 201           | 201        |
| **Create a Budget**      | sending the data | get a 201           | 201        |
| **Edit a Budget**        | sending the data | get a 201           | 201        |
| **View a Budget**        | sending the data | get a 201           | 201        |
| **Delete a Budget**      | sending the data | get a 201           | 201        |
| **Create a Profile**     | sending the data | get a 201           | 201        |
| **Edit a Profile**       | sending the data | get a 201           | 201        |
| **Delete a Profile**     | sending the data | get a 201           | 201        |
| **Edit a Password**      | sending the data | get a 201           | 201        |

## Bugs

No bugs found.
