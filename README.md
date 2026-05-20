# Payment Service Demo

A demo fintech payment backend for testing autonomous QA systems.

## Features

- Payment processing
- Refund processing
- Payment analytics
- User validation
- Notification delivery

## Expected Behaviors

- Reject payment amounts <= 0
- Reject missing user_id
- Reject unsupported currencies
- Refunds should only process once
- Refunds should validate payment existence
- Analytics endpoint should respond in under 1 second
- Notification failures should not break payment flow
- API responses should remain consistent across endpoints
- Payment processing should remain idempotent
- Invalid users should never receive payment success

## Known Risks

- High payment volume may degrade analytics performance
- Notification delivery depends on third-party services
- Refund logic is still experimental
