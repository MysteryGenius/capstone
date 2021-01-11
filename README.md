# Capstone Project
---
### Routes

#### Users

('id', 'username', 'first_name', 'last_name', 'email', 'status', 'document_type', 'pid', 'mobile_number', 'photo', 'residence_code', 'phone_area_code', 'enrolled_id', 'organisation_id')

- Get all users [GET]
```
/users/all
```
- Get user or Delete user [GET, DELETE]
```
/users/<user_id>
```
- Create user [POST: JSON/FORM]
```
/users/add
```



#### Operators

('id', 'username', 'first_name', 'last_name', 'email', 'status', 'document_type', 'pid', 'mobile_number', 'photo', 'residence_code', 'phone_area_code', 'enrolled_id', 'organisation_id')

- Get all operators
```
operators/all
```
- Get operator or Delete operator [GET, DELETE]
```
/operators/<operator_id>
```
- Create operator [POST: JSON/FORM]
```
/operators/add
```


#### Organization

('id', 'created_by', 'name', 'slug', 'status')

- Get all organizations
```
organizations/all
```
- Get organization or Delete organization [GET, DELETE]
```
/organizations/<organization_id>
```
- Create organization [POST: JSON/FORM]
```
/organizations/add
```

#### FacialFeatures

('id', 'user_id', 'face_vector')

- Get all features
```
features/all
```
- Get feature or Delete feature [GET, DELETE]
```
/features/<feature_id>
```
- Create feature [POST: JSON/FORM]
```
/features/add
```
---
### About 

This is a project to create a authentication layer using Facial recognition and OTP technology.

### Setup

Install all project requirements 

```
pip install -r requirements.txt
```

### Development Server

The dev.bat file will run all necessary setups and start a development server on localhost:5000

```
C:> dev
```