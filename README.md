# aws-translation-backend-service
This AWS project leverages a serverless architecture in which only the following services will be used:
- Amazon API Gateway
- AWS Lambda
- Amazon DynamoDB
- Amazon Simple Queue Service
- Amazon Simple Storage Service (S3)
  
These services will be used to create a translation backend service that utilizes the Python library "googletrans', which is Google translate's API.
The only HTTP methods (CRUD operations) used in this project are GET and POST methods, and will be interacted with using curl or postman as there is no webfront that will be developed (hence the emphasis of this being a backend service).
